# Twelve Labs Single Asset Process CLI

A Python CLI tool that traces each step in the granular single asset process for Twelve Labs media processing pipeline. Built with Click and uv for dependency management, with real Twelve Labs API integration.

## Overview

This CLI simulates the complete process flow described in the granular single asset process diagram, allowing you to trace each phase and step of media asset processing through the Twelve Labs system. It integrates with the actual Twelve Labs API and supports all modalities (video, audio, text, image).

## Features

- **Real API Integration**: Uses the actual Twelve Labs SDK and API
- **Multi-Modality Support**: Supports video, audio, text, and image modalities
- **Rich UI**: Beautiful terminal output with progress bars and formatted tables
- **Modular Design**: Each phase can be run independently or together
- **Data Persistence**: Save intermediate results as JSON files
- **Error Handling**: Graceful error handling with informative messages
- **Executable**: Can be built into a standalone executable

## Installation

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install the project
git clone <repository-url>
cd twelve_labs_sa
uv sync
```

### Using pip

```bash
pip install -e .
```

### Building Wheel and Executable

The project includes a comprehensive build script that creates both a wheel and executable binary:

```bash
# Build wheel and executable using uv
./build_with_uv.py
```

This will create:
- `dist/twelve_labs_sa-0.1.0-py3-none-any.whl` - Python wheel package
- `./twelve-labs-sa` - Standalone executable binary

### Using the tl Alias

After installation, you can use the `tl` command as a shorter alias:

```bash
# Install the package
uv pip install dist/twelve_labs_sa-0.1.0-py3-none-any.whl

# Use the tl alias
tl --help
tl modalities list
tl spec compliance-demo
```

## Configuration

Set your Twelve Labs API key:

```bash
# Option 1: Environment variable
export TWELVE_LABS_API_KEY=your_api_key_here

# Option 2: .env file
echo "TWELVE_LABS_API_KEY=your_api_key_here" > .env
```

## Usage

The CLI is organized into 5 phases, each corresponding to a different stage of the granular single asset process:

### Phase 1: Raw Asset Input

```bash
# Validate a media file and extract metadata
twelve-labs-sa phase1 validate video.mp4 --output metadata.json
# or using the tl alias:
tl phase1 validate video.mp4 --output metadata.json

# Upload video to Twelve Labs
twelve-labs-sa phase1 upload video.mp4 --title "My Video" --output video_metadata.json
# or using the tl alias:
tl phase1 upload video.mp4 --title "My Video" --output video_metadata.json
```

### Phase 2: Twelve Labs API Calls

```bash
# Generate vector embedding
twelve-labs-sa phase2 embed video_id --model embed-english-v1 --output embedding.json

# Search for videos using text query
twelve-labs-sa phase2 search-text "family picnic" --output search_results.json

# Search for similar videos using video as query
twelve-labs-sa phase2 search-video video_id --output similar_videos.json

# Generate text description
twelve-labs-sa phase2 generate video_id --model generate-english-v1 --output generated_text.json
```

### Phase 3: Content Processing

```bash
# Process through Labeler system
twelve-labs-sa phase3 labeler video_id \
  --embedding-file embedding.json \
  --search-file search_results.json \
  --generate-file generated_text.json \
  --output labels.json

# Process through Metadata Generator
twelve-labs-sa phase3 metadata-gen generated_text.json --video-id video_id --output metadata.json
```

### Phase 4: Data Storage

```bash
# Store processed data in databases
twelve-labs-sa phase4 store video_id \
  --metadata-file metadata.json \
  --labels-file labels.json \
  --embedding-file embedding.json
```

### Phase 5: Search Index Creation

```bash
# Create search index entry
twelve-labs-sa phase5 create-index asset_id \
  --video-id video_id \
  --metadata-file metadata.json \
  --embedding-file embedding.json \
  --labels-file labels.json \
  --output search_index.json
```

### Complete Process

Run the entire process in one command:

```bash
# Process a single asset through all phases
twelve-labs-sa process-all video.mp4 --title "Complete Demo" --output-dir ./output
# or using the tl alias:
tl process-all video.mp4 --title "Complete Demo" --output-dir ./output
```

### Batch Processing

Process multiple files from a directory or ZIP file:

```bash
# Process all files in a directory
tl batch process-batch /path/to/files --recursive

# Process specific file types
tl batch process-batch /path/to/files --file-types "mp4,avi,mov"

# Process ZIP file
tl batch process-batch archive.zip --output-dir batch_results
```

### Vector Store Inspection

Inspect the internal vector store state:

```bash
# View all vectors in the store
tl inspect vector-store

# Export vector store data
tl inspect vector-store --output vector_store.json

# Inspect specific embedding
tl inspect embeddings --asset-id asset_001

# View all embeddings with similarity scores
tl inspect embeddings
```

### Enhanced Data Export

Export embeddings, search terms, and metadata:

```bash
# Export all data for a file
tl output export-data video.mp4 --include-embeddings --format json

# Export in different formats
tl output export-data video.mp4 --format csv
tl output export-data video.mp4 --format yaml

# Export search results with embeddings
tl output search-export "family picnic" --limit 10 --format json
```

### Modality Information

```bash
# List supported modalities and their configurations
twelve-labs-sa modalities list
```

## CLI Structure

The CLI can be invoked using either the full command name or the `tl` alias:

```bash
# Full command name
twelve-labs-sa [COMMAND] [OPTIONS]

# Short alias
tl [COMMAND] [OPTIONS]
```

```
twelve-labs-sa / tl
├── modalities - Modality-specific operations
│   └── list - List supported modalities
├── phase1 (Raw Asset Input)
│   ├── validate - Validate file and extract metadata
│   └── upload - Upload video to Twelve Labs
├── phase2 (Twelve Labs API Calls)
│   ├── embed - Generate vector embedding
│   ├── search-text - Search for videos using text query
│   ├── search-video - Search for similar videos using video as query
│   └── generate - Generate text description
├── phase3 (Content Processing)
│   ├── labeler - Process through Labeler system
│   └── metadata-gen - Process through Metadata Generator
├── phase4 (Data Storage)
│   └── store - Store processed data in databases
├── phase5 (Search Index Creation)
│   └── create-index - Create search index entry
├── batch - Batch processing operations
│   └── process-batch - Process multiple files from directory or ZIP
├── inspect - Inspect internal state and data
│   ├── vector-store - Inspect vector store contents
│   └── embeddings - Inspect embedding data and similarities
├── output - Enhanced output and data export
│   ├── export-data - Export all data for a processed file
│   └── search-export - Export search results with embeddings
├── spec - Specification compliance demonstration
│   ├── compliance-demo - Demonstrate spec compliance
│   └── process-asset - Process specific asset
└── process-all - Run complete process
```

## Supported Modalities

| Modality | File Extensions | Max Size | Models |
|----------|----------------|----------|---------|
| Video | .mp4, .avi, .mov, .mkv, .webm | 100MB | embed-english-v1, embed-multilingual-v1 |
| Audio | .mp3, .wav, .aac, .flac, .m4a | 50MB | embed-english-v1, embed-multilingual-v1 |
| Text | .txt, .md, .json | 10MB | embed-english-v1, embed-multilingual-v1 |
| Image | .jpg, .jpeg, .png, .gif, .bmp | 20MB | embed-english-v1, embed-multilingual-v1 |

## Data Flow

The CLI follows the exact data flow described in the granular single asset process:

1. **Raw Asset Input** → File validation and metadata extraction
2. **API Calls** → Parallel calls to Embed, Search, and Generate APIs
3. **Content Processing** → Labeler and Metadata Generator systems
4. **Data Storage** → Store in Asset, Vector, and Label databases
5. **Search Index Creation** → Combine all data sources for search

## API Integration

This CLI integrates with the actual Twelve Labs API:

- **Video Upload**: Upload videos to Twelve Labs platform
- **Embedding Generation**: Create vector embeddings using embed models
- **Search Operations**: Search for videos using text or video queries
- **Text Generation**: Generate descriptions using generate models
- **Task Management**: Handle async operations and task status

## Development

### Setup Development Environment

```bash
# Install development dependencies
uv sync --extra dev

# Run tests
pytest

# Format code
black twelve_labs_sa/
isort twelve_labs_sa/

# Type checking
mypy twelve_labs_sa/
```

### Project Structure

```
twelve_labs_sa/
├── __init__.py          # Package initialization
├── cli.py              # Main CLI application
├── config.py           # Configuration and API settings
├── models.py           # Pydantic data models
└── services.py         # Service classes for API integration
```

## Building Executable

The project includes a build script to create a standalone executable:

```bash
# Build executable
python build_executable.py

# Test executable
./twelve-labs-sa --help
```

## Examples

### Basic Usage

```bash
# Validate a file
./twelve-labs-sa phase1 validate my_video.mp4

# Upload and process
./twelve-labs-sa process-all my_video.mp4 --output-dir ./results
```

### Advanced Usage

```bash
# Custom models and parameters
./twelve-labs-sa phase2 embed video_123 --model embed-multilingual-v1
./twelve-labs-sa phase2 search-text "outdoor activities" --limit 20
./twelve-labs-sa phase2 generate video_123 --model generate-multilingual-v1
```

## Error Handling

The CLI includes comprehensive error handling:

- **API Key Validation**: Checks for valid API key before operations
- **File Validation**: Validates file format, size, and modality
- **API Error Handling**: Graceful handling of API failures
- **Progress Tracking**: Real-time progress updates for long operations

## License

MIT License 