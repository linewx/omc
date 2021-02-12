import os
import shutil
from distutils.dir_util import copy_tree


def make_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def inplace_replace(file_name, old_string, new_string):
    with open(file_name) as f:
        new_content = f.read().replace(old_string, new_string)

    with open(file_name, "w") as f:
        f.write(new_content)


def copy(src, dest):
    if os.path.isfile(src):
        shutil.copy(src, dest)
    else:
        copy_tree(src, dest)
