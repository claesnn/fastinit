#!/usr/bin/env python
"""
Quick test script to verify fastinit installation and functionality.
Run this after installation to ensure everything is working correctly.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and report status."""
    print(f"\n{'=' * 60}")
    print(f"Testing: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'=' * 60}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ SUCCESS")
        if result.stdout:
            print(result.stdout)
        return True
    else:
        print("❌ FAILED")
        if result.stderr:
            print("Error:", result.stderr)
        return False


def main():
    """Run verification tests."""
    print("\n" + "=" * 60)
    print("fastinit Installation Verification")
    print("=" * 60)

    tests_passed = 0
    tests_total = 0

    # Test 1: Version command
    tests_total += 1
    if run_command(["fastinit", "version"], "Version command"):
        tests_passed += 1

    # Test 2: Help command
    tests_total += 1
    if run_command(["fastinit", "--help"], "Help command"):
        tests_passed += 1

    # Test 3: Init help
    tests_total += 1
    if run_command(["fastinit", "init", "--help"], "Init command help"):
        tests_passed += 1

    # Test 4: New help
    tests_total += 1
    if run_command(["fastinit", "new", "--help"], "New command help"):
        tests_passed += 1

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Tests Passed: {tests_passed}/{tests_total}")

    if tests_passed == tests_total:
        print("\n✅ All tests passed! fastinit is ready to use.")
        print("\nTry creating your first project:")
        print("  fastinit init my-first-api")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the installation.")
        print("\nTry reinstalling:")
        print("  pip install -e .")
        return 1


if __name__ == "__main__":
    sys.exit(main())
