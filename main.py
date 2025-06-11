# Main entry point for the Flutter/Dart Teaching Chatbot

from nlu import understand
from dialog_manager import handle_message

def run_chatbot():
    """Runs the main chatbot interaction loop."""
    print("Chatbot: Hello! I am your Flutter and Dart teaching assistant. Type \'bye\' to exit.")

    while True:
        user_input = input("You: ")
        if not user_input:
            continue

        # 1. Understand User Input
        nlu_result = understand(user_input)

        # 2. Manage Dialog & Generate Response
        response = handle_message(nlu_result)

        # 3. Display Response
        print(f"Chatbot: {response}")

        # 4. Check for Exit Condition
        if nlu_result.get("intent") == "goodbye":
            break

if __name__ == "__main__":
    run_chatbot()

