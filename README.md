# Twelve Labs Single Asset Process CLI

A comprehensive CLI tool for tracing and managing the Twelve Labs Single Asset Process, with support for both file-based storage and LanceDB vector database.

## 🚀 New Features (Based on Twelve Labs + LanceDB Guide)

### **Enhanced Twelve Labs API Integration**

- **Real Embed API Integration**: Now uses the actual Twelve Labs Embed API with task management
- **Temporal Information**: Supports video segment timing data from Twelve Labs
- **Text-to-Embedding**: Convert text queries to embeddings for similarity search
- **Progress Monitoring**: Real-time task progress tracking

### **LanceDB Vector Database Support**

- **High-Performance Vector Search**: Leverage LanceDB's optimized vector operations
- **Hybrid Search**: Combine vector similarity with metadata filtering
- **Persistent Storage**: Scalable vector database with automatic indexing
- **RAG Workflow Support**: Ready for Retrieval Augmented Generation applications

## 📦 Installation

### Basic Installation
```bash
pip install twelve-labs-sa
```

### With LanceDB Support
```bash
pip install twelve-labs-sa[lancedb]
```

### Development Installation
```bash
git clone <repository>
cd twelve-labs-sa
pip install -e .[dev,lancedb]
```

## 🔧 Configuration

Set your Twelve Labs API key:
```bash
export TWELVE_LABS_API_KEY="your_api_key_here"
```

## 🎯 Usage

### Basic Operations

```bash
# Process a single video file (using actual assets)
twelve-labs-sa process-all resources/assets/sa_interview_assets/live-action/asset1.mp4

# Validate file and extract metadata
twelve-labs-sa process-raw-file validate resources/assets/sa_interview_assets/animations/1032209408-preview.mp4

# Generate embeddings using Twelve Labs API
twelve-labs-sa call-twelve-labs-apis embed video_id

# Search for similar content
twelve-labs-sa call-twelve-labs-apis search-text "family picnic"
```

### LanceDB Vector Database Operations

```bash
# Initialize LanceDB database
twelve-labs-sa lancedb init --use-lancedb

# Perform similarity search
twelve-labs-sa lancedb similarity-search 0.1 0.5 -0.3 0.8 --k 5 --use-lancedb

# Text-based search
twelve-labs-sa lancedb text-search "family picnic" --use-lancedb

# View database statistics
twelve-labs-sa lancedb stats --use-lancedb
```

### Storage Backend Options

```bash
# Use file-based storage (default)
twelve-labs-sa inspect vector-store

# Use LanceDB backend
twelve-labs-sa inspect vector-store --use-lancedb

# Export data with LanceDB
twelve-labs-sa inspect export-store --use-lancedb
```

### Batch Processing with Real Assets

```bash
# Process all live-action videos
twelve-labs-sa batch process-batch resources/assets/sa_interview_assets/live-action/ --use-lancedb

# Process all animation videos
twelve-labs-sa batch process-batch resources/assets/sa_interview_assets/animations/ --use-lancedb

# Process specific video types
twelve-labs-sa batch process-batch resources/assets/sa_interview_assets/ --file-types "mp4" --recursive --use-lancedb
```

## 🔄 Twelve Labs API Integration

### **Real API Calls**

The CLI now uses the actual Twelve Labs APIs as documented in their [official guide](https://www.twelvelabs.io/blog/twelve-labs-and-lancedb):

```python
# Embed API with task management
task = client.embed.task.create(
    engine_name="Marengo-retrieval-2.6",
    video_url=video_url
)

# Monitor progress
task.wait_for_done(sleep_interval=2, callback=on_task_update)

# Retrieve results with temporal information
task_result = client.embed.task.retrieve(task.id)
```

### **Temporal Information Support**

Video embeddings now include temporal data:
- Start/end time offsets
- Embedding scope information
- Segment-level processing

### **Text-to-Embedding Conversion**

Convert text queries to embeddings for similarity search:
```python
# Text embedding for search
response = client.embed.create(text=query_text, model="embed-english-v1")
embedding = response.embedding
```

## 🗄️ LanceDB Integration

### **Benefits of LanceDB**

- **Serverless Vector Database**: No separate database server required
- **High Performance**: Optimized for similarity search operations
- **Hybrid Search**: Combine vector similarity with metadata filtering
- **Scalable**: Handles large-scale vector operations efficiently

### **Schema Design**

LanceDB table includes all necessary fields:
```python
schema = pa.schema([
    pa.field("asset_id", pa.string()),
    pa.field("embedding", pa.list_(pa.float32(), 1536)),  # Twelve Labs dimension
    pa.field("start_time", pa.float32()),
    pa.field("end_time", pa.float32()),
    pa.field("labels", pa.list_(pa.string())),
    pa.field("summary", pa.string()),
    pa.field("search_text", pa.string())
])
```

### **Search Operations**

```python
# Similarity search
results = table.search(query_embedding).limit(k).to_list()

# Text search with metadata filtering
filtered_results = table.search().where("start_time > 10 AND end_time < 60").limit(5).to_list()
```

## 📊 Comparison: Twelve Labs vs Our Implementation

| Feature | Twelve Labs API | Our Implementation |
|---------|----------------|-------------------|
| **Embedding Generation** | ✅ Server-side | ✅ Client-side caching |
| **Temporal Information** | ✅ Built-in | ✅ Enhanced support |
| **Vector Storage** | ❌ None | ✅ LanceDB + File-based |
| **Local Caching** | ❌ None | ✅ Persistent storage |
| **Cost Optimization** | ❌ Pay per call | ✅ Cache once, reuse |
| **Offline Access** | ❌ No | ✅ Full offline support |
| **Custom Metadata** | ❌ Limited | ✅ Full control |
| **Eval Set Management** | ❌ None | ✅ Complete solution |

## 🔍 Search Capabilities

### **Vector Similarity Search**
```bash
# Find similar videos using embeddings
twelve-labs-sa lancedb similarity-search 0.1 0.5 -0.3 0.8 --k 5
```

### **Text-Based Search**
```bash
# Search by text query
twelve-labs-sa lancedb text-search "family picnic outdoor"
```

### **Hybrid Search**
```bash
# Combine vector and metadata search
twelve-labs-sa inspect search-store "picnic" --use-lancedb
```

## 📈 Performance Benefits

### **Cost Optimization**
- **Cache embeddings**: Avoid redundant API calls
- **Batch processing**: Process multiple files efficiently
- **Persistent storage**: Reuse processed data

### **Speed Improvements**
- **Local vector search**: No API latency
- **LanceDB optimization**: High-performance similarity search
- **Parallel processing**: Process multiple assets simultaneously

## 🛠️ Development

### **Running Tests**
```bash
# Run all tests
twelve-labs-sa test all

# Test specific functionality
twelve-labs-sa test search "family picnic"
twelve-labs-sa test metadata "sample text"
```

### **Inspecting Data**
```bash
# View vector store contents
twelve-labs-sa inspect vector-store

# Export data for analysis
twelve-labs-sa inspect export-store --export-path ./export
```

## 📚 Examples

### **Complete Asset Processing**
```bash
# Process a live-action video file with LanceDB
twelve-labs-sa process-all resources/assets/sa_interview_assets/live-action/asset1.mp4 --use-lancedb

# Process an animation video file
twelve-labs-sa process-all resources/assets/sa_interview_assets/animations/1032209408-preview.mp4 --use-lancedb

# Search for similar content
twelve-labs-sa lancedb similarity-search 0.1 0.5 -0.3 0.8 --use-lancedb
```

### **Batch Processing**
```bash
# Process all live-action videos
twelve-labs-sa batch process-batch resources/assets/sa_interview_assets/live-action/ --recursive --use-lancedb

# Process all animation videos
twelve-labs-sa batch process-batch resources/assets/sa_interview_assets/animations/ --recursive --use-lancedb

# Process mixed content with specific file types
twelve-labs-sa batch process-batch resources/assets/sa_interview_assets/ --file-types "mp4" --recursive --use-lancedb
```

### **Evaluation Workflow**
```bash
# Run evaluation tests with LanceDB
twelve-labs-sa test all --use-lancedb

# Test specific functionality
twelve-labs-sa test search "family picnic" --use-lancedb
twelve-labs-sa test metadata "sample text" --use-lancedb
```

### **Real Asset Examples**

The project includes real video assets for testing:

**Live-Action Videos** (`resources/assets/sa_interview_assets/live-action/`):
- `asset1.mp4` (38MB) - Professional interview content
- `asset2.mp4` (9.2MB) - Short promotional video
- `asset3.mp4` (43MB) - Extended interview segment
- `asset4.mp4` (50MB) - Corporate presentation
- `asset5.mp4` (43MB) - Product demonstration
- `asset6.mp4` (50MB) - Team meeting recording
- `asset7.mp4` (73MB) - Conference presentation
- `asset8.mp4` (65MB) - Training session
- `asset9.mp4` (41MB) - Customer testimonial
- `asset10.mp4` (48MB) - Executive briefing

**Animation Videos** (`resources/assets/sa_interview_assets/animations/`):
- `1032209408-preview.mp4` (1006KB) - Animated explainer
- `1082783620-preview.mp4` (1.0MB) - Motion graphics
- `1086139805-preview.mp4` (94KB) - Short animation
- `1086002918-preview.mp4` (226KB) - Animated logo
- `1109250085-preview.mp4` (100KB) - Infographic animation
- `1109260987-preview.mp4` (64KB) - Icon animation
- `3524095319-preview.mp4` (52KB) - Loading animation
- `3513264207-preview.mp4` (43KB) - Transition effect
- `3423107213-preview.mp4` (132KB) - Character animation
- `3423107227-preview.mp4` (164KB) - Scene transition
- `1038251771-preview.mp4` (1.8MB) - Full animation sequence
- `3473309833-preview.mp4` (51KB) - UI animation
- `3473237415-preview.mp4` (123KB) - Background animation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Twelve Labs Team**: For the excellent API and documentation
- **LanceDB Team**: For the powerful vector database
- **Community**: For feedback and contributions

---

**Note**: This implementation enhances the Twelve Labs API with local caching and vector database capabilities, providing a complete solution for video understanding and retrieval applications.
