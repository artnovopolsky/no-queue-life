#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
"""Database interface for Telegram bot"""
import sqlite3
import hashlib
import typing as tp
from dataclasses import dataclass
from pathlib import Path

from datetime import datetime

path = Path(__file__).parents[0]


@dataclass
class User:
    """Dataclass that contains User info"""

    chat_id: tp.Optional[int]
    login: tp.Optional[str]
    city: tp.Optional[int]
    rating: tp.Optional[float] = 5.0


@dataclass
class Order:
    """Dataclass that contains Order info"""

    user_id: tp.Optional[int]
    order_name: tp.Optional[str]
    order_address: tp.Optional[str]
    order_time: tp.Optional[datetime]
    order_status: tp.Optional[str]
    order_actor_id: tp.Optional[int]


class BotDB:
    """Database class for telegram bot"""

    def __init__(self, bot_token: str) -> None:
        """
        :param bot_token: token for generate unique db name
        """
        self._db_name = (
            f"database{hashlib.sha1(bot_token.encode('utf-8')).hexdigest()}.db"
        )
        self._db_path = path.joinpath(self._db_name)
        self._create_tables()

    def _create_tables(self) -> None:
        """Private method creating tables"""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users
                              (chat_id INTEGER PRIMARY KEY,
                               login VARCHAR(100),
                               city VARCHAR(100),
                               rating REAL)
                           """
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS orders
                              (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                               user_id INTEGER,
                               order_name VARCHAR(100),
                               order_address VARCHAR(100),
                               order_time TIMESTAMP,
                               order_status VARCHAR(5),
                               order_actor_id INTEGER DEFAULT NULL,
                               FOREIGN KEY(user_id) REFERENCES users(chat_id))
                           """
            )

    def add_user(self, user: User) -> None:
        """Adding user to database"""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            if not self.check_user(user.chat_id):
                params = user.chat_id, user.login, user.city.lower(), user.rating
                cursor.execute(
                    "INSERT INTO users VALUES (?, ?, ?, ?) ", params)
            else:
                params = user.login, user.city, user.rating, user.chat_id
                cursor.execute(
                    "UPDATE users "
                    "SET login = ?, "
                    "city = ?, "
                    "rating = ? "
                    "WHERE chat_id = ?",
                    params,
                )

    def add_order(self, order: Order) -> None:
        """Adding user to database"""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            params = order.user_id, \
                     order.order_name, \
                     order.order_time, \
                     order.order_address, \
                     order.order_actor_id, \
                     order.order_status \

            cursor.execute(
                "INSERT INTO orders (user_id, order_name, "
                "order_time, order_address, order_actor_id, order_status) VALUES (?, ?, ?, ?, ?, ?) ", params)

    def check_user(self, chat_id: int) -> bool:
        """Checking if user already exists in db"""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT COUNT(*) FROM users WHERE chat_id = {chat_id}")
            data = cursor.fetchone()
        return data[0] != 0

    def get_user(self, chat_id: int) -> User:
        """Get user from database"""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT chat_id, "
                "login, "
                "city, "
                "rating "
                "FROM users "
                "WHERE chat_id = ?",
                (chat_id,),
            )
            data = cursor.fetchone()
        return User(*data)

    def get_users(self):
        """Return all users from DB"""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT *"
                "FROM users"
            )
            data = cursor.fetchall()
        return data

    def get_orders(self, city, id):
        """Return all orders from DB"""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT orders.user_id, orders.order_name, orders.order_address, orders.order_time, "
                "orders.order_status, orders.order_actor_id "
                "FROM orders JOIN users ON"
                " users.chat_id = orders.user_id WHERE orders.order_address = ? "
                "AND orders.user_id != ? AND users.city = ?", (city, id, city)
            )
            data = cursor.fetchall()
        return [Order(*order_data) for order_data in data]
