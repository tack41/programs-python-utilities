#!/usr/bin/env python3
"""Copy files from/to OCI object storage using Google Cloud Storage(GCS)

Prerequisites:
  * Google Cloud CLI must be already installed.
    https://cloud.google.com/sdk/docs/install
  * `gcloud init` command must have been run.
  * GCSにアクセスするアカウント(コンピューター/ユーザー)に対して、GCSの該当バケットの読み取り/書き込み権限を付与していること
"""

import pathlib
import shlex
import subprocess
from typing import Tuple

class GCIGCSRemoteCopier:
    """Class Copy files from/to OCI object storage using OCI CLI

    Attributes:
        __bucket_name(str): Target bucket name.
    """

    __gsutil_cmd: pathlib.Path
    __remote_dir: str = ""
    __bucket_name: str = ""

    def __init__(self, gsutil_cmd: pathlib.Path, bucket_name: str, remote_dir: str):
        """Constructor

        Args:
          gsutil_cmd: path of gsutil command
          remote_dir(str): remote directory to be copied from. If root directory, specify blank.
          bucket_name(str): Target bucket name.
        """

        self.__gsutil_cmd = gsutil_cmd

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
            cmd = f"{self.__gsutil_cmd} cp gs://{self.__bucket_name}/{self.__remote_dir}{file} {local_dir.joinpath(file)}"
            res = subprocess.run(shlex.split(
                cmd), capture_output=True, check=False)
            if res.returncode != 0:
                return False, f"Failed to executing '{cmd}\n{res.stdout.decode()}\n{res.stderr.decode()}"

        return True, ""

    def copy_to(self, local_dir: pathlib.Path, files: list[str])-> Tuple[bool, str]:
        """Copy files to remote storage from local

        Args:
          local_dir(pathlib.Path): local directory path to be copied to
          file_list(list[str]): file names to be copied

        Returns:
          bool: True is success, False is fail
          str: Message when fails.
        """

        for file in files:
            cmd = f"{self.__gsutil_cmd} cp  {local_dir.joinpath(file)} gs://{self.__bucket_name}/{self.__remote_dir}{file}"
            print(f"cmd: {cmd}")
            res = subprocess.run(shlex.split(
                cmd), capture_output=True, check=False)
            if res.returncode != 0:
                return False, f"Failed to executing '{cmd}\n{res.stdout.decode()}\n{res.stderr.decode()}"

        return True, ""
