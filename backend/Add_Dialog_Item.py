def add_dialog_item(user_id, conversation_id, question, answer):
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
            # Dialogeintrag hinzufügen
            new_entry = {"question": question, "answer": answer}
            conversation.setdefault("dialog", []).append(new_entry)

            # Datei speichern
            with open(conversations_db_path, 'w', encoding='utf-8') as file:
                json.dump(conversations_db, file, indent=4, ensure_ascii=False)
            return True  # Erfolgreich hinzugefügt

    return False  # Konversation nicht gefunden
