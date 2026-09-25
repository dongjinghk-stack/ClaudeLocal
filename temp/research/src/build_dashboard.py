import json

DATA = open("/home/user/ClaudeLocal/temp/research/research_data.json", encoding="utf-8").read()

# UI chrome strings (bilingual), separate from research content
UI = {
  "en": {
    "brandTag": "ET-DAO · AI+ Acceleration · Security Research Briefing",
    "nav": {"summary":"Summary","findings":"Key findings","evolution":"Attack evolution","victims":"Victims",
            "hf":"Hugging Face case","defense":"Defense architecture","prompts":"AI prompt catalog",
            "corrections":"Corrections","sources":"Sources"},
    "confidence":"Confidence","sources_lbl":"Sources","method":"Method",
    "issueTree":"Issue tree","hypotheses":"Hypotheses & verdicts","verdict":"Verdict","note":"Note",
    "selfLearning":"How the agents self-learn","commonality":"What the victims share",
    "attackAngles":"Attack angles","trigger":"Trigger / root cause","timeline":"Timeline",
    "attackPath":"Attack path","detection":"Detection","logSources":"Telemetry & log sources — what was actually used",
    "refusal":"The commercial-model refusal","glm":"What GLM-5.2 actually did","response":"Response & containment",
    "lessons":"Lessons learned","requirements":"Requirements","layers":"Layers","dataflow":"Data flow",
    "pros":"Pros","cons":"Cons","roadmap":"Roadmap","kpis":"KPIs","model":"Model","purpose":"Purpose",
    "systemPrompt":"System prompt","taskTemplate":"Task template","bestFit":"Best fit","used":"Used",
    "status":"Status","org":"Org","country":"Country","sector":"Sector","date":"Date","what":"What happened",
    "vector":"Vector","agent":"Agent","lag":"Disclosure lag","stage":"Stage","asset":"Asset","event":"Event",
    "premise":"Your premise","evidence":"What the evidence says","priority":"Priority","tapPrompt":"Show prompt",
    "hidePrompt":"Hide prompt","optA":"Option A","optB":"Option B",
    "evNote":"Evidence caveat","q1":"Q1 · How AI-agent attacks evolved through 2026",
    "q2":"Q2 · Who was hit and what they share","q4":"Q4 · A defense architecture against AI-agent attacks",
    "chooseArch":"Two alternatives — choose by your starting point and risk appetite"
  },
  "zh": {
    "brandTag": "ET-DAO · AI+ 加速 · 安全研究简报",
    "nav": {"summary":"摘要","findings":"核心发现","evolution":"攻击演进","victims":"受害方",
            "hf":"Hugging Face 案例","defense":"防御架构","prompts":"AI 提示词目录",
            "corrections":"事实校正","sources":"来源"},
    "confidence":"置信度","sources_lbl":"来源","method":"方法",
    "issueTree":"议题树","hypotheses":"假设与结论","verdict":"结论","note":"说明",
    "selfLearning":"智能体如何自学习","commonality":"受害方的共性",
    "attackAngles":"攻击角度","trigger":"起因 / 根因","timeline":"时间线",
    "attackPath":"攻击路径","detection":"检测","logSources":"遥测与日志来源——实际使用了哪些",
    "refusal":"商业模型的拒答","glm":"GLM-5.2 究竟做了什么","response":"响应与遏制",
    "lessons":"经验教训","requirements":"需求","layers":"分层","dataflow":"数据流",
    "pros":"优势","cons":"劣势","roadmap":"路线图","kpis":"关键指标","model":"模型","purpose":"用途",
    "systemPrompt":"系统提示词","taskTemplate":"任务模板","bestFit":"适用对象","used":"是否使用",
    "status":"状态","org":"机构","country":"国家","sector":"行业","date":"日期","what":"发生了什么",
    "vector":"入侵途径","agent":"智能体","lag":"披露滞后","stage":"阶段","asset":"资产","event":"事件",
    "premise":"你的前提","evidence":"证据表明","priority":"优先级","tapPrompt":"展开提示词",
    "hidePrompt":"收起提示词","optA":"方案 A","optB":"方案 B",
    "evNote":"证据说明","q1":"Q1 · 2026 年 AI 智能体攻击如何演进","q2":"Q2 · 谁被攻击、共性何在",
    "q4":"Q4 · 面向 AI 智能体攻击的防御架构","chooseArch":"两套备选——按起点与风险偏好选择"
  }
}

HTML = r'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>AI Agent Attack & Defense — ET-DAO Research</title>
<script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<style>
:root{--font-sans:"Inter","SF Pro Display",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
--radius-sm:8px;--radius-md:12px;--radius-lg:16px;--space-xs:4px;--space-sm:8px;--space-md:16px;--space-lg:24px;--space-xl:32px;}
[data-theme="light"]{--bg-primary:#fff;--bg-secondary:#f8f9fb;--bg-card:#fff;--text-primary:#0b1726;--text-secondary:#5b6777;--text-muted:#8b95a5;--accent-primary:#0c5c87;--accent-secondary:#1a7ab8;--accent-success:#2e7d32;--accent-warning:#c46b1c;--accent-danger:#c62828;--border:#e6ecf3;--shadow:rgba(10,25,41,.08);--callout-bg:#f0f7fb;--callout-border:#0c5c87;--callout-text:#0b1726;}
[data-theme="dark"]{--bg-primary:#0d1117;--bg-secondary:#161b22;--bg-card:#1c2128;--text-primary:#e6edf3;--text-secondary:#8b949e;--text-muted:#6e7681;--accent-primary:#58a6d4;--accent-secondary:#79c0e8;--accent-success:#3fb950;--accent-warning:#d29922;--accent-danger:#f85149;--border:#30363d;--shadow:rgba(0,0,0,.3);--callout-bg:#1e3a4f;--callout-border:#58a6d4;--callout-text:#e6edf3;}
*{box-sizing:border-box;}html,body{margin:0;padding:0;}
body{font-family:var(--font-sans);background:var(--bg-primary);color:var(--text-primary);font-size:14px;line-height:1.55;-webkit-font-smoothing:antialiased;transition:background .2s,color .2s;}
.page{max-width:1180px;margin:0 auto;padding:20px 18px 64px;}
.topbar{display:flex;align-items:center;justify-content:space-between;padding:14px 0;margin-bottom:10px;position:sticky;top:0;background:var(--bg-primary);z-index:50;border-bottom:1px solid var(--border);}
.brand a{display:inline-flex;align-items:center;gap:10px;text-decoration:none;color:var(--text-secondary);}
.logo{height:36px;width:auto;display:block;}
.brand .btag{font-size:11px;font-weight:600;letter-spacing:.03em;color:var(--text-muted);}
.controls{display:flex;align-items:center;gap:12px;}
.theme-toggle{width:40px;height:40px;border-radius:50%;border:1px solid var(--border);background:var(--bg-secondary);cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center;transition:all .2s;}
.theme-toggle:hover{background:var(--accent-primary);border-color:var(--accent-primary);}
.lang-toggle{display:inline-flex;border:1px solid var(--border);border-radius:999px;overflow:hidden;}
.lang-toggle button{padding:8px 14px;border:none;background:transparent;cursor:pointer;font-size:14px;color:var(--text-secondary);font-family:inherit;transition:all .2s;}
.lang-toggle button.active{background:var(--accent-primary);color:#fff;}
.lang-toggle button:hover:not(.active){background:var(--bg-secondary);}
.nav{display:flex;flex-wrap:wrap;gap:6px;margin:14px 0 26px;}
.nav a{font-size:12px;font-weight:600;padding:6px 12px;border-radius:999px;background:var(--bg-secondary);border:1px solid var(--border);color:var(--text-secondary);text-decoration:none;transition:all .15s;}
.nav a:hover{background:var(--accent-primary);color:#fff;border-color:var(--accent-primary);}
.hero{margin-bottom:var(--space-xl);}
.hero h1{font-size:32px;font-weight:700;line-height:1.2;margin:0 0 var(--space-sm);}
.hero p.subtitle{font-size:16px;color:var(--text-secondary);margin:0;max-width:900px;}
.section{margin-bottom:44px;scroll-margin-top:80px;}
.section>h2{font-size:22px;font-weight:600;margin:0 0 6px;}
.section .qlabel{font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--accent-secondary);margin-bottom:4px;}
.section h3{font-size:16px;font-weight:600;margin:18px 0 8px;}
.card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-md);padding:var(--space-md);box-shadow:0 10px 24px var(--shadow);}
.grid{display:grid;gap:16px;}
.grid-2{grid-template-columns:repeat(auto-fit,minmax(300px,1fr));}
.grid-3{grid-template-columns:repeat(auto-fit,minmax(210px,1fr));}
.grid-4{grid-template-columns:repeat(auto-fit,minmax(190px,1fr));}
.kpi-value{font-size:26px;font-weight:700;color:var(--accent-primary);line-height:1.1;margin:0 0 4px;}
.kpi-label{font-size:12px;font-weight:500;color:var(--text-secondary);margin:0 0 6px;}
.kpi-source{font-size:11px;color:var(--text-muted);margin-top:var(--space-sm);}
.callout{background:var(--callout-bg);border:2px solid var(--callout-border);border-radius:var(--radius-md);padding:var(--space-lg);color:var(--callout-text);}
.callout h3{margin-top:0;color:var(--callout-text);}
.callout-accent{border-left:4px solid var(--accent-primary);background:var(--bg-secondary);padding:var(--space-md);border-radius:var(--radius-sm);}
.data-table{width:100%;border-collapse:collapse;font-size:12.5px;}
.data-table thead th{background:var(--bg-secondary);text-align:left;padding:8px 10px;font-weight:600;color:var(--text-secondary);border-bottom:1px solid var(--border);text-transform:uppercase;letter-spacing:.03em;font-size:10.5px;}
.data-table tbody td{padding:8px 10px;border-bottom:1px solid var(--border);vertical-align:top;}
.data-table tbody tr:last-child td{border-bottom:none;}
.table-wrap{overflow-x:auto;border:1px solid var(--border);border-radius:var(--radius-md);}
.tag{display:inline-block;padding:2px 10px;border-radius:999px;font-size:11px;font-weight:600;background:var(--bg-secondary);color:var(--text-secondary);border:1px solid var(--border);}
.tag-success{background:var(--accent-success);color:#fff;border-color:transparent;}
.tag-warning{background:var(--accent-warning);color:#fff;border-color:transparent;}
.tag-danger{background:var(--accent-danger);color:#fff;border-color:transparent;}
.tag-info{background:var(--accent-secondary);color:#fff;border-color:transparent;}
.cite{font-size:10.5px;color:var(--accent-secondary);font-weight:600;}
.evidence-note{background:var(--bg-secondary);border-left:4px solid var(--accent-warning);border-radius:var(--radius-sm);padding:12px 16px;font-size:12.5px;color:var(--text-secondary);margin-bottom:20px;}
.tl{position:relative;margin:0;padding:0 0 0 22px;list-style:none;border-left:2px solid var(--border);}
.tl li{position:relative;padding:0 0 18px 18px;}
.tl li::before{content:'';position:absolute;left:-27px;top:3px;width:12px;height:12px;border-radius:50%;background:var(--accent-primary);border:2px solid var(--bg-primary);}
.tl .d{font-weight:700;color:var(--accent-secondary);font-size:12px;}
.track-rogue{border-left-color:var(--accent-warning)!important;}
.track-criminal{border-left-color:var(--accent-danger)!important;}
.track-eval{border-left-color:var(--accent-secondary)!important;}
.arch-layer{border:1px solid var(--border);border-radius:var(--radius-sm);padding:12px 14px;margin-bottom:10px;background:var(--bg-secondary);}
.arch-layer .lname{font-weight:700;font-size:13px;color:var(--accent-primary);margin-bottom:8px;}
.chips{display:flex;flex-wrap:wrap;gap:6px;}
.chip{font-size:11.5px;padding:4px 10px;border-radius:var(--radius-sm);background:var(--bg-card);border:1px solid var(--border);color:var(--text-primary);}
.flow{font-size:12px;color:var(--text-secondary);margin:10px 0;padding:10px 12px;background:var(--bg-secondary);border-radius:var(--radius-sm);}
.pill-row{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0;}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:11.5px;white-space:pre-wrap;background:var(--bg-secondary);border:1px solid var(--border);border-radius:var(--radius-sm);padding:10px 12px;color:var(--text-primary);}
.prompt-toggle{cursor:pointer;font-size:12px;font-weight:600;color:var(--accent-primary);background:none;border:1px solid var(--border);border-radius:var(--radius-sm);padding:5px 10px;font-family:inherit;}
.matrix td.y{color:var(--accent-success);font-weight:700;text-align:center;}
.matrix td.n{color:var(--text-muted);text-align:center;}
.matrix td.p{color:var(--accent-warning);font-weight:600;text-align:center;font-size:10px;}
.sources{list-style:none;padding:0;margin:0;counter-reset:src;}
.sources li{counter-increment:src;padding:8px 0 8px 34px;position:relative;font-size:12.5px;color:var(--text-secondary);border-bottom:1px solid var(--border);}
.sources li::before{content:counter(src);position:absolute;left:0;top:8px;width:22px;height:22px;border-radius:50%;background:var(--accent-primary);color:#fff;font-size:10.5px;font-weight:600;display:flex;align-items:center;justify-content:center;}
.sources a{color:var(--accent-secondary);text-decoration:none;word-break:break-all;}
.footer{margin-top:var(--space-xl);padding-top:var(--space-lg);border-top:1px solid var(--border);font-size:12px;color:var(--text-muted);text-align:center;}
.legend{font-size:11px;color:var(--text-muted);margin-top:8px;}
@media(max-width:720px){.topbar{flex-direction:column;gap:12px;align-items:flex-start;}.controls{width:100%;justify-content:flex-start;}.hero h1{font-size:24px;}.section>h2{font-size:18px;}.grid-2,.grid-3,.grid-4{grid-template-columns:1fr;}.kpi-value{font-size:22px;}}
</style>
</head>
<body>
<div id="root"></div>
<script>window.__DATA__ = __DATA_JSON__;
window.__UI__ = __UI_JSON__;</script>
<script type="text/babel">
const {useState,useEffect} = React;
const D = window.__DATA__, UI = window.__UI__;
const tx = (o,lang)=> o && typeof o==='object' && ('en' in o) ? o[lang] : o;

function Cite({ids}){ if(!ids||!ids.length) return null; return <span className="cite"> {ids.map(i=>'['+i+']').join(' ')}</span>; }
function confTag(c){ const s=(''+c).toLowerCase(); if(s.startsWith('high'))return 'tag-success'; if(s.startsWith('med'))return 'tag-info'; if(s.startsWith('low'))return 'tag-warning'; return 'tag'; }

function TopBar({theme,setTheme,lang,setLang}){
  const u=UI[lang];
  return (<div className="topbar">
    <div className="brand"><a href="https://et-dao.com/" target="_blank" rel="noopener noreferrer">
      <img src="https://et-dao.com/logo_d2_sm.png" alt="ET-DAO" className="logo"/>
      <span className="btag">{u.brandTag}</span></a></div>
    <div className="controls">
      <button className="theme-toggle" onClick={()=>setTheme(theme==='light'?'dark':'light')} aria-label="toggle theme">{theme==='light'?'🌙':'☀️'}</button>
      <div className="lang-toggle">
        <button className={lang==='en'?'active':''} onClick={()=>setLang('en')}>EN</button>
        <button className={lang==='zh'?'active':''} onClick={()=>setLang('zh')}>中文</button>
      </div></div></div>);
}

function Nav({lang}){const n=UI[lang].nav;const ids=Object.keys(n);
  return <nav className="nav">{ids.map(id=><a key={id} href={'#'+id}>{n[id]}</a>)}</nav>;}

function Section({id,qlabel,title,children}){
  return <section className="section" id={id}>
    {qlabel && <div className="qlabel">{qlabel}</div>}
    <h2>{title}</h2>{children}</section>;
}

function App(){
  const init = (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';
  const [theme,setTheme]=useState(init);
  const [lang,setLang]=useState('en');
  const [openP,setOpenP]=useState({});
  useEffect(()=>{document.documentElement.setAttribute('data-theme',theme);},[theme]);
  const u=UI[lang];
  const T=(o)=>tx(o,lang);

  return (<div className="page">
    <TopBar theme={theme} setTheme={setTheme} lang={lang} setLang={setLang}/>
    <Nav lang={lang}/>

    <header className="hero">
      <div style={{marginBottom:8}}><span className="tag">{D.meta.date} · MBB deep research</span></div>
      <h1>{T(D.meta.title)}</h1>
      <p className="subtitle">{T(D.meta.subtitle)}</p>
    </header>

    <div className="evidence-note"><strong>{u.evNote}. </strong>{T(D.meta.evidence_note)}</div>

    {/* Summary */}
    <Section id="summary" title={u.nav.summary}>
      <div className="callout" style={{marginBottom:16}}>
        <h3>{lang==='en'?'Bottom line':'核心结论'}</h3>
        <p style={{margin:0}}>{T(D.scqa.answer)}</p>
      </div>
      <div className="grid grid-2">
        {[['situation','Situation','情境'],['complication','Complication','冲突'],['question','Question','问题']].map(([k,en2,zh2])=>(
          <div className="card" key={k}><h3>{lang==='en'?en2:zh2}</h3>
            <p style={{margin:0,color:'var(--text-secondary)'}}>{T(D.scqa[k])}</p></div>))}
      </div>
      <h3>{u.kpis}</h3>
      <div className="grid grid-4">
        {D.kpis.map((k,i)=>(<div className="card" key={i}>
          <p className="kpi-value">{k.value}</p>
          <p className="kpi-label">{T(k.label)}</p>
          <p className="kpi-source">{u.sources_lbl}: {k.sources.join(', ')}</p></div>))}
      </div>
    </Section>

    {/* Key findings */}
    <Section id="findings" title={u.nav.findings}>
      <div className="grid grid-2">
        {D.key_findings.map((f,i)=>(<div className="card" key={i}>
          <span className={'tag '+confTag(f.confidence)} style={{marginBottom:8,display:'inline-block'}}>{u.confidence}: {f.confidence}</span>
          <h3 style={{marginTop:4}}>{f.id} · {T(f.title)}</h3>
          <p style={{margin:0,color:'var(--text-secondary)'}}>{T(f.body)}<Cite ids={f.sources}/></p></div>))}
      </div>
      <h3>{u.issueTree}</h3>
      <div className="grid grid-2">
        {D.issue_tree.branches.map((b,i)=>(<div className="card" key={i}>
          <h3 style={{marginTop:0}}>{T(b.q)}</h3>
          <ul style={{margin:0,paddingLeft:18,color:'var(--text-secondary)'}}>{b.children.map((c,j)=><li key={j}>{T(c)}</li>)}</ul></div>))}
      </div>
      <h3>{u.hypotheses}</h3>
      <div className="table-wrap"><table className="data-table"><thead><tr>
        <th>#</th><th>{lang==='en'?'Hypothesis':'假设'}</th><th>{u.verdict}</th><th>{u.confidence}</th><th>{u.note}</th></tr></thead>
        <tbody>{D.hypotheses.map(h=>(<tr key={h.id}><td><strong>{h.id}</strong></td><td>{T(h.text)}</td>
          <td><span className="tag tag-info">{h.verdict}</span></td><td>{h.confidence}</td>
          <td>{h.note?T(h.note):''}<Cite ids={h.sources}/></td></tr>))}</tbody></table></div>
    </Section>

    {/* Evolution */}
    <Section id="evolution" qlabel={u.q1} title={u.selfLearning.replace(/^./,c=>c)+''} >
      <ol className="tl">{D.attack_evolution.map((e,i)=>(<li key={i} className={'track-'+e.track}>
        <span className="d">{e.label}</span> · <strong>{T(e.technique)}</strong> <span className={'tag tag-'+(e.track==='criminal'?'danger':e.track==='rogue'?'warning':'info')}>{e.track}</span>
        <div style={{color:'var(--text-secondary)'}}>{T(e.detail)}<Cite ids={e.sources}/></div></li>))}</ol>
      <div className="legend">rogue = lab model escaped an eval · criminal = deliberate misuse · eval = controlled eval reached a real org</div>
      <h3>{u.selfLearning}</h3>
      <div className="table-wrap"><table className="data-table"><thead><tr>
        <th>{lang==='en'?'Mechanism':'机制'}</th><th>{u.what}</th><th>{u.confidence}</th><th>{u.sources_lbl}</th></tr></thead>
        <tbody>{D.self_learning.map((s,i)=>(<tr key={i}><td><strong>{T(s.mechanism)}</strong></td><td>{T(s.what)}</td>
          <td><span className={'tag '+confTag(s.confidence)}>{s.confidence}</span></td><td><Cite ids={s.sources}/></td></tr>))}</tbody></table></div>
    </Section>

    {/* Victims */}
    <Section id="victims" qlabel={u.q2} title={u.nav.victims}>
      <div className="table-wrap"><table className="data-table"><thead><tr>
        <th>{u.org}</th><th>{u.country}</th><th>{u.sector}</th><th>{u.date}</th><th>{u.what}</th><th>{u.vector}</th><th>{u.agent}</th><th>{u.lag}</th><th>{u.sources_lbl}</th></tr></thead>
        <tbody>{D.victims.map((v,i)=>(<tr key={i}><td><strong>{T(v.org)}</strong></td><td>{T(v.country)}</td><td>{T(v.sector)}</td>
          <td>{v.date}</td><td>{T(v.accessed)}</td><td>{T(v.vector)}</td><td>{T(v.agent)}</td><td>{T(v.lag)}</td><td><Cite ids={v.sources}/></td></tr>))}</tbody></table></div>
      <h3>{u.commonality}</h3>
      <div className="table-wrap"><table className="data-table matrix"><thead><tr><th>{lang==='en'?'Shared condition':'共性维度'}</th>
        {D.commonality.cols.map((c,i)=><th key={i}>{T(c)}</th>)}</tr></thead>
        <tbody>{D.commonality.rows.map((r,i)=>(<tr key={i}><td>{T(r.dim)}</td>
          {r.cells.map((c,j)=><td key={j} className={c===1?'y':c===2?'p':'n'}>{c===1?'✓':c===2?'~':'·'}</td>)}</tr>))}</tbody></table></div>
      <div className="legend">✓ present · ~ partial · · absent</div>
      <h3>{u.attackAngles}</h3>
      <div className="table-wrap"><table className="data-table"><thead><tr>
        <th>{lang==='en'?'Angle':'角度'}</th><th>{u.what}</th><th>{lang==='en'?'Victims observed':'观测到的受害方'}</th></tr></thead>
        <tbody>{D.attack_angles.map((a,i)=>(<tr key={i}><td><strong>{T(a.angle)}</strong></td><td>{T(a.desc)}</td><td>{T(a.victims)}</td></tr>))}</tbody></table></div>
    </Section>

    {/* HF case */}
    <Section id="hf" title={u.nav.hf}>
      <h3>{u.trigger}</h3>
      <div className="callout-accent"><p style={{margin:0}}>{T(D.hf_case.trigger)}</p></div>
      <h3>{u.timeline}</h3>
      <ol className="tl">{D.hf_case.timeline.map((t,i)=>(<li key={i}>
        <span className="d">{t.date}</span> {T(t.event)}<Cite ids={t.sources}/></li>))}</ol>
      <h3>{u.attackPath}</h3>
      <div className="table-wrap"><table className="data-table"><thead><tr>
        <th>{u.stage}</th><th>{u.what}</th><th>{u.asset}</th><th>{u.sources_lbl}</th></tr></thead>
        <tbody>{D.hf_case.attack_path.map((p,i)=>(<tr key={i}><td><strong>{T(p.stage)}</strong></td><td>{T(p.what)}</td><td>{T(p.asset)}</td><td><Cite ids={p.sources}/></td></tr>))}</tbody></table></div>
      <h3>{u.detection}</h3>
      <p style={{color:'var(--text-secondary)'}}>{T(D.hf_case.detection)}</p>
      <h3>{u.logSources}</h3>
      <div className="table-wrap"><table className="data-table"><thead><tr>
        <th>{lang==='en'?'Log source':'日志来源'}</th><th>{u.used}</th><th>{u.status}</th><th>{u.note}</th><th>{u.sources_lbl}</th></tr></thead>
        <tbody>{D.hf_case.log_sources.map((l,i)=>{const uu=l.used===true?(lang==='en'?'yes':'是'):l.used===false?(lang==='en'?'no':'否'):(lang==='en'?'not stated':'未说明');
          const st=l.status==='confirmed'?'tag-success':l.status==='not_disclosed'?'tag-warning':'tag-info';
          return (<tr key={i}><td><strong>{T(l.source)}</strong></td><td>{uu}</td><td><span className={'tag '+st}>{l.status}</span></td><td>{T(l.note)}</td><td><Cite ids={l.sources}/></td></tr>);})}</tbody></table></div>
      <h3>{u.refusal}</h3>
      <div className="callout" style={{marginBottom:16}}><p style={{margin:0}}>{T(D.hf_case.refusal)}</p></div>
      <h3>{u.glm}</h3>
      <div className="callout-accent" style={{marginBottom:12}}><p style={{margin:0}}>{T(D.hf_case.glm_deployment)}</p></div>
      <div className="table-wrap"><table className="data-table"><thead><tr>
        <th>{lang==='en'?'GLM analysis':'GLM 分析'}</th><th>{lang==='en'?'What it produced':'产出'}</th><th>{u.sources_lbl}</th></tr></thead>
        <tbody>{D.hf_case.glm_analysis.map((g,i)=>(<tr key={i}><td><strong>{T(g.task)}</strong></td><td>{T(g.what)}</td><td><Cite ids={g.sources}/></td></tr>))}</tbody></table></div>
      <div className="grid grid-2" style={{marginTop:16}}>
        <div className="card"><h3 style={{marginTop:0}}>{u.response}</h3>
          <ul style={{margin:0,paddingLeft:18,color:'var(--text-secondary)'}}>{D.hf_case.response.map((r,i)=><li key={i}>{T(r)}</li>)}</ul></div>
        <div className="card"><h3 style={{marginTop:0}}>{u.lessons}</h3>
          <ol style={{margin:0,paddingLeft:18,color:'var(--text-secondary)'}}>{D.hf_case.lessons.map((l,i)=><li key={i}>{T(l)}</li>)}</ol></div>
      </div>
    </Section>

    {/* Defense */}
    <Section id="defense" qlabel={u.q4} title={u.nav.defense}>
      <h3>{u.requirements}</h3>
      <div className="table-wrap"><table className="data-table"><thead><tr>
        <th>{lang==='en'?'Requirement':'需求'}</th><th>{lang==='en'?'Why (from the evidence)':'依据（源自证据）'}</th><th>{u.priority}</th></tr></thead>
        <tbody>{D.defense_requirements.map((r,i)=>(<tr key={i}><td><strong>{T(r.req)}</strong></td><td>{T(r.why)}</td>
          <td><span className={'tag '+(r.priority==='must'?'tag-danger':'tag-warning')}>{r.priority}</span></td></tr>))}</tbody></table></div>
      <p style={{color:'var(--text-secondary)',marginTop:18}}><strong>{u.chooseArch}</strong></p>
      <div className="grid grid-2">
        {D.architectures.map((a,ai)=>(<div className="card" key={ai}>
          <span className={'tag '+(a.id==='A'?'tag-info':'tag-danger')}>{a.id==='A'?u.optA:u.optB}</span>
          <h3 style={{marginTop:8}}>{T(a.name)}</h3>
          <p style={{color:'var(--text-secondary)',marginTop:0}}>{T(a.tagline)}</p>
          <p style={{fontSize:12}}><strong>{u.bestFit}: </strong><span style={{color:'var(--text-secondary)'}}>{T(a.fit)}</span></p>
          <div style={{margin:'10px 0'}}>{a.layers.map((ly,li)=>(<div className="arch-layer" key={li}>
            <div className="lname">{T(ly.name)}</div>
            <div className="chips">{ly.components.map((c,ci)=><span className="chip" key={ci}>{T(c)}</span>)}</div></div>))}</div>
          <div className="flow"><strong>{u.dataflow}: </strong>{a.flows.map(f=>T(f)).join('  →  ')}</div>
          <div className="grid grid-2">
            <div><h3 style={{margin:'6px 0'}}>{u.pros}</h3><ul style={{margin:0,paddingLeft:16,color:'var(--text-secondary)',fontSize:12.5}}>{a.pros.map((p,pi)=><li key={pi}>{T(p)}</li>)}</ul></div>
            <div><h3 style={{margin:'6px 0'}}>{u.cons}</h3><ul style={{margin:0,paddingLeft:16,color:'var(--text-secondary)',fontSize:12.5}}>{a.cons.map((c,ci)=><li key={ci}>{T(c)}</li>)}</ul></div>
          </div>
          <h3 style={{margin:'10px 0 6px'}}>{u.roadmap}</h3>
          {a.roadmap.map((ph,pi)=>(<div key={pi} style={{fontSize:12.5,marginBottom:6}}><span className="tag tag-info">{T(ph.phase)}</span> <span style={{color:'var(--text-secondary)'}}>{T(ph.items)}</span></div>))}
          <h3 style={{margin:'10px 0 6px'}}>{u.kpis}</h3>
          <div className="pill-row">{a.kpis.map((k,ki)=><span className="chip" key={ki}>{T(k)}</span>)}</div>
        </div>))}
      </div>
    </Section>

    {/* Prompts */}
    <Section id="prompts" title={u.nav.prompts}>
      <p style={{color:'var(--text-secondary)'}}>{lang==='en'?'The AI analysis layer should run these analyses, each with a vetted defensive system prompt. Prompts are authored in English; names and purposes are bilingual.':'AI 分析层应执行以下分析，每项都配有经审定的防御式系统提示词。提示词以英文撰写；名称与用途为中英双语。'}</p>
      <div className="grid grid-2">
        {D.prompt_catalog.map((p,i)=>{const open=!!openP[p.id];
          return (<div className="card" key={i}>
            <span className="tag tag-info">{p.id}</span>
            <h3 style={{marginTop:8}}>{T(p.name)}</h3>
            <p style={{fontSize:12,margin:'4px 0'}}><strong>{u.model}: </strong><span style={{color:'var(--text-secondary)'}}>{T(p.model)}</span></p>
            <p style={{fontSize:12.5,color:'var(--text-secondary)',margin:'4px 0 10px'}}>{T(p.purpose)}</p>
            <button className="prompt-toggle" onClick={()=>setOpenP({...openP,[p.id]:!open})}>{open?u.hidePrompt:u.tapPrompt}</button>
            {open && <div style={{marginTop:10}}>
              <div style={{fontSize:11,fontWeight:600,color:'var(--text-muted)',margin:'6px 0 2px'}}>{u.systemPrompt}</div>
              <div className="mono">{p.system}</div>
              <div style={{fontSize:11,fontWeight:600,color:'var(--text-muted)',margin:'8px 0 2px'}}>{u.taskTemplate}</div>
              <div className="mono">{p.task}</div></div>}
          </div>);})}
      </div>
    </Section>

    {/* Corrections */}
    <Section id="corrections" title={u.nav.corrections}>
      <div className="grid grid-2">
        {D.corrections.map((c,i)=>(<div className="card" key={i}>
          <div style={{fontSize:12.5}}><span className="tag tag-warning">{u.premise}</span> <strong>{T(c.premise)}</strong></div>
          <p style={{margin:'8px 0 0',color:'var(--text-secondary)'}}><span className="tag tag-success">{u.evidence}</span> {T(c.evidence)}<Cite ids={c.sources}/></p></div>))}
      </div>
    </Section>

    {/* Sources */}
    <Section id="sources" title={u.nav.sources}>
      <ol className="sources">{D.sources.map((s,i)=>(<li key={i}>
        {s.title} — <em>{s.publisher}</em>, {s.date}. <a href={s.url} target="_blank" rel="noopener noreferrer">{s.url}</a></li>))}</ol>
    </Section>

    <footer className="footer">ET-DAO · Accelerating AI+ Transition · {lang==='en'?'Confidential security research briefing · Generated 2026-09-25':'机密安全研究简报 · 生成于 2026-09-25'}</footer>
  </div>);
}
ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
</script>
</body>
</html>
'''

out = HTML.replace("__DATA_JSON__", DATA).replace("__UI_JSON__", json.dumps(UI, ensure_ascii=False))
open("/home/user/ClaudeLocal/temp/dashboard_ai_attack_defense.html","w",encoding="utf-8").write(out)
print("dashboard bytes:", len(out))
