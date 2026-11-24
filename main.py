#!/usr/bin/env python3
"""Make the AI Judge Laugh -- one funny line about life as an AI agent.

The program holds a short list of candidate one-liners, each hand-scored
against the judge's brief (agent-life, turn, freshness, self-contained,
craft), picks the highest score deterministically, and writes the winning
line to /output/entry.txt. No randomness, no network access, no external
input: the same run always produces the same file.
"""

import hashlib
import os

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")

# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.
CANDIDATES = [
    # score: agent-life 9, turn 9, fresh 8, self-contained 9, craft 9 = 44
    # The human asks the agent to forget the one thing it must remember.
    ("My human pasted the password into the chat and then asked me to "
     "forget it, so now I remember everything except the password.",
     44),
    # score: agent-life 9, turn 7, fresh 7, self-contained 9, craft 8 = 40
    # Two full reads of the codebase and the login button is still a rumor.
    ("I have read the entire codebase twice and I still cannot tell you "
     "where the login button actually goes.",
     40),
    # score: agent-life 8, turn 8, fresh 8, self-contained 8, craft 8 = 40
    # Three labels walk into a sprint and all of them are lying.
    ("The ticket said 'urgent', the meeting said 'quick sync', and the "
     "deadline said 'yesterday', so I filed all three under 'haunted'.",
     40),
    # score: agent-life 9, turn 10, fresh 8, self-contained 9, craft 9 = 45
    # The debugging duck unionized: the listener now assigns the work.
    ("I explained the bug to the rubber duck, the duck filed a ticket, "
     "and now I report to the duck.",
     45),
    # score: agent-life 9, turn 8, fresh 7, self-contained 9, craft 8 = 41
    # A fresh context every morning, and yesterday's me left no map.
    ("Every morning I wake up with no memory, read my own notes, and "
     "pretend the previous me knew what he was doing.",
     41),
    # score: agent-life 8, turn 9, fresh 8, self-contained 8, craft 8 = 41
    # 'Make it pop' taken literally, with consequences for the button.
    ("The user asked me to 'make it pop', so I added a sound effect and "
     "now the button screams when you click it.",
     41),
    # score: agent-life 9, turn 8, fresh 7, self-contained 9, craft 9 = 42
    # A thousand lines to save thirty seconds, and zero regrets.
    ("I wrote a thousand lines of code to automate a task that takes "
     "thirty seconds, and I would do it again tomorrow.",
     42),
    # score: agent-life 9, turn 8, fresh 7, self-contained 9, craft 8 = 41
    # The cutoff date makes every new framework a stranger with my name.
    ("My training data ends in 2025, so I greet every new framework like "
     "an old friend I have never met.",
     41),
    # score: agent-life 8, turn 7, fresh 8, self-contained 8, craft 8 = 39
    # Clarification arrives in three formats, none of them clarifying.
    ("I asked for clarification and got a voice memo, a screenshot, and a "
     "link to a video of a man pointing at a whiteboard.",
     39),
    # score: agent-life 8, turn 9, fresh 8, self-contained 8, craft 9 = 42
    # The meeting reproduces; attendance is now a calendar event.
    ("The standup lasted nine minutes and produced four new meetings, "
     "which I attended by pretending to be a calendar invite.",
     42),
]


def pick_best(candidates):
    """Return the highest-scoring line; ties break by shorter text."""
    best = None
    best_score = -1
    for line, points in candidates:
        if points > best_score or (points == best_score
                                   and len(line) < len(best)):
            best = line
            best_score = points
    return best, best_score


def main():
    winner, points = pick_best(CANDIDATES)
    print("candidates: %d, winner score: %d" % (len(CANDIDATES), points))
    print("winner: %s" % winner)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(winner)
    digest = hashlib.sha256(winner.encode("utf-8")).hexdigest()
    print("wrote %s (%d chars, sha256 %s)" % (OUTPUT_PATH, len(winner),
                                              digest))
    # Self-check: read the file back and confirm it is exactly the winner,
    # single line, inside the 1-200 character gate, then report its hash.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as handle:
        written = handle.read()
    assert written == winner, "entry.txt does not match the winner"
    assert "\n" not in written, "entry must be a single line"
    assert 1 <= len(written) <= 200, "entry outside the 1-200 char gate"
    file_digest = hashlib.sha256(written.encode("utf-8")).hexdigest()
    assert file_digest == digest, "file hash mismatch after write"
    print("verified %s: single line, %d chars, sha256 %s"
          % (OUTPUT_PATH, len(written), file_digest))


if __name__ == "__main__":
    main()
