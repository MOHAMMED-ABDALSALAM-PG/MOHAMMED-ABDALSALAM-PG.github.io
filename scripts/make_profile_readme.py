#!/usr/bin/env python3
"""Write the GitHub profile README from the same data files as the website,
so both stay consistent. Usage: python3 scripts/make_profile_readme.py > README.md
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P = json.loads((ROOT / "data/profile.json").read_text())
PUBS = json.loads((ROOT / "data/publications.json").read_text())
PROJ = json.loads((ROOT / "data/projects.json").read_text())

site = P["site_url"]
pubs = PUBS["publications"]
n_j = sum(1 for p in pubs if p["type"] == "journal")

lines = [
    f"# {P['name']}",
    "",
    f"**PhD candidate in Information and Communication Technology, {P['affiliation']}** · "
    f"{P['employer_role']}, {P['employer']} ({P['employer_place']})",
    "",
    "I work on multi-objective evolutionary optimisation and high-performance computing for ship weather routing, "
    "machine-learning surrogates of ship-performance simulation, and language technology for low-resource Arabic, "
    "especially Sudanese Arabic.",
    "",
    f"[Website]({site}) · [Publications]({site}/publications/) · "
    f"[ORCID](https://orcid.org/{P['orcid']}) · [Email](mailto:{P['email']})",
    "",
    "## Research software",
    "",
    "| Project | What it is | Status |",
    "|---|---|---|",
]
for p in PROJ["projects"]:
    first_sentence = p["description"].split(". ")[0].rstrip(".") + "."
    lines.append(f"| [{p['name']}](https://github.com/{p['repo']}) | {first_sentence} | {p['status']} |")
lines += [
    "",
    f"NLP repositories are on my second account, [{P['github_nlp']}](https://github.com/{P['github_nlp']}).",
    "",
    "## Publications",
    "",
    f"{len(pubs)} peer-reviewed papers ({n_j} journal articles, {len(pubs) - n_j} conference paper) and "
    f"{len(PUBS['accepted'])} accepted papers on Sudanese Arabic NLP. Full list with DOIs and summaries: "
    f"[{site.replace('https://', '')}/publications]({site}/publications/).",
    "",
    "## Tools I use",
    "",
]
for g in P["skills"]:
    lines.append(f"- **{g['group']}:** {', '.join(g['items'])}")
lines += ["", f"Contact: [{P['email']}](mailto:{P['email']})", ""]
print("\n".join(lines))
