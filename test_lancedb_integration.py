#!/usr/bin/env python3
"""Test script for LanceDB integration with real video assets."""

import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from twelve_labs_sa.cli import main
from click.testing import CliRunner

def test_lancedb_integration():
    """Test LanceDB integration with real video assets."""
    runner = CliRunner()
    
    # Test 1: Initialize LanceDB
    print("Testing LanceDB initialization...")
    result = runner.invoke(main, ['lancedb', 'init', '--use-lancedb'])
    print(f"Init result: {result.exit_code}")
    
    # Test 2: Process a real video asset
    video_path = "resources/assets/sa_interview_assets/animations/1032209408-preview.mp4"
    if os.path.exists(video_path):
        print(f"Testing with real video: {video_path}")
        result = runner.invoke(main, ['process-all', video_path, '--use-lancedb'])
        print(f"Process result: {result.exit_code}")
    else:
        print(f"Video file not found: {video_path}")
    
    # Test 3: Run all tests with LanceDB
    print("Testing all tests with LanceDB...")
    result = runner.invoke(main, ['test', 'all', '--use-lancedb'])
    print(f"All tests result: {result.exit_code}")
    
    # Test 4: LanceDB stats
    print("Testing LanceDB stats...")
    result = runner.invoke(main, ['lancedb', 'stats', '--use-lancedb'])
    print(f"Stats result: {result.exit_code}")

if __name__ == "__main__":
    test_lancedb_integration() 