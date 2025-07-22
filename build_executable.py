#!/usr/bin/env python3
"""
Build executable using uv and shiv.
"""

import subprocess


def main():
    """Build the executable using uv and shiv."""
    print("🔨 Building Twelve Labs Single Asset Process CLI executable...")
    
    # Install shiv if not available
    try:
        subprocess.run(["uv", "pip", "install", "shiv"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to install shiv")
        return
    
    # Build the executable using shiv
    cmd = [
        "uv", "run", "shiv",
        "--console-script", "twelve-labs-sa",
        "--output-file", "twelve-labs-sa",
        "."
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Executable built successfully!")
        print("📁 Executable location: ./twelve-labs-sa")
        
        # Make it executable
        subprocess.run(["chmod", "+x", "./twelve-labs-sa"], check=True)
        print("🔧 Made executable")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return
    
    # Test the executable
    print("🧪 Testing executable...")
    try:
        result = subprocess.run(["./twelve-labs-sa", "--help"], 
                              capture_output=True, text=True, check=True)
        print("✅ Executable test passed!")
        print("📋 Help output:")
        print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Executable test failed: {e}")
        print(f"Error output: {e.stderr}")


if __name__ == "__main__":
    main() 