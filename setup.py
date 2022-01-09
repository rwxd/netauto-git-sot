from setuptools import setup, find_packages
from os import path

requirements = []
with open("./requirements.txt") as f:
    for line in f.read().splitlines():
        requirements.append(line)

setup(
    name='eve',
    version='0.0.1',
    description='Eve is a tool for building device configurations',
    author='rwxd',
    author_email='rwxd@pm.me',
    url="https://github.com/rwxd/netauto-git-sot",
    license='MIT',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={"console_scripts": ["eve = eve.__main__:main"]},
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
