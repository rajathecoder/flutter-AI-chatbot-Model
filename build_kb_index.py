# Script to build the FAISS index for the knowledge base (Refined Chunking)

import os
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import re # For sentence splitting

# --- Configuration ---
MODEL_NAME = "all-MiniLM-L6-v2" # A good starting point
SOURCE_FILES = [
    "/home/ubuntu/flutter_concepts.md",
    "/home/ubuntu/dart_concepts.md",
    # Add more source files or scraped content later
]
INDEX_PATH = "/home/ubuntu/flutter_dart_chatbot/kb_index_refined.faiss"
METADATA_PATH = "/home/ubuntu/flutter_dart_chatbot/kb_metadata_refined.txt" # Store original chunks
CHUNK_SEPARATOR = "\n\n" # Initial split by double newline (paragraphs)
MAX_CHUNK_LENGTH = 512 # Approx characters, adjust as needed
CHUNK_OVERLAP = 50 # Character overlap for splitting long chunks

# --- Functions ---

def split_text_intelligently(text, max_length=MAX_CHUNK_LENGTH, overlap=CHUNK_OVERLAP):
    """Splits text into chunks, trying to respect sentence boundaries."""
    if len(text) <= max_length:
        return [text]

    chunks = []
    # Attempt to split by sentences first
    sentences = re.split(r'(?<=[.!?])\s+', text.replace("\n", " ")) # Basic sentence split
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # If adding the next sentence exceeds max length (minus overlap for context)
        if len(current_chunk) + len(sentence) + 1 > max_length and current_chunk:
            chunks.append(current_chunk)
            # Start new chunk with overlap from the end of the previous one
            overlap_text = current_chunk[-overlap:]
            # Find the start of the sentence within the overlap if possible
            overlap_sentence_start = overlap_text.find(". ")
            if overlap_sentence_start != -1:
                 overlap_text = overlap_text[overlap_sentence_start+2:]

            current_chunk = overlap_text + "... " + sentence # Indicate overlap
        else:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence

    if current_chunk: # Add the last chunk
        chunks.append(current_chunk)

    # Fallback: If sentence splitting didn't work well or chunks are still too long, use fixed split
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > max_length:
            start = 0
            while start < len(chunk):
                end = start + max_length
                final_chunks.append(chunk[start:end])
                start += max_length - overlap
        else:
            final_chunks.append(chunk)

    return final_chunks

def load_and_chunk_data(files):
    """Loads data from files and splits into refined chunks."""
    refined_chunks = []
    print(f"Loading data from: {files}")
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Initial split into paragraphs
            paragraphs = [p.strip() for p in content.split(CHUNK_SEPARATOR) if p.strip()]
            print(f"- Processing {len(paragraphs)} paragraphs from {file_path}")
            for para in paragraphs:
                 # Further split long paragraphs
                 para_chunks = split_text_intelligently(para)
                 refined_chunks.extend(para_chunks)

        except FileNotFoundError:
            print(f"Warning: File not found {file_path}, skipping.")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Clean up empty chunks potentially created by splitting
    refined_chunks = [chunk for chunk in refined_chunks if chunk.strip()]
    print(f"Total refined chunks loaded: {len(refined_chunks)}")
    return refined_chunks

def build_index(chunks, model_name, index_path, metadata_path):
    """Builds and saves the FAISS index and metadata."""
    if not chunks:
        print("No chunks to process. Exiting index building.")
        return

    print(f"Loading sentence transformer model: {model_name}")
    model = SentenceTransformer(model_name)

    print("Encoding chunks...")
    embeddings = model.encode(chunks, show_progress_bar=True)
    print(f"Embeddings shape: {embeddings.shape}")

    # Dimension of embeddings
    d = embeddings.shape[1]

    # Build the FAISS index
    print("Building FAISS index...")
    index = faiss.IndexFlatL2(d) # Using L2 distance
    index = faiss.IndexIDMap(index) # Allows mapping index IDs back to original chunk order

    # Add embeddings to the index with sequential IDs
    index.add_with_ids(np.array(embeddings).astype("float32"), np.arange(len(chunks)))

    print(f"Index built with {index.ntotal} vectors.")

    # Save the index
    print(f"Saving index to {index_path}")
    faiss.write_index(index, index_path)

    # Save the metadata (original chunks)
    print(f"Saving metadata to {metadata_path}")
    with open(metadata_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            # Replace newlines within a chunk to avoid issues when reading back
            f.write(chunk.replace("\n", "||NEWLINE||") + "\n")

    print("Index and metadata saved successfully.")

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting knowledge base index building process (refined chunking)...")
    all_chunks = load_and_chunk_data(SOURCE_FILES)
    build_index(all_chunks, MODEL_NAME, INDEX_PATH, METADATA_PATH)
    print("Knowledge base index building finished.")


