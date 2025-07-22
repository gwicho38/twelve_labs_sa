#!/usr/bin/env python3
"""
Build script for creating an executable of the Twelve Labs Single Asset Process CLI.
"""

import subprocess
import sys


def main():
    """Build the executable."""
    print("🔨 Building Twelve Labs Single Asset Process CLI executable...")
    
    # Check if pyinstaller is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to install pyinstaller")
        return
    
    # Build the executable
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name=twelve-labs-sa",
        "--add-data=twelve_labs_sa:twelve_labs_sa",
        "twelve_labs_sa/cli.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Executable built successfully!")
        print("📁 Executable location: dist/twelve-labs-sa")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return
    
    # Test the executable
    print("🧪 Testing executable...")
    try:
        result = subprocess.run(["./dist/twelve-labs-sa", "--help"], 
                              capture_output=True, text=True, check=True)
        print("✅ Executable test passed!")
        print("📋 Help output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Executable test failed: {e}")
        print(f"Error output: {e.stderr}")


if __name__ == "__main__":
    main() 