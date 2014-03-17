# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from mamba import __version__

setup(name='mamba',
      version=__version__,
      description="The definitive testing tool for Python. Born under the banner of Behavior Driven Development.",
      long_description=open('README.md').read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing'

      ],
      keywords='',
      author=u'Néstor Salceda',
      author_email='nestor.salceda@gmail.com',
      url='http://nestorsalceda.github.io/mamba',
      license='MIT/X11',
      packages=find_packages(exclude=['ez_setup', 'examples', 'spec', 'spec.*']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[line for line in open('requirements.txt')],
      entry_points={
          'console_scripts': [
              'mamba = mamba.cli:main'
          ]
      })
