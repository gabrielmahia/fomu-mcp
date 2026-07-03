# fomu-mcp

[![fomu-mcp Glama score](https://glama.ai/mcp/servers/gabrielmahia/fomu-mcp/badges/score.svg)](https://glama.ai/mcp/servers/gabrielmahia/fomu-mcp)
[![smithery badge](https://smithery.ai/badge/@gabrielmahia/fomu-mcp)](https://smithery.ai/server/@gabrielmahia/fomu-mcp)


---
**Compatible with `claude-sonnet-5`** (released 2026-06-30) — Anthropic's most agentic
Sonnet yet. Runs multi-step tool chains end-to-end without stopping short.
Install: `pip install fomu-mcp` · Use with any MCP client.

---


> Kenya civic form agent via MCP — turns citizen needs into government form checklists, draft applications, and timeline plans.

[![PyPI](https://img.shields.io/badge/PyPI-v0.1.0-blue?logo=pypi)](https://pypi.org/project/fomu-mcp/)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/gabrielmahia/fomu-mcp)

*Fomu (Swahili for "form")*

## Why This Exists

> *"Form Agent: turns messy user answers into applications, checklists, letters."*  
> — East Africa AI Infrastructure Schematic

Kenya's government processes are documented but navigating them requires knowing what to look for.  
fomu-mcp encodes the institutional knowledge: what to bring, where to go, how long it takes, what to pay.

## Install

```bash
pip install fomu-mcp
```

## Tools (6)

| Tool | Function |
|------|----------|
| `form_checklist` | Complete requirements list for any Kenya government form |
| `form_draft_letter` | Generate draft formal letters (introduction, reference, complaint, land inquiry) |
| `form_requirements_check` | Tell user what they have and what they're missing |
| `ecitizen_guide` | eCitizen portal service directory |
| `huduma_centre_guide` | Huduma Centre locations and services by county |
| `form_timeline_planner` | Sequence multiple processes with estimated completion dates |

## Example

```python
# Check readiness for business registration
await call_tool("form_requirements_check", {
    "form_type": "business_registration",
    "user_has": ["national ID", "KRA PIN", "passport photo"]
})
# Returns: missing items + completeness % + next step
```

## Part of AI-KungFU East Africa Coordination Infrastructure

Part of the SII Stack — the Form Agent layer in the 7-agent type framework:
Research · **Form** · Verification · Translation · Financial · Market · Escalation

→ [sii-stack](https://github.com/gabrielmahia/sii-stack)
→ [The Nairobi Stack](https://gabrielmahia.github.io/nairobi-stack)

## License

MIT © Gabriel Mahia | contact@aikungfu.dev

## Part of the East Africa Coordination Stack

This MCP server is one of 32 tools in the Kenya coordination infrastructure.
Connect it to [`africa-coord-bus`](https://github.com/gabrielmahia/africa-coord-bus) —
the coordination event bus that routes signals between domains automatically.

```bash
pip install africa-coord-bus
```

All 32 servers: [pypi.org/user/gmahia](https://pypi.org/user/gmahia/)
Live demo: [coord-cascade-demo](https://github.com/gabrielmahia/coord-cascade-demo)

## IP & Collaboration

MIT licensed. Feedback via GitHub Issues only — pull requests are not accepted. Demo data is labeled DEMO and is not suitable for operational decisions. Full policy: [docs/architecture/IP_POLICY.md](docs/architecture/IP_POLICY.md). Security reports: see [SECURITY.md](SECURITY.md).
