#!/usr/bin/env python3
"""Copy files from/to OCI object storage using OCI CLI

Prerequisites:
  * OCI CLI must be already installed.
    https://docs.oracle.com/ja-jp/iaas/Content/API/SDKDocs/cliinstall.htm
  * `oci setup config` command must have been run.
  * The user configured with the `oci setup config` command 
    must have read/write permission to the target bucket.
  * The path to `oci` command must be passed.
"""

import pathlib
import shlex
import subprocess
from typing import Tuple


class OCIOSRemoteCopier:
    """Copy files from/to OCI object storage using OCI CLI

    Attributes:
        __bucket_name(str): Target bucket name.
    """

    __oci_cmd: pathlib.Path
    __remote_dir: str = ""
    __bucket_name: str = ""

    def __init__(self, oci_cmd: pathlib.Path, bucket_name: str, remote_dir: str):
        """Constructor

        Args:
          oci_bin: path of oci command
          remote_dir(str): remote directory to be copied from. If root directory, specify blank.
          bucket_name(str): Target bucket name.
        """

        self.__oci_cmd = oci_cmd

        if len(remote_dir.strip()) != 0:
            self.__remote_dir = remote_dir.strip() + "/"
        else:
            self.__remote_dir = ""

        self.__bucket_name = bucket_name.strip()

    def copy_from(self, local_dir: pathlib.Path, files: list[str]) -> Tuple[bool, str]:
        """Copy files from remote storage to local

        Args:
          local_dir(pathlib.Path): local directory path to be copied to
          file_list(list[str]): file names to be copied

        Returns:
          bool: True is success, False is fail
          str: Message when fails.
        """

        for file in files:
            cmd = f"{self.__oci_cmd} os object get --bucket-name {self.__bucket_name} --name {self.__remote_dir}{file} --file {local_dir.joinpath(file)}"
            res = subprocess.run(shlex.split(
                cmd), capture_output=True, check=False)
            if res.returncode != 0:
                return False, f"Failed to executing '{cmd}\n{res.stdout.decode()}\n{res.stderr.decode()}"

        return True, ""

    def copy_to(self, local_dir: pathlib.Path, files: list[str]):
        """Copy files to remote storage from local

        Args:
          local_dir(pathlib.Path): local directory path to be copied to
          file_list(list[str]): file names to be copied

        Returns:
          bool: True is success, False is fail
          str: Message when fails.
        """

        for file in files:
            cmd = f"{self.__oci_cmd} os object put --bucket-name {self.__bucket_name} --name {self.__remote_dir}{file} --file {local_dir.joinpath(file)}"
            print(f"cmd: {cmd}")
            res = subprocess.run(shlex.split(
                cmd), capture_output=True, check=False)
            if res.returncode != 0:
                return False, f"Failed to executing '{cmd}\n{res.stdout.decode()}\n{res.stderr.decode()}"

        return True, ""
