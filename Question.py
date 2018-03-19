from langdetect import detect_langs
from pycountry import languages

def _detect_message_language(message):
    lang = detect_langs(message)[0]
    if (lang.prob > 0.99):
        lang = lang.lang
    else:
        lang = 'en'
    return languages.get(alpha_2 = lang).name

#ToDo: implement
def _detect_message_theme(message):
    return 'IT'

class Question:
    def __init__(self, asker_id_, text_):
        self.asker_id = asker_id_
        self.text = text_
        self.language = _detect_message_language(self.text)
        self.theme = _detect_message_theme(self.text)