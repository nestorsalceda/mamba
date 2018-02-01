Formatters
==========

Mamba bundles with two formatters.

Progress Formatter
------------------

This is the default formatter. It displays a point for every example executed:

* Green point: It means that example has passed
* Yellow point: It means that example has been skipped
* Red point: It means that example has failed

Documentation Formatter
-----------------------

This is an extra formatter that allows you to read in a tree way. It uses same color scheme than previous formatter.

Is useful when you have a few tests and want to check that examples are written in human language.

For enabling it:

::

  $ pipenv run mamba --format=documentation

Custom Formatters
-----------------

Mamba supports third party formatters. Imagine there is a new IDE or some specific needs for your Continuous Integration tool, so:

::

  $ pipenv run mamba --format=wondertech.MyCustomFormatter


And mamba tries to instantiate the *wondertech.MyCustomFormatter* class.  But there are 2 conditions that should be met:

* A settings object is passed to object constuctor
* Inherit from mamba.formatter.Formatter for overriding methods
