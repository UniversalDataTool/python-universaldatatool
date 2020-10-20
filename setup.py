from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

version = {}
with open(os.path.join(_here, "universaldatatool", "version.py")) as f:
    exec(f.read(), version)

with open('requirements.txt') as reqs:
    install_requires = [
        line for line in reqs.read().split('\n') if line
    ]

setup(
    name="universaldatatool",
    version=version["__version__"],
    description=(
        "Interact with any kind of kind of data directly in a jupyter notebook."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Severin Ibarluzea",
    author_email="seve@wao.ai",
    url="https://github.com/UniversalDataTool/python-universaldatatool",
    license="MIT",
    packages=["universaldatatool"],
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
