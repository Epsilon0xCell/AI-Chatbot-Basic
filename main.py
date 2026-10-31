import sys

from functions import create_bot, custom_train, start_chatbot, train_all_data

USAGE = "Usage: python main.py [--help]"


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    # I answer --help before building anything. An earlier version of
    # this file built the bot at import time, so even a help request
    # died with a ModuleNotFoundError traceback on a machine with no
    # ChatterBot installed.
    if args in (["--help"], ["-h"]):
        print(USAGE)
        print("Build Jordan, train the English corpus and one custom")
        print("answer, then chat until a bye word, EOF, or Ctrl-C.")
        return 0
    if args:
        print(USAGE, file=sys.stderr)
        return 2

    # The startup sequence, and the order is the point: I create the
    # bot first, train the corpus second, train my custom pair third,
    # and only then start the loop. Nothing here runs in parallel and
    # nothing is skipped on later launches, so every start pays the
    # full corpus training again even when the database already has it.
    try:
        bot = create_bot('Jordan')
    except ModuleNotFoundError:
        print("Jordan: ChatterBot is not installed. Install it with: "
              "pip install -r requirements.txt", file=sys.stderr)
        return 1

    train_all_data(bot)

    # My one custom pair. Jordan answers this question with this name
    # because I trained it here, not because the name is looked up
    # anywhere or appears in the corpus. The pair lives in code, so
    # changing the answer means editing this list, and the old answer
    # stays in an existing db.sqlite3 until I delete that file and
    # retrain from empty.
    house_owner = [
        "Who is the owner of the house?",
        "Mark Nicholas"
    ]
    custom_train(bot, house_owner)

    # This call blocks until the chat ends, so anything I put after it
    # in this function would only run once the conversation is over.
    start_chatbot(bot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
