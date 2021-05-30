#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
"""Exception for SimpleBot"""


class TgBotException(Exception):
    """Base exception for bot"""


class InfoInputException(TgBotException):
    """Exception of bad information input"""


class PhotoProcessingException(TgBotException):
    """Exception of photo processing"""
