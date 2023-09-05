import pytest
import os
from pathlib import Path
from collections import defaultdict

from src.debmirror.debmirror import download_contents_file, parse_contents_file, main

__author__ = "Himanshu Singhal"
__copyright__ = "Himanshu Singhal"
__license__ = "MIT"

def test_download_contents_file():
    arch = "amd64"
    mirror_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"
    output_dir = os.getcwd()
    assert download_contents_file(arch, False, mirror_url, output_dir) == (Path(output_dir) / f"{arch}")
    assert os.path.exists(Path(output_dir) / f"{arch}")
    assert download_contents_file(arch, True, mirror_url, output_dir) == (Path(output_dir) / f"udeb-{arch}")
    assert os.path.exists(Path(output_dir) / f"udeb-{arch}")

def test_parse_contents_file():
    arch = "amd64"
    mirror_url = "http://ftp.uk.debian.org/debian/dists/stable/main/"
    output_dir = os.getcwd()
    contents_file = download_contents_file(arch, False, mirror_url, output_dir)
    assert not parse_contents_file(contents_file) == defaultdict(list)

def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["amd64"])
    captured = capsys.readouterr()
    assert f"{'No.':<10}\t{'Package Name':<40}\tFile Count" in captured.out
