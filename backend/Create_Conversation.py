def create_conversation(user_id, conversation_id, title, dialog):
    import json
    conversations_db_path = 'Conversations_DB.json'

    try:
        with open(conversations_db_path, 'r') as file:
            conversations_db = json.load(file)
    except FileNotFoundError:
        conversations_db = []

    # Prüfen, ob bereits eine Konversation mit dieser ID für den Benutzer existiert
    for conversation in conversations_db:
        if conversation['user_id'] == user_id and conversation['conversation_id'] == conversation_id:
            return False

    conversations_db.append({
        "user_id": user_id,
        "conversation_id": conversation_id,
        "title": title,
        "dialog": dialog
    })

    with open(conversations_db_path, 'w') as file:
        json.dump(conversations_db, file, indent=4, ensure_ascii=False)

    return True