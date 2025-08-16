from unidecode import unidecode
def normalization(text:str):
    return unidecode(text.strip().lower())