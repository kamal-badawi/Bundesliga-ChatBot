def add_dialog_title(user_id, conversation_id, title):
    import json
    conversations_db_path = 'Conversations_DB.json'

    try:
        with open(conversations_db_path, 'r', encoding='utf-8') as file:
            conversations_db = json.load(file)
    except FileNotFoundError:
        return False  # Datei nicht vorhanden

    # Finde die passende Konversation
    for conversation in conversations_db:
        if conversation['user_id'] == user_id and conversation['conversation_id'] == conversation_id:
            # Titel aktualisieren
            conversation['title'] = title

            # Datei speichern
            with open(conversations_db_path, 'w', encoding='utf-8') as file:
                json.dump(conversations_db, file, indent=4, ensure_ascii=False)
            return True  # Erfolgreich aktualisiert

    return False  # Konversation nicht gefunden
