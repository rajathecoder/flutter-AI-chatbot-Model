# Dialog Management using updated KB

from knowledge_base import query_knowledge_base
from response_generator import generate_response

def handle_message(nlu_result: dict) -> str:
    """Manages the dialog flow based on NLU result."""
    intent = nlu_result.get("intent", "unknown")
    entities = nlu_result.get("entities", {})
    kb_result = None

    # Construct a query string based on intent and entities
    query = None
    concept = entities.get("concept")

    if intent == "request_explanation":
        if concept:
            query = f"Explain {concept}" # Use concept in the query for semantic search
            kb_result = query_knowledge_base(query=query)
        response = generate_response(intent, entities, kb_result)

    elif intent == "request_example":
        if concept:
            query = f"Show an example of {concept}" # Use concept in the query
            # We might need to refine the response generator later to better handle
            # extracting code examples from the retrieved context.
            # For now, retrieve general context.
            kb_result = query_knowledge_base(query=query)
        response = generate_response(intent, entities, kb_result)

    elif intent == "greeting":
        response = generate_response(intent, entities)

    elif intent == "goodbye":
        response = generate_response(intent, entities)

    else: # intent == "unknown"
        # Try a general query if the intent is unknown but there's text
        user_text = nlu_result.get("text") # Assuming NLU might pass original text
        if user_text:
             kb_result = query_knowledge_base(query=user_text)
             if kb_result:
                 # If KB found something relevant despite unknown intent, show it
                 response = f"I wasn't sure exactly what you meant, but here's some information that might be relevant:\n\n{kb_result}"
             else:
                 response = generate_response(intent, entities) # Standard unknown response
        else:
            response = generate_response(intent, entities)


    return response

