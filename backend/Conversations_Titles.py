def get_conversations_titles(user_id):
    import json
    conversations_db_path = 'Conversations_DB.json'

    # Lade die JSON-Datei (Liste von Konversationen)
    with open(conversations_db_path, 'r') as file:
        conversations_db = json.load(file)

    # Filtere nach passender user_id und extrahiere die Titel
    conversations_titles = [
        conv["title"] for conv in conversations_db if conv.get("user_id") == user_id
    ]

    conversations_ids = [
        conv["conversation_id"] for conv in conversations_db if conv.get("user_id") == user_id
    ]

    return {"conversations_titles": conversations_titles,
            "conversations_ids":conversations_ids
            }
