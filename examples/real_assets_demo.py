#!/usr/bin/env python3
"""Demo script using real video assets from the resources directory."""

import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from twelve_labs_sa.cli import main
from click.testing import CliRunner

def demo_with_real_assets():
    """Demonstrate the CLI with real video assets."""
    runner = CliRunner()
    
    print("🎬 Twelve Labs SA - Real Assets Demo")
    print("=" * 50)
    
    # Define asset paths
    live_action_dir = "resources/assets/sa_interview_assets/live-action"
    animations_dir = "resources/assets/sa_interview_assets/animations"
    
    # Check if assets exist
    if not os.path.exists(live_action_dir):
        print(f"❌ Live-action assets not found: {live_action_dir}")
        return
    
    if not os.path.exists(animations_dir):
        print(f"❌ Animation assets not found: {animations_dir}")
        return
    
    print("✅ Found real video assets!")
    
    # List available assets
    live_action_files = list(Path(live_action_dir).glob("*.mp4"))
    animation_files = list(Path(animations_dir).glob("*.mp4"))
    
    print(f"\n📹 Live-action videos: {len(live_action_files)} files")
    for file in live_action_files[:3]:  # Show first 3
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"  - {file.name} ({size_mb:.1f}MB)")
    
    print(f"\n🎨 Animation videos: {len(animation_files)} files")
    for file in animation_files[:3]:  # Show first 3
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"  - {file.name} ({size_mb:.1f}MB)")
    
    # Demo 1: Process a single live-action video
    print("\n" + "=" * 50)
    print("🎯 Demo 1: Process Single Live-Action Video")
    print("=" * 50)
    
    if live_action_files:
        test_video = str(live_action_files[0])
        print(f"Processing: {test_video}")
        
        # Test with file-based storage
        result = runner.invoke(main, ['process-all', test_video, '--output-dir', 'demo_output_file'])
        print(f"File-based processing: {'✅' if result.exit_code == 0 else '❌'}")
        
        # Test with LanceDB storage
        result = runner.invoke(main, ['process-all', test_video, '--output-dir', 'demo_output_lancedb', '--use-lancedb'])
        print(f"LanceDB processing: {'✅' if result.exit_code == 0 else '❌'}")
    
    # Demo 2: Batch process animations
    print("\n" + "=" * 50)
    print("🎯 Demo 2: Batch Process Animation Videos")
    print("=" * 50)
    
    if animation_files:
        print(f"Processing {len(animation_files)} animation files...")
        
        # Test with LanceDB
        result = runner.invoke(main, [
            'batch', 'process-batch', animations_dir,
            '--output-dir', 'demo_batch_animations',
            '--use-lancedb'
        ])
        print(f"Batch animation processing: {'✅' if result.exit_code == 0 else '❌'}")
    
    # Demo 3: Test LanceDB functionality
    print("\n" + "=" * 50)
    print("🎯 Demo 3: LanceDB Integration Tests")
    print("=" * 50)
    
    # Initialize LanceDB
    result = runner.invoke(main, ['lancedb', 'init', '--use-lancedb'])
    print(f"LanceDB init: {'✅' if result.exit_code == 0 else '❌'}")
    
    # Run all tests with LanceDB
    result = runner.invoke(main, ['test', 'all', '--use-lancedb', '--output-dir', 'demo_tests_lancedb'])
    print(f"LanceDB tests: {'✅' if result.exit_code == 0 else '❌'}")
    
    # Demo 4: Search functionality
    print("\n" + "=" * 50)
    print("🎯 Demo 4: Search Functionality")
    print("=" * 50)
    
    # Test similarity search
    test_embedding = [0.1, 0.5, -0.3, 0.8] * 384  # 1536 dimensions
    result = runner.invoke(main, [
        'lancedb', 'similarity-search',
        *[str(x) for x in test_embedding],
        '--k', '3',
        '--use-lancedb'
    ])
    print(f"Similarity search: {'✅' if result.exit_code == 0 else '❌'}")
    
    # Test text search
    result = runner.invoke(main, [
        'lancedb', 'text-search',
        'animation video',
        '--k', '3',
        '--use-lancedb'
    ])
    print(f"Text search: {'✅' if result.exit_code == 0 else '❌'}")
    
    # Demo 5: Export and inspection
    print("\n" + "=" * 50)
    print("🎯 Demo 5: Data Export and Inspection")
    print("=" * 50)
    
    # Export store data
    result = runner.invoke(main, [
        'inspect', 'export-store',
        '--export-path', 'demo_export',
        '--use-lancedb'
    ])
    print(f"Export store: {'✅' if result.exit_code == 0 else '❌'}")
    
    # Get store statistics
    result = runner.invoke(main, ['lancedb', 'stats', '--use-lancedb'])
    print(f"Store stats: {'✅' if result.exit_code == 0 else '❌'}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("📁 Check the following directories for results:")
    print("  - demo_output_file/ (file-based storage)")
    print("  - demo_output_lancedb/ (LanceDB storage)")
    print("  - demo_batch_animations/ (batch processing)")
    print("  - demo_tests_lancedb/ (test results)")
    print("  - demo_export/ (exported data)")
    print("=" * 50)

if __name__ == "__main__":
    demo_with_real_assets() 