from setuptools import setup, find_packages
import sys

if sys.version_info[0] < 3:
    with open("README.md") as f:
        README = f.read()
else:
    with open("README.md", encoding="utf-8") as f:
        README = f.read()

setup(
    name="fastapi-throttle",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "fastapi",
    ],
    description="A rate limiter for FastAPI without using Redis.",
    author="Ali Yaman",
    author_email="aliymn.db@gmail.com",
    url="https://github.com/AliYmn/fastapi-throttle",
    long_description_content_type="text/markdown",
    long_description=README,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8, <3.13",
)
