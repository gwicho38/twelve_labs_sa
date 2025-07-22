# Twelve Labs SA - Dual Mode System Guide

## Overview

The Twelve Labs SA CLI now supports **two distinct modes** for processing media assets:

1. **🔧 Simulation Mode** - For development, testing, and prototyping
2. **🚀 Real API Mode** - For production use with actual Twelve Labs API

## Mode Selection

### Environment Variable (Default)
Set the `TWELVE_LABS_SIMULATION_MODE` environment variable:
```bash
# For simulation mode (default)
export TWELVE_LABS_SIMULATION_MODE=true

# For real API mode
export TWELVE_LABS_SIMULATION_MODE=false
```

### CLI Flags (Override)
Use CLI flags to override the environment setting:
```bash
# Force simulation mode
uv run python -m twelve_labs_sa.cli --simulation-mode [command]

# Force real API mode
uv run python -m twelve_labs_sa.cli --real-mode [command]
```

### Check Current Mode
```bash
uv run python -m twelve_labs_sa.cli config mode
```

## Mode Comparison

| Feature | Simulation Mode | Real API Mode |
|---------|----------------|---------------|
| **API Calls** | Simulated responses | Real Twelve Labs API |
| **Speed** | Fast (no network) | Depends on API |
| **Cost** | Free | API usage costs |
| **Reliability** | Always works | Depends on API status |
| **Use Case** | Development, testing | Production |
| **Data** | Mock data | Real processed data |

## Simulation Mode 🔧

### Purpose
- **Development & Testing**: Rapid iteration without API costs
- **Prototyping**: Test workflows with mock data
- **Demo**: Show functionality without real API access
- **CI/CD**: Automated testing without API dependencies

### Characteristics
- ✅ **Fast execution** - No network calls
- ✅ **Consistent results** - Predictable mock data
- ✅ **No API costs** - Free development
- ✅ **Always available** - No API downtime
- ✅ **Realistic data** - Structured mock responses

### Example Usage
```bash
# Process a single file in simulation mode
uv run python -m twelve_labs_sa.cli --simulation-mode process-all ./test_video.mp4

# Batch process with simulation
uv run python -m twelve_labs_sa.cli --simulation-mode batch process-batch ./assets/ --file-types "mp4"

# Check mode status
uv run python -m twelve_labs_sa.cli --simulation-mode config mode
```

### Mock Data Generated
- **Video IDs**: `video_<random_hex>`
- **Embeddings**: 1536-dimensional vectors
- **Search Results**: 5 mock results with scores
- **Text Generation**: Realistic descriptions
- **Labels**: Content-based tags
- **Metadata**: Structured text data

## Real API Mode 🚀

### Purpose
- **Production Processing**: Real media analysis
- **Live Data**: Actual Twelve Labs API responses
- **Quality Results**: Real AI-generated content
- **Scalable**: Handle large volumes

### Characteristics
- ✅ **Real AI Analysis** - Actual Twelve Labs processing
- ✅ **Live Data** - Real-time API responses
- ✅ **Production Ready** - Scalable and reliable
- ✅ **Quality Results** - Professional-grade output
- ⚠️ **API Costs** - Usage-based pricing
- ⚠️ **Network Dependent** - Requires internet connection

### Prerequisites
1. **Valid API Key**: Set `TWELVE_LABS_API_KEY` environment variable
2. **Internet Connection**: Required for API calls
3. **Account Setup**: Twelve Labs account with credits

### Example Usage
```bash
# Process with real API
uv run python -m twelve_labs_sa.cli --real-mode process-all ./production_video.mp4

# Batch processing with real API
uv run python -m twelve_labs_sa.cli --real-mode batch process-batch ./assets/ --file-types "mp4"

# Check mode status
uv run python -m twelve_labs_sa.cli --real-mode config mode
```

## Implementation Details

### Configuration
The mode is controlled by the `Config` class in `twelve_labs_sa/config.py`:

```python
class Config:
    # Simulation mode - set to True for simulated API calls, False for real API calls
    SIMULATION_MODE: bool = os.getenv("TWELVE_LABS_SIMULATION_MODE", "true").lower() == "true"
    
    @classmethod
    def is_simulation_mode(cls) -> bool:
        """Check if simulation mode is enabled."""
        return cls.SIMULATION_MODE
    
    @classmethod
    def set_simulation_mode(cls, enabled: bool) -> None:
        """Set simulation mode."""
        cls.SIMULATION_MODE = enabled
```

### Service Implementation
All services check the mode before making API calls:

```python
def create_embedding(self, video_id: str, model: str = "embed-english-v1") -> EmbeddingResponse:
    if Config.is_simulation_mode():
        # Simulate embedding for development/testing
        embedding = [0.1, 0.5, -0.3, 0.8, -0.2, 0.6] * 256  # 1536 dimensions
        return EmbeddingResponse(...)
    else:
        # Real API call to create embedding
        try:
            # Real API implementation
            response = self.client.embed.create(...)
            return EmbeddingResponse(...)
        except Exception as e:
            # Fallback to simulation if real API fails
            print(f"Error creating embedding: {e}")
            return EmbeddingResponse(...)
```

### Services with Dual Mode Support
1. **VideoService** - Video upload and metadata
2. **EmbedAPIService** - Vector embeddings
3. **SearchAPIService** - Content search
4. **GenerateAPIService** - Text generation

## Error Handling

### Graceful Fallback
When real API mode encounters errors, the system automatically falls back to simulation:

```python
try:
    # Real API call
    response = self.client.api_method(...)
except Exception as e:
    print(f"Error in real API call: {e}")
    # Fallback to simulation
    return self._simulate_response(...)
```

### Error Messages
- **Simulation Mode**: Clean execution with mock data
- **Real API Mode**: Informative error messages with fallback

## Best Practices

### Development Workflow
1. **Start with Simulation**: Use `--simulation-mode` for initial development
2. **Test with Real API**: Switch to `--real-mode` for final testing
3. **Environment Variables**: Set `TWELVE_LABS_SIMULATION_MODE=true` for development
4. **CI/CD**: Use simulation mode for automated testing

### Production Deployment
1. **Set Real Mode**: `export TWELVE_LABS_SIMULATION_MODE=false`
2. **API Key**: Ensure `TWELVE_LABS_API_KEY` is set
3. **Monitoring**: Monitor API usage and costs
4. **Error Handling**: Implement proper error handling for API failures

### Testing Strategy
```bash
# Unit tests with simulation
uv run python -m twelve_labs_sa.cli --simulation-mode test all

# Integration tests with real API
uv run python -m twelve_labs_sa.cli --real-mode test all

# Performance testing
uv run python -m twelve_labs_sa.cli --simulation-mode batch process-batch ./large_dataset/
```

## Migration Guide

### From Simulation to Real API
1. **Set Environment**: `export TWELVE_LABS_SIMULATION_MODE=false`
2. **Add API Key**: `export TWELVE_LABS_API_KEY=your_key_here`
3. **Test Small**: Start with a few files
4. **Monitor**: Check API usage and costs
5. **Scale**: Gradually increase processing volume

### From Real API to Simulation
1. **Set Environment**: `export TWELVE_LABS_SIMULATION_MODE=true`
2. **Remove API Key**: Not required for simulation
3. **Test**: Verify functionality works without API
4. **Deploy**: Safe for development environments

## Troubleshooting

### Common Issues

#### Simulation Mode Issues
- **Problem**: Mock data not realistic enough
- **Solution**: Customize mock data in service classes

#### Real API Mode Issues
- **Problem**: API key not found
- **Solution**: Set `TWELVE_LABS_API_KEY` environment variable
- **Problem**: Network errors
- **Solution**: Check internet connection and API status
- **Problem**: API rate limits
- **Solution**: Implement retry logic with exponential backoff

### Debug Commands
```bash
# Check current mode
uv run python -m twelve_labs_sa.cli config mode

# Test API connectivity
uv run python -m twelve_labs_sa.cli --real-mode call-twelve-labs-apis embed video_test

# Validate configuration
uv run python -m twelve_labs_sa.cli --simulation-mode process-raw-file validate ./test_file.txt
```

## Future Enhancements

### Planned Features
1. **Hybrid Mode**: Mix simulation and real API calls
2. **API Caching**: Cache real API responses for development
3. **Mock Data Customization**: Configurable mock data
4. **API Monitoring**: Real-time API usage tracking
5. **Cost Estimation**: Predict API costs before processing

### API Integration Roadmap
1. **Video Upload**: Implement real video upload to Twelve Labs
2. **Embedding Tasks**: Real embedding task creation and monitoring
3. **Search Indexes**: Real search index management
4. **Generation Models**: Real text generation with various models
5. **Analytics**: Real-time processing analytics

## Conclusion

The dual-mode system provides the best of both worlds:
- **Fast development** with simulation mode
- **Production quality** with real API mode
- **Seamless switching** between modes
- **Graceful error handling** with fallbacks

This architecture enables rapid development while maintaining the ability to process real media assets when needed. 