"""Persistent storage for vector store data across sessions."""

import json
import pickle
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from .models import AssetRecord, VectorRecord, LabelRecord, MetadataOutput


class PersistentStore:
    """Persistent storage for vector store data that persists across sessions."""
    
    def __init__(self, storage_dir: str = ".vector_store"):
        """Initialize persistent store with storage directory."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # Storage file paths
        self.assets_file = self.storage_dir / "assets.json"
        self.vectors_file = self.storage_dir / "vectors.pkl"
        self.labels_file = self.storage_dir / "labels.json"
        self.metadata_file = self.storage_dir / "metadata.json"
        self.index_file = self.storage_dir / "search_index.json"
        
        # Cache for loaded data
        self._assets_cache: Dict[str, AssetRecord] = {}
        self._vectors_cache: Dict[str, VectorRecord] = {}
        self._labels_cache: Dict[str, LabelRecord] = {}
        self._metadata_cache: Dict[str, MetadataOutput] = {}
        
        # Load existing data
        self._load_existing_data()
    
    def _load_existing_data(self):
        """Load existing data from storage files."""
        # Load assets
        if self.assets_file.exists():
            try:
                with open(self.assets_file, 'r') as f:
                    assets_data = json.load(f)
                    for asset_id, asset_dict in assets_data.items():
                        self._assets_cache[asset_id] = AssetRecord(**asset_dict)
            except Exception as e:
                print(f"Warning: Could not load assets: {e}")
        
        # Load vectors (using pickle for binary data)
        if self.vectors_file.exists():
            try:
                with open(self.vectors_file, 'rb') as f:
                    self._vectors_cache = pickle.load(f)
            except Exception as e:
                print(f"Warning: Could not load vectors: {e}")
        
        # Load labels
        if self.labels_file.exists():
            try:
                with open(self.labels_file, 'r') as f:
                    labels_data = json.load(f)
                    for asset_id, label_dict in labels_data.items():
                        self._labels_cache[asset_id] = LabelRecord(**label_dict)
            except Exception as e:
                print(f"Warning: Could not load labels: {e}")
        
        # Load metadata
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    metadata_data = json.load(f)
                    for asset_id, metadata_dict in metadata_data.items():
                        self._metadata_cache[asset_id] = MetadataOutput(**metadata_dict)
            except Exception as e:
                print(f"Warning: Could not load metadata: {e}")
    
    def _save_assets(self):
        """Save assets to storage."""
        assets_data = {asset_id: asset.model_dump() for asset_id, asset in self._assets_cache.items()}
        with open(self.assets_file, 'w') as f:
            json.dump(assets_data, f, indent=2)
    
    def _save_vectors(self):
        """Save vectors to storage."""
        with open(self.vectors_file, 'wb') as f:
            pickle.dump(self._vectors_cache, f)
    
    def _save_labels(self):
        """Save labels to storage."""
        labels_data = {asset_id: label.model_dump() for asset_id, label in self._labels_cache.items()}
        with open(self.labels_file, 'w') as f:
            json.dump(labels_data, f, indent=2)
    
    def _save_metadata(self):
        """Save metadata to storage."""
        metadata_data = {asset_id: metadata.model_dump() for asset_id, metadata in self._metadata_cache.items()}
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata_data, f, indent=2)
    
    def store_asset(self, asset_record: AssetRecord) -> str:
        """Store asset record persistently."""
        self._assets_cache[asset_record.asset_id] = asset_record
        self._save_assets()
        return asset_record.asset_id
    
    def store_vector(self, vector_record: VectorRecord) -> str:
        """Store vector record persistently."""
        self._vectors_cache[vector_record.asset_id] = vector_record
        self._save_vectors()
        return vector_record.asset_id
    
    def store_labels(self, label_record: LabelRecord) -> str:
        """Store label record persistently."""
        self._labels_cache[label_record.asset_id] = label_record
        self._save_labels()
        return label_record.asset_id
    
    def store_metadata(self, asset_id: str, metadata: MetadataOutput) -> str:
        """Store metadata persistently."""
        self._metadata_cache[asset_id] = metadata
        self._save_metadata()
        return asset_id
    
    def get_asset(self, asset_id: str) -> Optional[AssetRecord]:
        """Retrieve asset record from persistent storage."""
        return self._assets_cache.get(asset_id)
    
    def get_vector(self, asset_id: str) -> Optional[VectorRecord]:
        """Retrieve vector record from persistent storage."""
        return self._vectors_cache.get(asset_id)
    
    def get_labels(self, asset_id: str) -> Optional[LabelRecord]:
        """Retrieve label record from persistent storage."""
        return self._labels_cache.get(asset_id)
    
    def get_metadata(self, asset_id: str) -> Optional[MetadataOutput]:
        """Retrieve metadata from persistent storage."""
        return self._metadata_cache.get(asset_id)
    
    def get_all_assets(self) -> Dict[str, AssetRecord]:
        """Get all stored assets."""
        return self._assets_cache.copy()
    
    def get_all_vectors(self) -> Dict[str, VectorRecord]:
        """Get all stored vectors."""
        return self._vectors_cache.copy()
    
    def get_all_labels(self) -> Dict[str, LabelRecord]:
        """Get all stored labels."""
        return self._labels_cache.copy()
    
    def get_all_metadata(self) -> Dict[str, MetadataOutput]:
        """Get all stored metadata."""
        return self._metadata_cache.copy()
    
    def get_store_stats(self) -> Dict[str, Any]:
        """Get statistics about stored data."""
        return {
            "total_assets": len(self._assets_cache),
            "total_vectors": len(self._vectors_cache),
            "total_labels": len(self._labels_cache),
            "total_metadata": len(self._metadata_cache),
            "modalities": list(set(a.modality for a in self._assets_cache.values())) if self._assets_cache else [],
            "models": list(set(v.model for v in self._vectors_cache.values())) if self._vectors_cache else [],
            "storage_location": str(self.storage_dir),
            "last_updated": datetime.now().isoformat()
        }
    
    def clear_store(self):
        """Clear all stored data."""
        self._assets_cache.clear()
        self._vectors_cache.clear()
        self._labels_cache.clear()
        self._metadata_cache.clear()
        
        # Remove storage files
        for file_path in [self.assets_file, self.vectors_file, self.labels_file, self.metadata_file, self.index_file]:
            if file_path.exists():
                file_path.unlink()
    
    def export_store(self, export_path: str):
        """Export all stored data to a directory."""
        export_dir = Path(export_path)
        export_dir.mkdir(exist_ok=True)
        
        # Export assets
        assets_data = {asset_id: asset.model_dump() for asset_id, asset in self._assets_cache.items()}
        with open(export_dir / "assets.json", 'w') as f:
            json.dump(assets_data, f, indent=2)
        
        # Export vectors
        with open(export_dir / "vectors.pkl", 'wb') as f:
            pickle.dump(self._vectors_cache, f)
        
        # Export labels
        labels_data = {asset_id: label.model_dump() for asset_id, label in self._labels_cache.items()}
        with open(export_dir / "labels.json", 'w') as f:
            json.dump(labels_data, f, indent=2)
        
        # Export metadata
        metadata_data = {asset_id: metadata.model_dump() for asset_id, metadata in self._metadata_cache.items()}
        with open(export_dir / "metadata.json", 'w') as f:
            json.dump(metadata_data, f, indent=2)
        
        # Export statistics
        stats = self.get_store_stats()
        with open(export_dir / "statistics.json", 'w') as f:
            json.dump(stats, f, indent=2)
    
    def import_store(self, import_path: str):
        """Import stored data from a directory."""
        import_dir = Path(import_path)
        
        # Import assets
        assets_file = import_dir / "assets.json"
        if assets_file.exists():
            with open(assets_file, 'r') as f:
                assets_data = json.load(f)
                for asset_id, asset_dict in assets_data.items():
                    self._assets_cache[asset_id] = AssetRecord(**asset_dict)
        
        # Import vectors
        vectors_file = import_dir / "vectors.pkl"
        if vectors_file.exists():
            with open(vectors_file, 'rb') as f:
                imported_vectors = pickle.load(f)
                self._vectors_cache.update(imported_vectors)
        
        # Import labels
        labels_file = import_dir / "labels.json"
        if labels_file.exists():
            with open(labels_file, 'r') as f:
                labels_data = json.load(f)
                for asset_id, label_dict in labels_data.items():
                    self._labels_cache[asset_id] = LabelRecord(**label_dict)
        
        # Import metadata
        metadata_file = import_dir / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata_data = json.load(f)
                for asset_id, metadata_dict in metadata_data.items():
                    self._metadata_cache[asset_id] = MetadataOutput(**metadata_dict)
        
        # Save imported data
        self._save_assets()
        self._save_vectors()
        self._save_labels()
        self._save_metadata()
    
    def get_asset_by_file_hash(self, file_path: str) -> Optional[AssetRecord]:
        """Find asset by file hash (useful for detecting duplicate files)."""
        file_hash = self._get_file_hash(file_path)
        for asset in self._assets_cache.values():
            if hasattr(asset, 'file_hash') and asset.file_hash == file_hash:
                return asset
        return None
    
    def _get_file_hash(self, file_path: str) -> str:
        """Generate hash for a file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def list_assets_by_modality(self, modality: str) -> List[AssetRecord]:
        """Get all assets of a specific modality."""
        return [asset for asset in self._assets_cache.values() if asset.modality == modality]
    
    def list_assets_by_model(self, model: str) -> List[VectorRecord]:
        """Get all vectors generated with a specific model."""
        return [vector for vector in self._vectors_cache.values() if vector.model == model]
    
    def search_assets_by_keyword(self, keyword: str) -> List[AssetRecord]:
        """Search assets by keyword in metadata."""
        results = []
        for asset in self._assets_cache.values():
            if asset.metadata and keyword.lower() in asset.metadata.search_text.lower():
                results.append(asset)
        return results 