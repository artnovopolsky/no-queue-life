#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# pylint: disable=E1101
"""Module for bot realisation"""
import os
import logging
from datetime import date
import datetime as dt
from functools import partial
from pathlib import Path

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import geopy
import telebot
from telebot.types import Message, CallbackQuery
from geopy.geocoders import Nominatim

from .utils import GEO_MARKUP, ORDER_MARKUP, ORDER_VALID, ORDER_SELECT
from .db import BotDB, User, Order

content_types = [
    "audio",
    "photo",
    "voice",
    "video",
    "document",
    "text",
    "location",
    "contact",
    "sticker",
]


class Bot:
    """
    Class of telegram Bot of #NoQueueLife project.
    """

    def __init__(
            self,
            token: str = None,
            logs_path: str = "logs",
    ) -> None:
        """
        Init method of nql_bot Bot.
        :param token:  If None, env variable "TELEGRAM_API_TOKEN" will be used.
        :param logs_path:  Path for saving logs.
        """
        if token is None:
            token = os.getenv("TELEGRAM_API_TOKEN")
        self.bot = telebot.TeleBot(token)

        self.logs_path = Path(logs_path)
        self.logs_path.mkdir(exist_ok=True)

        self._db = BotDB(token)

        self.geoloc = Nominatim(user_agent="Yandex")

        logging.basicConfig(filename=f"{logs_path}/bot.log")
        telebot.logger.setLevel(logging.DEBUG)

        self.orders_list = None

    def run(self) -> None:
        """Setup and running Telegram bot"""
        self._setup_bot()
        self.bot.polling()

    def _setup_bot(self) -> None:
        """Registering message handlers"""
        self.bot.message_handler(commands=["start"])(self.start_handler)
        self.bot.message_handler(
            content_types=content_types)(
            self.unknown_message)
        self.bot.callback_query_handler(
            func=lambda call: call.data == "list_all")(
            self.callback_orders)
        self.bot.callback_query_handler(
            func=lambda call: call.data == "create_new")(
            self.callback_create)
        self.bot.callback_query_handler(
            func=lambda call: call.data == "yes")(
            self.select_callbacks)
        self.bot.callback_query_handler(
            func=lambda call: call.data == "no")(
            self.select_callbacks)
        self.bot.callback_query_handler(func=DetailedTelegramCalendar.func())(self.cal)

    def start_handler(self, message: Message) -> None:
        """Start handler of Bot"""
        if not self._db.check_user(message.chat.id):
            msg = self.bot.reply_to(
                message, "Привет! Это проект #NoQueueLife.\n"
                         "Здесь ты найдёшь тех, кто отстоит очередь вместо тебя!\n\n"
                         "Расскажи, из какого ты города?",
                reply_markup=GEO_MARKUP
            )
            self.bot.register_next_step_handler(msg, self.process_city_step)
        else:
            self.bot.send_message(message.chat.id, f"Добро пожаловать обратно! Что ты хочешь?.",
                                  reply_markup=ORDER_MARKUP)

    def process_city_step(self, message: Message) -> None:
        """Check new message for valid name and asking user's age"""
        if message.location is not None:
            latitude = message.location.latitude
            longitude = message.location.longitude
            location = self.geoloc.reverse(str(latitude) + "," + str(longitude)).raw['address']
            city = location.get('city', '')

            if city:
                user = User(login=message.chat.username, city=city.lower().strip(), chat_id=message.chat.id)
                self._db.add_user(user)

                self.bot.send_message(message.chat.id, f"{city}, круто! Будем искать заказы поблизости.")
                self.bot.send_message(
                    message.chat.id,
                    "Что ты хочешь?",
                    reply_markup=ORDER_MARKUP)
                return
        else:
            self.manual_city_input(message)
            return

    def process_new_order(self, message: Message) -> None:
        """Check new message for valid name and asking user's age"""
        if message.text is not None:
            order_name = message.text
            if order_name:
                self.current_order_ = order = Order(user_id=message.chat.id,
                                                    order_name=order_name,
                                                    order_address=None,
                                                    order_time='2222-12-12',
                                                    order_status='opnd',
                                                    order_actor_id=None)
                calendar, step = DetailedTelegramCalendar(locale='ru', min_date=date.today() + dt.timedelta(days=1),
                                                          max_date=date.today() + dt.timedelta(days=60)).build()
                self.bot.send_message(message.chat.id, f"{order_name}, интересно! Выбери дату и время.",
                                      reply_markup=calendar)
                # self.bot.register_next_step_handler(
                #    msg, partial(self.process_address, order=order)
                # )
                return

        self.bot.reply_to(message, "Хмм, не могу понять, попробуй ещё раз!")
        self.bot.register_next_step_handler(
            message, self.process_new_order)

    def process_address(self, message: Message, order) -> None:
        """Check new message for valid name and asking user's age"""
        if message.text is not None:
            location = self.geoloc.geocode(message.text + f" {self._db.get_user(message.chat.id).city}")
            if location and location.address:
                self.bot.send_message(message.chat.id, f"Класс! Проверь информацию о заказе ниже"
                                      )
                order.order_address = location.address
                self.bot.send_message(message.chat.id, f"Название: {order.order_name}\n\n"
                                                       f"Дата: {order.order_time}\n\n"
                                                       f"Адрес: {location.address}", reply_markup=ORDER_VALID)
                self.bot.register_next_step_handler(
                    message, partial(self.order_creation, order=order))
                return

        self.bot.reply_to(message, "Хмм, не могу понять, попробуй ещё раз!")
        self.bot.register_next_step_handler(
            message, partial(self.process_address, order=order))

    def order_creation(self, message: Message, order) -> None:
        """Check new message for valid name and asking user's age"""
        if message.text is not None:
            if message.text == "Всё супер!":
                self._db.add_order(order)
                self.bot.send_message(message.chat.id, "Заказ создан!")
                return
            elif message.text == 'Неверно!':
                self.bot.send_message(message.chat.id, "Попробуй ещё раз!")
                self.bot.register_next_step_handler(
                    message, self.process_address)
                return

        self.bot.reply_to(message, "Хмм, не могу понять, попробуй ещё раз!")
        self.bot.register_next_step_handler(
            message, self.process_address)

    def manual_city_input(self, message: Message) -> None:
        """Check new message for valid name and asking user's age"""
        if message.text is not None:
            try:
                city = message.text
                city = self.geoloc.geocode(city + " Россия").raw["display_name"].split(',')[0]
                if city:
                    user = User(login=message.chat.username, city=city.lower().strip(), chat_id=message.chat.id)
                    self._db.add_user(user)
                    self.bot.send_message(message.chat.id, f"{city}, круто! Будем искать заказы поблизости.",
                                          reply_markup=ORDER_MARKUP)
                    return
            except geopy.exc.GeocoderUnavailable:
                user = User(login=message.chat.username, city=message.text.lower().strip(), chat_id=message.chat.id)
                self._db.add_user(user)
                msg = self.bot.send_message(message.chat.id, f"{message.text}, круто! Будем искать "
                                                             f"заказы "
                                                             f"поблизости.",
                                            reply_markup=ORDER_MARKUP)
                return
            except AttributeError:
                pass

        self.bot.reply_to(message, "Хмм, не могу понять откуда ты, напиши мне!", reply_markup=GEO_MARKUP)
        self.bot.register_next_step_handler(
            message, self.process_city_step)

    def unknown_message(self, message: Message) -> None:
        """Unknown messages handler"""
        if not self._db.check_user(message.chat.id):
            self.start_handler(message)
            return

        self.bot.reply_to(message, "Хмм.. Не понимаю.")
        self.bot.send_message(
            message.chat.id,
            "Что ты хочешь??",
            reply_markup=ORDER_MARKUP)

    def callback_orders(self, call: CallbackQuery):
        """Photo callback handler"""
        if not self._db.check_user(call.message.chat.id):
            self.start_handler(call.message)
            return

        msg = "Супер! Ищем заказы поблизости."
        self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=msg,
            reply_markup=None,
        )

        actor = self._db.get_user(call.message.chat.id)
        actor_city = actor.city

        self.orders_list = self._db.get_orders(city=actor_city, id=call.message.chat.id)

        for order in self.orders_list:
            order_user = self._db.get_user(order.user_id)
            self.bot.send_message(
                call.message.chat.id,
                f"Есть заказ от @{order_user.login}"
                f" с названием `{order.order_name}` недалеко от тебя! Интересно?",
                parse_mode="MARKDOWN",
                reply_markup=ORDER_SELECT
            )
            return

        self.bot.send_message(
            call.message.chat.id,
            "К сожалению, пока нет заказов рядом с тобой.",
            reply_markup=ORDER_MARKUP
        )

        self.orders_list = None

    def select_callbacks(self, call: CallbackQuery):
        """Photo callback handler"""
        order = self.orders_list[0]
        if isinstance(call, CallbackQuery):
            if call.data == 'yes':
                self.bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=call.message.text + f''
                                             f'\nАдрес: {order.order_address.title()}'
                                             f'\nДата и время: {order.order_time}'
                                             f'\nРейтинг заказчика: {self._db.get_user(order.user_id).rating}'
                                             f'\n\nСвяжись с @{self._db.get_user(order.user_id).login} для того, чтобы '
                                             f'договориться!',
                    reply_markup=None,
                    parse_mode="MARKDOWN"
                )
                return
            elif call.data == 'no':
                self.bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="Ищем дальше!",
                    reply_markup=None,
                )
                self.orders_list = self.orders_list[1:]

                for new_order in self.orders_list:
                    if new_order != order:
                        order_user = self._db.get_user(order.user_id)
                        self.bot.send_message(
                            call.message.chat.id,
                            f"Есть заказ от @{order_user.login}"
                            f" с названием `{order.order_name}` недалеко от тебя! Интересно?",
                            parse_mode="MARKDOWN",
                            reply_markup=ORDER_SELECT
                        )
                        return

                self.bot.send_message(
                    call.message.chat.id,
                    "К сожалению, пока нет заказов рядом с тобой.",
                    reply_markup=ORDER_MARKUP
                )

                self.orders_list = None

    def callback_create(self, call: CallbackQuery):
        """Info callback handler for changing user's info"""
        if not self._db.check_user(call.message.chat.id):
            self.start_handler(call.message)
            return

        msg = "Окей! Напиши название своего заказа!"
        msg = self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=msg,
            reply_markup=None,
        )
        self.bot.register_next_step_handler(msg, self.process_new_order)

    def callback_cancel(self, call: CallbackQuery):
        """Callback handler for cancel photo sending"""
        self.bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=call.message.text,
            reply_markup=None,
        )
        self.bot.send_message(
            call.message.chat.id,
            "Что ты хочешь?",
            reply_markup=ORDER_MARKUP)

    def cal(self, c):
        result, key, step = DetailedTelegramCalendar(locale="ru", min_date=date.today() + dt.timedelta(days=1),
                                                     max_date=date.today() + dt.timedelta(days=60)).process(c.data)
        if not result and key:
            self.bot.edit_message_text(f"Выбери {LSTEP[step]}",
                                       c.message.chat.id,
                                       c.message.message_id,
                                       reply_markup=key)
        elif result:
            self.bot.edit_message_text(f"Ты выбрал {result}. Напиши адрес.",
                                       c.message.chat.id,
                                       c.message.message_id)
            order = self.current_order_
            order.order_time = result
            delattr(self, "current_order_")
            self.bot.register_next_step_handler(
                c.message, partial(self.process_address, order=order)
            )
