from setuptools import setup

setup(
    name="jules-cli",
    version="0.1.0",
    py_modules=["jules_cli"],
    entry_points={
        "console_scripts": [
            "jules-cli=jules_cli:main",
        ],
    },
    install_requires=[],
    python_requires=">=3.6",
)
