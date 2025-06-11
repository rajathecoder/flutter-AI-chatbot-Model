# Flutter & Dart Teaching Chatbot

This project contains a Python-based chatbot designed to teach fundamental concepts of the Flutter framework and the Dart programming language.

## Features

*   **Conversational Interface:** Interact with the chatbot via a command-line interface.
*   **Knowledge Base:** Utilizes a knowledge base built from curated Flutter and Dart concepts.
*   **Semantic Search:** Employs sentence transformers and FAISS for semantic retrieval of relevant information based on user queries.
*   **Concept Explanation:** Answers questions about specific Flutter/Dart concepts.
*   **Modular Design:** Code is organized into modules for NLU, dialog management, knowledge base interaction, and response generation.

## Project Structure

```
flutter_dart_chatbot/
├── main.py               # Main chatbot execution script
├── nlu.py                # Natural Language Understanding module
├── dialog_manager.py     # Dialog flow management module
├── knowledge_base.py     # Knowledge base interaction (FAISS)
├── response_generator.py # Response generation module
├── build_kb_index.py     # Script to build/rebuild the FAISS index
├── requirements.txt      # Python dependencies
├── kb_index_refined.faiss # Pre-built FAISS index
├── kb_metadata_refined.txt # Metadata for the index (text chunks)
├── README.md             # This file
# Documentation/Source Files (Included for reference)
├── flutter_concepts.md
├── dart_concepts.md
├── data_sources.md
├── chatbot_architecture.md
└── todo.md
```

## Setup

1.  **Prerequisites:** Ensure you have Python 3.11 or later installed.
2.  **Clone/Download:** Obtain the project files.
3.  **Navigate:** Open a terminal or command prompt and navigate to the `flutter_dart_chatbot` directory.
4.  **Install Dependencies:** Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Installation might take some time due to the size of libraries like PyTorch and FAISS.*

## Running the Chatbot

Once the setup is complete, you can run the chatbot from the `flutter_dart_chatbot` directory:

```bash
python main.py
```

The chatbot will start, load the knowledge base, and prompt you for input. Type your questions about Flutter or Dart, or type `bye` to exit.

## Building/Rebuilding the Knowledge Base

The chatbot comes with a pre-built knowledge base index (`kb_index_refined.faiss`) based on the included `.md` files.

If you modify the source `.md` files (`flutter_concepts.md`, `dart_concepts.md`) or want to add new documents, you need to rebuild the index:

1.  **Modify Sources:** Update or add content to the relevant `.md` files.
2.  **Update Script (Optional):** If adding new files, update the `SOURCE_FILES` list in `build_kb_index.py`.
3.  **Run Build Script:** Execute the build script from the `flutter_dart_chatbot` directory:
    ```bash
    python build_kb_index.py
    ```
    This will overwrite the existing `kb_index_refined.faiss` and `kb_metadata_refined.txt` files.

## How it Works (Briefly)

1.  **Input:** The `main.py` script takes user input.
2.  **NLU:** `nlu.py` attempts to understand the user's intent (e.g., request explanation) and extract key concepts (e.g., "StatefulWidget", "async await").
3.  **Dialog Management:** `dialog_manager.py` receives the NLU result and decides the next action. If information is needed, it formulates a query.
4.  **Knowledge Base:** `knowledge_base.py` takes the query, encodes it using a sentence transformer model, and searches the FAISS index (`kb_index_refined.faiss`) for the most semantically similar text chunks stored in `kb_metadata_refined.txt`.
5.  **Response Generation:** `response_generator.py` takes the intent, entities, and retrieved knowledge base results to formulate a user-friendly response.
6.  **Output:** The `main.py` script prints the chatbot's response.

## Limitations & Future Improvements

*   **Knowledge Scope:** The current knowledge base is limited to the content in `flutter_concepts.md` and `dart_concepts.md`. Expanding this with official documentation scraping would significantly improve coverage.
*   **NLU Simplicity:** The NLU is basic keyword and regex-based. Using more advanced NLU tools (like Rasa or spaCy models) could improve understanding.
*   **Response Generation:** Responses are currently formed by concatenating retrieved chunks. Integrating a generative LLM (like GPT or similar) could produce more natural, synthesized answers (RAG approach).
*   **Context Management:** The dialog manager has limited memory of the conversation context.
*   **Code Example Extraction:** The chatbot doesn't specifically extract and format code examples from retrieved text; it relies on the source markdown having code blocks.

