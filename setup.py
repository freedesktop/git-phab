import subprocess
import sys

from setuptools import setup

setup_requires = []
if "upload" in sys.argv:
    setup_requires=['setuptools-markdown'],
else:
    setup_requires=['pre-commit']

setup(
    name="git-phab",
    version="2.0.0",
    author="Xavier Claessens",
    author_email="xavier.claessens@collabora.com",
    description=("Git subcommand to integrate with phabricator"),
    license="GPL",
    keywords="phabricator tool git",
    url="http://packages.python.org/git-phab",
    long_description_markdown_filename='README.md',
    setup_requires=setup_requires,
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)"
    ],
    install_requires=['GitPython>=2.0.0', 'appdirs', 'argcomplete', 'phabricator'],
    scripts=['git-phab'],
)

try:
    subprocess.check_call(["pre-commit", "install"])
except (FileNotFoundError, subprocess.CalledProcessError):
    print("Could not install `pre-commit` hook")
