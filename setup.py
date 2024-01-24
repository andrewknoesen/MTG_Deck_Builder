from setuptools import setup, find_packages
import codecs

# Get requirements contents
with open('requirements.txt', 'r') as fh:
    requirements_list = fh.readlines()

setup(
    name='mtg_deck_builder',
    packages=find_packages(),
    install_requires=requirements_list,
    keywords=['python', 'MTG_DECK_BUILDER'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X"
    ]
)
