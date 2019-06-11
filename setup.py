from setuptools import setup, find_packages
import versioneer

tests_require = ["pytest", "pytest-runner", "pytest-cov", "coverage", "coveralls"]

dev_require = [
    "pytest",
    "versioneer",
    "black",
    "sphinx_rtd_theme",
    "sphinx-autodoc-annotation",
    "recommonmark",
] + tests_require

with open("README.md", "r") as src:
    LONG_DESCRIPTION = src.read()

setup(
    name="pyogas",
    description="Import and generation of iogas templates using python.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version=versioneer.get_version(),
    url="https://github.com/morganjwilliams/pyogas-templates",
    author="Morgan Williams",
    author_email="morgan.williams@csiro.au",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["geochemistry", "visualisation", "petrology"],
    packages=find_packages(exclude=["test*"]),
    install_requires=[
        "pathlib",
        "numpy",
        "matplotlib",
        "periodictable",
        "dicttoxml",
        "xmljson",
    ],
    extras_require={"dev": dev_require},
    tests_require=tests_require,
    test_suite="test",
    license="MIT",
    cmdclass=versioneer.get_cmdclass(),
)
