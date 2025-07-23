# Twelve Labs Asset Processing & Search System Design

## System Architecture Overview

```mermaid
graph TB
    %% External Inputs
    subgraph "Input Assets"
        A[Video Files<br/>/resources/assets/] --> B[File Validator]
        C[Audio Files] --> B
        D[Text Files] --> B
        E[Image Files] --> B
    end

    %% Core Processing Pipeline
    subgraph "Asset Processing Pipeline"
        B --> F[Video Service]
        F --> G[Twelve Labs API]
        G --> H[Embed API Service]
        G --> I[Search API Service]
        G --> J[Generate API Service]
    end

    %% Labeling & Metadata Generation
    subgraph "Labeling & Metadata System"
        H --> K[Labeler Service]
        I --> K
        J --> K
        K --> L[Metadata Generator]
        L --> M[Semantic Text Metadata]
    end

    %% Storage Layer
    subgraph "Storage Layer"
        N[LanceDB Vector Store]
        O[File-based Storage]
        P[Search Index Service]
    end

    %% Search & Retrieval
    subgraph "Hybrid Multimodal Search"
        Q[Text Search]
        R[Vector Similarity Search]
        S[Label-based Search]
        T[Metadata Filtering]
        U[Hybrid Search Engine]
    end

    %% Connections
    M --> N
    M --> O
    K --> P
    N --> U
    O --> U
    P --> U
    Q --> U
    R --> U
    S --> U
    T --> U

    %% CLI Interface
    subgraph "CLI Interface"
        V[assets/*]
        W[api/*]
        X[processing/*]
        Y[storage/*]
        Z[inspect/*]
        AA[test/*]
    end

    %% CLI to System Connections
    V --> F
    W --> G
    X --> K
    Y --> N
    Z --> U
    AA --> U

    %% Styling
    classDef inputStyle fill:#e1f5fe
    classDef processStyle fill:#f3e5f5
    classDef storageStyle fill:#e8f5e8
    classDef searchStyle fill:#fff3e0
    classDef cliStyle fill:#fce4ec

    class A,C,D,E inputStyle
    class B,F,G,H,I,J,K,L,M processStyle
    class N,O,P storageStyle
    class Q,R,S,T,U searchStyle
    class V,W,X,Y,Z,AA cliStyle
```

## Detailed Component Architecture

```mermaid
graph LR
    %% Asset Input & Validation
    subgraph "Asset Input Layer"
        A1[Video Files<br/>MP4, AVI, MOV]
        A2[Audio Files<br/>MP3, WAV, AAC]
        A3[Text Files<br/>TXT, MD, JSON]
        A4[Image Files<br/>JPG, PNG, GIF]
    end

    %% File Processing
    subgraph "File Processing"
        B1[File Validator]
        B2[Modality Detection]
        B3[Size Validation]
        B4[Format Validation]
    end

    %% Twelve Labs API Integration
    subgraph "Twelve Labs API Layer"
        C1[Video Upload]
        C2[Embed API<br/>embed-english-v1]
        C3[Search API<br/>search-english-v1]
        C4[Generate API<br/>generate-english-v1]
    end

    %% Data Processing
    subgraph "Data Processing"
        D1[Embedding Generation]
        D2[Search Results]
        D3[Text Generation]
        D4[Temporal Information]
    end

    %% Labeling System
    subgraph "Labeling & Annotation"
        E1[Labeler Service]
        E2[Keyword Extraction]
        E3[Category Assignment]
        E4[Confidence Scoring]
    end

    %% Metadata Generation
    subgraph "Semantic Metadata"
        F1[Metadata Generator]
        F2[Summary Extraction]
        F3[Keyword Analysis]
        F4[Tag Generation]
        F5[Search Text Creation]
    end

    %% Storage Systems
    subgraph "Storage Layer"
        G1[LanceDB Vector Store]
        G2[File-based Storage]
        G3[Search Index]
        G4[Asset Records]
    end

    %% Search & Retrieval
    subgraph "Hybrid Search Engine"
        H1[Text Search]
        H2[Vector Similarity]
        H3[Label Matching]
        H4[Metadata Filtering]
        H5[Hybrid Ranker]
    end

    %% CLI Commands
    subgraph "CLI Interface"
        I1[assets/validate]
        I2[assets/upload]
        I3[assets/process]
        I4[api/embed]
        I5[api/search]
        I6[api/generate]
        I7[processing/labeler]
        I8[processing/metadata_gen]
        I9[storage/store]
        I10[storage/create_index]
        I11[inspect/vector_store]
        I12[inspect/search_store]
    end

    %% Flow Connections
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> C1
    C1 --> C2
    C1 --> C3
    C1 --> C4
    C2 --> D1
    C3 --> D2
    C4 --> D3
    D1 --> E1
    D2 --> E1
    D3 --> E1
    E1 --> F1
    F1 --> G1
    F1 --> G2
    E1 --> G3
    G1 --> H2
    G2 --> H1
    G3 --> H3
    F1 --> H4
    H1 --> H5
    H2 --> H5
    H3 --> H5
    H4 --> H5

    %% CLI Connections
    I1 --> B1
    I2 --> C1
    I3 --> C1
    I4 --> C2
    I5 --> C3
    I6 --> C4
    I7 --> E1
    I8 --> F1
    I9 --> G1
    I10 --> G3
    I11 --> G1
    I12 --> H5

    %% Styling
    classDef inputStyle fill:#e1f5fe,stroke:#01579b
    classDef processStyle fill:#f3e5f5,stroke:#4a148c
    classDef apiStyle fill:#fff3e0,stroke:#e65100
    classDef storageStyle fill:#e8f5e8,stroke:#1b5e20
    classDef searchStyle fill:#fce4ec,stroke:#880e4f
    classDef cliStyle fill:#f1f8e9,stroke:#33691e

    class A1,A2,A3,A4 inputStyle
    class B1,B2,B3,B4,D1,D2,D3,D4 processStyle
    class C1,C2,C3,C4 apiStyle
    class E1,E2,E3,E4,F1,F2,F3,F4,F5 processStyle
    class G1,G2,G3,G4 storageStyle
    class H1,H2,H3,H4,H5 searchStyle
    class I1,I2,I3,I4,I5,I6,I7,I8,I9,I10,I11,I12 cliStyle
```

## Data Flow for Asset Labeling

```mermaid
sequenceDiagram
    participant CLI as CLI Interface
    participant FV as File Validator
    participant VS as Video Service
    participant TL as Twelve Labs API
    participant ES as Embed Service
    participant SS as Search Service
    participant GS as Generate Service
    participant LS as Labeler Service
    participant MG as Metadata Generator
    participant DB as Database Service
    participant VS as Vector Store

    CLI->>FV: assets validate file.mp4
    FV->>FV: Check file format & size
    FV-->>CLI: File metadata

    CLI->>VS: assets upload file.mp4
    VS->>TL: Upload video
    TL-->>VS: Video ID
    VS-->>CLI: Video metadata

    CLI->>ES: api embed video_id
    ES->>TL: Create embedding
    TL-->>ES: Embedding vector
    ES-->>CLI: Embedding response

    CLI->>SS: api search "query"
    SS->>TL: Search videos
    TL-->>SS: Search results
    SS-->>CLI: Search response

    CLI->>GS: api generate video_id
    GS->>TL: Generate text
    TL-->>GS: Generated text
    GS-->>CLI: Generate response

    CLI->>LS: processing labeler video_id
    LS->>LS: Process embedding
    LS->>LS: Analyze search results
    LS->>LS: Extract keywords
    LS->>LS: Generate labels
    LS-->>CLI: Labeler output

    CLI->>MG: processing metadata_gen text
    MG->>MG: Extract summary
    MG->>MG: Generate keywords
    MG->>MG: Assign categories
    MG->>MG: Create search text
    MG-->>CLI: Metadata output

    CLI->>DB: storage store video_id
    DB->>VS: Store asset record
    DB->>VS: Store vector data
    DB->>VS: Store labels
    DB->>VS: Store metadata
    DB-->>CLI: Storage confirmation
```

## Hybrid Multimodal Search Architecture

```mermaid
graph TB
    %% Query Input
    subgraph "Query Input"
        Q1[Text Query]
        Q2[Video Query]
        Q3[Audio Query]
        Q4[Image Query]
    end

    %% Query Processing
    subgraph "Query Processing"
        P1[Query Parser]
        P2[Modality Detection]
        P3[Embedding Generation]
        P4[Query Expansion]
    end

    %% Search Engines
    subgraph "Search Engines"
        S1[Text Search Engine]
        S2[Vector Similarity Engine]
        S3[Label Matching Engine]
        S4[Metadata Filter Engine]
    end

    %% Storage Layer
    subgraph "Storage Layer"
        D1[LanceDB Vectors]
        D2[Text Index]
        D3[Label Index]
        D4[Metadata Index]
    end

    %% Ranking & Fusion
    subgraph "Ranking & Fusion"
        R1[Score Normalization]
        R2[Multi-modal Fusion]
        R3[Re-ranking]
        R4[Result Aggregation]
    end

    %% Output
    subgraph "Search Results"
        O1[Ranked Results]
        O2[Confidence Scores]
        O3[Modality Information]
        O4[Temporal Segments]
    end

    %% Flow
    Q1 --> P1
    Q2 --> P1
    Q3 --> P1
    Q4 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> S2
    P1 --> S1
    P1 --> S3
    P1 --> S4

    S1 --> D2
    S2 --> D1
    S3 --> D3
    S4 --> D4

    S1 --> R1
    S2 --> R1
    S3 --> R1
    S4 --> R1

    R1 --> R2
    R2 --> R3
    R3 --> R4
    R4 --> O1
    R4 --> O2
    R4 --> O3
    R4 --> O4

    %% Styling
    classDef queryStyle fill:#e3f2fd
    classDef processStyle fill:#f3e5f5
    classDef searchStyle fill:#fff3e0
    classDef storageStyle fill:#e8f5e8
    classDef rankingStyle fill:#fce4ec
    classDef outputStyle fill:#f1f8e9

    class Q1,Q2,Q3,Q4 queryStyle
    class P1,P2,P3,P4 processStyle
    class S1,S2,S3,S4 searchStyle
    class D1,D2,D3,D4 storageStyle
    class R1,R2,R3,R4 rankingStyle
    class O1,O2,O3,O4 outputStyle
```

## CLI Command Structure

```mermaid
graph TD
    subgraph "Main CLI Commands"
        M1[twelve-labs-sa]
        M2[--version]
        M3[--help]
    end

    subgraph "Asset Management"
        A1[assets list]
        A2[assets validate file]
        A3[assets upload file]
        A4[assets process file]
    end

    subgraph "API Operations"
        API1[api embed video_id]
        API2[api search-text query]
        API3[api search-video video_id]
        API4[api generate video_id]
    end

    subgraph "Processing Pipeline"
        P1[processing labeler video_id]
        P2[processing metadata_gen text]
    end

    subgraph "Storage Operations"
        S1[storage store video_id]
        S2[storage create_index asset_id]
    end

    subgraph "Inspection & Debugging"
        I1[inspect vector_store]
        I2[inspect export_store]
        I3[inspect import_store]
        I4[inspect clear_store]
        I5[inspect search_store keyword]
        I6[inspect list_by_modality]
        I7[inspect embeddings]
    end

    subgraph "Output & Export"
        O1[output export_data file]
        O2[output search_export query]
    end

    subgraph "Testing & Validation"
        T1[test search query]
        T2[test metadata text]
        T3[test eval asset_id]
        T4[test all]
        T5[test vector_store_demo]
    end

    subgraph "LanceDB Operations"
        L1[lancedb init]
        L2[lancedb similarity_search]
        L3[lancedb text_search]
        L4[lancedb stats]
    end

    subgraph "Batch Processing"
        B1[batch process_batch path]
    end

    subgraph "Specification Compliance"
        SP1[spec compliance_demo]
        SP2[spec process_asset]
    end

    %% Connections
    M1 --> A1
    M1 --> API1
    M1 --> P1
    M1 --> S1
    M1 --> I1
    M1 --> O1
    M1 --> T1
    M1 --> L1
    M1 --> B1
    M1 --> SP1

    %% Styling
    classDef mainStyle fill:#e1f5fe
    classDef assetStyle fill:#f3e5f5
    classDef apiStyle fill:#fff3e0
    classDef processStyle fill:#e8f5e8
    classDef storageStyle fill:#fce4ec
    classDef inspectStyle fill:#f1f8e9
    classDef outputStyle fill:#fff8e1
    classDef testStyle fill:#e0f2f1
    classDef lancedbStyle fill:#fafafa
    classDef batchStyle fill:#f5f5f5
    classDef specStyle fill:#fafafa

    class M1,M2,M3 mainStyle
    class A1,A2,A3,A4 assetStyle
    class API1,API2,API3,API4 apiStyle
    class P1,P2 processStyle
    class S1,S2 storageStyle
    class I1,I2,I3,I4,I5,I6,I7 inspectStyle
    class O1,O2 outputStyle
    class T1,T2,T3,T4,T5 testStyle
    class L1,L2,L3,L4 lancedbStyle
    class B1 batchStyle
    class SP1,SP2 specStyle
```

## System Benefits & Features

### Asset Labeling System
- **Multi-modal Support**: Handles video, audio, text, and image files
- **Automated Labeling**: Uses AI-generated content to create semantic labels
- **Confidence Scoring**: Provides confidence levels for generated labels
- **Category Assignment**: Automatically categorizes assets by content type

### Semantic Metadata Generation
- **Rich Descriptions**: Generates detailed, searchable text descriptions
- **Keyword Extraction**: Identifies relevant keywords and phrases
- **Tag Generation**: Creates semantic tags for improved discoverability
- **Search Text Creation**: Optimizes text for search engine compatibility

### Hybrid Multimodal Search
- **Multi-modal Queries**: Supports text, video, audio, and image queries
- **Vector Similarity**: High-performance similarity search using embeddings
- **Label Matching**: Semantic search using generated labels
- **Metadata Filtering**: Filter results by categories, tags, and metadata
- **Fusion Ranking**: Combines multiple search strategies for optimal results

### Storage & Scalability
- **LanceDB Integration**: High-performance vector database
- **File-based Storage**: Fallback storage option
- **Search Indexing**: Optimized search index creation
- **Export/Import**: Data portability and backup capabilities

### CLI Interface Benefits
- **Comprehensive Coverage**: All system operations accessible via CLI
- **Batch Processing**: Efficient processing of multiple assets
- **Testing Framework**: Built-in testing and validation tools
- **Inspection Tools**: Debugging and monitoring capabilities
- **Flexible Output**: Multiple output formats (JSON, CSV, YAML) 