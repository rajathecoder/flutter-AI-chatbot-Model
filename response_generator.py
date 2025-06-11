# Placeholder for Response Generation

def generate_response(intent: str, entities: dict, kb_result: str | None = None) -> str:
    """Generates a response based on intent, entities, and KB results."""

    if intent == "greeting":
        return "Hello! I am your Flutter and Dart teaching assistant. How can I help you today?"

    elif intent == "goodbye":
        return "Goodbye! Happy coding!"

    elif intent == "request_explanation":
        concept = entities.get("concept")
        if kb_result:
            return f"Sure, here is an explanation for {concept}:\n\n{kb_result}"
        elif concept:
            return f"Sorry, I don't have an explanation for {concept} right now."
        else:
            return "Sorry, I couldn't understand which concept you want explained."

    elif intent == "request_example":
        concept = entities.get("concept")
        if kb_result:
            return f"Okay, here is an example related to {concept}:\n\n{kb_result}"
        elif concept:
            return f"Sorry, I don't have an example for {concept} right now."
        else:
            return "Sorry, I couldn't understand which concept you want an example for."

    else: # intent == "unknown"
        return "Sorry, I didn't understand that. Can you please rephrase? You can ask me to explain concepts or show examples for Flutter and Dart."

