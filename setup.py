from setuptools import setup
import pip
import sys
import versioneer


def win_pip_install(package, install_list):
    if package not in install_list:
        return
    print("Installing %s using pip instead of setuptools." % package)
    pip.main(["install", package])
    install_list.remove(package)


# package required
install_packages = ["openpyxl",  # to manage excel spreadsheets
                    ]

windows_develop = ["cx_freeze", ]  # to build exe file
mac_develop = ["py2app", ]

develop_packages = ["nose", "pep8", "coverage"]
print("Installing auxiclean, the following packages are required:",
      install_packages)

if "develop" in sys.argv:
    print(("Development installation: installing more packages for testing"
           "  purposes:"), develop_packages)
    install_packages += develop_packages
    if sys.platform == "win32":
        install_packages += windows_develop
    elif sys.platform == "darwin":
        install_packages += mac_develop

# if on windows, there is a bug when installing some packages with setuptools.
# installing them with pip before setup fixes this.
problematics = ("cx_freeze", "coverage")
if sys.platform == "win32":
    for problematic in problematics:
        win_pip_install(problematic, install_packages)

setup(name="auxiclean",
      version=versioneer.get_version(),
      description="Distributeur de taches d'auxiliariat d'enseignement",
      url="https://github.com/physumasso/auxiclean",
      install_requires=install_packages,
      cmdclass=versioneer.get_cmdclass()
      )
