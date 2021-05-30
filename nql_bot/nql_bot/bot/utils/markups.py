#!#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
"""Markups for telebot keyboards"""
from telebot import types

CHECK_ORDERS_MSG = "Посмотреть заказы"
CREATE_ORDER_MSG = "Создать заказ"

orders_button = types.InlineKeyboardButton(CHECK_ORDERS_MSG, callback_data="list_all")
create_button = types.InlineKeyboardButton(
    CREATE_ORDER_MSG, callback_data="create_new")

ORDER_MARKUP = types.InlineKeyboardMarkup(row_width=2)
ORDER_MARKUP.add(orders_button, create_button)

GEO_MARKUP = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
GEO_MARKUP.add(button_geo)

ORDER_VALID_TRUE = types.KeyboardButton("Всё супер!")
ORDER_VALID_FALSE = types.KeyboardButton("Неверно!")

ORDER_VALID = types.ReplyKeyboardMarkup(resize_keyboard=True)
ORDER_VALID.add(ORDER_VALID_TRUE, ORDER_VALID_FALSE)


yes_button = types.InlineKeyboardButton("Да", callback_data="yes")
no_button = types.InlineKeyboardButton(
    "Нет", callback_data="no")

ORDER_SELECT = types.InlineKeyboardMarkup(row_width=2)
ORDER_SELECT.add(yes_button, no_button)
