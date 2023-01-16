import spacy
import pytesseract as tess
from heapq import nlargest
from string import punctuation
from spacy.lang.en.stop_words import STOP_WORDS

punctuation += '\\n'
tess.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class TextSummarizer:
    __stop_words = list(STOP_WORDS)

    def __init__(self, text, percentage):
        self.__text = text
        self.__word_frequency = {}

        if percentage:
            self.__percentage = int(percentage) / 100
        else:
            self.__percentage = 0.3

    def __get_tokens(self, text):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        return doc

    def __word_frequencies(self, tokens):
        for word in tokens:
            if word.text.lower() not in self.__stop_words and word.text.lower() not in punctuation:
                self.__word_frequency[word.text] = self.__word_frequency.get(word.text, 0) + 1

        max_freq = max(self.__word_frequency.values())

        for key in self.__word_frequency.keys():
            self.__word_frequency[key] = self.__word_frequency[key] / max_freq

        return self.__word_frequency

    def __sent_scores(self, tokens):
        sentence_tokens = [sent for sent in tokens.sents]
        sentence_scores = {}
        word_freq = self.__word_frequencies(tokens)
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_freq.keys():
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_freq[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_freq[word.text.lower()]
        return sentence_scores

    def get_summary(self):

        doc = self.__get_tokens(self.__text)
        sentence_tokens = [sent for sent in doc.sents]
        select_length = int(len(sentence_tokens) * self.__percentage)
        sentence_scores = self.__sent_scores(doc)

        summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)

        final_summary = [word.text for word in summary]
        result = ' '.join(final_summary)

        return result, len(result.split(' '))
