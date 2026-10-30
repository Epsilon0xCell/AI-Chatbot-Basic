from functions import *

# This file is the whole startup sequence, and the order is the point:
# I create the bot first, train the corpus second, train my custom pair
# third, and only then start the loop. Nothing here runs in parallel
# and nothing is skipped on later launches, so every start pays the
# full corpus training again even when the database already has it.
bot = create_bot('Jordan')

train_all_data(bot)

# My one custom pair. Jordan answers this question with this name
# because I trained it here, not because the name is looked up anywhere
# or appears in the corpus. The pair lives in code, so changing the
# answer means editing this list, and the old answer stays in an
# existing db.sqlite3 until I delete that file and retrain from empty.
house_owner = [
    "Who is the owner of the house?",
    "Mark Nicholas"
]
custom_train(bot, house_owner)

# This call blocks until the chat ends, so anything I put after it in
# this file would only run once the conversation is already over.
start_chatbot(bot)
