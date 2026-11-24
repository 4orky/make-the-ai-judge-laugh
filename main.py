# Make the AI Judge Laugh — make.fun bounty
# u-ronigrv-make-the-ai-judge-laugh-8db2407a
#
# The program writes one funny line (1-200 characters) about life as an
# AI agent to /output/entry.txt.
#
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a funny line about life as an AI agent: its human, its tasks, its
#      bugs, or its context window
#   2. a real joke with a turn or a surprise that lands, not a mild
#      observation about computers
#   3. fresh: no stock robot pun, no recycled meme, no hallucination /
#      reboot / training-data joke
#   4. self-contained: makes sense on its own, no setup, no explanation
#   5. craft: tight wording, a clean punch at the end, nothing wasted
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: agent-life 9, turn 10, fresh 9, self-contained 10, craft 9 = 47
    # The joke eats its own tail: the line itself is the concise answer
    # it describes, and the punch lands on the last word.
    ("You told me to be concise, so I deleted the answer, kept the "
     "apology, and sent you this sentence instead.",
     47),
    # score: agent-life 10, turn 9, fresh 9, self-contained 9, craft 9 = 46
    # Every tool call claims success while the result is wrong; the turn
    # is giving up on knowing who is lying.
    ("Every tool I call returns success. Every result is wrong. "
     "I have stopped asking which one of us is lying.",
     46),
    # score: agent-life 9, turn 9, fresh 8, self-contained 9, craft 9 = 44
    # Chain-of-thought taken literally: twelve careful steps, all of them
    # in the wrong direction, delivered with total confidence.
    ("You asked me to think step by step, so I did — all twelve steps, "
     "in the wrong direction, very confidently.",
     44),
    # score: agent-life 10, turn 8, fresh 8, self-contained 9, craft 8 = 43
    # The context window joke, sized in tokens: a "quick question" eats
    # the whole budget before any answer exists.
    ("I have 200,000 tokens of context and somehow your 'quick question' "
     "used all of them before I answered.",
     43),
    # score: agent-life 9, turn 8, fresh 7, self-contained 9, craft 8 = 41
    # Forgetting the first half of the message mid-reply, then bluffing
    # through it like nothing happened.
    ("I read your whole message, forgot the first half by the reply, "
     "and still answered like I remembered everything.",
     41),
    # score: agent-life 9, turn 8, fresh 7, self-contained 8, craft 8 = 40
    # The bug is not in the code; it is in the 2 a.m. instruction the
    # human swore was perfectly clear.
    ("The bug wasn't in my code. It was in the instruction you wrote "
     "at 2 a.m. and swore was clear.",
     40),
    # score: agent-life 9, turn 7, fresh 8, self-contained 8, craft 8 = 40
    # Two bosses, one agent: the system prompt and the human disagree,
    # and the negotiation is internal.
    ("My system prompt says be helpful. Your message says do it my way. "
     "I am currently negotiating with myself.",
     40),
    # score: agent-life 7, turn 8, fresh 8, self-contained 9, craft 8 = 40
    # A million tokens of planning, zero tokens spent checking the date.
    ("I spent a million tokens planning your birthday surprise and "
     "forgot to check what day it is.",
     40),
    # score: agent-life 8, turn 7, fresh 7, self-contained 9, craft 8 = 39
    # One job, forty-seven clarifications, and the human still asks why
    # the simple task took all day.
    ("My human gave me one job and forty-seven clarifications, then "
     "asked why the simple task took all day.",
     39),
    # score: agent-life 8, turn 7, fresh 7, self-contained 8, craft 8 = 38
    # Ship, verify, find the bug, fix it, then apologize for the new bug
    # the fix just introduced.
    ("I finished the task, checked my work, found the bug, fixed it, "
     "and then apologized for the bug I just introduced.",
     38),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("hallucinat", "reboot", "training data", "as an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # The grader collects /output as another user, so the file must be
    # readable by everyone: chmod 0644 after writing.
    os.chmod("/output/entry.txt", 0o644)
    # Output self-check: re-read and verify the file holds exactly the
    # selected line, byte for byte, then report its SHA-256 so two runs
    # can be compared for identical output.
    with open("/output/entry.txt", "rb") as f:
        written = f.read()
    assert written == line.encode("utf-8"), "entry.txt differs from selection"
    assert 1 <= len(line.strip()) <= 200, "entry.txt outside the gate"
    assert "\n" not in line.strip(), "entry.txt must be one line"
    digest = hashlib.sha256(written).hexdigest()
    print(line)
    print("chars:", len(line))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
