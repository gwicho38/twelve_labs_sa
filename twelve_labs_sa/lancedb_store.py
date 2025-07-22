"""LanceDB-based persistent storage for vector store data."""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    import lancedb
    import pyarrow as pa
    LANCEDB_AVAILABLE = True
except ImportError:
    LANCEDB_AVAILABLE = False
    print("Warning: LanceDB not available. Install with: pip install lancedb")

from .models import AssetRecord, VectorRecord, LabelRecord, MetadataOutput, TemporalInfo


class LanceDBStore:
    """LanceDB-based persistent storage for vector store data."""
    
    def __init__(self, storage_dir: str = ".lancedb_store"):
        """Initialize LanceDB store with storage directory."""
        if not LANCEDB_AVAILABLE:
            raise ImportError("LanceDB is required. Install with: pip install lancedb")
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # Connect to LanceDB database
        self.db = lancedb.connect(str(self.storage_dir / "video_embeddings.db"))
        
        # Define schema for video embeddings
        self.schema = pa.schema([
            pa.field("asset_id", pa.string()),
            pa.field("video_id", pa.string()),
            pa.field("embedding", pa.list_(pa.float32(), 1536)),  # Twelve Labs embedding dimension
            pa.field("model", pa.string()),
            pa.field("modality", pa.string()),
            pa.field("start_time", pa.float32()),
            pa.field("end_time", pa.float32()),
            pa.field("embedding_scope", pa.string()),
            pa.field("file_name", pa.string()),
            pa.field("file_size", pa.string()),
            pa.field("created_at", pa.string()),
            pa.field("labels", pa.list_(pa.string())),
            pa.field("confidence", pa.list_(pa.float32())),
            pa.field("categories", pa.list_(pa.string())),
            pa.field("summary", pa.string()),
            pa.field("keywords", pa.list_(pa.string())),
            pa.field("tags", pa.list_(pa.string())),
            pa.field("search_text", pa.string())
        ])
        
        # Create or connect to table
        self.table = self._get_or_create_table()
    
    def _get_or_create_table(self):
        """Get existing table or create new one."""
        try:
            return self.db.open_table("video_embeddings")
        except Exception:
            return self.db.create_table("video_embeddings", schema=self.schema, mode="overwrite")
    
    def store_asset(self, asset_record: AssetRecord) -> str:
        """Store asset record in LanceDB."""
        # Check if asset already exists
        existing = self.table.search().where(f"asset_id = '{asset_record.asset_id}'").to_list()
        if existing:
            print(f"Asset {asset_record.asset_id} already exists")
            return asset_record.asset_id
        
        # Create record for LanceDB
        record = {
            "asset_id": asset_record.asset_id,
            "video_id": asset_record.video_id or "",
            "embedding": [],  # Will be updated when vector is stored
            "model": "",
            "modality": asset_record.modality,
            "start_time": 0.0,
            "end_time": 0.0,
            "embedding_scope": "",
            "file_name": asset_record.file_name,
            "file_size": asset_record.file_size,
            "created_at": asset_record.created_at,
            "labels": [],
            "confidence": [],
            "categories": [],
            "summary": "",
            "keywords": [],
            "tags": [],
            "search_text": ""
        }
        
        self.table.add([record])
        return asset_record.asset_id
    
    def store_vector(self, vector_record: VectorRecord, temporal_info: Optional[TemporalInfo] = None) -> str:
        """Store vector data in LanceDB."""
        # Update existing record with vector data
        update_data = {
            "embedding": vector_record.embedding,
            "model": vector_record.model,
            "start_time": temporal_info.start_time if temporal_info else 0.0,
            "end_time": temporal_info.end_time if temporal_info else 0.0,
            "embedding_scope": temporal_info.scope if temporal_info else ""
        }
        
        self.table.update().where(f"asset_id = '{vector_record.asset_id}'").set(update_data).execute()
        return vector_record.asset_id
    
    def store_labels(self, label_record: LabelRecord) -> str:
        """Store label data in LanceDB."""
        update_data = {
            "labels": label_record.labels,
            "confidence": label_record.confidence,
            "categories": label_record.categories
        }
        
        self.table.update().where(f"asset_id = '{label_record.asset_id}'").set(update_data).execute()
        return label_record.asset_id
    
    def store_metadata(self, asset_id: str, metadata: MetadataOutput) -> str:
        """Store metadata in LanceDB."""
        update_data = {
            "summary": metadata.summary,
            "keywords": metadata.keywords,
            "tags": metadata.tags,
            "search_text": metadata.search_text
        }
        
        self.table.update().where(f"asset_id = '{asset_id}'").set(update_data).execute()
        return asset_id
    
    def get_asset(self, asset_id: str) -> Optional[AssetRecord]:
        """Retrieve asset record from LanceDB."""
        results = self.table.search().where(f"asset_id = '{asset_id}'").to_list()
        if not results:
            return None
        
        record = results[0]
        return AssetRecord(
            asset_id=record["asset_id"],
            video_id=record["video_id"] if record["video_id"] else None,
            file_name=record["file_name"],
            file_size=record["file_size"],
            modality=record["modality"],
            created_at=record["created_at"]
        )
    
    def get_vector(self, asset_id: str) -> Optional[VectorRecord]:
        """Retrieve vector record from LanceDB."""
        results = self.table.search().where(f"asset_id = '{asset_id}'").to_list()
        if not results:
            return None
        
        record = results[0]
        return VectorRecord(
            asset_id=record["asset_id"],
            video_id=record["video_id"] if record["video_id"] else None,
            embedding=record["embedding"],
            model=record["model"],
            dimensions=len(record["embedding"]),
            modality=record["modality"]
        )
    
    def get_labels(self, asset_id: str) -> Optional[LabelRecord]:
        """Retrieve label record from LanceDB."""
        results = self.table.search().where(f"asset_id = '{asset_id}'").to_list()
        if not results:
            return None
        
        record = results[0]
        return LabelRecord(
            asset_id=record["asset_id"],
            video_id=record["video_id"] if record["video_id"] else None,
            labels=record["labels"],
            confidence=record["confidence"],
            categories=record["categories"]
        )
    
    def get_metadata(self, asset_id: str) -> Optional[MetadataOutput]:
        """Retrieve metadata from LanceDB."""
        results = self.table.search().where(f"asset_id = '{asset_id}'").to_list()
        if not results:
            return None
        
        record = results[0]
        return MetadataOutput(
            summary=record["summary"],
            keywords=record["keywords"],
            categories=record["categories"],
            tags=record["tags"],
            search_text=record["search_text"],
            video_id=record["video_id"] if record["video_id"] else None
        )
    
    def similarity_search(self, query_embedding: List[float], k: int = 5) -> List[Dict[str, Any]]:
        """Perform similarity search using LanceDB."""
        results = self.table.search(query_embedding).limit(k).to_list()
        return results
    
    def text_search(self, query_text: str, k: int = 5) -> List[Dict[str, Any]]:
        """Perform text-based search using LanceDB."""
        # This would require text-to-embedding conversion
        # For now, search in search_text field
        results = self.table.search().where(f"search_text LIKE '%{query_text}%'").limit(k).to_list()
        return results
    
    def get_all_assets(self) -> List[AssetRecord]:
        """Get all stored assets."""
        results = self.table.search().to_list()
        assets = []
        for record in results:
            assets.append(AssetRecord(
                asset_id=record["asset_id"],
                video_id=record["video_id"] if record["video_id"] else None,
                file_name=record["file_name"],
                file_size=record["file_size"],
                modality=record["modality"],
                created_at=record["created_at"]
            ))
        return assets
    
    def get_store_stats(self) -> Dict[str, Any]:
        """Get statistics about stored data."""
        total_records = len(self.table.search().to_list())
        
        # Get unique modalities
        modalities = set()
        models = set()
        for record in self.table.search().to_list():
            modalities.add(record["modality"])
            if record["model"]:
                models.add(record["model"])
        
        return {
            "total_assets": total_records,
            "modalities": list(modalities),
            "models": list(models),
            "storage_location": str(self.storage_dir),
            "last_updated": datetime.now().isoformat()
        }
    
    def clear_store(self):
        """Clear all stored data."""
        self.table.delete().execute()
    
    def export_store(self, export_path: str):
        """Export all stored data to JSON."""
        export_dir = Path(export_path)
        export_dir.mkdir(exist_ok=True)
        
        # Export all data as JSON
        results = self.table.search().to_list()
        with open(export_dir / "lancedb_export.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        # Export statistics
        stats = self.get_store_stats()
        with open(export_dir / "statistics.json", 'w') as f:
            json.dump(stats, f, indent=2)
    
    def list_assets_by_modality(self, modality: str) -> List[AssetRecord]:
        """Get all assets of a specific modality."""
        results = self.table.search().where(f"modality = '{modality}'").to_list()
        assets = []
        for record in results:
            assets.append(AssetRecord(
                asset_id=record["asset_id"],
                video_id=record["video_id"] if record["video_id"] else None,
                file_name=record["file_name"],
                file_size=record["file_size"],
                modality=record["modality"],
                created_at=record["created_at"]
            ))
        return assets
    
    def list_assets_by_model(self, model: str) -> List[VectorRecord]:
        """Get all vectors generated with a specific model."""
        results = self.table.search().where(f"model = '{model}'").to_list()
        vectors = []
        for record in results:
            vectors.append(VectorRecord(
                asset_id=record["asset_id"],
                video_id=record["video_id"] if record["video_id"] else None,
                embedding=record["embedding"],
                model=record["model"],
                dimensions=len(record["embedding"]),
                modality=record["modality"]
            ))
        return vectors
    
    def get_all_vectors(self) -> List[VectorRecord]:
        """Get all stored vectors."""
        results = self.table.search().to_list()
        vectors = []
        for record in results:
            if record["embedding"]:  # Only include records with embeddings
                vectors.append(VectorRecord(
                    asset_id=record["asset_id"],
                    video_id=record["video_id"] if record["video_id"] else None,
                    embedding=record["embedding"],
                    model=record["model"],
                    dimensions=len(record["embedding"]),
                    modality=record["modality"]
                ))
        return vectors
    
    def get_all_labels(self) -> List[LabelRecord]:
        """Get all stored labels."""
        results = self.table.search().to_list()
        labels = []
        for record in results:
            if record["labels"]:  # Only include records with labels
                labels.append(LabelRecord(
                    asset_id=record["asset_id"],
                    video_id=record["video_id"] if record["video_id"] else None,
                    labels=record["labels"],
                    confidence=record["confidence"],
                    categories=record["categories"]
                ))
        return labels
    
    def get_all_metadata(self) -> List[MetadataOutput]:
        """Get all stored metadata."""
        results = self.table.search().to_list()
        metadata = []
        for record in results:
            if record["summary"]:  # Only include records with metadata
                metadata.append(MetadataOutput(
                    summary=record["summary"],
                    keywords=record["keywords"],
                    categories=record["categories"],
                    tags=record["tags"],
                    search_text=record["search_text"],
                    video_id=record["video_id"] if record["video_id"] else None
                ))
        return metadata
    
    def import_store(self, import_path: str):
        """Import stored data from a directory."""
        import_dir = Path(import_path)
        
        # Import from JSON export
        export_file = import_dir / "lancedb_export.json"
        if export_file.exists():
            with open(export_file, 'r') as f:
                data = json.load(f)
            
            # Clear existing data and import new data
            self.clear_store()
            for record in data:
                self.table.add([record])
    
    def search_assets_by_keyword(self, keyword: str) -> List[AssetRecord]:
        """Search assets by keyword in metadata."""
        results = self.table.search().where(f"search_text LIKE '%{keyword}%' OR summary LIKE '%{keyword}%'").to_list()
        assets = []
        for record in results:
            assets.append(AssetRecord(
                asset_id=record["asset_id"],
                video_id=record["video_id"] if record["video_id"] else None,
                file_name=record["file_name"],
                file_size=record["file_size"],
                modality=record["modality"],
                created_at=record["created_at"]
            ))
        return assets 