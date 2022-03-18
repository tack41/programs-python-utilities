# OSのmountコマンドを使用したCIFSドライブへ/からのコピー
import os.path
import pathlib
import shutil
import subprocess

class CIFSOSCopier:
  __domain_name = ""
  __remote_cifs_dir = ""
  __local_mount_dir = ""
  __cifs_id = ""
  __cifs_pw = ""

  def __init__(self, domain_name: str, remote_cifs_dir: str, local_mount_dir: pathlib.Path, cifs_id: str, cifs_pw: str):
    self.__domain_name = domain_name
    self.__remote_cifs_dir = remote_cifs_dir
    self.__local_mount_dir = str(local_mount_dir)
    self.__cifs_id = cifs_id
    self.__cifs_pw = cifs_pw

  def __enter__(self):
    cmd = "mount -t cifs -o "
    if self.__cifs_id:
      cmd += f"username={self.__cifs_id},password={self.__cifs_pw}"
    cmd += ",vers=3.0,sec=ntlmsspi"
    if self.__domain_name:
      cmd += f",domain={self.__domain_name}"
    cmd += f" {self.__remote_cifs_dir} {self.__local_mount_dir}"
    rc = subprocess.call(cmd, shell=True)
    if rc != 0:
      raise OSError(f"Failed to mount when executing '{cmd}'")

    return self

  def __exit__(self, exc_type, exc_value, traceback):
    cmd = f"umount {self.__local_mount_dir}"
    rc = subprocess.call(cmd, shell=True)
    if rc != 0:
      raise OSError(f"Failed to unmount when executing '{cmd}'")

  def copy(self, copy_from_list, copy_to: pathlib.Path):
    """コピー元は存在するファイル(pathlib.Path)の配列、コピー先は存在するディレクトリ(pathlib.Path)の場合のみサポート"""

    if not isinstance(copy_from_list, list):
      raise TypeError(f"Copy sources must be list of pathlib.Path: {copy_from_list}")
    for copy_from in copy_from_list:
      if not isinstance(copy_from, pathlib.Path):
        raise TypeError(f"An element of copy sources must be pathlib.Path: {copy_from}")
      if not copy_from.exists():
        raise FileNotFoundError(f"An element of copy sources does not exists: {copy_from}")
      if not copy_from.is_file():
        raise TypeError(f"An element of copy sources must be file: {copy_from}")
    
    if not copy_to.exists():
      raise FileNotFoundError(f"Copy destination does not exists: {copy_to}")
    if not copy_to.is_dir():
      raise TypeError(f"Copy destination must be a directory: {copy_to}")

    for copy_from in copy_from_list:
      shutil.copy2(copy_from,copy_to.joinpath(copy_from.name))