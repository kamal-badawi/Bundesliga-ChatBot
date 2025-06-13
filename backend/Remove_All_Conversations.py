def remove_all_conversations(user_id):
    import json
    conversations_db_path = 'Conversations_DB.json'

    # Lade die Konversationen (Liste von Einträgen)
    with open(conversations_db_path, 'r') as file:
        conversations_db = json.load(file)

    # Ursprüngliche Länge merken
    original_length = len(conversations_db)

    # Entferne alle Einträge mit passender user_id
    updated_conversations = [
        conv for conv in conversations_db if conv.get("user_id") != user_id
    ]

    # Prüfe, ob überhaupt etwas entfernt wurde
    if len(updated_conversations) == original_length:
        return False  # Keine Konversationen gefunden

    # Speichere die neue Liste ohne die gelöschten Einträge
    with open(conversations_db_path, 'w') as file:
        json.dump(updated_conversations, file, indent=4)

    return True  # Konversationen wurden gelöscht
