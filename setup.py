from setuptools import setup, find_packages

setup(
    name="kpi_tree_lib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "anytree",
    ],
)