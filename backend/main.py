from fastapi import FastAPI, UploadFile, File,  HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from Chatbot_Question_and_Answer_Gemini import get_chatbot_question_and_answer_gemini
from Text_to_Speech import run_text_to_speech
from Speech_to_Text import run_speech_to_text
from  Reset_Conversation import reset_conversation
from Conversations_Titles import get_conversations_titles
from Conversations_Dialogs import get_conversations_dialogs
from Remove_All_Conversations import remove_all_conversations
from Remove_Conversation_by_User_and_Conversation_ID import remove_conversation_by_user_and_conversation_id
from Create_Conversation import create_conversation
from Add_Dialog_Item import add_dialog_item
from Add_Dialog_Title import add_dialog_title
from Generate_Conversation_ID import generate_conversation_id
from Create_Conversation_Title_Gemini import create_conversation_title_gemini
import Create_PDF
import Send_Report_By_Email
import All_Data
import General_Information


app = FastAPI(version='1.0', title='Bundesliga-ChatBot')

#ORIGINS für das Frontend (React)
origins = ['http://localhost:5173',
           'http://localhost:5174',
           'http://localhost:4173',
           'http://localhost:4174',
           'http://localhost:4000',]

#CORS - Middlewares
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials = True,
                   allow_methods=['*'],
                   allow_headers=['*'])


@app.post("/question")
async def ask_question(question: str) -> dict:
    """
    Verarbeitet eine POST-Anfrage, um eine vom Benutzer gestellte Frage zu beantworten.

    Diese Endpoint-Funktion nimmt eine Frage als Eingabe entgegen, sammelt allgemeine Informationen
    sowie Datenquellen und übergibt diese an eine Chatbot-Funktion, die eine Antwort generiert.
    Die Antwort wird anschließend als JSON-Dictionary zurückgegeben.

    Args:
        question (str): Die vom Benutzer gestellte Frage.

    Returns:
        dict: Ein Dictionary mit der vom Chatbot generierten Antwort unter dem Schlüssel 'answer'.
    """

    # Infos holen
    information = General_Information.get_general_information()
    source = All_Data.get_all_data()

    # Antwort vom Chatbot
    response = get_chatbot_question_and_answer_gemini(source, information, question)
    answer = response.get("text")
    return {'answer':answer}


@app.get("/reset_conversation")
async def reset_chat_conversation():
  reset_conversation()
  print('Conversation has been reseted')
  return {'message':'Conversation has been reseted'}


class ConversationTitleRequest(BaseModel):
    user_id: str

@app.post("/conversations_titles")
async def post_conversations_titles(request: ConversationTitleRequest):
    """
    Lädt die Gesprächstitel eines Benutzers.

    Parameter:
    - request (ConversationTitleRequest): Objekt mit der user_id, für die die Gesprächstitel abgerufen werden sollen.

    Ablauf:
    - Ruft die Funktion `get_conversations_titles` mit der angegebenen Benutzer-ID auf, um die Gesprächstitel zu laden.
    - Gibt eine HTTP 404-Fehlermeldung zurück, wenn keine Daten oder keine Gesprächstitel gefunden werden.
    - Gibt bei Erfolg die Gesprächstitel als JSON zurück.
    - Protokolliert eine Konsolenausgabe bei erfolgreichem Abruf.

    Rückgabewert:
    - JSON-Objekt mit dem Schlüssel 'conversations_titles' und den zugehörigen Titeln.
    """


    data = get_conversations_titles(request.user_id)
    if not data or 'conversations_titles' not in data:
        # 404 Not Found, wenn keine Daten da sind
        raise HTTPException(status_code=404, detail="No conversations titles found")
    
    conversations_titles = data.get('conversations_titles')
    conversations_ids = data.get("conversations_ids")
    print('Conversation titles have been retrieved')
    return {'conversations_titles':conversations_titles,
            "conversations_ids":conversations_ids
            }





@app.post("/conversations_dialogs/{conversation_id}")
async def post_conversations_dialogs(conversation_id: str):
    """
    Ruft die Dialogeinträge einer bestimmten Konversation anhand der conversation_id ab.

    Parameter:
    - conversation_id (str): ID der Konversation.

    Ablauf:
    - Ruft `get_conversations_dialogs` mit conversation_id auf, um die zugehörigen Gesprächsdaten abzurufen.
    - Gibt eine HTTP 404-Fehlermeldung zurück, wenn keine Daten oder keine Dialogeinträge gefunden werden.
    - Gibt bei Erfolg die gefundenen Dialogeinträge als JSON zurück.
    - Protokolliert eine Konsolenausgabe bei erfolgreichem Abruf.

    Ausnahmen:
    - HTTPException mit Statuscode 404, wenn keine Gesprächsdaten vorhanden sind.
    """

    data = get_conversations_dialogs(conversation_id)

    if not data or 'conversations_dialogs' not in data or not data['conversations_dialogs']:
        raise HTTPException(status_code=404, detail="No conversation dialogs found")

    print('Conversation dialogs have been retrieved')
    return {'conversations_dialogs': data['conversations_dialogs']}



class DeleteAllConversationsRequest(BaseModel):
    user_id: str

@app.delete("/delete_all_conversations/{user_id}")
async def delete_all_conversations(request: DeleteAllConversationsRequest):
    """
    Löscht alle Konversationen eines bestimmten Benutzers.

    Parameter:
    - request (DeleteAllConversationsRequest): Objekt mit dem Feld user_id.

    Ablauf:
    - Ruft die Funktion `remove_all_conversations` auf, um alle Gespräche des angegebenen Benutzers zu löschen.
    - Gibt eine HTTP 404-Fehlermeldung zurück, wenn der Benutzer nicht existiert oder keine Konversationen zum Löschen vorhanden sind.
    - Gibt eine Bestätigung auf der Konsole aus und sendet eine Erfolgsnachricht zurück.

    Rückgabewert:
    - JSON-Antwort mit einer Bestätigung, dass alle Konversationen des Benutzers gelöscht wurden.
    """

    user_id = request.user_id
    success = remove_all_conversations(user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="User not found or no conversations to delete")

    
    print(f'Conversations for {user_id} have been removed')
    return {'message': f'Conversations for {user_id} have been removed'}




class DeleteConversationByUserAndconversationIDRequest(BaseModel):
    user_id: str
    conversation_id: str

@app.delete("/delete_conversation_by_user_and_conversation_id")
async def delete_conversation_by_user_and_conversation_id(request: DeleteConversationByUserAndconversationIDRequest):
    """
    Löscht eine spezifische Konversation basierend auf user_id und conversation_id.

    Parameter:
    - request (DeleteConversationByUserAndconversationIDRequest): Objekt mit den Feldern user_id und conversation_id.

    Ablauf:
    - Ruft die Funktion `remove_conversation_by_user_and_conversation_id` auf, um die Konversation zu löschen.
    - Gibt eine HTTP 404-Fehlermeldung zurück, wenn keine passende Konversation gefunden oder gelöscht wurde.

    Rückgabewert:
    - JSON-Antwort mit einer Bestätigungsmeldung bei erfolgreichem Löschen.
    """

    user_id = request.user_id
    conversation_id = request.conversation_id

    success = remove_conversation_by_user_and_conversation_id(user_id, conversation_id)

    if not success:
        raise HTTPException(status_code=404, detail="User or conversation not found or could not be deleted")

    print(f"Conversation '{conversation_id}' for user '{user_id}' has been removed.")
    return {"message": f"Conversation '{conversation_id}' for user '{user_id}' has been removed"}






# Datenmodell für die Anfrage zum Hinzufügen einer Konversation
class ConversationInputRequest(BaseModel):
    user_id: str
   

@app.post("/create_conversation")
async def create_chat_conversation(request: ConversationInputRequest):
    """
    Erstellt eine neue, leere Konversation für einen Benutzer.

    Parameter:
    - request (ConversationInputRequest): Objekt mit der user_id (weitere Felder wie Titel oder Dialog werden hier ignoriert).

    Ablauf:
    - Generiert eine eindeutige conversation_id.
    - Initialisiert eine leere Konversation ohne Titel und ohne Dialogeinträge.
    - Speichert die Konversation mit `create_conversation`.
    - Gibt eine HTTP 409-Fehlermeldung zurück, wenn bereits eine Konversation mit der gleichen ID existiert.

    Rückgabewert:
    - JSON-Antwort mit Bestätigungsnachricht und generierter conversation_id.
    """

    user_id = request.user_id
    conversation_id = generate_conversation_id()
    print(conversation_id)
    title = ""
    dialog = []

    success = create_conversation(
        user_id=user_id,
        conversation_id=conversation_id,
        title=title,
        dialog=dialog
    )

    if not success:
        raise HTTPException(status_code=409, detail=f"Conversation with this conversation_id {conversation_id} already exists.")

    print("Conversation added successfully.")
    return {
        "message": "Conversation added successfully.",
        "conversation_id": conversation_id
    }
    
        
  

class DownloadConversationRequest(BaseModel):
    user_id: str
    conversation_id: str
    
@app.get('/download_conversation')
async def download_conversation(request: DownloadConversationRequest):
    """
    Generiert ein PDF mit dem Dialogverlauf einer bestehenden Konversation und bereitet es zum Download vor.

    Parameter:
    - request (DownloadConversationRequest): Objekt mit user_id und conversation_id.

    Ablauf:
    - Ruft den Dialogverlauf der angegebenen Konversation ab.
    - Gibt eine HTTP 404-Fehlermeldung zurück, wenn keine Dialogdaten gefunden wurden.
    - Erzeugt ein PDF aus dem Konversationsverlauf mit Zeitstempel und Dateinamen.

    Rückgabewert:
    - PDF-Daten und zugehörige Metainformationen (z. B. Dateiname, Erstellungszeitpunkt)."""
    user_id = request.user_id
    conversation_id = request.conversation_id
    data = get_conversations_dialogs(user_id, conversation_id)
    if not data or 'conversations_dialogs' not in data:
      # 404 Not Found, wenn keine Daten da sind
          raise HTTPException(status_code=404, detail="No conversations dialogs found")
    
    conversations_dialogs = data.get('conversations_dialogs')
    text = conversations_dialogs
    pdf_data = Create_PDF.run_create_pdf(text)
    pdf_buffer = pdf_data.get('pdf_buffer')
    created_datetime_file_name = pdf_data.get('created_datetime_file_name')
    created_datetime_sending_time = pdf_data.get('created_datetime_sending_time')



class SendConversationRequest(BaseModel):
    user_id: str
    conversation_id: str
    email_address: str
    
@app.post('/send_conversation')
async def send_conversation( request: SendConversationRequest):
    """
    Sendet den Dialogverlauf einer bestehenden Konversation als PDF an eine angegebene E-Mail-Adresse.

    Parameter:
    - request (SendConversationRequest): Objekt mit user_id, conversation_id und email_address.

    Ablauf:
    - Ruft den Dialogverlauf zur angegebenen Konversation ab.
    - Gibt eine HTTP 404-Fehlermeldung zurück, wenn keine Dialogdaten gefunden wurden.
    - Erzeugt ein PDF aus dem Konversationsverlauf.
    - Versendet das generierte PDF an die angegebene E-Mail-Adresse.

    Rückgabewert:
    - JSON-Antwort mit einer Bestätigung, dass der Report erfolgreich versendet wurde.
    """
    user_id = request.user_id
    conversation_id = request.conversation_id
    email_address = request.email_address
    data = get_conversations_dialogs(user_id, conversation_id)
    
    if not data or 'conversations_dialogs' not in data:
        # Wenn keine Daten gefunden, 404 zurückgeben
        raise HTTPException(status_code=404, detail="No conversations dialogs found")
    
    
    
    
    conversations_dialogs = data['conversations_dialogs']
    
    # PDF erzeugen (deine Implementierung)
   
    pdf_data = Create_PDF.run_create_pdf(conversations_dialogs)
    pdf_buffer = pdf_data.get('pdf_buffer')
    created_datetime_file_name = pdf_data.get('created_datetime_file_name')
    created_datetime_sending_time = pdf_data.get('created_datetime_sending_time')
    
    # E-Mail versenden (deine Implementierung)
    Send_Report_By_Email.run_send_report_by_mail(
        email_address,
        pdf_buffer,
        created_datetime_file_name,
        created_datetime_sending_time
    )
    
    return {"message": f"Report sent to {email_address} successfully"}



from pydantic import BaseModel
from fastapi import HTTPException

# Datenmodell für die Anfrage
class DialogItemInputRequest(BaseModel):
    user_id: str
    conversation_id: str
    question: str
    answer: str

@app.post("/add_dialog_item")
async def post_add_dialog_item(request: DialogItemInputRequest):
    """
    Fügt einen Dialogeintrag (Frage und Antwort) zu einer bestehenden Konversation hinzu.

    Parameter:
    - request (DialogItemInputRequest): Objekt mit user_id, conversation_id, question und answer.

    Ablauf:
    - Verwendet die Funktion `add_dialog_item`, um den Eintrag zur angegebenen Konversation hinzuzufügen.
    - Gibt eine HTTP 404-Fehlermeldung zurück, wenn die Konversation nicht gefunden wird.

    Rückgabewert:
    - JSON-Antwort mit einer Erfolgsnachricht bei erfolgreichem Hinzufügen.
    """
    success = add_dialog_item(
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        question=request.question,
        answer=request.answer
    )

    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    print("Dialog item added successfully.")
    return {"message": "Dialog item added successfully."}


class QAItem(BaseModel):
    question: str
    answer: str

# Datenmodell für die Anfrage
class DialogTitleInputRequest(BaseModel):
    user_id: str
    conversation_id: str
    questions_and_answers: List[QAItem]
   

@app.post("/add_dialog_title")
async def post_add_dialog_title(request: DialogTitleInputRequest): 
    """
    Erstellt und fügt einen Titel basierend auf Dialogeinträgen zu einer bestehenden Konversation hinzu.

    Parameter:
    - request (DialogTitleInputRequest): Objekt mit user_id, conversation_id und einer Liste von Fragen & Antworten (questions_and_answers).

    Ablauf:
    - Erzeugt einen Konversationstitel durch Aufruf von `create_conversation_title_gemini` basierend auf den übergebenen Fragen und Antworten.
    - Aktualisiert die Konversation mit dem generierten Titel via `add_dialog_title`.
    - Gibt eine HTTP 404-Fehlermeldung zurück, falls die Konversation nicht gefunden wird.

    Rückgabewert:
    - JSON-Antwort mit einer Bestätigung, dass der Dialogtitel erfolgreich hinzugefügt wurde.
    """

    questions_and_answers = request.questions_and_answers
    
    title = create_conversation_title_gemini(questions_and_answers)
   
    success = add_dialog_title(
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        title=title
    )

    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    print("Dialog title added successfully.")
    return {"message": "Dialog title added successfully."}


@app.post("/text_to_speech")
async def post_text_to_speech(text:str)-> StreamingResponse:
    """
    Wandelt eingegebenen Text in gesprochene Sprache um und liefert die Audiodatei als Stream zurück.

    Dieser Endpoint nimmt einen Text-String entgegen, konvertiert ihn mittels einer
    Text-to-Speech-Engine in Audio (z. B. WAV oder MP3) und gibt das Ergebnis als
    gestreamte Datei zurück.

    Args:
        text (str): Der zu sprechende Text.

    Returns:
        StreamingResponse: Eine Streaming-Antwort mit der generierten Audiodatei
        im MIME-Typ "application/octet-stream"."""
    # Text-to-Speech
    answer_audio_bytes = run_text_to_speech(text)  
    def get_audio():
        yield answer_audio_bytes

    # StreamingResponse zurückgeben
    return  StreamingResponse(
        get_audio(),
        media_type="application/octet-stream")



@app.post("/speech_to_text")
async def post_speech_to_text(speech: UploadFile = File(...))-> dict:
    """
    Empfängt eine Audiodatei und wandelt sie mittels Speech-to-Text in Text um.

    Diese Endpoint-Funktion erwartet eine Audiodatei (z. B. im WAV- oder MP3-Format)
    als Upload über ein POST-Request. Die Datei wird gelesen und an eine
    Speech-to-Text-Funktion übergeben, die den gesprochenen Inhalt extrahiert und
    als Text zurückliefert.

    Args:
        speech (UploadFile): Die hochgeladene Audiodatei, die verarbeitet werden soll.

    Returns:
        dict: Ein Dictionary mit dem erkannten Text im Format {"text": erkannter_text}.
    """
    # Audiodatei lesen
    audio_bytes = await speech.read()

    # Speech-to-Text
    text = run_speech_to_text(audio_bytes)
    
    return {"text": text}
    