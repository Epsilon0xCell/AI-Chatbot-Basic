# I keep the ChatterBot imports inside each function instead of at the
# top of this file. That way importing this module on its own does not
# fail when ChatterBot is missing; the error only shows up when a
# function here is actually called.

# I create the bot with read_only set to False, so Jordan learns from
# every conversation and writes what it learns into the database below.
# That choice has a cost I accept here: answers can drift over time as
# user input piles up, and nothing in this file ever cleans that out.
# I pass no database_uri, so ChatterBot uses its default SQLite file,
# db.sqlite3, in whatever folder I started the program from. Launching
# from a different folder means a different, emptier bot.
# BestMatch is the only logic adapter I use. Every reply is a nearest
# match against stored statements, and I set no fallback response, so a
# question with no close match still gets whatever statement scored
# highest instead of an admission that the bot does not know.
def create_bot(name):
    from chatterbot import ChatBot
    Bot = ChatBot(name = name,
                  read_only = False,
                  logic_adapters = ["chatterbot.logic.BestMatch"],
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter")
    return Bot

# I train on the installed chatterbot-corpus package here, named by its
# package path. The YAML files in this repo's training-data folder are
# not what this reads; I checked in Wave 2 that no code in the repo
# opens that folder at all, so editing those files changes nothing the
# bot learns.
# main.py calls this on every launch, before any custom training. The
# corpus pass is the slow part of startup, and I pay it every run
# because there is no check here for whether the database already
# holds the corpus.
def train_all_data(Bot):
    from chatterbot.trainers import ChatterBotCorpusTrainer
    corpus_trainer = ChatterBotCorpusTrainer(Bot)
    corpus_trainer.train("chatterbot.corpus.english")

# ListTrainer reads my list as one conversation, not as separate
# question and answer pairs: each line is trained as the reply to the
# line before it. The two line list in main.py works because of that.
# A third line would become the reply to the second line, not a second
# pair, which is the mistake I would most likely make extending this.
def custom_train(Bot, conversation):
    from chatterbot.trainers import ListTrainer
    trainer = ListTrainer(Bot)
    trainer.train(conversation)

# I clear the screen before the greeting with an escape code. When
# stdout is a pipe instead of a terminal that code goes into the output
# as raw bytes, which is ugly but harmless for the scripted runs I test
# with.
# The bye check is an exact match on the lowercased input, with no
# stripping. "bye" and "good bye" end the chat, but "bye " with a
# trailing space or "bye!" do not; those go to the bot as questions.
# I check the bye list before calling get_response, so the bye words
# themselves are never stored as something the bot should learn from.
def start_chatbot(Bot):
    print('\033c')
    print("Hello, I am Jordan. How can I help you")
    bye_list = ["bye jordan", "bye", "good bye"]

    while (True):
        try:
            user_input = input("me: ")
        except (EOFError, KeyboardInterrupt):
            # I added this handler in Wave 2 after a piped run died
            # with an EOFError traceback when stdin closed. Closed
            # input and Ctrl-C now print the same goodbye as the bye
            # words and leave through the same break, so a scripted
            # run and a typed run end identically.
            print("Jordan: Good bye and have a blessed day!")
            break
        if user_input.lower() in bye_list:
            print("Jordan: Good bye and have a blessed day!")
            break

        response = Bot.get_response(user_input)
        print("Jordan:", response)
