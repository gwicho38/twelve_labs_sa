"""Data models for the Twelve Labs Single Asset Process."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class FileMetadata(BaseModel):
    """File metadata extracted from raw asset."""
    name: str
    size: str
    duration: Optional[str] = None
    format: str
    resolution: Optional[str] = None
    modality: str = "video"  # video, audio, text, image


class VideoMetadata(BaseModel):
    """Twelve Labs video metadata."""
    video_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    status: str = "ready"


class TemporalInfo(BaseModel):
    """Temporal information for video embeddings."""
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    scope: Optional[str] = None


class EmbeddingResponse(BaseModel):
    """Response from Embed API."""
    embedding: List[float]
    model: str = "embed-english-v1"
    dimensions: int = 1536
    video_id: Optional[str] = None
    modality: str = "video"
    temporal_info: Optional[TemporalInfo] = None


class SearchResult(BaseModel):
    """Individual search result."""
    video_id: str
    score: float
    start: Optional[float] = None
    end: Optional[float] = None
    text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    """Response from Search API."""
    results: List[SearchResult]
    total: int
    page: int
    limit: int


class GenerateResponse(BaseModel):
    """Response from Generate API."""
    text: str
    model: str = "generate-english-v1"
    video_id: Optional[str] = None


class Label(BaseModel):
    """Generated label with confidence score."""
    label: str
    confidence: float
    category: Optional[str] = None


class LabelerOutput(BaseModel):
    """Output from Labeler system."""
    labels: List[str]
    confidence: List[float]
    categories: List[str]
    video_id: Optional[str] = None


class MetadataOutput(BaseModel):
    """Output from Metadata Generator."""
    summary: str
    keywords: List[str]
    categories: List[str]
    tags: List[str]
    search_text: str
    video_id: Optional[str] = None


class AssetRecord(BaseModel):
    """Complete asset record stored in database."""
    asset_id: str
    video_id: Optional[str] = None
    file_name: str
    file_size: str
    duration: Optional[str] = None
    format: str
    resolution: Optional[str] = None
    modality: str = "video"
    metadata: MetadataOutput
    labels: List[str]
    created_at: str
    status: str = "processed"


class VectorRecord(BaseModel):
    """Vector data stored in vector database."""
    asset_id: str
    video_id: Optional[str] = None
    embedding: List[float]
    model: str
    dimensions: int
    modality: str = "video"


class LabelRecord(BaseModel):
    """Label data stored in label database."""
    asset_id: str
    video_id: Optional[str] = None
    labels: List[str]
    confidence: List[float]
    categories: List[str]


class SearchIndexEntry(BaseModel):
    """Search index entry combining all data sources."""
    asset_id: str
    video_id: Optional[str] = None
    text_index: str
    vector_index: List[float]
    label_index: List[str]
    modality: str = "video"


class TaskStatus(BaseModel):
    """Task status for async operations."""
    task_id: str
    status: str  # pending, processing, completed, failed
    progress: Optional[float] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ModalityConfig(BaseModel):
    """Configuration for different modalities."""
    modality: str
    supported_models: List[str]
    file_extensions: List[str]
    max_file_size: Optional[int] = None
    processing_options: Dict[str, Any] = Field(default_factory=dict) 