#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    reqs = fh.read().split('\n')[:-1]

setuptools.setup(
    name="no_queue_life",
    version="1.0.0",
    author="Slava Kostrov",
    author_email="slavkotrov@gmail.com",
    description="Telegram bot for predicting gender and age from photo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/slavkostrov/X5-Bot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["cmake", "pyTelegramBotAPI"].extend(reqs),
    python_requires='>=3.8'
)
