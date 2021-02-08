#!/usr/bin/env bash

USAGE=$(cat <<-END
USAGE: $0 <command> <options>*
    init: install all development dependencies. Creates a python virtual environment
        and then installs all dependencies using setuptools.
        --nuke: completely remove the virtual env dir and env config file before initializing
    edit: launch vim with settings to use the project’s version of python
    lint: run various programs to catch programming & style errors
    test: run automated tests. By default, all tests are run once, and then the
        script exits. There are a number of options to change this default. Some
        conflict with one another (e.g., --watch and --functional). Whichever is
        declared last will take precedence.
        Unit tests are those which run completely within the process space of
        the test runner (i.e., no disk or network access).
        Functional tests are those which require no 3rd-party software be
        installed or servers set up, but which otherwise do anything else.
        Integration tests have no limits on what they may require.
        --format: (optional) either "progress" or "documentation"
        --messy: (optional) leave scratch directories behind in ./tmp
        --watch: (optional) watch all the source files and repeat the unit tests
            when things change.
        --functional: (optional) run functional tests in isolation
        --integration: (optional) run integration tests in isolation
        --unit: (optional) run unit tests in isolation
    clean: remove temporary or one-off data from the ./tmp directory
    python: start a Python REPL console which is sure to use the correct
        version of Python pre-initialized with all the correct versions of
        this package’s dependencies
    publish: publish this package as an official release on GemFury. This should
        only be performed on the master branch, and only after a change has been
        merged which updates the package version.
    refresh: refresh this build script and its related helper files. This will
        download the latest version from the boom-pylib repo and replace the
        files in your current repo.
    upgrade: upgrade any Python dependencies which have new versions available
END
)

# Helper Functions #####################################################################################################

function build-log-cleanup {
    rm -rf ./tmp
}

function build-log-init {
    rm -rf $BUILD_LOG 2>/dev/null
    mkdir -p ./tmp && touch $BUILD_LOG
}

function build-python-env {
    PYTHON_ENV="MESSY=$MESSY USER=$USER"
}

function check-python-version {
    if ! $PYTHON --version 2>&1 | grep -q $PYTHON_VERSION; then
        echo "Please update PYTHON in $ENV_FILE to refer to a Python $PYTHON_VERSION executable."
        exit 1
    fi

    return 0
}

function clean-python-packages {
    echo "Cleaning up Python directories..." | tee -a $BUILD_LOG
    $VIRTUAL_BIN/python setup.py clean >> $BUILD_LOG 2>&1 ||
        die "ERROR! Python clean up failed. Check $BUILD_LOG"
}

function die {
    printf "$*\n"
    echo
    exit 1
}

function execute-functional-tests {
    if [[ "$TEST_FUNCTIONAL" == "YES" ]]; then
        printf "\nRunning functional tests...\n"
        eval $PYTHON_ENV $VIRTUAL_BIN/mamba run src --format=$FORMAT -t functional
        return $?
    fi
    return 0
}

function execute-integration-tests {
    if [[ "$TEST_INTEGRATION" == "YES" ]]; then
        printf "\nRunning integration tests...\n"
        eval $PYTHON_ENV $VIRTUAL_BIN/mamba run src --format=$FORMAT -t integration
        return $?
    fi
    return 0
}

function execute-test-run {
    echo "Starting test run $TEST_RUN at $(date):"

    if [[ "$TEST_ALL" == "YES" ]]; then
        TEST_FUNCTIONAL="YES"
        TEST_INTEGRATION="YES"
        TEST_UNIT="YES"
    fi

    echo "unit: $TEST_UNIT, functional: $TEST_FUNCTIONAL, integration: $TEST_INTEGRATION"

    build-python-env
    execute-unit-tests && execute-functional-tests && execute-integration-tests || return 1
    return 0
}

function execute-unit-tests {
    if [[ "$TEST_UNIT" == "YES" ]]; then
        printf "\nRunning unit tests...\n"
        eval $PYTHON_ENV $VIRTUAL_BIN/mamba run src --format=$FORMAT -t unit
        return $?
    fi
    return 0
}

function init-custom {
    # do nothing; repos with custom initialization can override this function in ./config/build_cfg.sh
    return 0
}

function on-unknown-argument {
    die "Unknown argument: $1"
}

function usage {
    die "$*\nTry \"$0 help\" for details"
}

function watch-source-files {
    fswatch -o -r src -e '.*' -i '\.cpp$' -i '\.h$' -i '\.py$' -m poll_monitor
}

function write-env-file {
    echo "# The location of the build_cfg file"                                                 >> $ENV_FILE
    echo "export BUILD_CONFIG=./config/build_cfg.sh"                                            >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The location of the build log file"                                                 >> $ENV_FILE
    echo "export BUILD_LOG=./tmp/build.log"                                                     >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The default command when running the build.sh file"                                 >> $ENV_FILE
    echo "export COMMAND=help"                                                                  >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The default value for confirming admin actions"                                     >> $ENV_FILE
    echo "export CONFIRM=NO"                                                                    >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The defalt format for test output"                                                  >> $ENV_FILE
    echo "export FORMAT=progress"                                                               >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The location of a python executable (same version specified by PYTHON_VERSION)"     >> $ENV_FILE
    echo "export PYTHON=$(which python)"                                                        >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The python version for this project"                                                >> $ENV_FILE
    echo "export PYTHON_VERSION=$(tail -1 ./config/python_version)"                             >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The authentication token used for uploading to GemFury"                             >> $ENV_FILE
    echo "export GEMFURY_TOKEN=$GEMFURY_TOKEN"                                                  >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The directory where the linter should run recursively"                              >> $ENV_FILE
    echo "export LINT_INCLUDE=src"                                                              >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# Any directories which the linter should ignore"                                     >> $ENV_FILE
    echo "export LINT_EXCLUDE=--exclude=.ropeproject"                                           >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The default messy option"                                                           >> $ENV_FILE
    echo "export MESSY=NO"                                                                      >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The default nuke option"                                                            >> $ENV_FILE
    echo "export NUKE=NO"                                                                       >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The default test all option"                                                        >> $ENV_FILE
    echo "export TEST_ALL=YES"                                                                  >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The default test file location"                                                     >> $ENV_FILE
    echo "export TEST_FILE=.pylib.testing"                                                      >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The default test functional option"                                                 >> $ENV_FILE
    echo "export TEST_FUNCTIONAL=NO"                                                            >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The default test integration option"                                                >> $ENV_FILE
    echo "export TEST_INTEGRATION=NO"                                                           >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The default test run option"                                                        >> $ENV_FILE
    echo "export TEST_RUN=1"                                                                    >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The default test unit option"                                                       >> $ENV_FILE
    echo "export TEST_UNIT=NO"                                                                  >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The location of virtual env bin dir"                                                >> $ENV_FILE
    echo "export VIRTUAL_BIN=./usr/bin"                                                         >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The location of the virtual env"                                                    >> $ENV_FILE
    echo "export VIRTUAL_ENV=./usr"                                                             >> $ENV_FILE
    echo ""                                                                                     >> $ENV_FILE
    echo "# The default watch option"                                                           >> $ENV_FILE
    echo "export WATCH=NO"                                                                      >> $ENV_FILE

    write-env-file-custom
}

function write-env-file-custom {
    # do nothing; repos with custom env file variables can override this function in ./config/build_cfg.sh
    return 0
}

# Local Commands #######################################################################################################

function command-clean {
    if [[ "$CONFIRM" == "YES" ]]; then
        rm -rf ./tmp
    else
        echo "Removing ./tmp... (skipped)"
        echo ""
    fi

    [[ "$CONFIRM" == "YES" ]] || printf "This was a dry run. To actually delete files, add: --confirm\n\n"
}

function command-edit {
    source $VIRTUAL_BIN/activate
    export VIRTUAL_ENV
    $EDITOR
}

function command-help {
    echo "$USAGE" | more
    echo ""
    exit
}

function command-init {
    build-log-init

    if [[ "$AUTO_REFRESH" == "YES" ]]; then
        echo "Refreshing the build.sh script..." | tee -a $BUILD_LOG
        command-refresh-build || exit 1
    fi
    check-python-version || exit 1

    echo "Building virtual Python environment in $VIRTUAL_ENV..." | tee -a $BUILD_LOG
    [[ "$NUKE" == "YES" ]] && rm -rf $VIRTUAL_ENV && rm -rf $ENV_FILE
    $PYTHON -m venv --copies $VIRTUAL_ENV || die "Environment build failed. Check $BUILD_LOG"

    echo "Upgrading pip to the latest version..." | tee -a $BUILD_LOG
    ./usr/bin/pip install --upgrade pip >> $BUILD_LOG 2>&1 || die "Upgrade failed. Check $BUILD_LOG"

    echo "Installing Python dependencies..." | tee -a $BUILD_LOG
    unset PYTHONPATH
    export PYTHONPATH

    $VIRTUAL_BIN/pip install -e . >> build-init.log 2>&1 \
        || die "Installation failed. Check build-init.log"

    clean-python-packages

    init-custom || exit 1

    $VIRTUAL_BIN/pip freeze | grep -v '^-e' > .pip.lock

    echo "Initialization successful!" | tee -a $BUILD_LOG
    echo ""

    build-log-cleanup
}

function command-lint {
    $VIRTUAL_BIN/pycodestyle $LINT_INCLUDE $LINT_EXCLUDE
    (( RESULT = $RESULT + $? ))

    $VIRTUAL_BIN/pydocstyle $LINT_INCLUDE
    (( RESULT = $RESULT + $? ))

    $VIRTUAL_BIN/pyflakes $LINT_INCLUDE
    (( RESULT = $RESULT + $? ))

    return $RESULT
}

function command-publish {
    CURRENT_BRANCH=$(git branch | grep '^\*' | awk '{print $2}')

    if [[ "$CURRENT_BRANCH" == "master" ]]; then
        [[ "$GEMFURY_TOKEN" == "" ]] && die "Please make sure GEMFURY_TOKEN is defined in $ENV_FILE"

        $VIRTUAL_BIN/python setup.py sdist
        PACKAGE="dist/$(ls dist | head -n1)"

        PUBLISHED_VERSION=$( \
            curl -s https://$GEMFURY_TOKEN@pypi.fury.io/boomtechnology/$PACKAGE \
            | grep boom-pylib- \
            | sed "s/.*$PACKAGE-\([0-9.].*\).tar.gz.*/\1/" \
            | tail -n1
        )
        CURRENT_VERSION=$(cat setup.py | grep version= | sed 's/.*version="\(.*\)".*/\1/')

        if [[ "$PUBLISHED_VERSION" != "$CURRENT_VERSION" ]]; then
            curl -F package=@$PACKAGE https://$GEMFURY_TOKEN@push.fury.io/boomtechnology \
                || die "\nUploading package failed!"
        else
            echo "Version $CURRENT_VERSION has already been published, skipping publish..."
        fi

        rm -rf dist 2>/dev/null
    else
        echo "Not on master branch, skipping publish..."
    fi
}

function command-python {
    source $VIRTUAL_BIN/activate
    eval $PYTHON_ENV $VIRTUAL_BIN/python
}

function command-refresh-build {
    # Install the Git Hooks
    pushd .git/hooks >/dev/null
    ls ../../src/hooks | while read HOOK_FILE; do
        ln -sf "../../src/hooks/$HOOK_FILE" .
    done
    popd >/dev/null

    if cat .git/config | grep 'url =' | head -n1 | grep -q boom-pylib; then
        # We're already in the boom-pylib repo.
        return 0
    fi

    # Download the current version of boom-pylib
    TMP_REPO=".boom-pylib"
    rm -rf $TMP_REPO 2>/dev/null
    git clone -q --depth 1 git@github.com:boomtechnology/boom-python-template.git $TMP_REPO

    # Copy over the files we need, replacing existing copies
    mkdir -p src
    rm -rf src/hooks 2>/dev/null
    cp $TMP_REPO/bin/build.sh ./bin/.build.sh.new
    cp -R $TMP_REPO/src/hooks src/hooks

    # Get rid of the boom-pylib repo
    rm -rf $TMP_REPO 2>/dev/null

    (sleep 1; mv ./bin/.build.sh.new ./bin/build.sh) &
}

function command-test {
    RESULT=0

    function do-watched-run {
        rm -rf ./tmp 2>/dev/null
        execute-test-run > "$TEST_FILE.out" 2>&1
        RESULT=$?

        clear
        SCREEN_HEIGHT=$(tput lines)
        (( VISIBLE_LINES = SCREEN_HEIGHT - 15 ))
        LOG_LENGTH=$(wc -l < "$TEST_FILE.out")
        if (( $LOG_LENGTH < $VISIBLE_LINES )); then
            cat "$TEST_FILE.out"
        else
            (( HIDDEN_LINES = LOG_LENGTH - VISIBLE_LINES ))
            head -n$VISIBLE_LINES < "$TEST_FILE.out"
            printf "\n<< snipped $HIDDEN_LINES lines >>\n"
        fi

        rm "$TEST_FILE.out" 2>/dev/null
        rm "$TEST_FILE" 2>/dev/null
        printf "\nWaiting for changes...\n"
    }

    if [[ "$WATCH" == "YES" ]]; then
        clear
        echo "Starting test run..."
        do-watched-run

        rm $TEST_FILE 2> /dev/null
        watch-source-files | while read FILE; do
            if [[ ! -e $TEST_FILE ]]; then
                touch $TEST_FILE
                (( TEST_RUN = TEST_RUN + 1 ))
                printf "\nChanges detected! Re-running tests...\n"
                do-watched-run &
            fi
        done
    else
        execute-test-run
        RESULT=$?
    fi

    # Delete any tmp dirs only if --messy flag not set and all tests pass
    if [[ "$MESSY" == "NO" ]] && [[ "$RESULT" -eq "0" ]]; then
        rm -rf ./tmp 2>/dev/null
    fi

    return $RESULT
}

function command-upgrade-pip {
    build-log-init

    $VIRTUAL_BIN/pip install -e . --upgrade
    $VIRTUAL_BIN/pip freeze | grep -v '^-e' > .pip.lock

    clean-python-packages
    build-log-cleanup
}

# Process Arguments ####################################################################################################

export ENV_FILE=./config/env
export USER=$(whoami)

[[ ! -f $ENV_FILE ]] && write-env-file

source $ENV_FILE
source $BUILD_CONFIG

while [[ "$1" != "" ]]; do
    case "$1" in
        clean) COMMAND="clean";;
        edit) COMMAND="edit";;
        help|--help|-h|-?) COMMAND="help";;
        init) COMMAND="init";;
        lint) COMMAND="lint";;
        python) COMMAND="python";;
        publish) COMMAND="publish";;
        refresh) COMMAND="refresh-build";;
        test) COMMAND="test";;
        upgrade) COMMAND="upgrade-pip";;

        --confirm) CONFIRM="YES";;
        --format) shift; FORMAT="$1";;
        --functional) TEST_ALL="NO"; TEST_FUNCTIONAL="YES";;
        --integration) TEST_ALL="NO"; TEST_INTEGRATION="YES";;
        --messy) MESSY="YES";;
        --nuke) NUKE="YES";;
        --unit) TEST_ALL="NO"; TEST_UNIT="YES";;
        --watch) TEST_ALL="NO"; TEST_UNIT="YES"; WATCH="YES";;

        *) on-unknown-argument $1;;
    esac
    shift
done

# Script ###############################################################################################################

"command-$COMMAND"
