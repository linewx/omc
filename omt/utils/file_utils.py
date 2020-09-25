import os


def make_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
