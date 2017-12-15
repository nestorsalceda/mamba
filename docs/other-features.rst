Other Features
==============

There are other features that does not fit in other categories. Just a little explanation.

Slow examples
-------------

Mamba is able to highlight an example when is tooking more time than a threeshold. By default is 0.75 seconds, but you can control with the command line:

::

  $ pipenv run mamba --slow 0.5

This will highlight all tests that takes more than 0.5 seconds.

Coverage
--------

Mamba can be used with coverage tool.

::

  $ pipenv run mamba --enable-coverage

And this generate a .coverage file and you can generate a HTML report:

::

  $ pipenv run coverage html
