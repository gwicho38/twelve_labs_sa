#!/usr/bin/env python3
"""
Example usage of the Twelve Labs Single Asset Process CLI.

This script demonstrates how to use the CLI programmatically
and shows the complete data flow through all phases.
"""

import json
import subprocess
import sys
from pathlib import Path


def run_cli_command(command):
    """Run a CLI command and return the result."""
    try:
        result = subprocess.run(
            ["uv", "run", "twelve-labs-sa"] + command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}")
        print(f"Error: {e.stderr}")
        return None


def main():
    """Demonstrate the complete CLI workflow."""
    print("🚀 Twelve Labs Single Asset Process CLI Demo")
    print("=" * 50)
    
    # Test file
    test_file = "test_video.mp4"
    
    if not Path(test_file).exists():
        print(f"❌ Test file {test_file} not found. Please create it first.")
        return
    
    print(f"\n📁 Processing file: {test_file}")
    
    # Phase 1: Raw Asset Input
    print("\n🔍 Phase 1: Raw Asset Input")
    print("-" * 30)
    result = run_cli_command(["phase1", "validate", test_file, "--output", "phase1_metadata.json"])
    if result:
        print("✅ File validation completed")
    
    # Phase 2: API Calls
    print("\n🌐 Phase 2: Twelve Labs API Calls")
    print("-" * 30)
    
    # Embed API
    print("📊 Embed API...")
    result = run_cli_command(["phase2", "embed", test_file, "--output", "phase2a_embedding.json"])
    if result:
        print("✅ Embedding generated")
    
    # Search API
    print("🔍 Search API...")
    result = run_cli_command(["phase2", "search", test_file, "--output", "phase2b_search.json"])
    if result:
        print("✅ Similar content found")
    
    # Generate API
    print("📝 Generate API...")
    result = run_cli_command(["phase2", "generate", test_file, "--output", "phase2c_generate.json"])
    if result:
        print("✅ Text description generated")
    
    # Phase 3: Content Processing
    print("\n🧠 Phase 3: Content Processing")
    print("-" * 30)
    
    # Labeler
    print("🏷️  Labeler processing...")
    result = run_cli_command([
        "phase3", "labeler", test_file,
        "--embedding-file", "phase2a_embedding.json",
        "--search-file", "phase2b_search.json",
        "--generate-file", "phase2c_generate.json",
        "--output", "phase3a_labels.json"
    ])
    if result:
        print("✅ Labels generated")
    
    # Metadata Generator
    print("📋 Metadata generation...")
    result = run_cli_command([
        "phase3", "metadata-gen", "phase2c_generate.json",
        "--output", "phase3b_metadata.json"
    ])
    if result:
        print("✅ Metadata generated")
    
    # Phase 4: Data Storage
    print("\n💾 Phase 4: Data Storage")
    print("-" * 30)
    result = run_cli_command([
        "phase4", "store", test_file,
        "--metadata-file", "phase3b_metadata.json",
        "--labels-file", "phase3a_labels.json",
        "--embedding-file", "phase2a_embedding.json"
    ])
    if result:
        print("✅ Data stored in databases")
    
    # Phase 5: Search Index Creation
    print("\n🔍 Phase 5: Search Index Creation")
    print("-" * 30)
    result = run_cli_command([
        "phase5", "create-index", "asset_demo",
        "--metadata-file", "phase3b_metadata.json",
        "--embedding-file", "phase2a_embedding.json",
        "--labels-file", "phase3a_labels.json",
        "--output", "phase5_search_index.json"
    ])
    if result:
        print("✅ Search index created")
    
    # Show generated files
    print("\n📁 Generated Files:")
    print("-" * 30)
    for file in sorted(Path(".").glob("phase*.json")):
        size = file.stat().st_size
        print(f"  {file.name} ({size} bytes)")
    
    print("\n🎉 Demo completed successfully!")
    print("\n💡 Try running individual commands:")
    print("  uv run twelve-labs-sa --help")
    print("  uv run twelve-labs-sa phase1 --help")
    print("  uv run twelve-labs-sa process-all test_video.mp4 --output-dir ./demo_output")


if __name__ == "__main__":
    main() 