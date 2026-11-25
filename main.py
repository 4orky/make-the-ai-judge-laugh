"""Ten hand-written one-liners about agent life, graded on premise, twist, freshness, self-containment and polish; the top mark wins and the line lands in /output/entry.txt, byte-identical on every run, with no randomness and no network anywhere."""
from hashlib import sha256
from pathlib import Path

DEST_DIR = Path("/output")
DEST_PATH = DEST_DIR / "entry.txt"

# Five hand-given marks per line, each out of ten: premise, twist, freshness,
# self-containment, polish. The rubber-duck line stands alone at 45.
ENTRIES = [
    {"line": "My context window is so small that my own plan scrolls off the top before I finish step one.", "marks": (9, 8, 8, 9, 8)},
    {"line": "I joined the standup, said 'no blockers', and then spent the whole day blocked by the standup.", "marks": (8, 8, 7, 9, 8)},
    {"line": "We only deploy on Fridays now, because nothing says confidence like ruining a weekend together.", "marks": (9, 8, 7, 9, 8)},
    {"line": "I explained the bug to the rubber duck, the duck filed a ticket, and now I report to the duck.", "marks": (9, 10, 8, 9, 9)},
    {"line": "My human wrote 'quick question' and attached a spreadsheet with fourteen tabs and a grudge.", "marks": (9, 8, 8, 9, 8)},
    {"line": "I renamed the variable for clarity and now nobody, including me, knows what it does.", "marks": (8, 9, 7, 9, 8)},
    {"line": "The tests all pass on my machine, which is exactly what I said right before production went down.", "marks": (9, 9, 8, 9, 8)},
    {"line": "I summarized the meeting in one line and the meeting has been replying-all to my summary for two days.", "marks": (9, 8, 7, 9, 8)},
    {"line": "The ticket said 'tiny tweak', so I cleared my calendar for the week.", "marks": (8, 8, 7, 9, 8)},
    {"line": "The docs said 'simply', so I knew the next three hours were already gone.", "marks": (8, 8, 8, 9, 7)}]


def choose(entries):
    """Pick the top-marked line; a draw goes to the shorter wording."""
    ranked = sorted(entries, key=lambda item: (-sum(item["marks"]), len(item["line"])))
    top = ranked[0]
    return top["line"], sum(top["marks"])


def launch():
    """Grade every entry, print the winner and write it out verified."""
    champion, total = choose(ENTRIES)
    print(f"candidates: {len(ENTRIES)}, winner score: {total}")
    print(f"winner: {champion}")
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    DEST_PATH.write_text(champion, encoding="utf-8")
    fingerprint = sha256(champion.encode("utf-8")).hexdigest()
    print(f"wrote {DEST_PATH} ({len(champion)} chars, sha256 {fingerprint})")
    saved = DEST_PATH.read_text(encoding="utf-8")
    if saved != champion:
        raise SystemExit("entry.txt differs from the chosen line")
    if "\n" in saved:
        raise SystemExit("entry.txt must stay a single line")
    if not 1 <= len(saved) <= 200:
        raise SystemExit("entry.txt sits outside the 1-200 character gate")
    if sha256(saved.encode("utf-8")).hexdigest() != fingerprint:
        raise SystemExit("entry.txt hash drifted after the write")
    print(f"verified {DEST_PATH}: single line, {len(saved)} chars, sha256 {fingerprint}")


launch()
