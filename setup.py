"""
Author: Tashfeen, Ahmad

The MIT License (MIT)
"""

from setuptools import setup, find_packages


setup(
    name='wordle',
    version='1.0.0',
    description='A word-game by Josh Wardle--implementation by Tashfeen.',
    author='Tashfeen Ahmad',
    author_email='tashfeen@ou.edu',
    license='MIT',
    url='https://github.com/simurgh9/wordle',
    python_requires='>=3.7',
    packages=find_packages(include=['wordle', 'wordle.*']),
    package_data={'wordle': ['data/word_list.csv']},
    install_requires=[
        'blessed == 1.19.1',
    ],
    entry_points={
        'console_scripts': [
            'wordle = wordle.__main__:main',
        ],
    },
)
