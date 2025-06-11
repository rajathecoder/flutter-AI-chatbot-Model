# Placeholder for Natural Language Understanding (Refined)

import re

# Predefined list of known concepts (can be expanded)
KNOWN_CONCEPTS = {
    "statefulwidget", "statelesswidget", "widget", "flutter", "dart",
    "async", "await", "async await", "future", "stream",
    "state management", "provider", "riverpod", "bloc", "cubit", "getx",
    "build method", "context", "setstate",
    "routing", "navigation",
    "null safety",
    "mixin", "inheritance", "class", "object",
    # Add more specific concepts, widgets, keywords
}

def understand(text: str) -> dict:
    """Analyzes user input to determine intent and extract entities (more specific)."""
    text_lower = text.lower()
    intent = "unknown"
    entities = {"concept": None} # Initialize concept entity

    # --- Intent Recognition (Simple) ---
    if "what is" in text_lower or "explain" in text_lower or "tell me about" in text_lower:
        intent = "request_explanation"
    elif "example" in text_lower or "show me" in text_lower or "how to use" in text_lower:
        intent = "request_example"
    elif "hello" in text_lower or "hi" in text_lower:
        intent = "greeting"
    elif "bye" in text_lower or "exit" in text_lower:
        intent = "goodbye"

    # --- Entity Extraction (More Specific Concept Matching) ---
    found_concepts = []
    # Prioritize longer matches first
    sorted_concepts = sorted(list(KNOWN_CONCEPTS), key=len, reverse=True)

    for concept in sorted_concepts:
        # Use word boundaries to avoid partial matches (e.g., "dart" in "dartboard")
        if re.search(r"\b" + re.escape(concept) + r"\b", text_lower):
            # Special handling for combined concepts like "async await"
            if concept == "async await":
                 # If we find "async await", prioritize it over just "async" or "await"
                 if "async" in found_concepts:
                     found_concepts.remove("async")
                 if "await" in found_concepts:
                     found_concepts.remove("await")
                 found_concepts.append("async await")
                 break # Found the most specific term
            elif concept == "async" and "async await" in found_concepts:
                continue # Already found the more specific term
            elif concept == "await" and "async await" in found_concepts:
                continue # Already found the more specific term
            else:
                found_concepts.append(concept)

    # Select the most relevant concept found (e.g., the first one, often the longest/most specific)
    if found_concepts:
        entities["concept"] = found_concepts[0]
        # If intent wasn't set but a concept was found, assume explanation request
        if intent == "unknown":
             intent = "request_explanation"

    # If no specific concept found, but intent is explanation/example, try broader terms
    if not entities["concept"] and intent in ["request_explanation", "request_example"]:
        if "dart" in text_lower:
            entities["concept"] = "Dart"
        elif "flutter" in text_lower:
            entities["concept"] = "Flutter"

    return {"intent": intent, "entities": entities, "original_text": text} # Pass original text too

