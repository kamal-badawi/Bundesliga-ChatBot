def remove_conversation_by_user_and_conversation_id(user_id, conversation_id):
    import json
    conversations_db_path = 'Conversations_DB.json'

    # Lade die JSON-Datei (Liste von Konversationen)
    with open(conversations_db_path, 'r') as file:
        conversations_db = json.load(file)

    # Ursprüngliche Länge speichern
    original_length = len(conversations_db)

    # Neue Liste ohne die zu löschende Konversation
    updated_conversations = [
        conv for conv in conversations_db
        if not (conv.get("user_id") == user_id and conv.get("conversation_id") == conversation_id)
    ]

    # Falls keine Änderung, Konversation nicht gefunden
    if len(updated_conversations) == original_length:
        return False

    # Neue Liste speichern
    with open(conversations_db_path, 'w') as file:
        json.dump(updated_conversations, file, indent=4)

    return True
