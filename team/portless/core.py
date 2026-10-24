"""Name-based service addressing for the team ("portless").

The rule the team already lives by (AGENTS.md section 7, learned rule r000):
reach test instances and team services by name, never by raw port. This
module is the tooling behind that rule.

Two halves:

- A registry of names. ``alias``/``resolve``/``list``/``rm`` manage it.
  State is machine-local (``~/.local/state/team-chaotix/portless``), never
  committed, so a registry can name things on the operator's machine
  without leaking them into the repository.
- A Host-routed reverse proxy (``serve``). One listener, one wildcard
  certificate for ``*.localhost``; the ``Host`` header picks the service.
  This is what makes ``https://<name>.localhost`` resolve to a service
  without DNS, without opening a port per service, and without bind
  collisions when several teams run on one machine (the failure this team
  was created to avoid).

Stdlib only.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import socket
import ssl
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib import request as _urlreq

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


class PortlessError(ValueError):
    pass


def state_dir() -> Path:
    env = os.environ.get("PORTLESS_STATE_DIR")
    if env:
        return Path(env)
    return Path.home() / ".local" / "state" / "team-chaotix" / "portless"


def registry_path() -> Path:
    return state_dir() / "registry.json"


def valid_name(name: str) -> bool:
    return bool(NAME_RE.match(name or ""))


def load_registry() -> dict:
    p = registry_path()
    if not p.exists():
        return {"version": 1, "services": {}}
    try:
        reg = json.loads(p.read_text())
    except (OSError, json.JSONDecodeError) as e:
        raise PortlessError("unreadable registry %s: %s" % (p, e)) from e
    reg.setdefault("version", 1)
    reg.setdefault("services", {})
    return reg


def save_registry(reg: dict) -> None:
    p = registry_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), prefix=".registry-")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(reg, fh, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, str(p))
    except OSError:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def add_alias(name: str, host: str, port: int, proto: str = "http",
              note: str = "") -> dict:
    if not valid_name(name):
        raise PortlessError(
            "invalid name %r: lowercase letters, digits, hyphens; "
            "must start/end alnum, max 63 chars" % name)
    if proto not in ("http", "https"):
        raise PortlessError("proto must be http or https")
    if not (0 < int(port) < 65536):
        raise PortlessError("port out of range: %s" % port)
    reg = load_registry()
    svc = {
        "host": host,
        "port": int(port),
        "proto": proto,
        "url": "%s://%s:%d" % (proto, host, port),
        "note": note,
    }
    reg["services"][name] = svc
    save_registry(reg)
    return svc


def remove_alias(name: str) -> bool:
    reg = load_registry()
    if name in reg["services"]:
        del reg["services"][name]
        save_registry(reg)
        return True
    return False


def resolve(name: str) -> dict:
    reg = load_registry()
    svc = reg["services"].get(name)
    if svc is None:
        known = ", ".join(sorted(reg["services"])) or "(none)"
        raise PortlessError("unknown service %r (known: %s)" % (name, known))
    return svc


def list_services() -> dict:
    return load_registry()["services"]


def probe(name: str, timeout: float = 10.0) -> dict:
    """Reach a service by name and report the HTTP status. TLS to the
    team's own CA is accepted; anything else fails closed."""
    svc = resolve(name)
    url = svc["url"]
    if svc["proto"] == "https":
        ctx = ssl.create_default_context(cafile=str(state_dir() / "ca" / "ca.pem"))
    else:
        ctx = None
    req = _urlreq.Request(url, method="GET")
    try:
        with _urlreq.urlopen(req, timeout=timeout,
                             context=ctx if ctx else None) as resp:
            return {"name": name, "url": url, "status": resp.status, "ok": True}
    except Exception as e:
        return {"name": name, "url": url, "status": None, "ok": False,
                "error": str(e)}


# ---------------------------------------------------------------------------
# Host-routed reverse proxy
# ---------------------------------------------------------------------------


def ensure_ca() -> Path:
    """Create (or reuse) the local CA and the ``*.localhost`` wildcard cert.

    Generated with openssl because stdlib cannot mint X.509 certificates.
    The CA is team-local: it only vouches for ``*.localhost`` on this
    machine, and installing it into a trust store is the operator's step.
    """
    ca_dir = state_dir() / "ca"
    ca_dir.mkdir(parents=True, exist_ok=True)
    ca_pem = ca_dir / "ca.pem"
    ca_key = ca_dir / "ca.key"
    crt = ca_dir / "server.crt"
    key = ca_dir / "server.key"
    if ca_pem.exists() and crt.exists() and key.exists():
        return ca_pem
    if shutil.which("openssl") is None:
        raise PortlessError(
            "openssl is required to mint the team CA (dnf install openssl)")

    def run(cmd):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise PortlessError("openssl failed: %s" % r.stderr.strip())
        return r

    run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
         "-keyout", str(ca_key), "-out", str(ca_pem), "-days", "3650",
         "-subj", "/CN=Team Chaotix portless local CA"])
    os.chmod(str(ca_key), 0o600)
    run(["openssl", "req", "-newkey", "rsa:2048", "-nodes",
         "-keyout", str(key),
         "-out", str(ca_dir / "server.csr"),
         "-subj", "/CN=localhost"])
    ext = str(ca_dir / "san.cnf")
    with open(ext, "w") as fh:
        fh.write(
            "[req]\n"
            "distinguished_name=req\n"
            "req_extensions=req_ext\n"
            "[req_ext]\n"
            "subjectAltName=DNS:localhost,DNS:*.localhost,IP:127.0.0.1\n"
        )
    run(["openssl", "x509", "-req", "-in", str(ca_dir / "server.csr"),
         "-CA", str(ca_pem), "-CAkey", str(ca_key), "-CAcreateserial",
         "-days", "3650", "-extfile", ext,
         "-out", str(crt)])
    os.chmod(str(key), 0o600)
    return ca_pem


def _host_matches(host_header: str, name: str) -> bool:
    host = (host_header or "").lower().split(":")[0].strip()
    return host == name or host == "%s.localhost" % name or host.endswith("." + name + ".localhost")


class _ProxyHandler(BaseHTTPRequestHandler):
    registry_fn = None
    target_timeout = 60.0

    def log_message(self, *a):
        pass

    def _find_service(self):
        host = (self.headers.get("Host") or "").lower().split(":")[0].strip()
        services = self.registry_fn()
        for name, svc in services.items():
            if _host_matches(host, name):
                return name, svc
        return None, None

    def _forward(self):
        name, svc = self._find_service()
        if svc is None:
            body = json.dumps({"error": "no service named %r"
                               % (self.headers.get("Host") or "")}).encode()
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        length = int(self.headers.get("Content-Length", 0) or 0)
        body = self.rfile.read(length) if length else b""
        headers = {
            k: v for k, v in self.headers.items()
            if k.lower() not in ("host", "connection", "content-length")
        }
        headers["Host"] = "%s:%d" % (svc["host"], svc["port"])
        if length:
            headers["Content-Length"] = str(length)
        if svc["proto"] == "https":
            ctx = ssl.create_default_context(cafile=str(state_dir() / "ca" / "ca.pem"))
            url = "https://%s:%d%s" % (svc["host"], svc["port"], self.path)
        else:
            ctx = None
            url = "http://%s:%d%s" % (svc["host"], svc["port"], self.path)
        req = _urlreq.Request(url, data=body if self.command != "GET" else None,
                              headers=headers, method=self.command)
        try:
            with _urlreq.urlopen(req, timeout=self.target_timeout,
                                 context=ctx) as resp:
                data = resp.read()
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    if k.lower() in ("transfer-encoding", "connection"):
                        continue
                    self.send_header(k, v)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            body = json.dumps({"error": "upstream %s:%s failed: %s"
                               % (svc["host"], svc["port"], e)}).encode()
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    do_GET = _forward
    do_POST = _forward
    do_PUT = _forward
    do_DELETE = _forward
    do_PATCH = _forward
    do_HEAD = _forward


def serve(port: int = 443, bind: str = "127.0.0.1", tls: bool = True):
    """Run the Host-routed proxy. Returns the bound port.

    ``tls`` False serves plain HTTP (useful for tests and for machines
    without openssl). With TLS, the ``*.localhost`` wildcard certificate is
    presented and the caller trusts the team CA.
    """
    server = ThreadingHTTPServer((bind, port), _ProxyHandler)
    # staticmethod: the handler looks this up through the instance, which
    # would otherwise bind the handler as the first argument.
    _ProxyHandler.registry_fn = staticmethod(lambda: load_registry()["services"])
    if tls:
        ca_pem = ensure_ca()
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(
            str(state_dir() / "ca" / "server.crt"),
            str(state_dir() / "ca" / "server.key"),
        )
        ctx.verify_mode = ssl.CERT_NONE
        server.socket = ctx.wrap_socket(server.socket, server_side=True)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port
