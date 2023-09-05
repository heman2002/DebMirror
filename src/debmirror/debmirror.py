import argparse
import logging
import sys
import requests
from pathlib import Path
import os
from collections import defaultdict
import gzip

#from debmirror import __version__

__author__ = "Himanshu Singhal"
__copyright__ = "Himanshu Singhal"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from debmirror.debmirror import download_contents_file`,
# when using this Python module as a library.

def download_contents_file(arch: str, udeb: bool, mirror_url: str, output_dir: str) -> str:
    """This function takes debian architecture, if file is udeb, mirror URL, and output directory 
    and downloads the file from the mirror URLto the given output directory

    Arguments:

        arch: architecture of the contents file to be downloaded
        udeb: if the contents file to be downloaded is udeb or not
        mirror_url: the mirror URL from where the contents file is to be downloaded from
        output_dir: Directory where the file should be downloaded to

    Returns:
        str: path of the content file where it was downloaded and extracted.
    """
    
    
    # download the file given the url
    if udeb:
        url = f"{mirror_url}Contents-udeb-{arch}.gz"
        output_gz_file = Path(output_dir) / f"udeb-{arch}.gz"
        output_file = Path(output_dir) / f"udeb-{arch}"
    else:
        url = f"{mirror_url}Contents-{arch}.gz"
        output_gz_file = Path(output_dir) / f"{arch}.gz"
        output_file = Path(output_dir) / f"{arch}"

    response = requests.get(url, stream=True)
    
    #saving output in chunks in case of large files
    with open(output_gz_file, mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)

    with gzip.open(output_gz_file, "rb") as buffer:
        data = buffer.read()

    with open(output_file, "wb") as buffer:
        buffer.write(data)

    return output_file

def parse_contents_file(contents_file: str) -> dict:
    """Parses a given contents index file and returns a dictionary with the
    package names and their associated files

    Arguments:
        contents_file: local path of content file to be parsed.

    Returns:
        package_dict: dictionary containing the packages as keys and
              a list of associated files as the values
    """
    package_dict = defaultdict(list)
    with open(contents_file) as buffer:
        for line in buffer:
            line = line.strip()
            if line == "":
                # skip empty lines
                continue
            file_name, packages = line.rsplit(" ", maxsplit=1)
            packages = packages.split(",")
            for package in packages:
                    package_dict[package].append(file_name)
    return package_dict

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Argument Parser for debian mirror")
    parser.add_argument("arch", type=str, help="architecture of contents index to be parsed")
    parser.add_argument("-m", "--mirror_url", type=str, default="http://ftp.uk.debian.org/debian/dists/stable/main/", help=("debian mirror URL to fetch contents file"))
    parser.add_argument("-u", "--udeb", action='store_true', help=("flag if file is udeb. DEFAULT False"))
    parser.add_argument("-o", "--output_dir", type=str, help=("output directory for files to be stored, DEFAULT current directory"), default=os.getcwd())
    return parser.parse_args(args)

def main(args):
    """Wrapper allowing debian mirror to be downloaded and parsed with string arguments in a CLI fashion

    It prints the top 10 packages result to the ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["arch", "--mirror_url", "--udeb", "--output_dir"]``).
    """
    args = parse_args(args)
    
    #downloading the appropriate file for content
    contents_file = download_contents_file(args.arch, args.udeb, args.mirror_url, args.output_dir)

    #parsing file to obtain files for each package
    package_data = parse_contents_file(contents_file)
    package_list = package_data.keys()
    
    #sorting packages in descending order by number of files in the package
    package_list = sorted(package_list, key=lambda x: len(package_data[x]), reverse=True)
    
    for idx, package in enumerate(package_list):
        if idx == 0:
            print(f"{'No.':<10}\t{'Package Name':<40}\tFile Count")
        print(f"{idx+1:<10}\t{package:<40}\t{len(package_data[package])}")
        if idx+1 == 10:
            break
    

def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m debmirror.debmirror <deb> 
    #
    run()
