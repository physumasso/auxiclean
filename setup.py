from setuptools import setup
import pip
import sys
import versioneer


# package required
install_packages = ["openpyxl",  # to manage excel spreadsheets
                    ]

develop_packages = ["nose", "pep8", "coverage"]
print("Installing auxiclean, the following packages are required:",
      install_packages)

if "develop" in sys.argv:
    print(("Development installation: installing more packages for testing"
           "  purposes:"), develop_packages)
    install_packages += develop_packages

# if on windows, there is a bug when installing coverage with setuptools.
# installing it with pip before setup fixes this.
if sys.platform == "win32" and "coverage" in install_packages:
    pip.main(["install", "coverage"])
    install_packages.remove("coverage")

setup(name="auxiclean",
      version=versioneer.get_version(),
      description="Distributeur de taches d'auxiliariat d'enseignement",
      url="https://github.com/physumasso/auxiclean",
      install_requires=install_packages,
      cmdclass=versioneer.get_cmdclass()
      )
