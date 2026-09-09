#!/usr/bin/env python3
"""
Draw the profile's stat graphics from the GitHub GraphQL API — no third-party
services, stdlib only. Run by .github/workflows/stats.yml on a daily cron.

Outputs (same visual language as the banner: near-black + dark red):
  assets/stat-summary.svg   total contributions, current/longest streak, top language
  assets/stat-year.svg      the last 52 weeks, one cell per day, using the portrait ramp

Local test:  GITHUB_TOKEN=$(gh auth token) GH_LOGIN=onyxmytrojin python scripts/generate_stats.py
"""
import datetime as dt
import json
import os
import urllib.request

TOKEN = os.environ["GITHUB_TOKEN"]
LOGIN = os.environ.get("GH_LOGIN", "onyxmytrojin")

BG = "#0d1117"
DIM = "#8b929c"
TEXT = "#d6dae0"
RED = "#e0555f"
RAMP_HEX = ["#161b22", "#3a1418", "#6b2028", "#9e2f3a", "#e0555f"]  # empty -> busy
FONT = "ui-monospace, 'SF Mono', 'JetBrains Mono', Consolas, monospace"

# --- whole-UTC-day window so nightly runs are byte-identical -----------------
today = dt.datetime.now(dt.timezone.utc).date()
FROM = dt.datetime.combine(today - dt.timedelta(days=364), dt.time.min, dt.timezone.utc)
TO = dt.datetime.combine(today, dt.time.max, dt.timezone.utc)

QUERY = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    contributionsCollection(from:$from, to:$to) {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def gql():
    body = json.dumps({
        "query": QUERY,
        "variables": {"login": LOGIN, "from": FROM.isoformat(), "to": TO.isoformat()},
    }).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json",
                 "User-Agent": LOGIN},
    )
    with urllib.request.urlopen(req) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit(payload["errors"])
    return payload["data"]["user"]


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def compute(user):
    cc = user["contributionsCollection"]
    days = []
    for wk in cc["contributionCalendar"]["weeks"]:
        for d in wk["contributionDays"]:
            days.append((d["date"], d["contributionCount"]))
    days.sort()
    total = cc["contributionCalendar"]["totalContributions"]
    commits = cc["totalCommitContributions"]
    prs = cc["totalPullRequestContributions"]

    # current streak: consecutive days ending today (today with 0 doesn't break)
    cur = 0
    for date, c in reversed(days):
        if c > 0:
            cur += 1
        elif date != today.isoformat():
            break
        elif cur:
            break
    longest = run = 0
    for _, c in days:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    return days, total, cur, longest, commits, prs


# --- summary card ----------------------------------------------------------
def summary_svg(total, cur, longest, commits, prs):
    W, H = 720, 118
    col = [(30, "CONTRIBUTIONS · YR", f"{total:,}", TEXT),
           (215, "COMMITS · YR", f"{commits:,}", TEXT),
           (360, "PULL REQUESTS", f"{prs:,}", TEXT),
           (505, "CURRENT STREAK", f"{cur}", RED),
           (615, "LONGEST", f"{longest}", TEXT)]
    fields = ""
    for x, label, val, fill in col:
        fields += (f'<text x="{x}" y="38" font-size="11" fill="{DIM}" letter-spacing="1.5">{label}</text>'
                   f'<text x="{x}" y="82" font-size="34" font-weight="600" fill="{fill}">{val}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">
<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="#20252d"/>
{fields}
<rect x="0" y="{H-4}" width="{W}" height="4" fill="{RED}" opacity="0.5"/>
</svg>"""


# --- year heatmap (portrait ramp) ----------------------------------------
def year_svg(days):
    CELL, GAP = 11, 3
    weeks = [days[i:i + 7] for i in range(0, len(days), 7)]
    W = len(weeks) * (CELL + GAP) + 30
    H = 7 * (CELL + GAP) + 40
    mx = max((c for _, c in days), default=1) or 1
    cells = ""
    for wi, wk in enumerate(weeks):
        for di, (date, c) in enumerate(wk):
            lvl = 0 if c == 0 else min(4, 1 + int(c / mx * 3.999))
            x = 15 + wi * (CELL + GAP)
            y = 25 + di * (CELL + GAP)
            cells += f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{RAMP_HEX[lvl]}"/>'
    legend = "".join(
        f'<rect x="{W - 95 + i*15}" y="{H-18}" width="11" height="11" rx="2" fill="{c}"/>'
        for i, c in enumerate(RAMP_HEX)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">
<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="10" fill="none" stroke="#20252d"/>
<text x="15" y="17" font-size="11" fill="{DIM}" letter-spacing="2">THE LAST 52 WEEKS</text>
{cells}
<text x="{W-115}" y="{H-9}" font-size="10" fill="{DIM}" text-anchor="end">less</text>
{legend}
<text x="{W-15}" y="{H-9}" font-size="10" fill="{DIM}">more</text>
</svg>"""


def main():
    user = gql()
    days, total, cur, longest, commits, prs = compute(user)
    out = {
        "assets/stat-summary.svg": summary_svg(total, cur, longest, commits, prs),
        "assets/stat-year.svg": year_svg(days),
    }
    for path, svg in out.items():
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
        print("wrote", path, len(svg), "bytes")


if __name__ == "__main__":
    main()
