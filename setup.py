from os.path import dirname, join
from setuptools import setup

version = '0.1.0'


def _strip_comments(requirements):
    return [l.split('#', 1)[0].strip() for l in requirements]


def _get_requirements(file):
    requirements = []
    with open(join(dirname(__file__), file)) as f:
        requirements = f.readlines()
    return [r for r in _strip_comments(requirements) if r]


setup(name='pwnd_passwords',
      version=version,
      author='Chad Dotson',
      author_email="chad@cdotson.com",
      description='Script for displaying pwnd password counts.',
      license="GNUv3",
      keywords=[],
      url="https://github.com/chaddotson/pwnd_passwords/",
      packages=['bin'],
      install_requires=_get_requirements('requirements.txt'),
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'pwndpasswords = bin.pwnd_passwords:cli',
          ]
      },
      classifiers=[
          "Development Status :: 4 - Beta",
          "Topic :: Utilities",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      ]
)
