from setuptools import setup
import sys


# package required
install_packages = []

develop_packages = ["nose", "pep8", "coverage"]
print("Installing auxiclean, the following packages are required:",
      install_packages)

if "develop" in sys.argv:
    print(("Development installation: installing more packages for testing"
           "  purposes:"), develop_packages)
    install_packages += develop_packages


setup(name="auxiclean",
      version="0.0.1",
      description="Distributeur de taches d'auxiliariat d'enseignement",
      url="https://github.com/physumasso/auxiclean",
      install_requires=install_packages,
      )
