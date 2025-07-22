#!/usr/bin/env python3
"""Test script to demonstrate vector store functionality."""

from twelve_labs_sa.services import DatabaseService
from twelve_labs_sa.models import AssetRecord, VectorRecord, LabelRecord, MetadataOutput
from datetime import datetime

def test_vector_store():
    """Test vector store operations."""
    print("🧪 Testing Vector Store Functionality")
    print("=" * 50)
    
    # Create database service
    db_service = DatabaseService()
    
    # Check initial state
    print("\n📊 Initial Vector Store State:")
    stored_vectors = db_service.get_all_vectors()
    stored_assets = db_service.get_all_assets()
    stored_labels = db_service.get_all_labels()
    
    print(f"  • Assets: {len(stored_assets)}")
    print(f"  • Vectors: {len(stored_vectors)}")
    print(f"  • Labels: {len(stored_labels)}")
    
    # Store some test data
    print("\n📝 Storing Test Data...")
    
    # Create test asset
    asset_record = AssetRecord(
        asset_id="test_asset_001",
        video_id="video_123",
        file_name="test_video.mp4",
        file_size="15.2MB",
        duration="2:30",
        format="MP4",
        resolution="1920x1080",
        modality="video",
        metadata=MetadataOutput(
            summary="A family enjoying a picnic in the park",
            keywords=["family", "picnic", "park", "outdoor"],
            categories=["lifestyle", "family", "outdoor"],
            tags=["#family", "#picnic", "#outdoor"],
            search_text="family picnic park outdoor lifestyle",
            video_id="video_123"
        ),
        labels=["family", "outdoor", "picnic", "lifestyle"],
        created_at=datetime.now().isoformat(),
        status="processed"
    )
    
    # Store asset
    db_service.store_asset(asset_record)
    print("  ✅ Asset stored")
    
    # Create test vector
    vector_record = VectorRecord(
        asset_id="test_asset_001",
        video_id="video_123",
        embedding=[0.1, 0.5, -0.3, 0.8, -0.2, 0.6] * 256,  # 1536 dimensions
        model="embed-english-v1",
        dimensions=1536,
        modality="video"
    )
    
    # Store vector
    db_service.store_vector(vector_record)
    print("  ✅ Vector stored")
    
    # Create test labels
    label_record = LabelRecord(
        asset_id="test_asset_001",
        video_id="video_123",
        labels=["family", "outdoor", "picnic", "lifestyle"],
        confidence=[0.95, 0.87, 0.92, 0.78],
        categories=["lifestyle", "family", "outdoor"]
    )
    
    # Store labels
    db_service.store_labels(label_record)
    print("  ✅ Labels stored")
    
    # Check updated state
    print("\n📊 Updated Vector Store State:")
    stored_vectors = db_service.get_all_vectors()
    stored_assets = db_service.get_all_assets()
    stored_labels = db_service.get_all_labels()
    
    print(f"  • Assets: {len(stored_assets)}")
    print(f"  • Vectors: {len(stored_vectors)}")
    print(f"  • Labels: {len(stored_labels)}")
    
    # Show stored data
    print("\n📋 Stored Data Details:")
    for asset_id, asset in stored_assets.items():
        print(f"  Asset: {asset_id}")
        print(f"    File: {asset.file_name}")
        print(f"    Modality: {asset.modality}")
        
        vector = stored_vectors.get(asset_id)
        if vector:
            print(f"    Vector: {vector.dimensions} dimensions, {vector.model}")
        
        labels = stored_labels.get(asset_id)
        if labels:
            print(f"    Labels: {labels.labels}")
            print(f"    Confidence: {labels.confidence}")
    
    # Get statistics
    stats = db_service.get_store_stats()
    print("\n📊 Store Statistics:")
    print(f"  • Total assets: {stats['total_assets']}")
    print(f"  • Total vectors: {stats['total_vectors']}")
    print(f"  • Total labels: {stats['total_labels']}")
    print(f"  • Modalities: {stats['modalities']}")
    print(f"  • Models: {stats['models']}")
    
    print("\n✅ Vector store test completed successfully!")

if __name__ == "__main__":
    test_vector_store() 