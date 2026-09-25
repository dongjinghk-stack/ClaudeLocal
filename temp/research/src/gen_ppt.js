const pptxgen = require("pptxgenjs");
const fs = require("fs");
const D = JSON.parse(fs.readFileSync("/home/user/ClaudeLocal/temp/research/research_data.json", "utf-8"));

// ---- palette (ET-DAO) ----
const C = {
  navy: "0B2233", blue: "0C5C87", blue2: "1A7AB8", ice: "CADCFC",
  ink: "0B1726", gray: "5B6777", muted: "8B95A5", line: "E6ECF3",
  bg: "FFFFFF", panel: "F4F7FB", green: "2E7D32", orange: "C46B1C", red: "C62828",
  white: "FFFFFF", chip: "EAF2F8", chipInk: "0C5C87",
};
const FT = { title: "Calibri", body: "Calibri" };

const T = (o, lang) => (o && typeof o === "object" && "en" in o) ? o[lang] : o;

// UI strings
const S = {
  en: {
    conf: "Confidential — security research briefing", by: "ET-DAO · Accelerating AI+ Transition",
    date: "25 September 2026",
    deckKicker: "AI Agent Attack & Defense",
    exec: "Executive summary", bottom: "Bottom line",
    threat: "The 2026 threat: intrusions went autonomous",
    victims: "Victims share one profile", hf: "The Hugging Face case: what happened",
    hfLesson: "Hugging Face lessons: telemetry, refusal & sovereignty",
    principles: "Design principles for AI-agent defense",
    archTitle: "Reference architecture", flow: "How data flows",
    roster: "Model roster: which model does what",
    prompts: "AI analysis: what to run, with which prompt",
    tradeoff: "When to choose this option", roadmap: "A 12-month roadmap", kpis: "Success metrics",
    reco: "Recommendation", sources: "Selected sources",
    layers: "Layers (top → bottom)", why: "Why", priority: "Priority",
    pros: "Strengths", cons: "Trade-offs", fit: "Best fit",
    model: "Model", analyzes: "Analyzes", purpose: "Purpose",
    optA_short: "Option A · SOC-Evolved", optB_short: "Option B · AI-Native Defense Mesh",
    chooseThis: "Choose this if", chooseOther: "Choose the other option if",
    recoBody: "Adopt Option A now to close the gaps the 2026 incidents exposed — correlation, escalation and sovereign AI forensics on top of your existing SOC — and evolve into Option B, an AI-native defense mesh, within 12 months as autonomous swarms become routine.",
    evNote: "Evidence: public reporting Jan–Sep 2026, triangulated across independent outlets; primary pages were not fetched directly, so figures are labelled by confidence.",
  },
  zh: {
    conf: "机密 — 安全研究简报", by: "ET-DAO · 加速 AI+ 转型",
    date: "2026 年 9 月 25 日",
    deckKicker: "AI 智能体攻击与防御",
    exec: "执行摘要", bottom: "核心结论",
    threat: "2026 年的威胁：入侵走向自主化",
    victims: "受害方共享同一画像", hf: "Hugging Face 案例：发生了什么",
    hfLesson: "Hugging Face 的教训：遥测、拒答与自主可控",
    principles: "面向 AI 智能体攻击的防御设计原则",
    archTitle: "参考架构", flow: "数据如何流动",
    roster: "模型阵列：各模型分工",
    prompts: "AI 分析：做什么、用哪条提示词",
    tradeoff: "何时选择该方案", roadmap: "12 个月路线图", kpis: "成效指标",
    reco: "建议", sources: "主要来源",
    layers: "分层（从上到下）", why: "依据", priority: "优先级",
    pros: "优势", cons: "取舍", fit: "适用对象",
    model: "模型", analyzes: "分析对象", purpose: "用途",
    optA_short: "方案 A · SOC 演进式", optB_short: "方案 B · AI 原生防御网格",
    chooseThis: "适合选择本方案的情形", chooseOther: "更适合另一方案的情形",
    recoBody: "立即采用方案 A，补上 2026 年事件暴露的缺口——在现有 SOC 之上加装跨层关联、告警升级与自主可控的 AI 取证；并在 12 个月内演进到方案 B（AI 原生防御网格），以应对日渐常态化的自主智能体集群。",
    evNote: "证据：2026 年 1–9 月公开报道，经多家独立媒体交叉验证；未直接抓取原始页面，数据均标注置信度。",
  },
};

function buildDeck(optId, lang, p, PAGE) {
  const u = S[lang];
  const arch = D.architectures.find(a => a.id === optId);
  const other = D.architectures.find(a => a.id !== optId);
  const optShort = optId === "A" ? u.optA_short : u.optB_short;
  const mk = () => { PAGE.n++; return p.addSlide(); };

  // helpers
  const foot = (slide) => {
    slide.addText(u.by + "   ·   " + optShort, { x: 0.5, y: 7.08, w: 10, h: 0.3, fontFace: FT.body, fontSize: 9, color: C.muted, isTextBox: true, margin: 0 });
    slide.addText(String(PAGE.n), { x: 12.4, y: 7.08, w: 0.5, h: 0.3, fontFace: FT.body, fontSize: 9, color: C.muted, align: "right", isTextBox: true, margin: 0 });
  };
  const kicker = (slide, txt) => {
    slide.addText(txt.toUpperCase(), { x: 0.5, y: 0.32, w: 12.3, h: 0.3, fontFace: FT.body, fontSize: 11, color: C.blue2, bold: true, charSpacing: 1, isTextBox: true, margin: 0 });
  };
  const atitle = (slide, txt) => {
    slide.addText(txt, { x: 0.5, y: 0.62, w: 12.3, h: 0.9, fontFace: FT.title, fontSize: 26, bold: true, color: C.ink, isTextBox: true, margin: 0, valign: "top" });
  };
  const src = (slide, ids) => {
    if (!ids || !ids.length) return;
    slide.addText("Sources: " + ids.join(", "), { x: 0.5, y: 6.72, w: 11.8, h: 0.3, fontFace: FT.body, fontSize: 9, italic: true, color: C.muted, isTextBox: true, margin: 0 });
  };

  // ---- Slide 1: Title (dark) ----
  let s = mk();
  s.background = { color: C.navy };
  s.addText("ET-DAO", { x: 0.6, y: 0.5, w: 4, h: 0.5, fontFace: FT.title, fontSize: 20, bold: true, color: C.white, isTextBox: true, margin: 0 });
  s.addText(u.deckKicker, { x: 0.6, y: 2.0, w: 12, h: 0.5, fontFace: FT.body, fontSize: 16, color: C.ice, bold: true, charSpacing: 2, isTextBox: true, margin: 0 });
  s.addText(T(D.meta.title, lang), { x: 0.6, y: 2.55, w: 12.1, h: 1.6, fontFace: FT.title, fontSize: 34, bold: true, color: C.white, isTextBox: true, margin: 0, valign: "top" });
  s.addText(optShort, { x: 0.6, y: 4.25, w: 12, h: 0.55, fontFace: FT.title, fontSize: 22, bold: true, color: C.ice, isTextBox: true, margin: 0 });
  s.addText(T(D.meta.subtitle, lang), { x: 0.6, y: 4.95, w: 11.5, h: 1.1, fontFace: FT.body, fontSize: 14, color: "C9D6E5", isTextBox: true, margin: 0, valign: "top" });
  s.addText(u.date + "   ·   " + u.conf, { x: 0.6, y: 6.7, w: 12, h: 0.4, fontFace: FT.body, fontSize: 11, color: C.muted, isTextBox: true, margin: 0 });

  // ---- Slide 2: Exec summary (SCQA) ----
  s = mk(); s.background = { color: C.bg };
  kicker(s, u.deckKicker); atitle(s, T(D.scqa.question, lang));
  s.addShape(p.ShapeType.roundRect, { x: 0.5, y: 1.65, w: 12.33, h: 1.95, rectRadius: 0.08, fill: { color: C.panel }, line: { color: C.blue, width: 2 } });
  s.addText(u.bottom, { x: 0.75, y: 1.8, w: 11, h: 0.4, fontFace: FT.title, fontSize: 15, bold: true, color: C.blue, isTextBox: true, margin: 0 });
  s.addText(T(D.scqa.answer, lang), { x: 0.75, y: 2.2, w: 11.85, h: 1.35, fontFace: FT.body, fontSize: 13.5, color: C.ink, isTextBox: true, margin: 0, valign: "top" });
  const scqa = [["S", D.scqa.situation], ["C", D.scqa.complication], ["Q", D.scqa.question]];
  scqa.forEach((it, i) => {
    const x = 0.5 + i * 4.16;
    s.addShape(p.ShapeType.roundRect, { x, y: 3.9, w: 3.9, h: 2.7, rectRadius: 0.06, fill: { color: C.bg }, line: { color: C.line, width: 1 } });
    s.addText(it[0], { x: x + 0.2, y: 4.05, w: 3.5, h: 0.5, fontFace: FT.title, fontSize: 22, bold: true, color: C.blue2, isTextBox: true, margin: 0 });
    s.addText(T(it[1], lang), { x: x + 0.2, y: 4.6, w: 3.55, h: 1.95, fontFace: FT.body, fontSize: 11.5, color: C.gray, isTextBox: true, margin: 0, valign: "top" });
  });
  foot(s);

  // ---- Slide 3: Threat evolution ----
  s = mk(); s.background = { color: C.bg };
  kicker(s, "Q1"); atitle(s, u.threat);
  const ev = D.attack_evolution.filter((e, i) => [0,2,5,6,7,8].includes(i));
  const evShow = D.attack_evolution;
  // timeline row of milestones (pick 6 key)
  const picks = [D.attack_evolution[3], D.attack_evolution[5], D.attack_evolution[6], D.attack_evolution[7], D.attack_evolution[8], D.attack_evolution[10]];
  picks.forEach((e, i) => {
    const x = 0.5 + i * 2.06;
    const col = e.track === "criminal" ? C.red : e.track === "rogue" ? C.orange : C.blue2;
    s.addShape(p.ShapeType.roundRect, { x, y: 1.7, w: 1.9, h: 3.2, rectRadius: 0.06, fill: { color: C.panel }, line: { color: C.line, width: 1 } });
    s.addShape(p.ShapeType.ellipse, { x: x + 0.8, y: 1.85, w: 0.3, h: 0.3, fill: { color: col } });
    s.addText(e.label, { x: x + 0.08, y: 2.2, w: 1.75, h: 0.3, align: "center", fontFace: FT.title, fontSize: 12, bold: true, color: col, isTextBox: true, margin: 0 });
    s.addText(T(e.technique, lang), { x: x + 0.12, y: 2.55, w: 1.66, h: 2.3, align: "center", fontFace: FT.body, fontSize: 9.5, color: C.ink, isTextBox: true, margin: 0, valign: "top", fit: "shrink" });
  });
  // self-learning callout
  s.addShape(p.ShapeType.roundRect, { x: 0.5, y: 5.15, w: 12.33, h: 1.4, rectRadius: 0.06, fill: { color: C.panel }, line: { color: C.blue, width: 1.5 } });
  s.addText((lang === "en" ? "Why swarms are dangerous: " : "集群为何危险："), { x: 0.7, y: 5.28, w: 12, h: 0.35, fontFace: FT.title, fontSize: 13, bold: true, color: C.blue, isTextBox: true, margin: 0 });
  const sl = D.self_learning.slice(0, 3).map(m => "• " + T(m.mechanism, lang) + " — " + T(m.what, lang));
  s.addText(sl.map((t, i) => ({ text: t, options: { breakLine: true, paraSpaceAfter: 3 } })), { x: 0.7, y: 5.62, w: 11.9, h: 0.9, fontFace: FT.body, fontSize: 9.5, color: C.gray, isTextBox: true, margin: 0, valign: "top" });
  foot(s);

  // ---- Slide 4: Victim commonality ----
  s = mk(); s.background = { color: C.bg };
  kicker(s, "Q2"); atitle(s, u.victims);
  const vic = D.victims.slice(0, 6);
  const vrows = [[{ text: T({en:"Organisation",zh:"机构"},lang), options: hcell() }, { text: T({en:"What happened",zh:"发生了什么"},lang), options: hcell() }, { text: T({en:"Front door",zh:"突破口"},lang), options: hcell() }]];
  vic.forEach(v => vrows.push([
    { text: T(v.org, lang), options: bcell(true) },
    { text: T(v.accessed, lang), options: bcell() },
    { text: T(v.vector, lang), options: bcell() },
  ]));
  s.addTable(vrows, { x: 0.5, y: 1.65, w: 7.4, colW: [2.2, 3.0, 2.2], border: { type: "solid", color: C.line, pt: 0.5 }, autoPage: false });
  // commonality highlights
  s.addShape(p.ShapeType.roundRect, { x: 8.15, y: 1.65, w: 4.68, h: 4.9, rectRadius: 0.06, fill: { color: C.panel }, line: { color: C.line, width: 1 } });
  s.addText(T({en:"The common thread",zh:"共同点"},lang), { x: 8.35, y: 1.8, w: 4.3, h: 0.4, fontFace: FT.title, fontSize: 14, bold: true, color: C.blue, isTextBox: true, margin: 0 });
  const cc = D.commonality.rows.filter((r,i)=>[0,2,3,5,8,9].includes(i)).map(r => "• " + T(r.dim, lang));
  s.addText(cc.map(t => ({ text: t, options: { breakLine: true, paraSpaceAfter: 8 } })), { x: 8.35, y: 2.25, w: 4.35, h: 4.15, fontFace: FT.body, fontSize: 11, color: C.gray, isTextBox: true, margin: 0, valign: "top" });
  src(s, ["S40","S47","S48","S15"]); foot(s);

  // ---- Slide 5: HF case ----
  s = mk(); s.background = { color: C.bg };
  kicker(s, T({en:"Anchor case",zh:"锚点案例"},lang)); atitle(s, u.hf);
  s.addText(T(D.hf_case.trigger, lang), { x: 0.5, y: 1.55, w: 12.33, h: 1.15, fontFace: FT.body, fontSize: 11.5, color: C.gray, isTextBox: true, margin: 0, valign: "top" });
  const tl = D.hf_case.timeline.filter((t,i)=>[1,3,4,5,6,7,9].includes(i));
  const trows = [[{text:T({en:"When",zh:"时间"},lang),options:hcell()},{text:T({en:"Event",zh:"事件"},lang),options:hcell()}]];
  tl.forEach(t => trows.push([{ text: t.date, options: bcell(true) }, { text: T(t.event, lang), options: bcell() }]));
  s.addTable(trows, { x: 0.5, y: 2.8, w: 12.33, colW: [2.5, 9.83], border: { type: "solid", color: C.line, pt: 0.5 }, autoPage: false });
  src(s, ["S2","S16","S3","S15"]); foot(s);

  // ---- Slide 6: HF lessons (telemetry, refusal, sovereignty) ----
  s = mk(); s.background = { color: C.bg };
  kicker(s, T({en:"Anchor case",zh:"锚点案例"},lang)); atitle(s, u.hfLesson);
  const cols6 = [
    { t: T({en:"Telemetry that mattered",zh:"真正有用的遥测"},lang), b: D.hf_case.log_sources.filter(l=>l.status==="confirmed").slice(0,5).map(l=>"✓ "+T(l.source,lang)), col: C.green },
    { t: T({en:"Not the perimeter",zh:"并非边界"},lang), b: D.hf_case.log_sources.filter(l=>l.status==="not_disclosed").map(l=>"– "+T(l.source,lang)+" ("+T({en:"not stated",zh:"未说明"},lang)+")"), col: C.orange },
    { t: T({en:"Refusal → sovereignty",zh:"拒答 → 自主可控"},lang), b: [T({en:"Commercial models blocked the forensics",zh:"商业模型拦截了取证"},lang), T({en:"Self-hosted GLM-5.2 did it in hours",zh:"自托管 GLM-5.2 数小时完成"},lang), T({en:"No attacker data left HF",zh:"攻击数据未离开 HF"},lang)], col: C.blue },
  ];
  cols6.forEach((c, i) => {
    const x = 0.5 + i * 4.16;
    s.addShape(p.ShapeType.roundRect, { x, y: 1.7, w: 3.9, h: 4.15, rectRadius: 0.06, fill: { color: C.panel }, line: { color: c.col, width: 1.5 } });
    s.addText(c.t, { x: x + 0.2, y: 1.85, w: 3.55, h: 0.7, fontFace: FT.title, fontSize: 13, bold: true, color: c.col, isTextBox: true, margin: 0, valign: "top" });
    s.addText(c.b.map(t => ({ text: t, options: { breakLine: true, paraSpaceAfter: 6 } })), { x: x + 0.2, y: 2.6, w: 3.55, h: 3.15, fontFace: FT.body, fontSize: 11, color: C.gray, isTextBox: true, margin: 0, valign: "top" });
  });
  s.addText(T(D.hf_case.refusal, lang), { x: 0.5, y: 6.0, w: 12.33, h: 0.75, fontFace: FT.body, fontSize: 9.5, italic: true, color: C.muted, isTextBox: true, margin: 0, valign: "top" });
  foot(s);

  // ---- Slide 7: Design principles ----
  s = mk(); s.background = { color: C.bg };
  kicker(s, "Q4"); atitle(s, u.principles);
  const req = D.defense_requirements;
  const rrows = [[{text:"#",options:hcell()},{text:T({en:"Requirement",zh:"需求"},lang),options:hcell()},{text:u.why,options:hcell()},{text:u.priority,options:hcell()}]];
  req.forEach((r, i) => rrows.push([
    { text: String(i+1), options: bcell(true) },
    { text: T(r.req, lang), options: bcell(true) },
    { text: T(r.why, lang), options: bcell() },
    { text: r.priority.toUpperCase(), options: { ...bcell(), color: r.priority==="must"?C.red:C.orange, bold: true, align: "center" } },
  ]));
  s.addTable(rrows, { x: 0.5, y: 1.6, w: 12.33, colW: [0.5, 3.6, 7.03, 1.2], border: { type: "solid", color: C.line, pt: 0.5 }, fontSize: 10.5, autoPage: false });
  foot(s);

  // ---- Slide 8: THE architecture (layered) ----
  s = mk(); s.background = { color: C.bg };
  kicker(s, optShort); atitle(s, u.archTitle + " — " + T(arch.name, lang).split("—").pop().trim());
  const layers = arch.layers;
  const topY = 1.55, availH = 5.0, gap = 0.12;
  const lh = (availH - gap * (layers.length - 1)) / layers.length;
  layers.forEach((ly, i) => {
    const y = topY + i * (lh + gap);
    const shade = i % 2 === 0 ? C.panel : C.chip;
    s.addShape(p.ShapeType.roundRect, { x: 0.5, y, w: 12.33, h: lh, rectRadius: 0.04, fill: { color: shade }, line: { color: C.line, width: 1 } });
    s.addText(T(ly.name, lang), { x: 0.62, y: y, w: 2.7, h: lh, fontFace: FT.title, fontSize: 11.5, bold: true, color: C.blue, isTextBox: true, margin: 4, valign: "middle", fit: "shrink" });
    // chips
    const chips = ly.components.map(c => T(c, lang));
    const chipText = chips.map((t, j) => ({ text: "  " + t + "  ", options: { fontSize: 9.5, color: C.chipInk, breakLine: false } }));
    s.addText(chips.map((t,j)=>({text: t + (j<chips.length-1?"     ":""), options:{fontSize:9.7, color:C.ink, breakLine:false}})), { x: 3.4, y: y, w: 9.3, h: lh, fontFace: FT.body, isTextBox: true, margin: 4, valign: "middle", fit: "shrink" });
  });
  foot(s);

  // ---- Slide 9: Data flow ----
  s = mk(); s.background = { color: C.bg };
  kicker(s, optShort); atitle(s, u.flow);
  const flows = arch.flows.map(f => T(f, lang));
  const fy = 2.4, fw = 12.33 / flows.length;
  flows.forEach((f, i) => {
    const x = 0.5 + i * fw;
    s.addShape(p.ShapeType.roundRect, { x: x + 0.1, y: fy, w: fw - 0.5, h: 2.0, rectRadius: 0.06, fill: { color: i===flows.length-1?C.blue:C.panel }, line: { color: C.blue, width: 1 } });
    s.addText(String(i+1), { x: x + 0.1, y: fy + 0.15, w: fw - 0.5, h: 0.4, align: "center", fontFace: FT.title, fontSize: 16, bold: true, color: i===flows.length-1?C.white:C.blue2, isTextBox: true, margin: 0 });
    s.addText(f, { x: x + 0.2, y: fy + 0.6, w: fw - 0.7, h: 1.3, align: "center", fontFace: FT.body, fontSize: 10.5, color: i===flows.length-1?C.white:C.gray, isTextBox: true, margin: 0, valign: "top", fit: "shrink" });
    if (i < flows.length - 1) s.addText("→", { x: x + fw - 0.42, y: fy + 0.7, w: 0.4, h: 0.6, align: "center", fontFace: FT.title, fontSize: 20, bold: true, color: C.muted, isTextBox: true, margin: 0 });
  });
  s.addText(T({en:"Human-approved, machine-speed: reversible actions run automatically; anything destructive or irreversible waits for a human.",zh:"人工审批、机器速度：可逆动作自动执行；任何破坏性或不可逆动作须待人工确认。"},lang), { x: 0.5, y: 5.0, w: 12.33, h: 0.8, fontFace: FT.body, fontSize: 12, italic: true, color: C.gray, isTextBox: true, margin: 0, align: "center" });
  foot(s);

  // ---- Slide 10: Model roster ----
  s = mk(); s.background = { color: C.bg };
  kicker(s, optShort); atitle(s, u.roster);
  const roster = optId === "A" ? [
    [{en:"Self-hosted open-weight LLM (sovereign)",zh:"自托管开源权重 LLM（自主可控）"},{en:"Forensics: triage, correlation, timeline, payload decoding, containment planning",zh:"取证：研判、关联、时间线、载荷解码、遏制规划"},{en:"Runs on your own GPUs; never refuses incident data",zh:"在自有 GPU 上运行；不会拒绝事件数据"}],
    [{en:"Refusal-fallback router",zh:"拒答回退路由"},{en:"Routes each task to the first model that will answer",zh:"把每个任务路由到第一个愿意作答的模型"},{en:"Avoids a refusal mid-investigation",zh:"避免调查中途被拒答"}],
    [{en:"Small fast classifiers",zh:"小型快速分类器"},{en:"Alert triage; agent-cadence / behaviour-shift scoring",zh:"告警研判；智能体节奏 / 行为漂移打分"},{en:"Cheap, high-volume, low latency",zh:"低成本、高吞吐、低延迟"}],
    [{en:"UEBA / anomaly + graph model",zh:"UEBA / 异常 + 图模型"},{en:"Baselines and attack-path reasoning over the entity graph",zh:"实体图上的基线与攻击路径推理"},{en:"Finds the choke point to cut",zh:"找出可切断的关键节点"}],
  ] : [
    [{en:"Self-hosted open-weight LLM (primary defender)",zh:"自托管开源权重 LLM（主防御体）"},{en:"Powers the triage, correlation, attack-path and detection-writer agents",zh:"驱动研判、关联、攻击路径与检测编写智能体"},{en:"Sovereign core of the defender mesh",zh:"防御网格的自主可控核心"}],
    [{en:"Model registry + refusal-fallback router",zh:"模型注册表 + 拒答回退路由"},{en:"Selects and swaps models per task; no external refusal",zh:"按任务选择/切换模型；无外部拒答"},{en:"Resilience and sovereignty",zh:"韧性与自主可控"}],
    [{en:"Small fast classifiers",zh:"小型快速分类器"},{en:"Gateway triage; human-vs-machine cadence detection",zh:"网关研判；人机节奏识别"},{en:"Screens every AI/agent action at line rate",zh:"以线速筛查每个 AI/智能体动作"}],
    [{en:"UEBA / anomaly + graph model",zh:"UEBA / 异常 + 图模型"},{en:"Streaming entity graph; blast-radius and path reasoning",zh:"流式实体图；爆炸半径与路径推理"},{en:"Real-time, no batch delay",zh:"实时、无批处理延迟"}],
    [{en:"Embedding / similarity model",zh:"嵌入 / 相似度模型"},{en:"IOC clustering and leaked-secret matching",zh:"IOC 聚类与泄露密钥匹配"},{en:"Connects related evidence fast",zh:"快速关联相关证据"}],
  ];
  const mrows = [[{text:u.model,options:hcell()},{text:u.analyzes,options:hcell()},{text:u.purpose,options:hcell()}]];
  roster.forEach(r => mrows.push([{ text: T(r[0], lang), options: bcell(true) }, { text: T(r[1], lang), options: bcell() }, { text: T(r[2], lang), options: bcell() }]));
  s.addTable(mrows, { x: 0.5, y: 1.6, w: 12.33, colW: [3.6, 5.13, 3.6], border: { type: "solid", color: C.line, pt: 0.5 }, fontSize: 10.5, autoPage: false });
  foot(s);

  // ---- Slide 11: Prompt catalog ----
  s = mk(); s.background = { color: C.bg };
  kicker(s, optShort); atitle(s, u.prompts);
  const pc = D.prompt_catalog;
  const half = Math.ceil(pc.length / 2);
  [[0, half, 0.5], [half, pc.length, 6.75]].forEach(([a, b, x]) => {
    const items = [];
    for (let i = a; i < b; i++) {
      items.push({ text: pc[i].id + "  " + T(pc[i].name, lang), options: { bold: true, color: C.blue, fontSize: 11, breakLine: true, paraSpaceAfter: 1 } });
      items.push({ text: T(pc[i].purpose, lang), options: { color: C.gray, fontSize: 9.5, breakLine: true, paraSpaceAfter: 7 } });
    }
    s.addText(items, { x, y: 1.6, w: 6.05, h: 5.0, fontFace: FT.body, isTextBox: true, margin: 0, valign: "top" });
  });
  foot(s);

  // ---- Slide 12: Trade-off / when to choose ----
  s = mk(); s.background = { color: C.bg };
  kicker(s, optShort); atitle(s, u.tradeoff);
  // this option
  s.addShape(p.ShapeType.roundRect, { x: 0.5, y: 1.7, w: 6.0, h: 4.9, rectRadius: 0.06, fill: { color: C.panel }, line: { color: C.blue, width: 2 } });
  s.addText(optShort, { x: 0.7, y: 1.85, w: 5.6, h: 0.4, fontFace: FT.title, fontSize: 14, bold: true, color: C.blue, isTextBox: true, margin: 0 });
  s.addText(T(arch.fit, lang), { x: 0.7, y: 2.3, w: 5.6, h: 0.9, fontFace: FT.body, fontSize: 11, italic: true, color: C.gray, isTextBox: true, margin: 0, valign: "top" });
  s.addText(u.pros, { x: 0.7, y: 3.2, w: 5.6, h: 0.3, fontFace: FT.title, fontSize: 12, bold: true, color: C.green, isTextBox: true, margin: 0 });
  s.addText(arch.pros.map(pr => ({ text: "✓ " + T(pr, lang), options: { breakLine: true, paraSpaceAfter: 4 } })), { x: 0.7, y: 3.5, w: 5.6, h: 1.5, fontFace: FT.body, fontSize: 10.5, color: C.gray, isTextBox: true, margin: 0, valign: "top" });
  s.addText(u.cons, { x: 0.7, y: 5.05, w: 5.6, h: 0.3, fontFace: FT.title, fontSize: 12, bold: true, color: C.orange, isTextBox: true, margin: 0 });
  s.addText(arch.cons.map(cn => ({ text: "△ " + T(cn, lang), options: { breakLine: true, paraSpaceAfter: 4 } })), { x: 0.7, y: 5.35, w: 5.6, h: 1.2, fontFace: FT.body, fontSize: 10.5, color: C.gray, isTextBox: true, margin: 0, valign: "top" });
  // vs other
  s.addShape(p.ShapeType.roundRect, { x: 6.83, y: 1.7, w: 6.0, h: 4.9, rectRadius: 0.06, fill: { color: C.bg }, line: { color: C.line, width: 1 } });
  s.addText(u.chooseThis, { x: 7.03, y: 1.85, w: 5.6, h: 0.35, fontFace: FT.title, fontSize: 12.5, bold: true, color: C.blue, isTextBox: true, margin: 0 });
  const chooseThis = optId === "A"
    ? [{en:"You already run a SIEM/SOC and want lower cost and risk",zh:"已有 SIEM/SOC，希望更低成本与风险"},{en:"You need to close the 2026 gaps within a quarter",zh:"需在一个季度内补上 2026 年缺口"},{en:"Humans should stay at the decision point for now",zh:"当前仍希望由人把守决策点"}]
    : [{en:"You are a high-value target facing autonomous swarms",zh:"你是面对自主集群的高价值目标"},{en:"Human-paced response is already too slow",zh:"人类节奏的响应已然过慢"},{en:"You can run and govern sovereign defender-agents",zh:"有能力运行并治理自主防御智能体"}];
  s.addText(chooseThis.map(c => ({ text: "• " + T(c, lang), options: { breakLine: true, paraSpaceAfter: 6 } })), { x: 7.03, y: 2.25, w: 5.6, h: 1.7, fontFace: FT.body, fontSize: 11, color: C.gray, isTextBox: true, margin: 0, valign: "top" });
  s.addText(u.chooseOther, { x: 7.03, y: 4.1, w: 5.6, h: 0.35, fontFace: FT.title, fontSize: 12.5, bold: true, color: C.muted, isTextBox: true, margin: 0 });
  s.addText(T(other.name, lang), { x: 7.03, y: 4.5, w: 5.6, h: 0.6, fontFace: FT.body, fontSize: 11, bold: true, color: C.gray, isTextBox: true, margin: 0, valign: "top" });
  s.addText(T(other.tagline, lang), { x: 7.03, y: 5.05, w: 5.6, h: 1.4, fontFace: FT.body, fontSize: 10.5, italic: true, color: C.muted, isTextBox: true, margin: 0, valign: "top" });
  foot(s);

  // ---- Slide 13: Roadmap + KPIs ----
  s = mk(); s.background = { color: C.bg };
  kicker(s, optShort); atitle(s, u.roadmap);
  arch.roadmap.forEach((ph, i) => {
    const x = 0.5 + i * 4.16;
    s.addShape(p.ShapeType.roundRect, { x, y: 1.7, w: 3.9, h: 3.0, rectRadius: 0.06, fill: { color: C.panel }, line: { color: C.blue, width: 1 } });
    s.addShape(p.ShapeType.roundRect, { x, y: 1.7, w: 3.9, h: 0.55, rectRadius: 0.06, fill: { color: C.blue } });
    s.addText(T(ph.phase, lang), { x: x + 0.15, y: 1.72, w: 3.6, h: 0.5, fontFace: FT.title, fontSize: 13, bold: true, color: C.white, isTextBox: true, margin: 0, valign: "middle" });
    s.addText(T(ph.items, lang), { x: x + 0.2, y: 2.4, w: 3.5, h: 2.2, fontFace: FT.body, fontSize: 10.5, color: C.gray, isTextBox: true, margin: 0, valign: "top" });
  });
  s.addText(u.kpis, { x: 0.5, y: 4.95, w: 12, h: 0.4, fontFace: FT.title, fontSize: 15, bold: true, color: C.blue, isTextBox: true, margin: 0 });
  arch.kpis.forEach((k, i) => {
    const x = 0.5 + i * 3.11;
    s.addShape(p.ShapeType.roundRect, { x, y: 5.4, w: 2.95, h: 1.2, rectRadius: 0.06, fill: { color: C.bg }, line: { color: C.blue2, width: 1 } });
    s.addText(T(k, lang), { x: x + 0.15, y: 5.5, w: 2.65, h: 1.0, fontFace: FT.body, fontSize: 10.5, bold: true, color: C.ink, isTextBox: true, margin: 0, valign: "middle", align: "center" });
  });
  foot(s);

  // ---- Slide 14: Recommendation + sources ----
  s = mk(); s.background = { color: C.navy };
  s.addText(u.reco, { x: 0.6, y: 0.7, w: 12, h: 0.6, fontFace: FT.title, fontSize: 24, bold: true, color: C.white, isTextBox: true, margin: 0 });
  s.addShape(p.ShapeType.roundRect, { x: 0.6, y: 1.6, w: 12.1, h: 2.2, rectRadius: 0.08, fill: { color: "12354A" }, line: { color: C.ice, width: 1.5 } });
  s.addText(u.recoBody, { x: 0.9, y: 1.85, w: 11.5, h: 1.7, fontFace: FT.body, fontSize: 15, color: C.white, isTextBox: true, margin: 0, valign: "top" });
  s.addText(u.evNote, { x: 0.6, y: 4.1, w: 12.1, h: 0.8, fontFace: FT.body, fontSize: 10.5, italic: true, color: "9FB3C8", isTextBox: true, margin: 0, valign: "top" });
  // a few sources
  const key = ["S1","S2","S3","S5","S7","S40","S42","S49"];
  const srcs = key.map(id => D.sources.find(x => x.id === id)).filter(Boolean);
  s.addText(u.sources, { x: 0.6, y: 4.85, w: 12, h: 0.35, fontFace: FT.title, fontSize: 13, bold: true, color: C.ice, isTextBox: true, margin: 0 });
  s.addText(srcs.map(x => ({ text: x.title + " — " + x.publisher + ", " + x.date, options: { breakLine: true, paraSpaceAfter: 2, fontSize: 9.5 } })), { x: 0.6, y: 5.2, w: 12.1, h: 1.7, fontFace: FT.body, color: "C9D6E5", isTextBox: true, margin: 0, valign: "top" });

  return;
}

function hcell() { return { fill: { color: C.panel }, color: C.gray, bold: true, fontSize: 10, fontFace: FT.body, align: "left", valign: "middle", margin: [3, 4, 3, 4] }; }
function bcell(bold) { return { color: bold ? C.ink : C.gray, bold: !!bold, fontSize: 10, fontFace: FT.body, align: "left", valign: "top", margin: [3, 4, 3, 4], fill: { color: C.bg } }; }

function newPres() {
  const p = new pptxgen();
  p.defineLayout({ name: "W", width: 13.333, height: 7.5 });
  p.layout = "W";
  p.author = "ET-DAO";
  return p;
}

// Cover + contents for the combined deck
function addCover(p) {
  let s = p.addSlide();
  s.background = { color: C.navy };
  s.addText("ET-DAO", { x: 0.6, y: 0.5, w: 4, h: 0.5, fontFace: FT.title, fontSize: 20, bold: true, color: C.white, isTextBox: true, margin: 0 });
  s.addText("AI Agent Attack & Defense  ·  AI 智能体攻击与防御", { x: 0.6, y: 1.9, w: 12, h: 0.5, fontFace: FT.body, fontSize: 15, color: C.ice, bold: true, charSpacing: 1, isTextBox: true, margin: 0 });
  s.addText(T(D.meta.title, "en"), { x: 0.6, y: 2.45, w: 12.1, h: 1.0, fontFace: FT.title, fontSize: 30, bold: true, color: C.white, isTextBox: true, margin: 0, valign: "top" });
  s.addText(T(D.meta.title, "zh"), { x: 0.6, y: 3.5, w: 12.1, h: 0.7, fontFace: FT.title, fontSize: 20, bold: true, color: "C9D6E5", isTextBox: true, margin: 0, valign: "top" });
  s.addText("Two defense architectures × two languages, in one deck  ·  两套防御架构 × 双语，合并为一份", { x: 0.6, y: 4.35, w: 12, h: 0.5, fontFace: FT.body, fontSize: 13, color: "9FB3C8", isTextBox: true, margin: 0 });
  s.addText("25 September 2026   ·   Confidential — security research briefing  ·  机密安全研究简报", { x: 0.6, y: 6.7, w: 12, h: 0.4, fontFace: FT.body, fontSize: 11, color: C.muted, isTextBox: true, margin: 0 });

  // contents
  s = p.addSlide();
  s.background = { color: C.bg };
  s.addText("CONTENTS · 目录", { x: 0.5, y: 0.32, w: 12.3, h: 0.3, fontFace: FT.body, fontSize: 11, color: C.blue2, bold: true, charSpacing: 1, isTextBox: true, margin: 0 });
  s.addText("Four parts — pick your architecture and language", { x: 0.5, y: 0.62, w: 12.3, h: 0.9, fontFace: FT.title, fontSize: 26, bold: true, color: C.ink, isTextBox: true, margin: 0, valign: "top" });
  const parts = [
    ["Part 1 · Option A — SOC-Evolved (English)", "第一部分 · 方案 A — SOC 演进式（英文）", "Slides 3–16", C.blue],
    ["Part 2 · 方案 A — SOC 演进式（中文）", "Part 2 · Option A — SOC-Evolved (Chinese)", "Slides 17–30", C.blue2],
    ["Part 3 · Option B — AI-Native Defense Mesh (English)", "第三部分 · 方案 B — AI 原生防御网格（英文）", "Slides 31–44", C.blue],
    ["Part 4 · 方案 B — AI 原生防御网格（中文）", "Part 4 · Option B — AI-Native Defense Mesh (Chinese)", "Slides 45–58", C.blue2],
  ];
  parts.forEach((pt, i) => {
    const y = 1.75 + i * 1.28;
    s.addShape(p.ShapeType.roundRect, { x: 0.5, y, w: 12.33, h: 1.1, rectRadius: 0.06, fill: { color: C.panel }, line: { color: pt[3], width: 1.5 } });
    s.addText(pt[0], { x: 0.8, y: y + 0.14, w: 9.5, h: 0.42, fontFace: FT.title, fontSize: 15, bold: true, color: C.ink, isTextBox: true, margin: 0 });
    s.addText(pt[1], { x: 0.8, y: y + 0.58, w: 9.5, h: 0.42, fontFace: FT.body, fontSize: 12, color: C.gray, isTextBox: true, margin: 0 });
    s.addText(pt[2], { x: 10.4, y: y + 0.32, w: 2.2, h: 0.5, align: "right", fontFace: FT.body, fontSize: 12, bold: true, color: pt[3], isTextBox: true, margin: 0, valign: "middle" });
  });
}

const outDir = "/home/user/ClaudeLocal/temp";
const jobs = [["A", "en"], ["A", "zh"], ["B", "en"], ["B", "zh"]];
const sectionTitle = { "A_en": "Option A — SOC-Evolved (EN)", "A_zh": "方案 A — SOC 演进式 (中文)", "B_en": "Option B — AI-Native Defense Mesh (EN)", "B_zh": "方案 B — AI 原生防御网格 (中文)" };

(async () => {
  // 1) individual decks (refreshed with continuous-style footers)
  for (const [opt, lang] of jobs) {
    const p = newPres();
    const PAGE = { n: 0 };
    buildDeck(opt, lang, p, PAGE);
    const name = `${outDir}/AI_Defense_Architecture_Option_${opt}_${lang.toUpperCase()}.pptx`;
    await p.writeFile({ fileName: name });
    console.log("wrote", name);
  }
  // 2) combined deck
  const P = newPres();
  const PAGE = { n: 0 };
  addCover(P); PAGE.n = 2; // cover + contents counted
  for (const [opt, lang] of jobs) {
    P.addSection({ title: sectionTitle[opt + "_" + lang] });
    buildDeck(opt, lang, P, PAGE);
  }
  const combined = `${outDir}/AI_Attack_Defense_ALL_EN_ZH.pptx`;
  await P.writeFile({ fileName: combined });
  console.log("wrote", combined, "| total slides:", PAGE.n);
})();
