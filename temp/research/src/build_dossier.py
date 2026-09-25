import json

d = json.load(open("/home/user/ClaudeLocal/temp/research/research_data.json", encoding="utf-8"))
srcmap = {s["id"]: s for s in d["sources"]}


def cite(ids):
    return " ".join(f"[{i}]" for i in ids) if ids else ""


def en(x):
    return x["en"] if isinstance(x, dict) else x


def zh(x):
    return x["zh"] if isinstance(x, dict) else x


L = []
w = L.append

m = d["meta"]
w(f"# {en(m['title'])}\n")
w(f"**{en(m['subtitle'])}**\n")
w(f"_Date: {m['date']} · Prepared with the MBB methodology. {en(m['method'])}_\n")
w(f"> **Evidence caveat.** {en(m['evidence_note'])}\n")
w(f"> **中文摘要.** {zh(m['evidence_note'])}\n")

w("\n## 0. Problem statement\n")
w(en(m["problem_statement"]) + "\n")
w("> 中文：" + zh(m["problem_statement"]) + "\n")

s = d["scqa"]
w("\n## 1. Executive summary (SCQA)\n")
for k, label in [("situation", "Situation"), ("complication", "Complication"),
                 ("question", "Question"), ("answer", "Answer")]:
    w(f"- **{label}.** {en(s[k])}")
w("\n**答案（中文）：** " + zh(s["answer"]) + "\n")

w("\n## 2. Key findings\n")
for f in d["key_findings"]:
    w(f"### {f['id']} · {en(f['title'])}")
    w(f"{en(f['body'])}  ")
    w(f"_Confidence: {f['confidence']}. Sources: {cite(f['sources'])}_")
    w(f"> 中文：**{zh(f['title'])}** — {zh(f['body'])}\n")

w("\n## 3. Headline numbers\n")
w("| Metric | Meaning | Sources |")
w("|---|---|---|")
for k in d["kpis"]:
    w(f"| **{k['value']}** | {en(k['label'])} | {cite(k['sources'])} |")

w("\n## 4. Issue tree (MECE)\n")
it = d["issue_tree"]
w(f"**{en(it['root'])}**\n")
for b in it["branches"]:
    w(f"- {en(b['q'])}")
    for c in b["children"]:
        w(f"  - {en(c)}")

w("\n## 5. Hypotheses & verdicts\n")
w("| # | Hypothesis | Verdict | Confidence | Note |")
w("|---|---|---|---|---|")
for h in d["hypotheses"]:
    note = en(h.get("note", "")) if h.get("note") else ""
    w(f"| {h['id']} | {en(h['text'])} | **{h['verdict']}** | {h['confidence']} | {note} {cite(h['sources'])} |")

w("\n## 6. Q1 — How AI-agent attacks evolved in 2026\n")
w("| Date | Milestone | What changed | Example | Track | Sources |")
w("|---|---|---|---|---|---|")
for e in d["attack_evolution"]:
    w(f"| {e['label']} | {en(e['technique'])} | {en(e['detail'])} | — | {e['track']} | {cite(e['sources'])} |")
w("\n### Self-learning / adaptation mechanisms (public evidence)\n")
w("| Mechanism | What was observed | Confidence | Sources |")
w("|---|---|---|---|")
for s2 in d["self_learning"]:
    w(f"| {en(s2['mechanism'])} | {en(s2['what'])} | {s2['confidence']} | {cite(s2['sources'])} |")

w("\n## 7. Q2 — Victims and what they share\n")
w("| Org | Country | Sector | Date | What happened | Vector | Agent | Disclosure lag | Sources |")
w("|---|---|---|---|---|---|---|---|---|")
for v in d["victims"]:
    w(f"| {en(v['org'])} | {en(v['country'])} | {en(v['sector'])} | {v['date']} | {en(v['accessed'])} | "
      f"{en(v['vector'])} | {en(v['agent'])} | {en(v['lag'])} | {cite(v['sources'])} |")

w("\n### Commonality matrix\n")
cols = d["commonality"]["cols"]
w("| Commonality | " + " | ".join(en(c) for c in cols) + " |")
w("|---" * (len(cols) + 1) + "|")
mark = {0: "·", 1: "✓", 2: "partial"}
for r in d["commonality"]["rows"]:
    w(f"| {en(r['dim'])} | " + " | ".join(mark.get(c, str(c)) for c in r["cells"]) + " |")

w("\n### Attack angles (MECE)\n")
w("| Angle | What it looks like | Victims observed |")
w("|---|---|---|")
for a in d["attack_angles"]:
    w(f"| {en(a['angle'])} | {en(a['desc'])} | {en(a['victims'])} |")

hc = d["hf_case"]
w("\n## 8. Hugging Face case reconstruction (deep dive)\n")
w("### 8.1 Trigger / root cause\n")
w(en(hc["trigger"]) + "\n")
w("> 中文：" + zh(hc["trigger"]) + "\n")
w("### 8.2 Timeline\n")
w("| When (UTC) | Event | Sources |")
w("|---|---|---|")
for t in hc["timeline"]:
    w(f"| {t['date']} | {en(t['event'])} | {cite(t['sources'])} |")
w("\n### 8.3 Attack path\n")
w("| Stage | What happened | Asset | Sources |")
w("|---|---|---|---|")
for p in hc["attack_path"]:
    w(f"| {en(p['stage'])} | {en(p['what'])} | {en(p['asset'])} | {cite(p['sources'])} |")
w("\n### 8.4 Detection\n")
w(en(hc["detection"]) + "\n")
w("> 中文：" + zh(hc["detection"]) + "\n")
w("### 8.5 Telemetry / log sources — what was used\n")
w("This directly answers the question 'SIEM? NDR? EDR? firewall? cloud logs?'\n")
w("| Log source | Used? | Status | Note | Sources |")
w("|---|---|---|---|---|")
usemap = {True: "yes", False: "no", None: "not stated"}
for lg in hc["log_sources"]:
    w(f"| {en(lg['source'])} | {usemap[lg['used']]} | {lg['status']} | {en(lg['note'])} | {cite(lg['sources'])} |")
w("\n### 8.6 The commercial-model refusal\n")
w(en(hc["refusal"]) + "\n")
w("> 中文：" + zh(hc["refusal"]) + "\n")
w("### 8.7 What GLM-5.2 actually did\n")
w(en(hc["glm_deployment"]) + "\n")
w("> 中文：" + zh(hc["glm_deployment"]) + "\n")
w("| GLM analysis | What it produced | Sources |")
w("|---|---|---|")
for g in hc["glm_analysis"]:
    w(f"| {en(g['task'])} | {en(g['what'])} | {cite(g['sources'])} |")
w("\n### 8.8 Response & containment\n")
for r in hc["response"]:
    w(f"- {en(r)}")
w("\n### 8.9 Lessons learned\n")
for i, ls in enumerate(hc["lessons"], 1):
    w(f"{i}. {en(ls)}")

w("\n## 9. Q4 — Defense architecture\n")
w("### 9.1 Requirements (what a defense against AI-agent attacks must have)\n")
w("| Requirement | Why (from the evidence) | Priority |")
w("|---|---|---|")
for rq in d["defense_requirements"]:
    w(f"| {en(rq['req'])} | {en(rq['why'])} | {rq['priority']} |")

for a in d["architectures"]:
    w(f"\n### 9.{'2' if a['id']=='A' else '3'} {en(a['name'])}\n")
    w(f"_{en(a['tagline'])}_\n")
    w(f"**Best fit:** {en(a['fit'])}\n")
    w("**Layers (top → bottom):**\n")
    for ly in a["layers"]:
        w(f"- **{en(ly['name'])}** — " + "; ".join(en(c) for c in ly["components"]))
    w("\n**Data flow:** " + " → ".join(en(fl) for fl in a["flows"]))
    w("\n**Pros:** " + " ".join("✓ " + en(p) for p in a["pros"]))
    w("\n**Cons:** " + " ".join("✗ " + en(c) for c in a["cons"]))
    w("\n**Roadmap:**")
    for ph in a["roadmap"]:
        w(f"- _{en(ph['phase'])}:_ {en(ph['items'])}")
    w("\n**KPIs:** " + " · ".join(en(k) for k in a["kpis"]))

w("\n### 9.4 AI analysis prompt catalog\n")
w("The AI layer should run these analyses, each with a vetted, defensive system prompt. Prompts are authored in English; names/purposes given bilingually.\n")
for p in d["prompt_catalog"]:
    w(f"#### {p['id']} · {en(p['name'])} — {zh(p['name'])}")
    w(f"- **Model:** {en(p['model'])}")
    w(f"- **Purpose:** {en(p['purpose'])} / {zh(p['purpose'])}")
    w(f"- **System prompt:**\n  > {p['system']}")
    w(f"- **Task template:** `{p['task']}`\n")

w("\n## 10. Corrections to the requesting premises\n")
w("These are stated politely because the underlying facts differ from the brief.\n")
for c in d["corrections"]:
    w(f"- **{en(c['premise'])}** → {en(c['evidence'])} {cite(c['sources'])}")
    w(f"  - 中文：{zh(c['evidence'])}")

w("\n## 11. Sources\n")
for s2 in d["sources"]:
    w(f"{s2['id']}. {s2['title']} — {s2['publisher']}, {s2['date']}. {s2['url']}")

open("/home/user/ClaudeLocal/temp/research/research_dossier.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print("dossier lines:", len(L))
