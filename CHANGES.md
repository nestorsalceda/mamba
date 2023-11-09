# ChangeLog

## Version 0.11.3

* Add support up to Python 3.12

## Version 0.11.2

* Fix time field format for JUnit formatter

## Version 0.11.1

* Fix compatiblity issue with 3.8.4
* Fix some typos

## Version 0.11.0

* Fix hooks execution
* Avoid linter warnings on before and after each hook
* Document spec_helper.py file usage
* Support for Python 3.8
* Add JUnit XML formatter
* Remove Python 2 support
* Fix error location reporting

## Version 0.10

* Use metadata instead of encode in spec names
* Shared context: Remove duplication on spec files using shared contexts
* Improve execution context binding in helper methods
* Remove requirements from MANIFEST.in since is using pipenv

## Version 0.9.3

* Improve documentation
* Fix *_all hooks execution

## Version 0.9.2

* Fix error with set_failed call
* Add focus feature

## Version 0.9.1

* Just a little fix for pypi installation :)

## Version 0.9

* Add filtering support using tags
* Use new execution context for every example. Properties on self are never shared
* Changed execution model
* Added functions for description, it, context, before, after for making mamba more friendly to PEP8 checkers
* Removed subject autoinstantiation
* Removed filewatch feature, use entr or other similar utility
* Dropped Python 2.6 support

## Version 0.8.6

* Check for python 3.5
* Stick only minimal dependencies versions
* Allow loading of local non-installed modules and packages

## Version 0.8.5

* Show spec filename in each error
* Use .coveragerc file
* Run examples in natural order

## Version 0.8.4

* Added Python 2.6 support

## Version 0.8.3

* Upgrade coverage
* Fix error reporting in hooks
* Add support for mock.patch

## Version 0.8.2

* Fixes loading a file without package name
* Use newer expect version
* Report all example that have not been executed as pending
* Fix exampe execution in python3
* Update watchdog requirements

## Version 0.8.1

* Improved failure traceback

## Version 0.8

* Add support for --no-color option for turn off all output coloring
* Do not colorize on non-TTY
* New tests specification. This change breaks compatibility and all your existing tests
* Search in spec and specs directories by default
* Allow helper methods in describe/context context for being used in examples

## Version 0.6

* First version with changelog
* Added ProgressFormatter
* Fix RuntimeWarning when collecting specs
* Added module version
* Propagate exceptions raised in hooks to children
* Fix exception when adding a new test and sourceline can't be retrieved
