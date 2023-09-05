.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/debmirror.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/debmirror
    .. image:: https://readthedocs.org/projects/debmirror/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://debmirror.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/debmirror/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/debmirror
    .. image:: https://img.shields.io/pypi/v/debmirror.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/debmirror/
    .. image:: https://img.shields.io/conda/vn/conda-forge/debmirror.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/debmirror
    .. image:: https://pepy.tech/badge/debmirror/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/debmirror
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/debmirror

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=========
debmirror
=========


    Canonical Take home assignment


INSTRUCTIONS
====

Debian uses *deb packages to deploy and upgrade software. The packages are stored in repositories and each repository contains the so called "Contents index". The format of that file is well described here https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices

Your task is to develop a python command line tool that takes the architecture (amd64, arm64, mips etc.) as an argument and downloads the compressed Contents file associated with it from a Debian mirror. The program should parse the file and output the statistics of the top 10 packages that have the most files associated with them. An example output could be:

 

./package_statistics.py amd64

    <package name 1>         <number of files>
    <package name 2>         <number of files>

......

    <package name 10>         <number of files>

You can use the following Debian mirror: http://ftp.uk.debian.org/debian/dists/stable/main/. Please try to follow Python's best practices in your solution. Hint: there are tools that can help you verify your code is compliant. In-line comments are appreciated.

Please do your work in a local Git repository. Your repo should contain a README that explains your thought process and approach to the problem, and roughly how much time you spent on the exercise. When you are finished, create a tar.gz of your repo and submit it to the link included in this email. Please do not make the repository publicly available.

Note: We are interested not only in quality code, but also in seeing your approach to the problem and how you organize your work.

SETUP
====

After cd-ing into your new project and creating (or activating) an isolated development environment (with virtualenv, conda or your preferred tool), you can do the usual editable install:

pip install -e .

We also recommend using tox, so you can take advantage of the automation tasks we have setup for you, like:

tox -e build  # to build package distribution

tox -e publish  # to test project uploads correctly in test.pypi.org

tox -e publish -- --repository pypi  # to release package to PyPI

tox -av  # to list all the tasks available

USAGE
====

The following command can be executed to run the program.

python -m debmirror.py <arguments>

EXAMPLE
====

Below is an example command to execute the code.

python3 debmirror.py amd64 -o ../Desktop/ -u

CLI ARGUMENTS
====

The list below describes all the arguments that can be passed to the CLI.
usage: python3 debmirror.py [-h] [-m MIRROR_URL] [-u] [-o OUTPUT_DIR] arch

Argument Parser for debian mirror

positional arguments:
  arch                  architecture of contents index to be parsed

options:
  -h, --help            show this help message and exit
  -m MIRROR_URL, --mirror_url MIRROR_URL
                        debian mirror URL to fetch contents file
  -u, --udeb            flag if file is udeb. DEFAULT False
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        output directory for files to be stored, DEFAULT current directory

TESTING
====

The command below can be used to execute the test cases.

pytest



.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
