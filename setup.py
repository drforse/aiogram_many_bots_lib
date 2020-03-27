import setuptools
import aiomanybots

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiomanybots",
    version=aiomanybots.__version__,
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
    python_requires='>=3.6',
)
