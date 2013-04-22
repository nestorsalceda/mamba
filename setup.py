from setuptools import setup, find_packages

version = '0.1'

setup(name='mamba',
      version=version,
      description="",
      long_description=open('README.md').read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='MIT/X11',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[line for line in open('requirements.txt')],
      entry_points={
          'console_scripts': [
              'mamba = mamba.cli:main'
          ]
      })
