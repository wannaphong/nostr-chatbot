# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open("README.md","r",encoding="utf-8-sig") as f:
    readme = f.read()

with open("requirements.txt","r",encoding="utf-8-sig") as f:
    requirements = [i.strip() for i in f.readlines()]

setup(
    name="nostr-chatbot",
    version="0.1.0dev1",
    description="Nostr chatbotlibrary",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Wannaphong",
    author_email="wannaphong@yahoo.com",
    url="https://github.com/wannaphong/nostr-chatbot",
    packages=find_packages(),
    test_suite="tests",
    python_requires=">=3.8",
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords=[
        "chatbot",
        "nostr",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
    ],
)
