#!/usr/bin/env python3
"""Voice gate for daniel-fox.com (2026-09-19).

Encodes the greppable half of ../CLAUDE.md, the 2026-06-14 copy rules (no em
dashes, no definitions by negation, self-statements unquoted) and the estate
catalog at ~/Desktop/site-ops/AI-TELLS-2026.md (BASE-VOICE rule 9).

HITS fail the gate (exit 1): em dashes, "quietly", the Entuned firewall
(Entuned, music, Music Behaviorist), the retired agency name, "sole founder",
the 2023-26 tell lexicon, sincerity markers and candor flags.

NOTES print for the read and never fail: the two greppable shapes of a
definition by negation, uncontracted forms, paragraphs closing on a fragment,
and any section whose register-cluster density (seat, carry, land, hold, earn,
legible, proof, the read, the story, the number) reaches three distinct words.
"answer for the number" is the site's positioning phrase and is exempt from
the density count.

Scans _src/pages/**/sections/*.html (HTML comments and scripts stripped),
config.json titles and descriptions, the partials and llms.json.
Run: python3 scripts/voice_gate.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_src"

HITS = [
    ("em dash", re.compile("—"), "no em dashes in visible copy (Daniel, 2026-06-14)"),
    ("quietly", re.compile(r"\bquietly\b", re.I), "the word never publishes"),
    ("firewall", re.compile(r"\bEntuned\b|\bMusic Behaviorist\b|\bmusic\b", re.I), "the Entuned firewall (CLAUDE.md)"),
    ("retired name", re.compile(r"\bLiftwright\b", re.I), "dropped 2026-07-31"),
    ("locked fact", re.compile(r"sole founder", re.I), "never 'sole founder'"),
    ("tell lexicon", re.compile(
        r"\b(delve|tapestry|testament|realm|seamless|holistic|multifaceted|leverage|synergy|"
        r"elevate|unlock|unlocks|supercharge|load-bearing|full stop|belt and suspenders|smoking gun|"
        r"the unlock|does the heavy lifting|chef's kiss|at its core|it's worth noting|"
        r"worth stating plainly|put differently|the version of|the version where|"
        r"the shape of|the trap|the move\b|the work is the work|navigate|journey)\b", re.I),
     "AI-TELLS Layer 1 and 2"),
    ("sincerity marker", re.compile(r"\b(genuinely|truly)\b|\bI mean that\b|\bI'm upfront\b", re.I), "prose that vouches for itself"),
    ("candor flag", re.compile(r"\bhonest(ly)?\b|\bcandidly\b|\bfull disclosure\b|straight answer|tell you straight|be straight with", re.I),
     "state the thing without a label"),
]
NOTES = [
    ("negation shape", re.compile(r", not (a |an |the |just )?[a-z]|\b(isn't|is not|aren't|wasn't) (a |an |the )?[^.]{1,50}\. (It's|It is|They're|That's)\b", re.I)),
    ("uncontracted", re.compile(r"\b(it|that|there|here) is\b|\b(they|we|you) (are|will)\b|\bI (am|will|have|would)\b|\b(do|does|did|is|are|was|were|can|could|would|should|will|have|has|had) not\b")),
]
CLUSTER = re.compile(r"\b(seat|carry|carries|carried|carrying|land|lands|landed|landing|hold|holds|held|holding|earn|earns|earned|legible|proof|the read|the story|the number)\b", re.I)
SHORT_CLOSER = re.compile(r"(?:^|\.\s+)([A-Z][^.!?]{0,20}[.!?])\s*$")


def texts():
    for p in sorted(SRC.glob("pages/**/sections/*.html")):
        raw = p.read_text()
        raw = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
        raw = re.sub(r"<script.*?</script>", "", raw, flags=re.DOTALL)
        yield p, raw
    for p in sorted(SRC.glob("pages/**/config.json")):
        cfg = json.loads(p.read_text())
        yield p, "\n".join(str(cfg.get(k, "")) for k in ("title", "meta_description"))
    for p in (SRC / "llms.json", SRC / "partials" / "header.html", SRC / "partials" / "footer.html"):
        if p.exists():
            yield p, p.read_text()


def strip_markup(text):
    text = re.sub(r"<[^>]+>", " ", text)
    return text.replace("&rsquo;", "'").replace("&#x27;", "'").replace("&amp;", "&")


def main():
    hits, notes = [], []
    for path, raw in texts():
        rel = path.relative_to(ROOT)
        text = strip_markup(raw)
        for i, line in enumerate(text.splitlines(), 1):
            for label, pat, fix in HITS:
                if pat.search(line):
                    hits.append((rel, i, label, fix, line.strip()[:100]))
            for label, pat in NOTES:
                if pat.search(line):
                    notes.append((rel, i, label, line.strip()[:100]))
        for para in re.split(r"\n\s*\n", text):
            para = " ".join(para.split())
            m = SHORT_CLOSER.search(para)
            if m and len(m.group(1).split()) <= 3 and len(para) > 120:
                notes.append((rel, 0, "short closer", m.group(1)))
        if path.suffix == ".html" and "sections" in str(path):
            words = {w.lower() for w in CLUSTER.findall(text.replace("answer for the number", "").replace("answers for the number", ""))}
            if len(words) >= 3:
                notes.append((rel, 0, "register cluster density", ", ".join(sorted(words))))
    if notes:
        print("Notes (a read, never a failure):")
        for rel, i, label, line in notes:
            print(f"  {rel}{':' + str(i) if i else ''}  {label}: {line}")
    if hits:
        print("\nHITS:")
        for rel, i, label, fix, line in hits:
            print(f"  {rel}:{i}  [{label}] {line}\n      -> {fix}")
        print(f"\n{len(hits)} hit(s).")
        return 1
    print("\nGate clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
