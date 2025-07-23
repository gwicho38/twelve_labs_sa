# Twelve Labs SA Examples

This directory contains example scripts and demonstrations using the real video assets provided in the project.

## 🎬 Real Video Assets

The project includes real video assets for testing and demonstration:

### Live-Action Videos

Location: `resources/assets/sa_interview_assets/live-action/`

- 10 professional video files (asset1.mp4 through asset10.mp4)
- Sizes range from 9.2MB to 73MB
- Content includes interviews, presentations, demonstrations, and testimonials

### Animation Videos

Location: `resources/assets/sa_interview_assets/animations/`

- 13 animation files with various styles and purposes
- Sizes range from 43KB to 1.8MB
- Content includes explainers, motion graphics, UI animations, and transitions

## 📋 Example Scripts

### `real_assets_demo.py`

A comprehensive demonstration script that shows:

- Processing single videos with both file-based and LanceDB storage
- Batch processing of animation videos
- LanceDB integration testing
- Search functionality (similarity and text-based)
- Data export and inspection

### Usage

```bash
# Run the demo script
python examples/real_assets_demo.py

# Or run individual commands
twelve-labs-sa process-all resources/assets/sa_interview_assets/live-action/asset1.mp4 --use-lancedb
twelve-labs-sa batch process-batch resources/assets/sa_interview_assets/animations/ --use-lancedb
```

## 🧪 Testing with Real Assets

### Basic Testing

```bash
# Test with a single live-action video
twelve-labs-sa process-all resources/assets/sa_interview_assets/live-action/asset1.mp4

# Test with an animation video
twelve-labs-sa process-all resources/assets/sa_interview_assets/animations/1032209408-preview.mp4
```

### LanceDB Testing

```bash
# Initialize LanceDB
twelve-labs-sa lancedb init --use-lancedb

# Process with LanceDB storage
twelve-labs-sa process-all resources/assets/sa_interview_assets/live-action/asset2.mp4 --use-lancedb

# Run all tests with LanceDB
twelve-labs-sa test all --use-lancedb
```

### Batch Processing

```bash
# Process all live-action videos
twelve-labs-sa batch process-batch resources/assets/sa_interview_assets/live-action/ --use-lancedb

# Process all animation videos
twelve-labs-sa batch process-batch resources/assets/sa_interview_assets/animations/ --use-lancedb

# Process mixed content
twelve-labs-sa batch process-batch resources/assets/sa_interview_assets/ --file-types "mp4" --recursive --use-lancedb
```

## 📊 Expected Results

When running with real assets, you should see:

1. **File Validation**: Proper metadata extraction from real video files
2. **Embedding Generation**: Real Twelve Labs API calls (if API key is set)
3. **Label Generation**: Meaningful labels based on video content
4. **Metadata Extraction**: Relevant keywords and categories
5. **Vector Storage**: Persistent storage in LanceDB or file-based system
6. **Search Results**: Functional similarity and text-based search

## 🔧 Troubleshooting

### Missing Assets

If the video assets are not found:

```bash
# Check if assets exist
ls -la resources/assets/sa_interview_assets/

# Extract from ZIP if needed
unzip resources/assets/sa_interview_assets.zip -d resources/assets/
```

### API Key Issues

If you don't have a Twelve Labs API key:

- The system will use real Twelve Labs API responses
- All functionality will still work for testing
- Real API integration requires a valid API key

### LanceDB Installation

If LanceDB is not available:

```bash
# Install with LanceDB support
pip install twelve-labs-sa[lancedb]

# Or install manually
pip install lancedb pyarrow
```

## 📈 Performance Notes

- **Live-action videos**: Larger files (9-73MB), longer processing time
- **Animation videos**: Smaller files (43KB-1.8MB), faster processing
- **LanceDB**: Better performance for similarity search with large datasets
- **File-based storage**: Good for smaller datasets and development

## 🎯 Use Cases

These real assets are perfect for:

- **Development testing**: Real file formats and sizes
- **Performance benchmarking**: Actual processing times
- **Content analysis**: Real video content for label generation
- **Search testing**: Diverse content for similarity search
- **Batch processing**: Multiple files for workflow testing
