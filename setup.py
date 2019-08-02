from setuptools import setup, find_packages

import pathlib


version = pathlib.Path("version.txt").read_text().strip()

setup(
    name="jibrel-notable-accounts",
    version=version,
    description="Ethereum Mainnet accounts' information manager",
    packages=find_packages(
        exclude=["*.tests.*"],
    ),
    zip_safe=False,
    platforms="any",
    install_requires=[],
    include_package_data=True,
    package_data={
        "jibrel_notable_accounts": ["*.list"],
    },
    entry_points={
        "console_scripts": [
            "jibrel-notable-accounts-parser = jibrel_notable_accounts.parser.__main__:main",
        ]
    }
)
