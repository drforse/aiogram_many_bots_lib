import re
import setuptools
import pathlib

WORK_DIR = pathlib.Path(__file__).parent


with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version():
    """
    Read version
    :return: str
    """
    txt = (WORK_DIR / 'aiomanybots' / '__init__.py').read_text('utf-8')
    try:
        return re.findall(r"^__version__ = ('|\")([^\1]+)\1r?$", txt, re.M)[0][1]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


setuptools.setup(
    name="aiomanybots",
    version=get_version(),
    author="drforse",
    author_email="george.lifeslice@gmail.com",
    description="Library for running bots concurrently on aiogram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drforse/aiogram_many_bots_lib",
    packages=setuptools.find_packages(),
    install_requires=[
        'manybots@git+git://github.com/Senderman/manybotslib.git#egg=manybots',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
