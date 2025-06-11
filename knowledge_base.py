# Knowledge Base Interface using FAISS (Refined Index)

import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os

# --- Configuration ---
MODEL_NAME = "all-MiniLM-L6-v2"
# Use raw strings (r"...") for Windows paths
INDEX_PATH = r"C:\Users\DELL\Downloads\flutter_dart_chatbot_project\flutter_dart_chatbot\kb_index_refined.faiss"
METADATA_PATH = r"C:\Users\DELL\Downloads\flutter_dart_chatbot_project\flutter_dart_chatbot\kb_metadata_refined.txt"
TOP_K = 3


# --- Load Resources (Load once when the module is imported) ---
print("KB: Loading refined resources...")
try:
    if not os.path.exists(INDEX_PATH) or not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(f"Refined index ({INDEX_PATH}) or metadata ({METADATA_PATH}) file not found. Please run build_kb_index.py first.")

    print(f"KB: Loading FAISS index from {INDEX_PATH}")
    index = faiss.read_index(INDEX_PATH)
    print(f"KB: Refined index loaded with {index.ntotal} vectors.")

    print(f"KB: Loading metadata from {METADATA_PATH}")
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        # Read chunks, restoring internal newlines
        metadata_chunks = [line.strip().replace("||NEWLINE||", "\n") for line in f.readlines()]
    print(f"KB: Refined metadata loaded with {len(metadata_chunks)} chunks.")

    print(f"KB: Loading sentence transformer model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    print("KB: Refined resources loaded successfully.")
    resources_loaded = True

except FileNotFoundError as e:
    print(f"KB Error: {e}")
    index = None
    metadata_chunks = []
    model = None
    resources_loaded = False
except Exception as e:
    print(f"KB Error loading refined resources: {e}")
    index = None
    metadata_chunks = []
    model = None
    resources_loaded = False

def query_knowledge_base(query: str, query_type: str = "explanation") -> str | None:
    """Retrieves information relevant to the query from the FAISS index."""
    if not resources_loaded or index is None or model is None or not metadata_chunks:
        print("KB Error: Refined resources not loaded. Cannot query.")
        # Fallback to placeholder if needed, or return None
        return "Knowledge base is not available right now."

    print(f"KB: Encoding query: ", query)
    query_embedding = model.encode([query])

    print(f"KB: Searching refined index...")
    # Ensure the index has vectors before searching
    if index.ntotal == 0:
        print("KB Warning: Refined index is empty.")
        return "The knowledge base seems empty."

    # Search the index
    distances, indices = index.search(np.array(query_embedding).astype("float32"), TOP_K)

    # Retrieve and format results
    results = []
    print(f"KB: Found indices: {indices}")
    if len(indices[0]) > 0 and indices[0][0] != -1: # Check if any results found
        for i in indices[0]:
            if 0 <= i < len(metadata_chunks):
                results.append(metadata_chunks[i])
            else:
                print(f"KB Warning: Retrieved invalid index {i}")

    if not results:
        print("KB: No relevant chunks found.")
        return None

    # Combine the retrieved chunks into a single response context
    print(f"KB: Retrieved {len(results)} chunks.")
    context = "\n\n---\n\n".join(results)

    # Note: In a full RAG system, this 'context' would be passed to an LLM
    # along with the original query to generate a final answer.
    # For this implementation, we return the raw context directly.
    return context

# Example of how to use it (for testing)
if __name__ == "__main__":
    if resources_loaded:
        test_query = "What is async await in Dart?"
        print(f"\nTesting query: {test_query}")
        result = query_knowledge_base(test_query)
        if result:
            print("\nRetrieved Context:")
            print(result)
        else:
            print("No result found.")
    else:
        print("\nCannot run test because refined resources failed to load.")

