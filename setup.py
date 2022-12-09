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

# Import version number
from yuos_query.version import version

setup(
    name="yuos_query",
    version=version,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="ScreamingUdder",
    url="https://github.com/ess-dmsc/yuos_query",
    license="BSD 2-Clause License",
    packages=find_packages(exclude=["*tests", "tests.*"]),
    python_requires=">=3.6.0",
    install_requires=["gql>=3.0.0", "requests>=2.27.1", "requests-toolbelt>=0.9.1"],
    extras_require={},
)
