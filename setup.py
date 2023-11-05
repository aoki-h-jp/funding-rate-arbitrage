from setuptools import find_packages, setup

setup(
    name="funding-rate-arbitrage",
    version="1.2.1",
    description="A framework to help you easily perform funding rate arbitrage on major centralized cryptocurrency "
    "exchanges.",
    install_requires=["ccxt", "pandas", "rich", "matplotlib"],
    packages=find_packages(include=["funding_rate_arbitrage*"], exclude=["img"]),
    author="aoki-h-jp",
    author_email="aoki.hirotaka.biz@gmail.com",
    license="MIT",
)
