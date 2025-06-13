def get_conversations_dialogs(conversation_id: str):
    import json
    conversations_db_path = 'Conversations_DB.json'

    # Lade die JSON-Datei (Liste von Konversationen)
    with open(conversations_db_path, 'r') as file:
        conversations_db = json.load(file)

    conversations_dialogs = []

    # Suche nach passender conversation_id
    for conv in conversations_db:
        if conv.get("conversation_id") == conversation_id:
            conversations_dialogs = [
                {"question": entry["question"], "answer": entry["answer"]}
                for entry in conv.get("dialog", [])
            ]
            break  # Nur die erste passende Konversation zurückgeben

    return {"conversations_dialogs": conversations_dialogs}