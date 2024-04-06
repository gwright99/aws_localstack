import sys
import pathlib

# Don't write __pycache__ folder
sys.dont_write_bytecode = True

# https://stackoverflow.com/questions/41748464/pytest-cannot-import-module-while-python-can
# See `mide rodent` comment
this_file_path = pathlib.Path(__file__)
src_core_dir_path_str = str(this_file_path.parent.joinpath('src'))
sys.path.insert(0, src_core_dir_path_str)