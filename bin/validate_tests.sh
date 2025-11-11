#!/bin/bash
# Quick test validation script

echo "========================================"
echo "Hockey Photo Project - Test Validation"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -d "bin/tests" ]; then
    echo "❌ Error: Please run this script from the project root"
    echo "   cd /Users/srs/src/latex-rosters && ./bin/validate_tests.sh"
    exit 1
fi

echo "1. Checking Python version..."
python3 --version

echo ""
echo "2. Checking for pytest..."
if python3 -c "import pytest" 2>/dev/null; then
    PYTEST_VERSION=$(python3 -c "import pytest; print(pytest.__version__)")
    echo "   ✓ pytest ${PYTEST_VERSION} is installed"
else
    echo "   ❌ pytest is not installed"
    echo "   Install with: pip3 install pytest"
    exit 1
fi

echo ""
echo "3. Checking for required packages..."
MISSING_PACKAGES=()

for package in pandas openpyxl xlsxwriter; do
    if python3 -c "import ${package}" 2>/dev/null; then
        echo "   ✓ ${package} is installed"
    else
        echo "   ❌ ${package} is not installed"
        MISSING_PACKAGES+=("${package}")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo ""
    echo "Install missing packages with:"
    echo "   pip3 install ${MISSING_PACKAGES[@]}"
    exit 1
fi

echo ""
echo "4. Checking syntax of test files..."
if python3 -m py_compile bin/tests/test_export_csv_from_excel.py 2>/dev/null; then
    echo "   ✓ test_export_csv_from_excel.py - syntax OK"
else
    echo "   ❌ test_export_csv_from_excel.py - syntax errors"
    exit 1
fi

if python3 -m py_compile bin/tests/test_create_latex_rosters.py 2>/dev/null; then
    echo "   ✓ test_create_latex_rosters.py - syntax OK"
else
    echo "   ❌ test_create_latex_rosters.py - syntax errors"
    exit 1
fi

echo ""
echo "5. Running test suite..."
echo "========================================" 
python3 -m pytest bin/tests/ -v --tb=short

TEST_RESULT=$?

echo ""
echo "========================================" 
echo ""
echo "Test Summary:"
python3 -m pytest bin/tests/ --collect-only -q | tail -3

echo ""
if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ All tests passed!"
    echo ""
    echo "Test Coverage:"
    echo "  • CSV Export (test_export_csv_from_excel.py): 10 tests"
    echo "  • Roster Creation (test_create_latex_rosters.py): 12 tests"
    echo "  • Player Count (test_count_players.py): 9 tests"
    echo "  • Memory Mate (test_create_mm_csv_data.py): 11 tests"
    echo "  Total: 42 comprehensive tests"
else
    echo "❌ Some tests failed (exit code: $TEST_RESULT)"
    echo ""
    echo "For more details, run:"
    echo "   pytest bin/tests/ -v --tb=long"
fi

echo ""
echo "For test documentation, see: TEST_UPDATES.md"
exit $TEST_RESULT
