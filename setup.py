from setuptools import setup

import pathlib


version = pathlib.Path("version.txt").read_text().strip()

setup(
    name="jibrel-notable-accounts",
    version=version,
    description="Ethereum Mainnet accounts' information manager",
    packages=["jibrel_notable_accounts"],
    zip_safe=False,
    platforms="any",
    install_requires=[],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "jibrel-notable-accounts-parser = jibrel_notable_accounts.parser.__main__:main",
        ]
    }
)
