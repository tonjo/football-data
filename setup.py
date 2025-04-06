from setuptools import setup, find_packages

setup(
    name="football_data",
    version="1.0.0",
    packages=find_packages(),
    description="A Python wrapper around the football-data API.",
    url="https://github.com/tonjo/football-data",
    author="Antonio Mignolli",
    author_email="antoniomignolli@gmail.com",
    license="AGPL-3.0",
    classifiers=[
        "Development Status :: Working Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3.8"
    ],
    keywords="football football-data api",
    install_requires=['requests'],
    python_requires=">=3.6"
)
