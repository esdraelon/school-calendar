"""ICS feed service + event query MCP.

Pattern: FastMCP application — an Adapter over the merged events
store, read-only for queries; the ICS feed projects the merged
store (plus due dates that matter, projected from the school
MCP — never stored as events).

Every collection-returning tool documents its default limit, its
ordering, and how a consumer pages to exhaustion (cursor/offset,
or time-window parameters where no cursor exists) — see the
pagination/full-coverage standing gate in docs/PLAN.md. Served
per the gateway deployment standard: MCP at the app root,
public host allowlisted, uvicorn proxy headers on, and its own
path-scoped gateway token. Feed + MCP land in M4.
"""
