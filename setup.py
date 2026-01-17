from setuptools import find_packages, setup

setup(
    name="windfarm_curtailment",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Any dependencies your jobs need
        "pandas",
        "numpy",
        "scikit-learn",
        "requests",
        "pyarrow",
    ],
)
