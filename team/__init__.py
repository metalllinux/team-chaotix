"""Team Chaotix platform package.

Original implementations of the team's shared machinery:

- ``team.graph``     the langgraph state machine for the task cycle
- ``team.a2a``       the A2A (agent-to-agent) protocol server and client
- ``team.portless``  name-based service addressing (aliases, proxy)
- ``team.licenses``  the licence scanner and policy engine (Flicky's tooling)

Everything here is deterministic and testable without a model: the graph takes
an injectable runner, the A2A server takes an injectable task runner, and the
scanner and registry are pure file I/O. CI never invokes an LLM.
"""

__version__ = "2.0.0"
