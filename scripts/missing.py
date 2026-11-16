import json
import os
import re
import sys

owner, readme_path = sys.argv[1], sys.argv[2]
repos = json.load(sys.stdin)
readme = open(readme_path, encoding="utf-8").read().lower()
listed = set(re.findall(r"github\.com/" + re.escape(owner.lower()) + r"/([a-z0-9._-]+)", readme))

ignore_path = os.path.join(os.path.dirname(__file__), "ignore.txt")
ignored = set()
if os.path.exists(ignore_path):
    ignored = {l.strip().lower() for l in open(ignore_path, encoding="utf-8") if l.strip()}

missing = []
for r in repos:
    name = r["name"].lower()
    if r.get("fork") or r.get("archived") or r.get("private") or r.get("disabled"):
        continue
    if name in (owner.lower(), owner.lower() + ".github.io") or name in ignored or name in listed:
        continue
    missing.append(r)

if missing:
    print("These public repositories are not linked from the profile README.\n")
    for r in sorted(missing, key=lambda r: r["name"].lower()):
        desc = (r.get("description") or "no description").strip()
        print("- [ ] [%s](%s): %s" % (r["name"], r["html_url"], desc))
    print("\nRun the workflow **Draft a tool entry** with the repository name to open a draft pull request for one.")
    print("To leave a repository off the page for good, add its name to `scripts/ignore.txt`.")
