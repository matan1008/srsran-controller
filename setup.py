from setuptools import setup, find_packages

setup(
    name='srsran-controller',
    packages=find_packages(),
    install_requires=['docker', 'libconf', 'pyshark'],
    tests_require=['pytest'],
)
