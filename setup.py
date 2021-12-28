from pathlib import Path

from setuptools import setup, find_packages

BASE_DIR = Path(__file__).parent.resolve(strict=True)
VERSION = '0.0.1'
PACKAGE_NAME = 'srsran-controller'
PACKAGES = [p for p in find_packages() if not p.startswith('tests')]


def parse_requirements():
    reqs = []
    with open(BASE_DIR / 'requirements.txt', 'r') as fd:
        for line in fd.readlines():
            line = line.strip()
            if line:
                reqs.append(line)
    return reqs


def get_description():
    return (BASE_DIR / 'README.md').read_text()


setup(
    version=VERSION,
    name=PACKAGE_NAME,
    description='A python controller for srsRAN',
    cmdclass={},
    packages=find_packages(),
    data_files=[('.', ['requirements.txt'])],
    install_requires=parse_requirements(),
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    tests_require=['pytest'],
)
