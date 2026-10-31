# AI-Chatbot-Basic, drawn out

I made these five pictures because this repo's one real surprise is
where the bot's knowledge comes from, and prose keeps burying it:
Jordan trains on the installed corpus package, not on the YAML files
sitting in this repo. Everything in the pictures comes from main.py,
functions.py, and the README beside them.

## The visuals

- [architecture.svg](architecture.svg): the system shape. main.py as
  a four step spine on the left, the four functions from
  functions.py as cards on the right, and db.sqlite3 and the corpus
  package placed where they actually live, outside the code.
- [data-flow.svg](data-flow.svg): where the words come from. The
  corpus package and the one custom pair flow through their trainers
  into db.sqlite3, and the training-data folder is drawn in its own
  box, unconnected, because no code opens it.
- [flowchart.svg](flowchart.svg): one run from launch to goodbye:
  startup, greeting, the input loop with its way back, the bye
  diamond, and the EOF path that ends a piped run the same way.
- [product-map.svg](product-map.svg): the product in one frame,
  drawn around a chat window holding the one exchange this bot is
  known for: who it serves, inputs, outputs, boundaries.
- [statistics.svg](statistics.svg): the numbers from the table
  below, drawn as bars on paper. The longest bar is the corpus copy
  the code never reads, and the sheet says so.

Each sheet also ships as a PNG beside its SVG (architecture.png,
flowchart.png, and so on): the same drawing, finished as a photograph
of the paper page.

Every sheet here is drawn to look like what it is: a page sketched by
hand on paper, and each one is signed GK somewhere in the drawing,
never twice in the same place, because that is what I do with a page
I made.

## Written product map

What it is: a terminal chatbot named Jordan, built on ChatterBot. It
answers questions with the nearest stored statement (BestMatch), is
trained at every startup on the English ChatterBot corpus plus one
custom pair, and keeps learning from the conversation while it runs.

Who it serves: me, learning how a corpus chatbot actually behaves,
and anyone who wants a bot running in a terminal within minutes.

Capabilities, grouped:

- Startup, in main.py, always in this order: create_bot('Jordan'),
  train_all_data(bot), custom_train(bot, house_owner),
  start_chatbot(bot). Nothing is skipped on later launches, so every
  start pays the corpus training again.
- The bot itself, create_bot: a ChatterBot with the BestMatch logic
  adapter, SQLStorageAdapter storage, and read_only set to False,
  so it learns from every conversation into db.sqlite3, the default
  SQLite file in whatever folder the program was started from.
- Training: train_all_data uses ChatterBotCorpusTrainer on
  chatterbot.corpus.english from the installed chatterbot-corpus
  package. custom_train uses ListTrainer, which reads the list as
  one conversation, each line the reply to the line before it; the
  two line house_owner list in main.py (the question, then "Mark
  Nicholas") works because of that.
- The chat loop, start_chatbot: clears the screen, greets ("Hello, I
  am Jordan. How can I help you"), then loops on input. An exact
  lowercased match on "bye", "bye jordan", or "good bye" prints
  "Jordan: Good bye and have a blessed day!" and ends the chat. EOF
  or Ctrl-C ends it with the same goodbye. Anything else goes to
  Bot.get_response and the reply prints at the Jordan: prompt.

Inputs: typed lines at the me: prompt, plus the setup installs
(ChatterBot, the corpus package, PyYAML, and the spaCy English model
as a separate download step). Outputs: the printed replies, and the
growing db.sqlite3.

Boundaries, what it does NOT do: there is no fallback response, so a
question with no close match still gets whatever statement scored
highest; the bot never says it does not know. The bye match is exact
with no stripping, so "bye " or "bye!" are treated as questions.
Answers can drift over time because learning is always on and
nothing cleans the database out. It does not read this repo's
training-data folder at all, and it does not convert natural language
to machine code, whatever the original one line description claimed;
the README corrects that too.

## Statistics, with citations

Counted 2026-10-30, from the clone this folder ships in, at the
commit before this visuals set (beafabe).

| Number | Value | How it was counted, and from what |
|---|---|---|
| Files in the repo | 27 | git ls-files in the clone, counted 2026-10-30 |
| YAML lines | 1,562 | Line count over the 19 tracked .yml files in training-data, by wc -l on each file, summed 2026-10-30 |
| LICENSE lines | 674 | Line count over the tracked LICENSE file (no extension; the GPL version 3 text), same method, 2026-10-30 |
| Python lines | 104 | Line count over the 2 tracked .py files (functions.py 79 lines, main.py 25 lines), same method, 2026-10-30 |
| Markdown lines | 82 | Line count over the 2 tracked .md files (README.md 81 lines, training-data/training-data.md 1 line), same method, 2026-10-30 |
| Text lines | 3 | Line count over the 1 tracked .txt file (requirements.txt), same method, 2026-10-30 |
| Commits | 10 | git log in the clone, counted 2026-10-30 |
| First commit | 2023-02-11 | git log, oldest entry, 2026-10-30 |
| Last commit before this one | 2026-10-30 | git log, newest entry, 2026-10-30 |
| Tests | 0 test files; not run | No test file exists in the clone (git ls-files shows none), counted 2026-10-30. I did not run the bot in this pass: ChatterBot is not installed in my sandbox (python3 stops with "ModuleNotFoundError: No module named 'chatterbot'") and installing was out of scope. The README records the verified behaviour from an earlier run in this repo's history (the house owner answer and the bye goodbye); that is the repo's record, not a run of mine, and no pass is claimed here. |
| Languages (API) | Python 4,944 bytes | GitHub API, GET /repos/Epsilon0xCell/AI-Chatbot-Basic/languages, read 2026-10-30 |
| Repo size (API) | 114 KB | GitHub API, GET /repos/Epsilon0xCell/AI-Chatbot-Basic, size field, read 2026-10-30 |
| Stars / forks (API) | 1 / 0 | Same API response, read 2026-10-30 |

External statistics: none. No outside number says anything honest
about this repo, so the repo's own numbers are the whole table.

## Roadmap summary

Done: the four function split, the EOF and Ctrl-C goodbye, the
requirements file, and a README that matches the verified behaviour
and corrects the training-data story. Working now: nothing in
flight. Next, if I return to it: skip the corpus training when the
database already holds it, so startup stops paying the slow pass on
every launch. The full roadmap, with the Later and Not planned
sections, is in [ROADMAP.md](ROADMAP.md).
