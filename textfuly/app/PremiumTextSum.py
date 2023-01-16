import pytesseract as tess
from transformers import pipeline

tess.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

summarizer = pipeline('summarization', model="t5-base", tokenizer="t5-base", framework="tf")


class TextSummarizer:
    def __init__(self, text, percentage):
        self.__text = text

        if percentage:
            self.__percentage = int(percentage) / 100
        else:
            self.__percentage = 0.3

    def get_summary(self):

        length = int(len(self.__text.split(' ')) * self.__percentage)

        if len(self.__text.split(' ')) <= 1000:
            summ = summarizer(self.__text, max_length=length * 2, min_length=length, do_sample=False)
            result = summ[0]['summary_text']
        else:
            summ = summarizer(self.__text, max_length=length * 2, min_length=length, do_sample=False)
            result = ' '.join(i['summary_text'] for i in summ)

        return result, len(result.split(' '))

    def __get_chunks(self, text):
        max_chunk = 500
        current_chunk = 0
        chunks = []

        text = text.replace('.', '.<eos>')
        text = text.replace('!', '!<eos>')
        text = text.replace('?', '?<eos>')
        sentences = text.split('<eos>')

        for sentence in sentences:
            if len(chunks) == current_chunk + 1:
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                    chunks[current_chunk].extend(sentence.split(' '))
                else:
                    current_chunk += 1
                    chunks.append(sentence.split(' '))
            else:
                chunks.append(sentence.split(' '))

        for chunk_id in range(len(chunks)):
            chunks[chunk_id] = ' '.join(chunks[chunk_id])

        return chunks
