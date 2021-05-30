"""Module for test Telegram bot, based on the bot's conversation with itself"""
import os
from nql_bot.bot import Bot
from telebot import types
from pathlib import Path
import time

bot = None
CHAT_ID = None
TOKEN = None


def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    global bot
    global TOKEN
    global CHAT_ID
    _download.download_model()
    bot = Bot(token=TOKEN, model=AgeGenderModel())
    TOKEN = os.environ['TELEGRAM_API_TOKEN']
    CHAT_ID = os.environ['CHAT_ID']
    bot.bot.send_message(CHAT_ID, f"TESTS ARE STARTED AT {time.ctime()}")
    bot.bot.send_message(CHAT_ID, "TESTS SETUP: SUCCESS")


def test_model():
    for i in range(1, 4):
        img = cv2.imread(str(Path(__file__).parents[0].joinpath('content/img1.jpg'.replace('1', str(i)))))
        predictions = bot.model.predict(img)
        assert all(i is not None for i in predictions)
        assert all(len(i) == 1 for i in predictions)

    bot.bot.send_message(CHAT_ID, "TEST MODEL: SUCCESS")


def create_message_update(text, msg=None):
    params = {'text': text}
    chat = types.User(CHAT_ID, False, 'test')
    if msg is None:
        message = types.Message(1, None, None, chat, 'text', params, "")
    else:
        message = msg
    edited_message = None
    channel_post = None
    edited_channel_post = None
    inline_query = None
    chosen_inline_result = None
    callback_query = None
    shipping_query = None
    pre_checkout_query = None
    poll = None
    poll_answer = None
    return types.Update(-1001234038283, message, edited_message, channel_post, edited_channel_post, inline_query,
                        chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer)


def test_start_correct():
    bot = Bot(token=TOKEN, model=AgeGenderModel())
    bot._setup_bot()
    update1 = create_message_update('/start')
    bot.bot.process_new_updates([update1])

    time.sleep(3)

    msg = bot.bot.send_message(CHAT_ID, "Slava")
    update2 = create_message_update('Slava', msg=msg)
    bot.bot.process_new_updates([update2])

    time.sleep(3)

    msg = bot.bot.send_message(CHAT_ID, "19")
    update3 = create_message_update('19', msg=msg)
    bot.bot.process_new_updates([update3])

    time.sleep(3)

    msg = bot.bot.send_message(CHAT_ID, "Male")
    update4 = create_message_update('Male', msg=msg)
    bot.bot.process_new_updates([update4])

    time.sleep(3)
    user = bot._db.get_users()[0]
    age = int(user[1])
    name = user[2]
    gender = user[3]

    assert age == 19
    assert name == "Slava"
    assert gender.lower() == 'male'

    msg = bot.bot.send_message(CHAT_ID, "TEST START CORRECT: SUCCESS")


def test_start_incorrect():
    """Test incorrect age and gender + test update in database"""
    bot = Bot(token=TOKEN, model=AgeGenderModel())
    bot._setup_bot()
    update1 = create_message_update('/start')
    bot.bot.process_new_updates([update1])

    time.sleep(3)

    msg = bot.bot.send_message(CHAT_ID, "Slava")
    update2 = create_message_update('Slava', msg=msg)
    bot.bot.process_new_updates([update2])

    time.sleep(3)

    msg = bot.bot.send_message(CHAT_ID, "gdsffsdf")
    update3 = create_message_update('gdsffsdf', msg=msg)
    bot.bot.process_new_updates([update3])

    time.sleep(3)

    msg = bot.bot.send_message(CHAT_ID, "17")
    update3 = create_message_update('17', msg=msg)
    bot.bot.process_new_updates([update3])

    time.sleep(3)

    msg = bot.bot.send_message(CHAT_ID, "Massle")
    update4 = create_message_update('Massle', msg=msg)
    bot.bot.process_new_updates([update4])

    time.sleep(3)

    msg = bot.bot.send_message(CHAT_ID, "Male")
    update4 = create_message_update('Male', msg=msg)
    bot.bot.process_new_updates([update4])

    time.sleep(3)
    user = bot._db.get_users()[0]
    age = int(user[1])
    name = user[2]
    gender = user[3]

    assert age == 17
    assert name == "Slava"
    assert gender.lower() == 'male'

    msg = bot.bot.send_message(CHAT_ID, "TEST START INCORRECT: SUCCESS")


def test_photo_process():
    bot = Bot(token=TOKEN, model=AgeGenderModel())
    with open(str(Path(__file__).parents[0].joinpath('content/img1.jpg')), "rb") as photo:
        msg = bot.bot.send_photo(CHAT_ID, photo)
    time.sleep(5)
    msg.chat.id = CHAT_ID
    bot.photo_messages(msg)
    time.sleep(15)

    assert bot.photo_path.joinpath(f'photo_{CHAT_ID}.jpg').is_file()


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    TOKEN = os.environ['TELEGRAM_API_TOKEN']
    CHAT_ID = os.environ['CHAT_ID']
    bot = Bot(token=TOKEN)
    bot.bot.send_message(CHAT_ID, f"TESTS ARE FINISHED AT {time.ctime()}")


if __name__ == '__main__':
    pass
