def create_conversation_title_gemini(questions_and_answers) -> dict:
    import google.generativeai as genai
    from decouple import config

    
    API_KEY = config("GOOGLE_GEMINI_API_KEY")


    genai.configure(api_key=API_KEY)

   

    prompt = f"""
        Du bist ein datenbasierter Assistent mit fundierter Expertise in der 1. Fußball-Bundesliga.

        Dir werden Fragen und Antworten vorgelegt, die zuvor an ein Sprachmodell gestellt wurden: {questions_and_answers}

        Deine Aufgabe:  
        Formuliere einen prägnanten, sachlichen Titel, der den Inhalt der Fragen und Antworten treffend zusammenfasst.

        Vorgaben:
        - 2 bis 4 Wörter
        - Klar, verständlich und inhaltlich korrekt
        - Keine Wertungen, Zusätze oder Sonderzeichen
        - Gib nur den Titel als einzeiligen Fließtext aus – nichts weiter
        """



    # Schritt 5: Anfrage an Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(prompt)
    except Exception as e:
        import time
        time.sleep(60)
        response = model.generate_content(prompt)

    return {"title": response.text}


