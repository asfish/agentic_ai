# YouTube Agent

## Overview

The `youtube_agent.ipynb` notebook demonstrates a complete workflow for processing YouTube video content through audio extraction, transcription, and question-answering capabilities using AI technologies. This notebook is designed for developers and researchers interested in building YouTube content analysis systems.

## Features

- **YouTube Audio Download**: Downloads audio from YouTube videos using `yt-dlp` and converts to MP3 format
- **Audio Transcription**: Transcribes audio files to text using OpenAI's Whisper API
- **Document Processing**: Loads transcripts using LangChain's TextLoader for further processing
- **Token Analysis**: Counts and analyzes tokens in transcripts using tiktoken
- **RAG Implementation**: Implements Retrieval-Augmented Generation (RAG) for intelligent Q&A on video content
- **Vector Store**: Uses in-memory vector store with OpenAI embeddings for semantic search

## Requirements

Before running the notebook, ensure you have the following prerequisites:

- Python 3.x
- Jupyter Notebook
- FFmpeg (for audio processing)
- Required libraries:
  - `openai`
  - `yt-dlp`
  - `docarray`
  - `python-dotenv`
  - `langchain`
  - `langchain-classic`
  - `langchain-core`
  - `langchain-community`
  - `tiktoken`
  
You can install the necessary libraries using pip:

```bash
pip install openai yt-dlp docarray python-dotenv langchain langchain-classic langchain-core langchain-community tiktoken
```

## Environment Setup

1. Create a `.env` file in the project root directory
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Notebook Workflow

### Cell 1: Setup and Imports
Imports required libraries and loads environment variables.

### Cell 2: YouTube Audio Download
- Downloads audio from a YouTube URL using `yt-dlp`
- Converts audio to MP3 format with 192kbps quality
- Saves to `files/audio/` directory

### Cell 3: File Listing
Lists all downloaded MP3 files in the output directory.

### Cell 4: Audio Transcription
- Transcribes audio files using OpenAI's Whisper API (`whisper-1` model)
- Saves transcripts to `files/transcripts/` directory as text files

### Cell 5: Document Loading
Loads the transcript using LangChain's TextLoader for document processing.

### Cell 6: Token Analysis
Counts tokens in the transcript using tiktoken's cl100k_base encoding.

### Cell 7: LangChain Setup
Sets up LangChain components including:
- ChatOpenAI for language model
- InMemoryVectorStore for vector storage
- OpenAIEmbeddings for text embeddings
- RetrievalQA for question-answering

### Cell 8: Basic Q&A
Creates a vector store from documents and runs a sample query using RetrievalQA.

### Cell 9: Advanced Q&A with Sources
Implements a more sophisticated Q&A chain that:
- Returns source documents along with answers
- Uses verbose logging for debugging
- Demonstrates retrieval with context

### Cell 10: Modern Alternative (Reference)
Shows commented-out code for the modern LangChain approach using:
- `create_retrieval_chain`
- `create_stuff_documents_chain`
- Updated prompt templates

## Usage

1. Open the Jupyter Notebook:
   ```bash
   jupyter notebook youtube_agent.ipynb
   ```
2. Run cells sequentially to execute the workflow
3. Modify the `youtube_url` variable to process different videos
4. Customize queries in the Q&A cells to explore video content

## Example Queries

The notebook includes example queries such as:
- "What are the key steps to create a YouTube agent?"
- "What is the main message about?"

You can modify these queries to ask questions about the specific video content you've processed.

## Directory Structure

```
notebook/
├── youtube_agent.ipynb
├── README.md
└── files/
    ├── audio/          # Downloaded MP3 files
    └── transcripts/    # Generated text transcripts
```

## Notes

- The notebook requires a valid OpenAI API key for transcription and embeddings
- FFmpeg must be installed on your system for audio processing
- The transcription step may take time depending on audio length
- The notebook uses both classic and modern LangChain approaches for reference

## Troubleshooting

- **Download Error**: Ensure the YouTube URL is valid and accessible
- **Transcription Error**: Verify your OpenAI API key is correct and has sufficient credits
- **Import Error**: Install all required dependencies using the pip command above
- **FFmpeg Error**: Install FFmpeg using your system package manager (e.g., `brew install ffmpeg` on macOS)