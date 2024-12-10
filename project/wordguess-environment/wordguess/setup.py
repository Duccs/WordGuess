from setuptools import setup, find_packages

setup(
    name="wordguess",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={"wordguess": ['data/*.json']},
    install_requires=["gym>=0.26.0", "pygame>=2.1.0"],
)