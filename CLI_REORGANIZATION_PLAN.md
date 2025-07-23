# CLI Reorganization Plan

## Current Structure (Scattered)
```
Commands:
  batch                  Batch processing operations.
  call-twelve-labs-apis  Phase 2: Twelve Labs API Calls - Embed, Search,...
  config                 Configuration and mode management.
  create-search-index    Phase 5: Search Index Creation - Create...
  inspect                Inspect internal state and data.
  lancedb                LanceDB vector database operations.
  modalities             Modality-specific operations.
  output                 Enhanced output and data export.
  process-all            Process a single asset through all phases of the...
  process-content        Phase 3: Content Processing - Labeler and...
  process-raw-file       Phase 1: Raw Asset Input - File validation and...
  spec                   Specification compliance demonstration.
  store-data             Phase 4: Data Storage - Store processed data in...
  test                   Convenience test commands for key functionality.
```

## Proposed Logical Structure

### 1. **Core Operations** (Most Used)
```
assets/                  # Asset management
├── validate file       # Validate and extract metadata
├── upload              # Upload to Twelve Labs
└── process             # Complete processing pipeline

api/                    # Twelve Labs API operations
├── embed               # Create embeddings
├── search-text         # Text-based search
├── search-video        # Video-based search
└── generate            # Generate text descriptions

batch/                  # Batch processing
└── process-batch       # Process multiple files
```

### 2. **Processing & Analysis**
```
processing/             # Content processing operations
├── labeler             # Generate labels from content
└── metadata-gen        # Generate metadata from text

storage/                # Data storage operations
├── store               # Store processed data
└── create-index        # Create search indexes
```

### 3. **Data Management**
```
inspect/                # Data inspection and analysis
├── vector-store        # Inspect vector store
├── export-store        # Export data
├── import-store        # Import data
├── clear-store         # Clear data
├── search-store        # Search stored data
├── list-by-modality    # List by modality
└── embeddings          # Inspect embeddings

lancedb/                # LanceDB operations
├── init                # Initialize LanceDB
├── similarity-search    # Vector similarity search
├── text-search         # Text search
└── stats               # Database statistics
```

### 4. **Output & Export**
```
output/                 # Data export operations
├── export-data         # Export processed data
└── search-export       # Export search results
```

### 5. **Configuration & Testing**
```
config/                 # Configuration management
└── mode                # Check API configuration mode

test/                   # Testing operations
├── search              # Test search functionality
├── metadata            # Test metadata generation
├── eval                # Test evaluation
├── all                 # Run all tests
└── vector-store-demo   # Vector store demo

modalities/             # Modality information
└── list                # List supported modalities
```

### 6. **Development & Demo**
```
spec/                   # Specification compliance
├── compliance-demo     # Compliance demonstration
└── process-asset       # Asset processing demo
```

## Benefits of This Structure

1. **Logical Flow**: Commands follow the natural processing pipeline
2. **Discoverability**: Related commands are grouped together
3. **Usability**: Most common operations are easily accessible
4. **Scalability**: Easy to add new commands to appropriate groups
5. **Consistency**: Clear naming conventions and hierarchy

## Implementation Strategy

1. **Phase 1**: Reorganize existing commands into new groups
2. **Phase 2**: Update command descriptions and help text
3. **Phase 3**: Add aliases for backward compatibility
4. **Phase 4**: Update documentation and examples

## Example Usage After Reorganization

```bash
# Core operations
tl assets validate file video.mp4
tl assets upload video.mp4
tl assets process video.mp4

tl api embed video_123
tl api search-text "family picnic"
tl api generate video_123

tl batch process-batch ./assets/ --file-types "mp4"

# Processing
tl processing labeler video_123
tl processing metadata-gen text.json

# Storage
tl storage store video_123
tl storage create-index asset_123

# Inspection
tl inspect vector-store
tl inspect search-store "family"

# Configuration
tl config mode
tl test all
``` 