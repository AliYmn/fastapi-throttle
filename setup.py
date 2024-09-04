from setuptools import setup, find_packages

setup(
    name="fastapi-limiter",
    version="0.",
    packages=find_packages(),
    install_requires=[
        "fastapi",
    ],
    description="A rate limiter for FastAPI without using Redis.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/AliYmn/fastapi-limiter",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
