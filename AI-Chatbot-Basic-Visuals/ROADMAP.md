# AI-Chatbot-Basic roadmap

Written 2026-10-30 from the repo as it stands. No dates on the future
items, because I do not know when I will be back in this code, and a
date I invent here would be a small lie in a public file.

## Done

- The bot: Jordan, a ChatterBot with BestMatch and SQL storage,
  trained at startup on the English corpus and on one custom pair,
  learning from conversations because read_only is off.
- The split into functions.py (create_bot, train_all_data,
  custom_train, start_chatbot) with main.py as the four step startup
  sequence, and the ChatterBot imports kept inside the functions so
  importing the module alone never fails.
- The repair pass: the chat loop no longer dies with an EOFError
  traceback when piped input runs out; EOF and Ctrl-C print the same
  goodbye as the bye words. requirements.txt added. The README
  rewritten to match the verified behaviour, including the spaCy
  model download step and what each missing piece does.
- An honest training-data note: the folder in this repo is a
  reference copy, no code reads it, and the README and the code
  comments both say so now.
- These visuals.

## Working now

- Nothing in flight. The repo is in a finished, working state as of
  the 2026-10-30 campaigns.

## Next

- Skip corpus training when the database already holds it. The
  comments in main.py and functions.py both name the cost: every
  launch pays the full corpus pass because nothing checks whether
  db.sqlite3 already has the corpus. A check there is the one
  change that would make daily use of this bot noticeably better.
- Nothing else is queued. The code has no TODO or FIXME markers in
  it (checked 2026-10-30), so this section stays short on purpose.

## Later

- A fallback response for questions with no close match. BestMatch
  currently returns the highest scoring statement whatever it is,
  so Jordan never admits it does not know. Worth doing if I ever
  use the bot with other people, not before.
- Stripping input before the bye check, so "bye " ends the chat the
  way a person typing it expects. Small, and only worth it beside
  other loop work.

## Not planned

- Training on the local training-data folder. The installed corpus
  package is the source the code uses; wiring the local copies in
  would fork the corpus into a second, drifting source for no gain.
- A graphical or web interface. The terminal loop is the whole
  product here; Jordan in a window is a different project.
