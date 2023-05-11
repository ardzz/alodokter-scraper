import string

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory


class Sanitizer:
    def __init__(self, text: str):
        self.text = text

    def sanitize(self):
        self.remove_punctuation().lower().strip().stimulate()
        return self.text

    def lower(self):
        self.text = self.text.lower()
        return self

    def strip(self):
        self.text = self.text.strip()
        return self

    def remove_punctuation(self):
        self.text = self.text.translate(str.maketrans("", "", string.punctuation))
        return self

    def stimulate(self):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        self.text = stemmer.stem(self.text)
        return self

    def remove_stopwords(self):
        factory = StopWordRemoverFactory()
        stopword = factory.create_stop_word_remover()
        self.text = stopword.remove(self.text)
        return self
