@echo off
setlocal enabledelayedexpansion

REM --- Default Configuration ---
set "DEFAULT_TEST_PATH=Tests"
set "DEFAULT_BROWSER=chrome"
set "NO_REPORT_FLAG=false"
set "OPEN_REPORT_FLAG=false"
set "RUN_PYTEST_XDIST_PARALLEL="

REM --- Argument Parsing ---
set "TEST_PATH=%DEFAULT_TEST_PATH%"
set "BROWSER=%DEFAULT_BROWSER%"

:parse_args
IF "%~1"=="" GOTO end_parse_args

IF /I "%~1"=="-b" (
    SET "BROWSER=%~2"
    SHIFT
    SHIFT
    GOTO parse_args
)
IF /I "%~1"=="--browser" (
    SET "BROWSER=%~2"
    SHIFT
    SHIFT
    GOTO parse_args
)
IF /I "%~1"=="-p" (
    SET "RUN_PYTEST_XDIST_PARALLEL=-n %~2"
    SHIFT
    SHIFT
    GOTO parse_args
)
IF /I "%~1"=="--parallel" (
    SET "RUN_PYTEST_XDIST_PARALLEL=-n %~2"
    SHIFT
    SHIFT
    GOTO parse_args
)
IF /I "%~1"=="--no-report" (
    SET "NO_REPORT_FLAG=true"
    SHIFT
    GOTO parse_args
)
IF /I "%~1"=="-o" (
    SET "OPEN_REPORT_FLAG=true"
    SHIFT
    GOTO parse_args
)
IF /I "%~1"=="--open-report" (
    SET "OPEN_REPORT_FLAG=true"
    SHIFT
    GOTO parse_args
)
IF /I "%~1"=="-h" (
    CALL :usage
    EXIT /B 0
)
IF /I "%~1"=="--help" (
    CALL :usage
    EXIT /B 0
)

REM Assume the first non-flag argument is the test path.
REM This only captures the first such argument.
set "first_char_check=%~1"
set "first_char_check=!first_char_check:~0,1!"
IF "!first_char_check!" NEQ "-" IF "!first_char_check!" NEQ "" (
    SET "TEST_PATH=%~1"
    SHIFT
    GOTO parse_args
)

ECHO Unrecognized option or misplaced argument: %~1
SHIFT
GOTO parse_args

:end_parse_args

REM --- Basic Dependency Checks ---
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    ECHO ERROR: Python is not installed or not in PATH.
    EXIT /B 1
)
pip show pytest >nul 2>&1
IF ERRORLEVEL 1 (
    ECHO ERROR: Pytest is not installed. Please run: pip install pytest
    EXIT /B 1
)
IF "%NO_REPORT_FLAG%"=="false" (
    pip show allure-pytest >nul 2>&1
    IF ERRORLEVEL 1 (
        ECHO ERROR: allure-pytest is not installed. Please run: pip install allure-pytest
        EXIT /B 1
    )
    allure --version >nul 2>&1
    IF ERRORLEVEL 1 (
        ECHO ERROR: Allure command-line tool is not installed or not in PATH.
        EXIT /B 1
    )
)

ECHO.
ECHO ================================================================================
ECHO 🚀 Starting Windows Test Run...
ECHO ================================================================================
ECHO Test Path:          %TEST_PATH%
ECHO Browser:            %BROWSER%
IF DEFINED RUN_PYTEST_XDIST_PARALLEL (
    ECHO Pytest Workers:    %RUN_PYTEST_XDIST_PARALLEL%
)
ECHO Generate Report:    %NO_REPORT_FLAG% (false means report will be generated)
ECHO Open Report on End: %OPEN_REPORT_FLAG%
ECHO --------------------------------------------------------------------------------

set "ALLURE_RESULTS_SUBDIR=%BROWSER%"
IF DEFINED RUN_PYTEST_XDIST_PARALLEL (
    set "ALLURE_RESULTS_SUBDIR=%BROWSER%_parallel"
)
set "ALLURE_RESULTS_DIR=allure-results\%ALLURE_RESULTS_SUBDIR%"
set "ALLURE_REPORT_DIR=allure-report\%ALLURE_RESULTS_SUBDIR%"

REM Prepare allure results directory
IF EXIST "%ALLURE_RESULTS_DIR%" (
    ECHO 🗑️ Cleaning previous results from %ALLURE_RESULTS_DIR%...
    RMDIR /S /Q "%ALLURE_RESULTS_DIR%"
    IF ERRORLEVEL 1 (
        ECHO Retrying to remove directory contents one by one...
        FOR /D %%i IN ("%ALLURE_RESULTS_DIR%\*") DO RD /S /Q "%%i"
        DEL /Q "%ALLURE_RESULTS_DIR%\*.*"
    )
)
MKDIR "%ALLURE_RESULTS_DIR%"
IF ERRORLEVEL 1 (
    ECHO ERROR: Could not create directory %ALLURE_RESULTS_DIR%
    EXIT /B 1
)


REM --- Execute Pytest ---
ECHO.
ECHO 🐍 Running Pytest...
set "PYTEST_CMD_BASE=python -m pytest "%TEST_PATH%" -v --browser %BROWSER%"
set "PYTEST_CMD_ALLURE_ARG="

IF "%NO_REPORT_FLAG%"=="false" (
    SET "PYTEST_CMD_ALLURE_ARG=--alluredir="%ALLURE_RESULTS_DIR%""
)

set "FULL_PYTEST_CMD=%PYTEST_CMD_BASE% %RUN_PYTEST_XDIST_PARALLEL% %PYTEST_CMD_ALLURE_ARG%"

ECHO Executing: %FULL_PYTEST_CMD%
%FULL_PYTEST_CMD%
set pytest_exit_code=%ERRORLEVEL%

IF %pytest_exit_code% NEQ 0 (
    ECHO ❌ Pytest execution finished with failures (exit code %pytest_exit_code%).
) ELSE (
    ECHO ✅ Pytest execution completed successfully.
)
ECHO.

REM --- Generate and Open Allure Report ---
IF "%NO_REPORT_FLAG%"=="false" (
    ECHO 📊 Generating Allure Report...
    IF EXIST "%ALLURE_REPORT_DIR%" (
         RMDIR /S /Q "%ALLURE_REPORT_DIR%"
         IF ERRORLEVEL 1 (
            ECHO Retrying to remove directory contents one by one...
            FOR /D %%i IN ("%ALLURE_REPORT_DIR%\*") DO RD /S /Q "%%i"
            DEL /Q "%ALLURE_REPORT_DIR%\*.*"
        )
    )
    MKDIR "%ALLURE_REPORT_DIR%"
    IF ERRORLEVEL 1 (
        ECHO ERROR: Could not create directory %ALLURE_REPORT_DIR%
        EXIT /B 1
    )


    allure generate "%ALLURE_RESULTS_DIR%" -o "%ALLURE_REPORT_DIR%" --clean
    IF ERRORLEVEL 1 (
        ECHO ❌ Error generating Allure report.
    ) ELSE (
        ECHO ✅ Allure Report Generated Successfully!
        ECHO 📁 Report Location: %ALLURE_REPORT_DIR%
        IF "%OPEN_REPORT_FLAG%"=="true" (
            ECHO 🌐 Opening Allure Report (from %ALLURE_RESULTS_DIR%)...
            REM 'allure serve' uses the results directory, not the generated report directory
            allure serve "%ALLURE_RESULTS_DIR%"
            REM 'allure serve' is a blocking command. The script will wait here until you manually stop it (Ctrl+C).
        )
    )
) ELSE (
    ECHO ℹ️ Report generation skipped.
)

ECHO.
ECHO ================================================================================
ECHO 🎉 Windows Test Run Finished.
ECHO ================================================================================
EXIT /B %pytest_exit_code%

:usage
ECHO.
ECHO Simple Test Runner for Windows (.bat)
ECHO.
ECHO Usage: %~nx0 [TEST_PATH] [-b BROWSER] [-p NUM_WORKERS] [--no-report] [-o] [-h]
ECHO.
ECHO Arguments:
ECHO   TEST_PATH          (Optional) Path to test file or directory.
ECHO                      Default: Tests
ECHO.
ECHO Options:
ECHO   -b, --browser B    Browser: chrome, firefox, edge, safari.
ECHO                      Default: chrome
ECHO   -p, --parallel NUM Number of parallel workers for pytest-xdist (e.g., 2, 4).
ECHO   --no-report        Skip Allure report generation.
ECHO   -o, --open-report  Automatically open Allure report after generation.
ECHO   -h, --help         Show this help message.
ECHO.
ECHO Examples:
ECHO   %~nx0
ECHO   %~nx0 Tests\test_swag_login.py -b firefox -o
ECHO   %~nx0 -p 2 --no-report
ECHO.
ECHO Note: For advanced features like multi-browser parallel execution,
ECHO       iterations, detailed statistics, and trend reports, please use
ECHO       the run_tests.sh script (via Git Bash or WSL on Windows) or
ECHO       develop a more comprehensive PowerShell script.
EXIT /B 0