# AI-Agent Attack & Defense — deliverables

Deep research (MBB method) on 2026 AI-agent cyber-intrusions and a defense architecture, with a bilingual dashboard and four PowerPoint decks.

## Files

| File | What it is |
|---|---|
| `dashboard_ai_attack_defense.html` | Bilingual (EN/中文) ET-DAO dashboard — the full MBB analysis. Open in any browser; theme + language toggles top-right. Needs internet for React/logo CDNs. |
| `AI_Defense_Architecture_Option_A_EN.pptx` | Architecture **Option A — SOC-Evolved** (English) |
| `AI_Defense_Architecture_Option_A_ZH.pptx` | Architecture **Option A — SOC 演进式** (中文) |
| `AI_Defense_Architecture_Option_B_EN.pptx` | Architecture **Option B — AI-Native Defense Mesh** (English) |
| `AI_Defense_Architecture_Option_B_ZH.pptx` | Architecture **Option B — AI 原生防御网格** (中文) |
| `research/research_dossier.md` | Full narrative research report (EN + 中文 summaries) |
| `research/research_data.json` | Structured, fully bilingual dataset behind the dashboard and decks |
| `research/src/` | Generators (data + dashboard + decks) — re-run to rebuild |

## The two architectures (choose one)

- **Option A — SOC-Evolved.** Evolutionary. Keep your SIEM/SOC and add the four things Hugging Face was missing: a full telemetry fabric, cross-layer correlation that escalates, a sovereign self-hosted AI forensics layer with a refusal-fallback router, and human-approved machine-speed containment. Lower cost/risk; humans stay at the decision point.
- **Option B — AI-Native Defense Mesh.** Frontier. An agentic SOC where sovereign defender-agents watch, reason and contain at machine speed behind an agent-gateway, with a human gate on irreversible actions. For high-value targets facing autonomous swarms.

**Recommendation:** adopt Option A now, evolve into Option B within 12 months.

## Evidence caveat

This research ran in an environment whose egress proxy blocked direct page fetches, so findings rest on search-result summaries of the cited sources, triangulated across independent outlets. Figures carry confidence levels; items marked "not disclosed" are not in the public record. See `research/research_dossier.md` §10 and the `corrections` section for premises in the original brief that the evidence corrects (e.g. GLM-5.2 not 5.3; METR not Meta; Data USA not "USA Data").
