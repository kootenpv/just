from setuptools import find_packages
from setuptools import setup

MAJOR_VERSION = "0"
MINOR_VERSION = "8"
MICRO_VERSION = "139"
VERSION = "{}.{}.{}".format(MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION)

setup(
    name="just",
    version=VERSION,
    description="Automatically just read and write files based on extension.",
    author="Pascal van Kooten",
    url="https://github.com/kootenpv/just",
    author_email="kootenpv@gmail.com",
    install_requires=[
        "pyyaml",
        "glob2",
        "dill",
        "jsonpath_rw",
        "preconvert",
        "preconvert_numpy",
        "requests",
        "python-dateutil",
    ],
    entry_points={"console_scripts": ["just = just.__main__:main"]},
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Customer Service",
        "Intended Audience :: System Administrators",
        "Operating System :: Microsoft",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    platforms="any",
)
