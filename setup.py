import os

from setuptools import find_packages, setup

DESCRIPTION = "Python wrapper for querying the ESS user office system"

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n" + f.read()
except Exception as error:
    print("COULD NOT GET LONG DESC: {}".format(error))
    LONG_DESCRIPTION = DESCRIPTION

setup(
    name="yuos_query",
    version="0.1.4",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="ScreamingUdder",
    url="https://github.com/ess-dmsc/yuos_query",
    license="BSD 2-Clause License",
    packages=find_packages(exclude=["*tests", "tests.*"]),
    python_requires=">=3.6.0",
    install_requires=["gql==3.0.0a5", "requests"],
    extras_require={},
)
