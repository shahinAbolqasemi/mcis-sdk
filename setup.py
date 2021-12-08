import setuptools
import pathlib

REQUIRES = [
    'httpx==0.21.1',
    'pydantic==1.8.2',
    'redis==4.0.2',
]

EXTRA_REQUIRE_UTILITY = []

DIR = pathlib.Path(__file__).parent

VERSION = (DIR / "VERSION").read_text()
README = (DIR / "README.md").read_text()

PLATFORMS = [
    'Operating System :: POSIX :: Linux',
]

KEYWORDS = [
    'MCI',
    'SDK',
    'EBCOM',
]

setuptools.setup(
    name="mci_service_sdk",
    version="0.0.1",
    author='Amerandish Dev',
    author_email='info@amerandish.com',
    maintainer="Shahin Abolqasemi",
    maintainer_email="shahin.abolqasemi@yahoo.com",
    description="An SDK to simplify MCI APIs",
    long_description=README,
    long_description_content_type="text/markdown",
    platforms=PLATFORMS,
    url="https://github.com/shahinAbolqasemi/mcis-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: Apache License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    license='Proprietary and Confidential',
    install_requires=REQUIRES,
    extras_require={
        "utility": EXTRA_REQUIRE_UTILITY,
    },
)
