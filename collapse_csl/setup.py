from setuptools import setup, find_packages

setup(
    name="collapse_vm",
    version="0.1.0",
    description="Collapse Symbolic Language VM for anchor-based collapse evaluation",
    author="G. Bogans",
    packages=find_packages(),  # discovers collapse_vm package
    include_package_data=True,
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
        # "fractions" removed — standard lib
    ],
    entry_points={
        "console_scripts": [
            "collapse-vm=collapse_vm.cli:run",
        ],
    },
    python_requires=">=3.8",
)
