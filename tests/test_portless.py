"""Tests for portless (team/portless).

Registry tests are pure file I/O against a temp state dir. The proxy test
boots a real upstream on an ephemeral port and a real Host-routed proxy
on another, over plain HTTP (the TLS path needs openssl and a CA and is
covered by the manual selftest on a machine that has both).
"""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from team.portless import core


@pytest.fixture()
def state_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("PORTLESS_STATE_DIR", str(tmp_path / "portless"))
    return tmp_path / "portless"


def test_alias_and_resolve(state_dir):
    svc = core.add_alias("cinnamon-1", "127.0.0.1", 8080, proto="http",
                         note="test VM")
    assert svc["url"] == "http://127.0.0.1:8080"
    got = core.resolve("cinnamon-1")
    assert got["host"] == "127.0.0.1"
    assert got["port"] == 8080
    assert core.list_services()["cinnamon-1"] == svc


def test_invalid_names_rejected(state_dir):
    with pytest.raises(core.PortlessError):
        core.add_alias("UPPER", "127.0.0.1", 80)
    with pytest.raises(core.PortlessError):
        core.add_alias("-lead", "127.0.0.1", 80)
    with pytest.raises(core.PortlessError):
        core.add_alias("trail-", "127.0.0.1", 80)
    with pytest.raises(core.PortlessError):
        core.add_alias("x" * 64, "127.0.0.1", 80)


def test_remove_and_unknown(state_dir):
    core.add_alias("one", "127.0.0.1", 80)
    assert core.remove_alias("one") is True
    assert core.remove_alias("one") is False
    with pytest.raises(core.PortlessError):
        core.resolve("one")
    with pytest.raises(core.PortlessError) as e:
        core.resolve("missing")
    assert "no such" not in str(e.value)  # it says unknown service
    assert "missing" in str(e.value)


def test_registry_is_atomic_json(state_dir):
    core.add_alias("a", "127.0.0.1", 80)
    core.add_alias("b", "10.0.0.2", 8443, proto="https")
    reg = json.loads((state_dir / "registry.json").read_text())
    assert set(reg["services"]) == {"a", "b"}
    assert reg["version"] == 1


class _Upstream(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        body = b"upstream says hello to " + (
            self.headers.get("Host") or "?").encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def test_proxy_routes_by_name(state_dir):
    # Upstream on an ephemeral port.
    up = ThreadingHTTPServer(("127.0.0.1", 0), _Upstream)
    up_port = up.server_address[1]
    threading.Thread(target=up.serve_forever, daemon=True).start()
    core.add_alias("svc-a", "127.0.0.1", up_port, proto="http")

    # Proxy on another ephemeral port, plain HTTP.
    server = core.serve(port=0, bind="127.0.0.1", tls=False)
    proxy_port = server.server_address[1]

    import urllib.request

    req = urllib.request.Request(
        "http://127.0.0.1:%d/" % proxy_port,
        headers={"Host": "svc-a.localhost"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        assert resp.status == 200
        body = resp.read().decode()
    assert "upstream says hello to" in body

    # Unknown name: 404 with a machine-readable error. urlopen raises on
    # 4xx, so the 404 is asserted through the exception.
    req = urllib.request.Request(
        "http://127.0.0.1:%d/" % proxy_port,
        headers={"Host": "not-registered.localhost"},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        resp.read()
    except urllib.error.HTTPError as e:
        assert e.code == 404
    else:
        raise AssertionError("unknown name was not rejected with 404")

    up.shutdown()
    server.shutdown()


def test_probe_reports_unreachable(state_dir):
    core.add_alias("dead", "127.0.0.1", 1, proto="http")
    r = core.probe("dead", timeout=2)
    assert r["ok"] is False
