# @author  Julien Gourgue
from setuptools import setup, find_packages

setup(
    name='sniff',
    version='0.1.0',
    author='GourgueJulien',
    description='CLI tool to capture and analyse Matter/Thread packet',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pyshark',
        'prettytable',
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'sniff=sniffer.cli:sniff',
        ],
    },
)