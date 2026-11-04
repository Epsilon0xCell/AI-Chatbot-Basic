# AI-Chatbot-Basic

**Printed, and Growing**

A basic chatbot named Jordan, built on ChatterBot.

![Python](https://img.shields.io/badge/python-3-blue.svg)
![ChatterBot](https://img.shields.io/badge/ChatterBot-1.2.11-blue.svg)
![Tests](https://img.shields.io/badge/tests-10%20passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)

![AI-Chatbot-Basic banner](banner.png)

[What the code does](#what-the-code-does) · [Setup](#setup) · [The training-data folder](#the-training-data-folder) · [Notes](#notes) · [Tests](#tests) · [License](#license) · [Diagrams and maps](#diagrams-and-maps)

A basic chatbot named Jordan, built on ChatterBot. It answers basic questions from the English ChatterBot corpus it is trained on at startup, plus one custom trained answer, and it learns from the conversation while it runs (its storage is a local SQLite database and `read_only` is off).

Example session:

```text
$ python main.py
Hello, I am Jordan. How can I help you
me: Who is the owner of the house?
Jordan: Mark Nicholas
me: bye
Jordan: Good bye and have a blessed day!
```

<p align="center"><img src="sep-heavy.svg" alt=""></p>

## What the code does

- `functions.py`
  - `create_bot(name)`: builds a ChatterBot with the BestMatch logic adapter and SQL storage.
  - `train_all_data(bot)`: trains the bot on `chatterbot.corpus.english` from the installed chatterbot-corpus package. This runs on every launch and takes a few seconds.
  - `custom_train(bot, conversation)`: trains one question and answer pair with the ListTrainer.
  - `start_chatbot(bot)`: the chat loop. It greets you as Jordan and answers until you type one of the bye words below.
- `main.py`: creates the bot, trains the corpus, trains the custom pair ("Who is the owner of the house?" / "Mark Nicholas"), and starts the chat loop.

![AI-Chatbot-Basic architecture](AI-Chatbot-Basic-Visuals/architecture.svg)

<p align="center"><sub>Architecture diagram from AI-Chatbot-Basic-Visuals.</sub></p>

Exit the chat by typing `bye`, `bye jordan`, `good bye`, or `goodbye`. Case and spaces around the word do not matter. An empty line is asked again instead of being sent to the bot as a question. If the input simply ends (piped input runs out, stdin is closed, or you press Ctrl-C), the bot prints the same goodbye message and exits cleanly.

| Input | Behaviour |
| --- | --- |
| `python main.py --help` | prints a short usage line and exits 0, and it works before ChatterBot is installed |
| An unknown argument | prints the usage line to stderr and exits 2 |
| Running the chat without ChatterBot installed | prints `ChatterBot is not installed` with the install command to stderr and exits 1, with no traceback |
| A bye word (`bye`, `bye jordan`, `good bye`, `goodbye`) | ends the session |
| An empty line | is asked again instead of being sent to the bot as a question |
| EOF or Ctrl-C | prints the same goodbye message and exits cleanly |

Verified behaviour: asked "Who is the owner of the house?", the bot answers "Mark Nicholas"; `bye` ends the session with "Jordan: Good bye and have a blessed day!".

## Setup

Python 3, then:

The setup runs in three steps:

1. Install the Python requirements.
2. Download the spaCy English model.
3. Start the bot with `python main.py`.

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python main.py
```

Each piece is required, and each missing piece fails in its own way (all reproduced):

| Missing component | Symptom | Fix |
| --- | --- | --- |
| ChatterBot | `main.py` catches the failure and prints the install hint described above, exit 1 | `pip install -r requirements.txt` |
| The spaCy English model | ChatterBot reports that the spaCy model for the English language is missing. The model is a download step, not a pip requirement, which is why it is a separate command above | `python -m spacy download en_core_web_sm` |
| PyYAML | corpus training fails asking for it | `pip install -r requirements.txt` |
| The chatterbot-corpus package | there is no `chatterbot.corpus.english` data to train on | `pip install -r requirements.txt` |

<p align="center"><img src="sep-heavy.svg" alt=""></p>

## The training-data folder

> [!NOTE]
> **FROM THE CLERK'S DESK**: No code in this repo reads that folder. The bot trains on the installed package's corpus, so editing the local copies does not change what the bot learns.

`training-data/` holds YAML corpus files, and `training-data.md` in that folder says "All of our training data is in this folder." That is not how the code works: no code in this repo reads that folder (checked by searching every Python and Markdown file), and its `greetings.yml` is identical to the English `greetings.yml` inside the installed chatterbot-corpus package. The bot trains on the installed package's corpus, so editing the local copies does not change what the bot learns. The folder is kept as a local reference copy of the corpus format.

## Notes

- The bot creates its SQLite database (`db.sqlite3`) in the folder you run it from, and because it keeps learning, answers can drift over time. Delete the database to start over.
- The original one line description claimed the bot "converts natural language to machine code". It does not: nothing in the code converts anything to machine code. It is a question answering chatbot, as described above.

## Tests

```bash
python3 -m unittest
```

10 tests in `test_chatbot.py`: the bye word rule (plain, padded, capitalised, and near misses like `bye!`), the chat loop driven by a stand-in bot (a question is answered, an empty line is re-asked, a bye with a trailing space ends the chat, EOF ends it with the same goodbye), and the entry point run as a subprocess (`--help` exits 0, an unknown argument exits 2, and a missing ChatterBot exits 1 with the hint and no traceback). The live chat itself is not covered: it needs ChatterBot installed, and the tests run on machines without it by design.

<p align="center"><img src="sep-heavy.svg" alt=""></p>

## License

See LICENSE.

## Diagrams and maps

I drew the system out in [AI-Chatbot-Basic-Visuals](AI-Chatbot-Basic-Visuals/): an architecture diagram, a data-flow diagram of where the bot's training actually comes from, a flowchart of a run, and a product map, with the written product map, statistics with citations, and the roadmap in [VISUAL.md](AI-Chatbot-Basic-Visuals/VISUAL.md). Every sheet also ships as a PNG photograph of the paper page beside its SVG. The architecture diagram itself is shown in What the code does above.

## Visual Identity

<p align="center"><img src="intro-banner.png" alt="AI-Chatbot-Basic introduction, wordless" width="800"></p>

<p align="center"><img src="logo.png" alt="AI-Chatbot-Basic logo" width="180"></p>

![AI-Chatbot-Basic animated scene](assets-scene.svg)

_A friendly clerk in teal and rust, printed on cream paper, learning from every conversation._
