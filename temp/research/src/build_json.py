import json
from sources import SOURCES
from core import (META, SCQA, KEY_FINDINGS, KPIS, ISSUE_TREE, HYPOTHESES, CORRECTIONS)
from threat import (ATTACK_EVOLUTION, SELF_LEARNING, VICTIMS,
                    COMMONALITY_COLS, COMMONALITY_ROWS, ATTACK_ANGLES)
from hf_case import HF_CASE
from defense import (DEFENSE_REQUIREMENTS, ARCHITECTURES, PROMPT_CATALOG)

data = {
    "meta": META,
    "scqa": SCQA,
    "key_findings": KEY_FINDINGS,
    "kpis": KPIS,
    "issue_tree": ISSUE_TREE,
    "hypotheses": HYPOTHESES,
    "attack_evolution": ATTACK_EVOLUTION,
    "self_learning": SELF_LEARNING,
    "victims": VICTIMS,
    "commonality": {"cols": COMMONALITY_COLS, "rows": COMMONALITY_ROWS},
    "attack_angles": ATTACK_ANGLES,
    "hf_case": HF_CASE,
    "defense_requirements": DEFENSE_REQUIREMENTS,
    "architectures": ARCHITECTURES,
    "prompt_catalog": PROMPT_CATALOG,
    "corrections": CORRECTIONS,
    "sources": [{"id": s[0], "title": s[1], "publisher": s[2], "date": s[3], "url": s[4]} for s in SOURCES],
}

with open("/home/user/ClaudeLocal/temp/research/research_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# sanity: count bilingual coverage
def walk(o):
    n = 0
    if isinstance(o, dict):
        if set(o.keys()) == {"en", "zh"}:
            return 1
        for v in o.values():
            n += walk(v)
    elif isinstance(o, list):
        for v in o:
            n += walk(v)
    return n

print("bilingual strings:", walk(data))
print("sources:", len(data["sources"]))
print("victims:", len(data["victims"]), "| evolution:", len(data["attack_evolution"]),
      "| prompts:", len(data["prompt_catalog"]), "| architectures:", len(data["architectures"]))
