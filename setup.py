# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open("README.md","r",encoding="utf-8-sig") as f:
    readme = f.read()

requirements = [
    "cffi>=1.15.0",
    "cryptography>=37.0.4",
    "pycparser>=2.21",
    "python-socks>=2.1.1",
    "secp256k1>=0.14.0",
    "websocket-client>=1.3.3"
]

setup(
    name="nostr-chatbot",
    version="0.1.0dev2",
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
