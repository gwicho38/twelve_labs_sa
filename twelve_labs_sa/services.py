"""Service classes for Twelve Labs API integration."""

import json
import time
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any
import asyncio
from datetime import datetime

from twelvelabs import TwelveLabs

from .config import Config
from .models import (
    AssetRecord,
    EmbeddingResponse,
    FileMetadata,
    GenerateResponse,
    LabelRecord,
    LabelerOutput,
    MetadataOutput,
    SearchIndexEntry,
    SearchResponse,
    SearchResult,
    VideoMetadata,
    VectorRecord,
    TaskStatus,
    ModalityConfig,
)


class TwelveLabsService:
    """Main service for Twelve Labs API integration."""
    
    def __init__(self):
        """Initialize Twelve Labs client."""
        self.client = TwelveLabs(api_key=Config.get_api_key())
        self.modalities = self._setup_modalities()
    
    def _setup_modalities(self) -> Dict[str, ModalityConfig]:
        """Setup modality configurations."""
        return {
            "video": ModalityConfig(
                modality="video",
                supported_models=["embed-english-v1", "embed-multilingual-v1"],
                file_extensions=[".mp4", ".avi", ".mov", ".mkv", ".webm"],
                max_file_size=100 * 1024 * 1024,  # 100MB
                processing_options={
                    "chunk_length": 10,
                    "overlap": 2
                }
            ),
            "audio": ModalityConfig(
                modality="audio", 
                supported_models=["embed-english-v1", "embed-multilingual-v1"],
                file_extensions=[".mp3", ".wav", ".aac", ".flac", ".m4a"],
                max_file_size=50 * 1024 * 1024,  # 50MB
                processing_options={
                    "chunk_length": 10,
                    "overlap": 2
                }
            ),
            "text": ModalityConfig(
                modality="text",
                supported_models=["embed-english-v1", "embed-multilingual-v1"], 
                file_extensions=[".txt", ".md", ".json"],
                max_file_size=10 * 1024 * 1024,  # 10MB
                processing_options={}
            ),
            "image": ModalityConfig(
                modality="image",
                supported_models=["embed-english-v1", "embed-multilingual-v1"],
                file_extensions=[".jpg", ".jpeg", ".png", ".gif", ".bmp"],
                max_file_size=20 * 1024 * 1024,  # 20MB
                processing_options={}
            )
        }


class FileValidator:
    """Validates files and extracts metadata."""
    
    def __init__(self):
        self.twelve_labs = TwelveLabsService()
    
    def validate_file(self, file_path: str) -> FileMetadata:
        """Validate file and extract metadata."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine modality based on file extension
        modality = self._get_modality(path.suffix.lower())
        
        # Check file size
        size_bytes = path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        
        # Validate against modality limits
        modality_config = self.twelve_labs.modalities.get(modality)
        if modality_config and modality_config.max_file_size:
            if size_bytes > modality_config.max_file_size:
                raise ValueError(f"File too large for {modality} modality")
        
        return FileMetadata(
            name=path.name,
            size=f"{size_mb:.1f}MB",
            duration="2:30",  # Would extract from actual file
            format=path.suffix.upper().lstrip('.'),
            resolution="1920x1080" if modality == "video" else None,
            modality=modality
        )
    
    def _get_modality(self, extension: str) -> str:
        """Get modality from file extension."""
        for modality, config in self.twelve_labs.modalities.items():
            if extension in config.file_extensions:
                return modality
        return "video"  # Default


class VideoService:
    """Service for video operations."""
    
    def __init__(self):
        self.client = TwelveLabs(api_key=Config.get_api_key())
    
    def upload_video(self, file_path: str, title: Optional[str] = None) -> VideoMetadata:
        """Upload video to Twelve Labs."""
        path = Path(file_path)
        
        # For now, simulate video upload since we need to use the correct API
        # In a real implementation, this would use the actual upload API
        video_id = f"video_{uuid.uuid4().hex[:8]}"
        
        return VideoMetadata(
            video_id=video_id,
            title=title or path.name,
            description=None,
            duration=120.0,  # 2 minutes
            width=1920,
            height=1080,
            fps=30.0,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            status="ready"
        )
    
    def get_video(self, video_id: str) -> VideoMetadata:
        """Get video metadata."""
        # Simulate getting video metadata
        return VideoMetadata(
            video_id=video_id,
            title="Test Video",
            description="A test video for CLI demonstration",
            duration=120.0,
            width=1920,
            height=1080,
            fps=30.0,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            status="ready"
        )
    
    def wait_for_processing(self, video_id: str, timeout: int = 300) -> bool:
        """Wait for video processing to complete."""
        # Simulate processing wait
        time.sleep(2)
        return True


class EmbedAPIService:
    """Service for embedding operations."""
    
    def __init__(self):
        self.client = TwelveLabs(api_key=Config.get_api_key())
    
    def create_embedding(self, video_id: str, model: str = "embed-english-v1") -> EmbeddingResponse:
        """Create embedding for video."""
        # Simulate embedding creation
        # In a real implementation, this would use the actual embed API
        embedding = [0.1, 0.5, -0.3, 0.8, -0.2, 0.6] * 256  # 1536 dimensions
        
        return EmbeddingResponse(
            embedding=embedding,
            model=model,
            dimensions=len(embedding),
            video_id=video_id,
            modality="video"
        )


class SearchAPIService:
    """Service for search operations."""
    
    def __init__(self):
        self.client = TwelveLabs(api_key=Config.get_api_key())
    
    def search_videos(self, query: str, index_id: Optional[str] = None, 
                     model: str = "search-english-v1", limit: int = 10) -> SearchResponse:
        """Search for videos."""
        # Simulate search results
        search_results = [
            SearchResult(
                video_id=f"video_{i}",
                score=0.9 - (i * 0.1),
                start=0.0,
                end=10.0,
                text=f"Sample video content {i}",
                metadata={"category": "test"}
            )
            for i in range(min(limit, 5))
        ]
        
        return SearchResponse(
            results=search_results,
            total=len(search_results),
            page=1,
            limit=limit
        )
    
    def search_by_video(self, video_id: str, index_id: Optional[str] = None,
                       model: str = "search-english-v1", limit: int = 10) -> SearchResponse:
        """Search for similar videos using video as query."""
        # Simulate similar video search
        search_results = [
            SearchResult(
                video_id=f"similar_video_{i}",
                score=0.85 - (i * 0.1),
                start=0.0,
                end=10.0,
                text=f"Similar video content {i}",
                metadata={"category": "similar"}
            )
            for i in range(min(limit, 5))
        ]
        
        return SearchResponse(
            results=search_results,
            total=len(search_results),
            page=1,
            limit=limit
        )


class GenerateAPIService:
    """Service for text generation operations."""
    
    def __init__(self):
        self.client = TwelveLabs(api_key=Config.get_api_key())
    
    def generate_description(self, video_id: str, model: str = "generate-english-v1") -> GenerateResponse:
        """Generate text description of video."""
        # Simulate text generation
        description = (
            "A family enjoying a picnic in the park on a sunny afternoon. "
            "Children are playing while adults are setting up food on a blanket. "
            "The scene shows outdoor family activities with natural lighting and a relaxed atmosphere."
        )
        
        return GenerateResponse(
            text=description,
            model=model,
            video_id=video_id
        )


class LabelerService:
    """Service for label generation."""
    
    def process_asset(self, video_id: str, embedding: List[float], 
                     search_results: List[SearchResult], generated_text: str) -> LabelerOutput:
        """Process asset to generate labels."""
        # Simulate content analysis based on generated text and search results
        # In a real implementation, this would use ML models
        
        # Extract keywords from generated text
        keywords = self._extract_keywords(generated_text)
        
        # Analyze search results for patterns
        search_keywords = self._analyze_search_results(search_results)
        
        # Combine and generate labels
        all_keywords = keywords + search_keywords
        labels = self._generate_labels(all_keywords)
        
        # Generate confidence scores
        confidence = [0.95, 0.87, 0.92, 0.78][:len(labels)]
        
        # Categorize labels
        categories = self._categorize_labels(labels)
        
        return LabelerOutput(
            labels=labels,
            confidence=confidence,
            categories=categories,
            video_id=video_id
        )
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Simple keyword extraction
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        words = text.lower().split()
        keywords = [word for word in words if word not in common_words and len(word) > 3]
        return list(set(keywords))[:10]
    
    def _analyze_search_results(self, results: List[SearchResult]) -> List[str]:
        """Analyze search results for patterns."""
        keywords = []
        for result in results:
            if result.text:
                keywords.extend(self._extract_keywords(result.text))
        return list(set(keywords))[:5]
    
    def _generate_labels(self, keywords: List[str]) -> List[str]:
        """Generate labels from keywords."""
        # Map keywords to common labels
        label_mapping = {
            "family": ["family", "children", "kids", "parents"],
            "outdoor": ["outdoor", "park", "nature", "outside"],
            "food": ["food", "picnic", "eating", "meal"],
            "lifestyle": ["lifestyle", "leisure", "relaxation", "enjoyment"],
            "activity": ["activity", "playing", "fun", "entertainment"]
        }
        
        labels = []
        for keyword in keywords:
            for label, related_words in label_mapping.items():
                if keyword in related_words or any(word in keyword for word in related_words):
                    if label not in labels:
                        labels.append(label)
        
        return labels[:5]  # Limit to 5 labels
    
    def _categorize_labels(self, labels: List[str]) -> List[str]:
        """Categorize labels."""
        categories = []
        for label in labels:
            if label in ["family", "children"]:
                categories.append("family")
            elif label in ["outdoor", "park", "nature"]:
                categories.append("outdoor")
            elif label in ["food", "picnic", "eating"]:
                categories.append("food")
            elif label in ["lifestyle", "leisure"]:
                categories.append("lifestyle")
        
        return list(set(categories))


class MetadataGeneratorService:
    """Service for metadata generation."""
    
    def process_text_description(self, text_description: str, video_id: Optional[str] = None) -> MetadataOutput:
        """Process generated text to create structured metadata."""
        # Extract summary
        summary = self._extract_summary(text_description)
        
        # Extract keywords
        keywords = self._extract_keywords(text_description)
        
        # Assign categories
        categories = self._assign_categories(keywords)
        
        # Generate tags
        tags = [f"#{keyword}" for keyword in keywords[:5]]
        
        # Create search text
        search_text = " ".join(keywords + categories)
        
        return MetadataOutput(
            summary=summary,
            keywords=keywords,
            categories=categories,
            tags=tags,
            search_text=search_text,
            video_id=video_id
        )
    
    def _extract_summary(self, text: str) -> str:
        """Extract summary from text."""
        sentences = text.split('.')
        if sentences:
            return sentences[0].strip()
        return text[:100] + "..." if len(text) > 100 else text
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "being"}
        words = text.lower().split()
        keywords = [word for word in words if word not in common_words and len(word) > 3]
        return list(set(keywords))[:10]
    
    def _assign_categories(self, keywords: List[str]) -> List[str]:
        """Assign categories based on keywords."""
        categories = []
        
        if any(word in keywords for word in ["family", "children", "kids"]):
            categories.append("family")
        
        if any(word in keywords for word in ["outdoor", "park", "nature", "outside"]):
            categories.append("outdoor")
        
        if any(word in keywords for word in ["food", "picnic", "eating", "meal"]):
            categories.append("food")
        
        if any(word in keywords for word in ["lifestyle", "leisure", "relaxation"]):
            categories.append("lifestyle")
        
        return categories


class DatabaseService:
    """Simulates database storage operations."""
    
    def __init__(self):
        self.assets = {}
        self.vectors = {}
        self.labels = {}
    
    def store_asset(self, asset_record: AssetRecord) -> str:
        """Store asset record in database."""
        self.assets[asset_record.asset_id] = asset_record
        return asset_record.asset_id
    
    def store_vector(self, vector_record: VectorRecord) -> str:
        """Store vector data in vector database."""
        self.vectors[vector_record.asset_id] = vector_record
        return vector_record.asset_id
    
    def store_labels(self, label_record: LabelRecord) -> str:
        """Store label data in label database."""
        self.labels[label_record.asset_id] = label_record
        return label_record.asset_id


class SearchIndexService:
    """Service for search index creation."""
    
    def create_search_index(self, asset_id: str, metadata: MetadataOutput,
                           embedding: List[float], labels: List[str]) -> SearchIndexEntry:
        """Create search index entry combining all data sources."""
        return SearchIndexEntry(
            asset_id=asset_id,
            video_id=metadata.video_id,
            text_index=metadata.search_text,
            vector_index=embedding,
            label_index=labels,
            modality="video"
        ) 