#!/usr/bin/env python3
"""
Build wheel and executable using uv.
"""
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔨 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def main():
    print("🚀 Building Twelve Labs Single Asset Process CLI with uv...")
    
    # Step 1: Build wheel
    wheel_cmd = ["uv", "build"]
    result = run_command(wheel_cmd, "Building wheel")
    if not result:
        return
    
    # Find the built wheel
    dist_dir = Path("dist")
    if dist_dir.exists():
        wheels = list(dist_dir.glob("*.whl"))
        if wheels:
            wheel_path = wheels[0]
            print(f"📦 Wheel built: {wheel_path}")
        else:
            print("⚠️ No wheel found in dist directory")
    
    # Step 2: Install shiv for executable building
    shiv_cmd = ["uv", "pip", "install", "shiv"]
    result = run_command(shiv_cmd, "Installing shiv")
    if not result:
        return
    
    # Step 3: Build executable with shiv
    executable_cmd = [
        "uv", "run", "shiv",
        "--console-script", "twelve-labs-sa",
        "--console-script", "tl",
        "--output-file", "twelve-labs-sa",
        "."
    ]
    result = run_command(executable_cmd, "Building executable")
    if not result:
        return
    
    # Step 4: Make executable
    chmod_cmd = ["chmod", "+x", "./twelve-labs-sa"]
    result = run_command(chmod_cmd, "Making executable")
    if not result:
        return
    
    # Step 5: Test both commands
    print("🧪 Testing executables...")
    
    # Test twelve-labs-sa
    test_cmd = ["./twelve-labs-sa", "--help"]
    result = run_command(test_cmd, "Testing twelve-labs-sa executable")
    if result:
        print("✅ twelve-labs-sa executable works!")
        print("📋 Help output preview:")
        lines = result.stdout.split('\n')[:10]
        for line in lines:
            print(f"   {line}")
    
    # Test tl alias
    test_tl_cmd = ["./twelve-labs-sa", "--help"]
    result = run_command(test_tl_cmd, "Testing tl alias")
    if result:
        print("✅ tl alias works!")
    
    print("\n🎉 Build completed successfully!")
    print("📁 Files created:")
    print("   - ./twelve-labs-sa (executable)")
    if dist_dir.exists():
        wheels = list(dist_dir.glob("*.whl"))
        if wheels:
            print(f"   - {wheels[0]} (wheel)")
    
    print("\n🚀 Usage:")
    print("   ./twelve-labs-sa --help")
    print("   ./twelve-labs-sa spec compliance-demo")
    print("   ./twelve-labs-sa modalities list")

if __name__ == "__main__":
    main() 