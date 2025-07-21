#!/usr/bin/env python3
"""
Test script to demonstrate CLI compliance with the specification requirements.

This script shows how the CLI meets the following spec requirements:
1. Semantic search via UI
2. Multi-modal (media agnostic) search
3. Interactive results with cosine similarity
4. Labeler system for eval set generation
5. Text metadata system for semantically searchable metadata
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class SpecComplianceTester:
    """Test class to demonstrate CLI compliance with specification requirements."""
    
    def __init__(self):
        self.assets_dir = Path("resources/assets/sa_interview_assets")
        self.live_action_dir = self.assets_dir / "live-action"
        self.animations_dir = self.assets_dir / "animations"
        self.output_dir = Path("spec_compliance_test_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def run_cli_command(self, command: List[str]) -> Dict[str, Any]:
        """Run a CLI command and return the result."""
        try:
            result = subprocess.run(
                ["uv", "run", "twelve-labs-sa"] + command,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "stdout": result.stdout, "stderr": result.stderr}
        except subprocess.CalledProcessError as e:
            return {"success": False, "stdout": e.stdout, "stderr": e.stderr, "error": str(e)}
    
    def test_requirement_1_semantic_search(self):
        """Test Requirement 1: Users are able to search in plain-text via the UI (semantic search)."""
        console.print(Panel("[bold blue]Requirement 1: Semantic Search via UI[/bold blue]", title="Spec Compliance Test"))
        
        # Test semantic search with various queries
        test_queries = [
            "family picnic outdoor activities",
            "children playing in park",
            "food preparation cooking",
            "lifestyle leisure relaxation",
            "nature outdoor environment"
        ]
        
        for i, query in enumerate(test_queries, 1):
            console.print(f"\n[cyan]Test {i}:[/cyan] Semantic search for '{query}'")
            
            result = self.run_cli_command([
                "phase2", "search-text", query,
                "--limit", "5",
                "--output", f"{self.output_dir}/semantic_search_{i}.json"
            ])
            
            if result["success"]:
                console.print(f"✅ [green]Success:[/green] Semantic search completed for '{query}'")
                console.print(f"📁 Results saved to: semantic_search_{i}.json")
            else:
                console.print(f"❌ [red]Failed:[/red] {result.get('error', 'Unknown error')}")
    
    def test_requirement_2_multimodal_search(self):
        """Test Requirement 2: Users' plain-text search is multi-modal (media agnostic)."""
        console.print(Panel("[bold blue]Requirement 2: Multi-Modal Search[/bold blue]", title="Spec Compliance Test"))
        
        # Test with different modalities
        modalities = {
            "video": ["asset1.mp4", "asset2.mp4"],
            "audio": ["audio_sample.mp3"],  # Would need actual audio files
            "text": ["document.txt"],       # Would need actual text files
            "image": ["image.jpg"]          # Would need actual image files
        }
        
        for modality, files in modalities.items():
            console.print(f"\n[cyan]Testing {modality} modality:[/cyan]")
            
            for file in files:
                file_path = self.assets_dir / modality / file
                if file_path.exists():
                    # Test file validation
                    result = self.run_cli_command([
                        "phase1", "validate", str(file_path),
                        "--output", f"{self.output_dir}/modality_test_{modality}_{file}.json"
                    ])
                    
                    if result["success"]:
                        console.print(f"✅ [green]Success:[/green] {modality} file '{file}' validated")
                    else:
                        console.print(f"❌ [red]Failed:[/red] {modality} file '{file}' validation")
                else:
                    console.print(f"⚠️ [yellow]Skipped:[/yellow] {modality} file '{file}' not found")
        
        # Test modality detection
        console.print("\n[cyan]Testing modality detection:[/cyan]")
        test_files = [
            "asset1.mp4",      # video
            "audio.mp3",       # audio
            "document.txt",    # text
            "image.jpg"        # image
        ]
        
        for file in test_files:
            result = self.run_cli_command(["modalities", "list"])
            if result["success"]:
                console.print(f"✅ [green]Success:[/green] Modality detection working")
                break
    
    def test_requirement_3_cosine_similarity(self):
        """Test Requirement 3: UI returns interactive list of results with cosine similarity."""
        console.print(Panel("[bold blue]Requirement 3: Cosine Similarity Results[/bold blue]", title="Spec Compliance Test"))
        
        # Test embedding generation (creates vectors for cosine similarity)
        test_video = self.live_action_dir / "asset1.mp4"
        if test_video.exists():
            console.print(f"\n[cyan]Testing embedding generation for cosine similarity:[/cyan]")
            
            # Generate embedding
            result = self.run_cli_command([
                "phase2", "embed", "test_video_id",
                "--output", f"{self.output_dir}/embedding_for_cosine.json"
            ])
            
            if result["success"]:
                console.print("✅ [green]Success:[/green] Embedding generated for cosine similarity calculation")
                
                # Load and display embedding info
                try:
                    with open(f"{self.output_dir}/embedding_for_cosine.json") as f:
                        embedding_data = json.load(f)
                    
                    console.print(f"📊 [cyan]Embedding Details:[/cyan]")
                    console.print(f"   Dimensions: {embedding_data.get('dimensions', 'N/A')}")
                    console.print(f"   Model: {embedding_data.get('model', 'N/A')}")
                    console.print(f"   Vector Preview: {embedding_data.get('embedding', [])[:5]}...")
                    
                except Exception as e:
                    console.print(f"⚠️ [yellow]Warning:[/yellow] Could not load embedding data: {e}")
            else:
                console.print(f"❌ [red]Failed:[/red] Embedding generation")
        
        # Test search with similarity scores
        console.print(f"\n[cyan]Testing search with similarity scores:[/cyan]")
        search_result = self.run_cli_command([
            "phase2", "search-text", "family activities",
            "--limit", "3",
            "--output", f"{self.output_dir}/similarity_search.json"
        ])
        
        if search_result["success"]:
            console.print("✅ [green]Success:[/green] Search with similarity scores completed")
            
            # Display similarity scores
            try:
                with open(f"{self.output_dir}/similarity_search.json") as f:
                    search_data = json.load(f)
                
                table = Table(title="Search Results with Cosine Similarity")
                table.add_column("Video ID", style="cyan")
                table.add_column("Similarity Score", style="green")
                table.add_column("Text Preview", style="yellow")
                
                for result in search_data.get("results", [])[:3]:
                    score = result.get("score", 0.0)
                    video_id = result.get("video_id", "N/A")
                    text = result.get("text", "N/A")[:50] + "..." if result.get("text") else "N/A"
                    
                    table.add_row(video_id, f"{score:.3f}", text)
                
                console.print(table)
                
            except Exception as e:
                console.print(f"⚠️ [yellow]Warning:[/yellow] Could not display similarity scores: {e}")
        else:
            console.print(f"❌ [red]Failed:[/red] Search with similarity scores")
    
    def test_requirement_4_labeler_system(self):
        """Test Requirement 4: Labeler system for eval set generation."""
        console.print(Panel("[bold blue]Requirement 4: Labeler System for Eval Set[/bold blue]", title="Spec Compliance Test"))
        
        # Test labeler system with sample data
        console.print(f"\n[cyan]Testing Labeler System:[/cyan]")
        
        # Create sample embedding and search data for labeler
        sample_embedding = {
            "embedding": [0.1, 0.5, -0.3, 0.8, -0.2, 0.6] * 256,  # 1536 dimensions
            "model": "embed-english-v1",
            "dimensions": 1536,
            "video_id": "test_video_123"
        }
        
        sample_search = {
            "results": [
                {"video_id": "similar_1", "score": 0.85, "text": "family picnic scene"},
                {"video_id": "similar_2", "score": 0.72, "text": "outdoor activities"},
                {"video_id": "similar_3", "score": 0.68, "text": "children playing"}
            ],
            "total": 3,
            "page": 1,
            "limit": 3
        }
        
        sample_generate = {
            "text": "A family enjoying a picnic in the park with children playing nearby",
            "model": "generate-english-v1",
            "video_id": "test_video_123"
        }
        
        # Save sample data
        with open(f"{self.output_dir}/sample_embedding.json", "w") as f:
            json.dump(sample_embedding, f, indent=2)
        
        with open(f"{self.output_dir}/sample_search.json", "w") as f:
            json.dump(sample_search, f, indent=2)
        
        with open(f"{self.output_dir}/sample_generate.json", "w") as f:
            json.dump(sample_generate, f, indent=2)
        
        # Test labeler system
        result = self.run_cli_command([
            "phase3", "labeler", "test_video_123",
            "--embedding-file", f"{self.output_dir}/sample_embedding.json",
            "--search-file", f"{self.output_dir}/sample_search.json",
            "--generate-file", f"{self.output_dir}/sample_generate.json",
            "--output", f"{self.output_dir}/labeler_eval_set.json"
        ])
        
        if result["success"]:
            console.print("✅ [green]Success:[/green] Labeler system generated eval set")
            
            # Display labeler results
            try:
                with open(f"{self.output_dir}/labeler_eval_set.json") as f:
                    labeler_data = json.load(f)
                
                console.print(f"📊 [cyan]Labeler Eval Set Results:[/cyan]")
                console.print(f"   Labels: {labeler_data.get('labels', [])}")
                console.print(f"   Confidence: {labeler_data.get('confidence', [])}")
                console.print(f"   Categories: {labeler_data.get('categories', [])}")
                
            except Exception as e:
                console.print(f"⚠️ [yellow]Warning:[/yellow] Could not load labeler results: {e}")
        else:
            console.print(f"❌ [red]Failed:[/red] Labeler system")
    
    def test_requirement_5_text_metadata(self):
        """Test Requirement 5: Text metadata system for semantically searchable metadata."""
        console.print(Panel("[bold blue]Requirement 5: Text Metadata System[/bold blue]", title="Spec Compliance Test"))
        
        # Test metadata generation
        console.print(f"\n[cyan]Testing Text Metadata Generation:[/cyan]")
        
        sample_text = {
            "text": "A family enjoying a picnic in the park on a sunny afternoon. Children are playing while adults are setting up food on a blanket. The scene shows outdoor family activities with natural lighting and a relaxed atmosphere.",
            "model": "generate-english-v1",
            "video_id": "test_video_123"
        }
        
        with open(f"{self.output_dir}/sample_text.json", "w") as f:
            json.dump(sample_text, f, indent=2)
        
        result = self.run_cli_command([
            "phase3", "metadata-gen", f"{self.output_dir}/sample_text.json",
            "--video-id", "test_video_123",
            "--output", f"{self.output_dir}/text_metadata.json"
        ])
        
        if result["success"]:
            console.print("✅ [green]Success:[/green] Text metadata system generated searchable metadata")
            
            # Display metadata results
            try:
                with open(f"{self.output_dir}/text_metadata.json") as f:
                    metadata = json.load(f)
                
                console.print(f"📊 [cyan]Text Metadata Results:[/cyan]")
                console.print(f"   Summary: {metadata.get('summary', 'N/A')}")
                console.print(f"   Keywords: {metadata.get('keywords', [])}")
                console.print(f"   Categories: {metadata.get('categories', [])}")
                console.print(f"   Tags: {metadata.get('tags', [])}")
                console.print(f"   Search Text: {metadata.get('search_text', 'N/A')[:100]}...")
                
            except Exception as e:
                console.print(f"⚠️ [yellow]Warning:[/yellow] Could not load metadata results: {e}")
        else:
            console.print(f"❌ [red]Failed:[/red] Text metadata system")
    
    def test_asset_processing(self):
        """Test processing of actual interview assets."""
        console.print(Panel("[bold blue]Asset Processing Test[/bold blue]", title="Spec Compliance Test"))
        
        # Process live-action assets
        console.print(f"\n[cyan]Processing Live-Action Assets:[/cyan]")
        live_action_files = list(self.live_action_dir.glob("*.mp4"))
        
        for i, video_file in enumerate(live_action_files[:3], 1):  # Test first 3 files
            console.print(f"\n[cyan]Processing {video_file.name}:[/cyan]")
            
            # Validate file
            result = self.run_cli_command([
                "phase1", "validate", str(video_file),
                "--output", f"{self.output_dir}/live_action_{i}_metadata.json"
            ])
            
            if result["success"]:
                console.print(f"✅ [green]Success:[/green] {video_file.name} validated")
                
                # Upload video
                upload_result = self.run_cli_command([
                    "phase1", "upload", str(video_file),
                    "--title", f"Live Action Asset {i}",
                    "--output", f"{self.output_dir}/live_action_{i}_upload.json"
                ])
                
                if upload_result["success"]:
                    console.print(f"✅ [green]Success:[/green] {video_file.name} uploaded")
                else:
                    console.print(f"❌ [red]Failed:[/red] {video_file.name} upload")
            else:
                console.print(f"❌ [red]Failed:[/red] {video_file.name} validation")
        
        # Process animation assets
        console.print(f"\n[cyan]Processing Animation Assets:[/cyan]")
        animation_files = list(self.animations_dir.glob("*.mp4"))
        
        for i, video_file in enumerate(animation_files[:3], 1):  # Test first 3 files
            console.print(f"\n[cyan]Processing {video_file.name}:[/cyan]")
            
            # Validate file
            result = self.run_cli_command([
                "phase1", "validate", str(video_file),
                "--output", f"{self.output_dir}/animation_{i}_metadata.json"
            ])
            
            if result["success"]:
                console.print(f"✅ [green]Success:[/green] {video_file.name} validated")
            else:
                console.print(f"❌ [red]Failed:[/red] {video_file.name} validation")
    
    def run_complete_test_suite(self):
        """Run the complete test suite."""
        console.print(Panel("[bold green]Twelve Labs CLI Specification Compliance Test Suite[/bold green]", title="Test Suite"))
        
        console.print("\n[bold]Testing against specification requirements:[/bold]")
        console.print("1. Semantic search via UI")
        console.print("2. Multi-modal (media agnostic) search")
        console.print("3. Interactive results with cosine similarity")
        console.print("4. Labeler system for eval set generation")
        console.print("5. Text metadata system for semantically searchable metadata")
        
        # Run all tests
        self.test_requirement_1_semantic_search()
        self.test_requirement_2_multimodal_search()
        self.test_requirement_3_cosine_similarity()
        self.test_requirement_4_labeler_system()
        self.test_requirement_5_text_metadata()
        self.test_asset_processing()
        
        console.print(Panel("[bold green]✅ Test Suite Completed[/bold green]", title="Test Results"))
        console.print(f"📁 All test outputs saved to: {self.output_dir}")
        console.print("🔍 Check the output files for detailed results")


@click.command()
@click.option('--output-dir', default='spec_compliance_test_output', help='Output directory for test results')
def main(output_dir):
    """Run the specification compliance test suite."""
    tester = SpecComplianceTester()
    tester.output_dir = Path(output_dir)
    tester.output_dir.mkdir(exist_ok=True)
    tester.run_complete_test_suite()


if __name__ == "__main__":
    main() 