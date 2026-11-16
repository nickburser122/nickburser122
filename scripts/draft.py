import argparse
import json
import re

ap = argparse.ArgumentParser()
ap.add_argument("--owner", required=True)
ap.add_argument("--repo", required=True)
ap.add_argument("--name", default="")
ap.add_argument("--description", default="")
ap.add_argument("--audit", required=True)
ap.add_argument("--testlog", default="")
ap.add_argument("--tool-readme", default="")
ap.add_argument("--profile-readme", required=True)
ap.add_argument("--entry-out", default="")
ap.add_argument("--body-out", required=True)
args = ap.parse_args()

audit = json.load(open(args.audit, encoding="utf-8"))
name = args.name or args.repo
slug = re.sub(r"[^a-z0-9]+", "-", args.repo.lower()).strip("-")
base = "https://github.com/%s/%s" % (args.owner, args.repo)

tests = {}
if args.testlog:
    log = open(args.testlog, encoding="utf-8", errors="replace").read()
    for key in ("tests", "pass", "fail"):
        m = re.search(r"^# %s (\d+)" % key, log, re.M)
        if m:
            tests[key] = int(m.group(1))
    m = re.search(r"all (\d+) passed", log)
    if m and "pass" not in tests:
        tests["pass"] = tests["tests"] = int(m.group(1))
        tests["fail"] = 0

checked = []
if tests.get("tests"):
    if tests.get("fail", 0) == 0:
        checked.append("%d tests pass in Node." % tests["pass"])
    else:
        checked.append("%d of %d tests pass in Node; %d fail." % (tests["pass"], tests["tests"], tests["fail"]))
else:
    checked.append("TODO: add a check that was run, with its count.")

candidates = []
limits_anchor = ""
if args.tool_readme:
    text = open(args.tool_readme, encoding="utf-8", errors="replace").read()
    m = re.search(r"^#{1,4}\s*(known limits|limits|limitations|what it does not do)\s*$", text, re.I | re.M)
    if m:
        limits_anchor = "#" + re.sub(r"[^a-z0-9 -]", "", m.group(1).lower()).replace(" ", "-")
        rest = text[m.end():]
        stop = re.search(r"^#{1,4}\s", rest, re.M)
        section = rest[: stop.start()] if stop else rest
        for line in section.splitlines():
            line = line.strip()
            if line.startswith(("- ", "* ")):
                candidates.append(re.sub(r"\s+", " ", line[2:]))
    for line in text.splitlines():
        if re.search(r"\b(not tested|untested|not checked|has not been|have not been|never been)\b", line, re.I):
            clean = re.sub(r"\s+", " ", line.strip(" -*"))
            if clean not in candidates:
                candidates.append(clean)

links = ["[Source](%s)" % base]
if limits_anchor:
    links.append("[Known limits](%s/blob/main/README.md%s)" % (base, limits_anchor))

desc = args.description.strip() or "TODO: one sentence on what the tool does."
second = audit["network"] + (" " + audit["install"] if audit.get("install") else "")
alt = "%s: TODO describe what the screen shows" % name

rows = max(len(checked), 1)
ledger = ["| Checked | Not checked |", "| --- | --- |"]
for i in range(rows):
    left = checked[i] if i < len(checked) else ""
    right = "TODO: one limit that has a source in the repo." if i == 0 else ""
    ledger.append("| %s | %s |" % (left, right))

entry = "\n".join(
    [
        "### %s" % name,
        "",
        " · ".join(links),
        "",
        "![%s](assets/%s-light.png#gh-light-mode-only)" % (alt, slug),
        "![%s](assets/%s-dark.png#gh-dark-mode-only)" % (alt, slug),
        "",
        "%s TODO: the main limit. %s" % (desc, second),
        "",
        *ledger,
        "",
        "",
    ]
)

readme = open(args.profile_readme, encoding="utf-8").read()
marker = "## How these are built"
if marker not in readme:
    raise SystemExit("marker heading not found in profile README")
if ("github.com/%s/%s" % (args.owner, args.repo)).lower() in readme.lower():
    raise SystemExit("%s is already linked from the profile README" % args.repo)
open(args.profile_readme, "w", encoding="utf-8").write(readme.replace(marker, entry + marker, 1))
if args.entry_out:
    open(args.entry_out, "w", encoding="utf-8").write(entry)

body = ["Draft entry for [%s](%s). Nothing here is final: every `TODO` in the README diff needs a person.\n" % (name, base)]
body.append("### Generated")
body.append("- Network and install lines come from reading the source (`scripts/audit.mjs`).")
body.append("- Test counts come from the tool's own test script, run in CI. " + ("Counts: %s." % json.dumps(tests) if tests else "No test script ran."))
body.append("- Screenshots are in `assets/%s-light.png` and `assets/%s-dark.png`, captured offline with fonts that may fall back.\n" % (slug, slug))
if audit.get("needsHuman"):
    body.append("### Audit flags")
    body += ["- %s" % x for x in audit["needsHuman"]]
    body.append("")
if audit.get("evidence"):
    body.append("### Network evidence")
    for e in audit["evidence"]:
        body.append("- %s: %s (%s)" % (e["kind"], e["host"], ", ".join(e["files"])))
    body.append("")
if candidates:
    body.append("### Candidate limits from the tool's README")
    body += ["- %s" % c for c in candidates[:12]]
    body.append("")
body += [
    "### Checklist",
    "- [ ] Every `TODO` is replaced or the cell is left empty",
    "- [ ] Each Not checked cell has a source in the repo",
    "- [ ] Screenshots show no real names, numbers or patient data",
    "- [ ] Alt text states what the screen shows",
    "- [ ] \"Four tools\" in the Selected tools text is updated",
    "- [ ] The tool is removed from More tools or Everything else if it was listed there",
    "- [ ] The navigation line still matches the headings",
    "- [ ] Live links and test-page links loaded and reported zero failures, or were left out",
]
open(args.body_out, "w", encoding="utf-8").write("\n".join(body) + "\n")
