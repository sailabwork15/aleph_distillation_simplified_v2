from setuptools import setup, find_packages

setup(
    name='distill',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyomo',
        'numpy',
        'pandas',
        'matplotlib',
        'openpyxl',
    ],
)
