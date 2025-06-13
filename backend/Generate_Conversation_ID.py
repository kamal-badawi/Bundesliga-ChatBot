import random
import string
from datetime import datetime

def generate_conversation_id(length=15) -> str:
    """
    Erzeugt eine eindeutige Konversations-ID bestehend aus:

    - Einem zufälligen alphanumerischen Präfix (Standard: 15 Zeichen)
    - Einem Zeitstempel im Format YYYYMMDDHHMMSSmmm (bis auf Millisekunden)
    - Einem weiteren zufälligen alphanumerischen Suffix (ebenfalls 15 Zeichen)

    Parameter:
    - length (int): Die Länge der zufälligen Präfix- und Suffix-Komponenten (Standard: 15)

    Rückgabe:
    - str: Eine zusammengesetzte, eindeutige Konversations-ID
    """

    chars = string.ascii_letters + string.digits
    random_part_one = ''.join(random.choices(chars, k=length))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    random_part_two = ''.join(random.choices(chars, k=length))
    return f"{random_part_one}{timestamp}{random_part_two}"



