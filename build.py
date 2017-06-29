import versioneer
import sys
import pip
import os


if sys.platform == "darwin":
    # need to find an alternative for mac OS
    raise OSError("Build does not work on MacOS because of cx_freeze.")
if "build" not in sys.argv:
    raise ValueError("Run this script using the 'build' option.")

# we need cv_Freeze
try:
    from cx_Freeze import setup as setupcx, Executable
except ImportError:
    pip.main(["install", "cx_Freeze"])
    from cx_Freeze import setup as setupcx, Executable

base = None
include_files = []
if sys.platform == "win32":
    base = 'Win32GUI'
    # there's a bug in cx_freeze for windows while searching for some library
    # this manually fixes it. see link below
    # https://bitbucket.org/anthony_tuininga/cx_freeze/issues/155/required-environment-variables-tcl_library

    PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
    os.environ["TCL_LIBRARY"] = os.path.join(PYTHON_INSTALL_DIR, "tcl",
                                             "tcl8.6")
    os.environ["TK_LIBRARY"] = os.path.join(PYTHON_INSTALL_DIR, "tcl", "tk8.6")
    include_files = [os.path.join(PYTHON_INSTALL_DIR, "DLLs", "tk86t.dll"),
                     os.path.join(PYTHON_INSTALL_DIR, "DLLs", "tcl86t.dll")]

executables = [Executable("run.py", base=base, targetName="auxiclean.exe")]
version = versioneer.get_version()
short = version[:version.find("+")].strip("v")
setupcx(name="auxiclean",
        version=short,
        executables=executables,
        options={"build_exe": {"include_files": include_files}})
