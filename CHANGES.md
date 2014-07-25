# ChangeLog

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
