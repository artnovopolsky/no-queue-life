#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="no_queue_life",
    version="1.0.0",
    author="Artyom Novopolsky, Pavel Mescheryakov, Vyacheslav Kostrov",
    author_email="slavkostrov@gmail.com",
    description="no-queue-life project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/artnovopolsky/no-queue-life",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["django==3.1.7"],
    python_requires='>=3.8'
)

