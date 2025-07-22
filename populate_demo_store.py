#!/usr/bin/env python3
"""
Script to populate the demo vector store with actual test assets from the resources directory.

This script processes the real video assets found in resources/assets/sa_interview_assets/
and populates the vector store with their embeddings, metadata, and labels.
"""

import json
import subprocess
import uuid
from pathlib import Path
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()


class DemoStorePopulator:
    """Populate the demo vector store with real test assets."""
    
    def __init__(self):
        self.assets_dir = Path("resources/assets/sa_interview_assets")
        self.live_action_dir = self.assets_dir / "live-action"
        self.animations_dir = self.assets_dir / "animations"
        self.output_dir = Path("demo_vector_store_data")
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
    
    def process_live_action_assets(self):
        """Process live-action video assets."""
        console.print(Panel("[bold blue]Processing Live-Action Assets[/bold blue]", title="Live-Action Assets"))
        
        live_action_files = list(self.live_action_dir.glob("*.mp4"))
        console.print(f"📁 Found {len(live_action_files)} live-action video files")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing live-action assets...", total=len(live_action_files))
            
            for i, video_file in enumerate(live_action_files, 1):
                progress.update(task, description=f"Processing {video_file.name} ({i}/{len(live_action_files)})")
                
                # Generate unique asset ID
                asset_id = f"live_action_{video_file.stem}_{uuid.uuid4().hex[:8]}"
                
                # Process the asset through the complete pipeline
                self.process_single_asset(video_file, asset_id, "live-action")
                
                progress.update(task, advance=1)
    
    def process_animation_assets(self):
        """Process animation video assets."""
        console.print(Panel("[bold blue]Processing Animation Assets[/bold blue]", title="Animation Assets"))
        
        animation_files = list(self.animations_dir.glob("*.mp4"))
        console.print(f"📁 Found {len(animation_files)} animation video files")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing animation assets...", total=len(animation_files))
            
            for i, video_file in enumerate(animation_files, 1):
                progress.update(task, description=f"Processing {video_file.name} ({i}/{len(animation_files)})")
                
                # Generate unique asset ID
                asset_id = f"animation_{video_file.stem}_{uuid.uuid4().hex[:8]}"
                
                # Process the asset through the complete pipeline
                self.process_single_asset(video_file, asset_id, "animation")
                
                progress.update(task, advance=1)
    
    def process_single_asset(self, video_file: Path, asset_id: str, asset_type: str):
        """Process a single asset through the complete pipeline."""
        try:
            # Phase 1: Validation
            console.print(f"\n[cyan]Processing {video_file.name} as {asset_id}[/cyan]")
            
            # Validate file using correct command structure
            result = self.run_cli_command([
                "process-raw-file", "validate", str(video_file),
                "--output", f"{self.output_dir}/{asset_id}_metadata.json"
            ])
            
            if not result["success"]:
                console.print(f"❌ [red]Failed to validate {video_file.name}: {result.get('error', 'Unknown error')}[/red]")
                return False
            
            # Phase 2: API Calls (simulated for demo)
            console.print(f"✅ [green]Validated {video_file.name}[/green]")
            
            # Create simulated API responses for demo purposes
            self.create_simulated_api_responses(asset_id, asset_type)
            
            # Phase 3: Content Processing
            self.process_content_phase(asset_id)
            
            # Phase 4: Data Storage
            self.store_asset_data(asset_id, video_file.name, asset_type)
            
            console.print(f"✅ [green]Successfully processed {video_file.name}[/green]")
            return True
            
        except Exception as e:
            console.print(f"❌ [red]Error processing {video_file.name}: {e}[/red]")
            return False
    
    def create_simulated_api_responses(self, asset_id: str, asset_type: str):
        """Create simulated API responses for demo purposes."""
        # Simulate embedding response
        embedding_data = {
            "embedding": [0.1, 0.5, -0.3, 0.8, -0.2, 0.6] * 256,  # 1536 dimensions
            "model": "embed-english-v1",
            "dimensions": 1536,
            "video_id": asset_id
        }
        
        # Simulate search response
        search_data = {
            "results": [
                {"video_id": f"similar_{asset_type}_1", "score": 0.85, "text": f"{asset_type} content scene"},
                {"video_id": f"similar_{asset_type}_2", "score": 0.72, "text": f"{asset_type} activities"},
                {"video_id": f"similar_{asset_type}_3", "score": 0.68, "text": f"{asset_type} presentation"}
            ],
            "total": 3,
            "page": 1,
            "limit": 3
        }
        
        # Simulate generate response
        generate_data = {
            "text": f"A {asset_type} video showing professional content with clear presentation and engaging visuals",
            "model": "generate-english-v1",
            "video_id": asset_id
        }
        
        # Save simulated data
        with open(f"{self.output_dir}/{asset_id}_embedding.json", "w") as f:
            json.dump(embedding_data, f, indent=2)
        
        with open(f"{self.output_dir}/{asset_id}_search.json", "w") as f:
            json.dump(search_data, f, indent=2)
        
        with open(f"{self.output_dir}/{asset_id}_generate.json", "w") as f:
            json.dump(generate_data, f, indent=2)
    
    def process_content_phase(self, asset_id: str):
        """Process content through labeler and metadata generator."""
        # Process through labeler using correct command structure
        labeler_result = self.run_cli_command([
            "process-content", "labeler", asset_id,
            "--embedding-file", f"{self.output_dir}/{asset_id}_embedding.json",
            "--search-file", f"{self.output_dir}/{asset_id}_search.json",
            "--generate-file", f"{self.output_dir}/{asset_id}_generate.json",
            "--output", f"{self.output_dir}/{asset_id}_labels.json"
        ])
        
        if not labeler_result["success"]:
            console.print(f"⚠️ [yellow]Labeler processing failed for {asset_id}: {labeler_result.get('error', 'Unknown error')}[/yellow]")
        else:
            console.print(f"✅ [green]Labeler processing completed for {asset_id}[/green]")
        
        # Process through metadata generator using correct command structure
        metadata_result = self.run_cli_command([
            "process-content", "metadata-gen", f"{self.output_dir}/{asset_id}_generate.json",
            "--video-id", asset_id,
            "--output", f"{self.output_dir}/{asset_id}_metadata_gen.json"
        ])
        
        if not metadata_result["success"]:
            console.print(f"⚠️ [yellow]Metadata generation failed for {asset_id}: {metadata_result.get('error', 'Unknown error')}[/yellow]")
        else:
            console.print(f"✅ [green]Metadata generation completed for {asset_id}[/green]")
    
    def store_asset_data(self, asset_id: str, file_name: str, asset_type: str):
        """Store asset data in the vector store."""
        # Store asset data using correct command structure
        store_result = self.run_cli_command([
            "store-data", "store", asset_id,
            "--metadata-file", f"{self.output_dir}/{asset_id}_metadata_gen.json",
            "--labels-file", f"{self.output_dir}/{asset_id}_labels.json",
            "--embedding-file", f"{self.output_dir}/{asset_id}_embedding.json"
        ])
        
        if not store_result["success"]:
            console.print(f"⚠️ [yellow]Data storage failed for {asset_id}: {store_result.get('error', 'Unknown error')}[/yellow]")
        else:
            console.print(f"✅ [green]Data storage completed for {asset_id}[/green]")
        
        # Create search index using correct command structure
        index_result = self.run_cli_command([
            "create-search-index", "create-index", asset_id,
            "--video-id", asset_id,
            "--metadata-file", f"{self.output_dir}/{asset_id}_metadata_gen.json",
            "--embedding-file", f"{self.output_dir}/{asset_id}_embedding.json",
            "--labels-file", f"{self.output_dir}/{asset_id}_labels.json",
            "--output", f"{self.output_dir}/{asset_id}_search_index.json"
        ])
        
        if not index_result["success"]:
            console.print(f"⚠️ [yellow]Search index creation failed for {asset_id}: {index_result.get('error', 'Unknown error')}[/yellow]")
        else:
            console.print(f"✅ [green]Search index creation completed for {asset_id}[/green]")
    
    def show_population_summary(self):
        """Show summary of populated data."""
        console.print(Panel("[bold blue]Demo Vector Store Population Summary[/bold blue]", title="Population Summary"))
        
        # Count processed files
        processed_files = list(self.output_dir.glob("*_metadata.json"))
        live_action_files = list(self.output_dir.glob("live_action_*_metadata.json"))
        animation_files = list(self.output_dir.glob("animation_*_metadata.json"))
        
        console.print(f"📊 Total assets processed: {len(processed_files)}")
        console.print(f"📊 Live-action assets: {len(live_action_files)}")
        console.print(f"📊 Animation assets: {len(animation_files)}")
        
        # Show sample assets
        if processed_files:
            console.print("\n[bold]Sample Processed Assets:[/bold]")
            table = Table()
            table.add_column("Asset ID", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Status", style="yellow")
            
            for file in processed_files[:5]:  # Show first 5
                asset_id = file.stem.replace("_metadata", "")
                asset_type = "live-action" if "live_action" in asset_id else "animation"
                table.add_row(asset_id, asset_type, "✅ Processed")
            
            console.print(table)
        
        console.print(f"\n📁 All data saved to: {self.output_dir}")
        console.print("🔍 Use 'tl inspect vector-store' to view the populated store")
    
    def run_population(self):
        """Run the complete population process."""
        console.print(Panel("[bold green]Demo Vector Store Population[/bold green]", title="Population Process"))
        
        console.print("🎯 This script will populate the demo vector store with real test assets.")
        console.print("📁 Source: resources/assets/sa_interview_assets/")
        console.print("💾 Target: Demo vector store with simulated API responses")
        
        # Process live-action assets
        self.process_live_action_assets()
        
        # Process animation assets
        self.process_animation_assets()
        
        # Show summary
        self.show_population_summary()
        
        console.print("\n✅ Demo vector store population completed!")
        console.print("\n💡 Next steps:")
        console.print("  1. Run 'tl inspect vector-store' to view populated data")
        console.print("  2. Run 'tl test eval <asset_id>' with a real asset ID")
        console.print("  3. Run 'tl lancedb stats' to see LanceDB statistics")


def main():
    """Main function to run the population process."""
    populator = DemoStorePopulator()
    populator.run_population()


if __name__ == "__main__":
    main() 