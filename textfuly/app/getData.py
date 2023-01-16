import io
import docx2txt
import requests
from PIL import Image
import pytesseract as tess
from bs4 import BeautifulSoup
from .YouTubeToText import YoutubeToText
from pdfminer.high_level import extract_text

tess.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class GetData:
    def __init__(self, files):
        self.files = files

    def get_data(self):
        text = ""
        try:
            for i in self.files:
                if i.name.endswith("txt"):
                    text += self.__get_text_data(i)

                elif i.name.endswith("jpg"):
                    text += self.__get_text_from_image(i)
                elif i.name.endswith("pdf"):
                    text += self.__get_pdf_data(i)
                elif i.name.endswith("docx"):
                    text += self.__get_docs_data(i)
        except:
            http = "http"
            youtube = "youtube"
            if youtube in self.files:
                text += self.__get_youtube_text(self.files)
            elif http in self.files:
                text += self.__parsed_data(self.files)

        return text, len(text.split(' '))

    def __get_youtube_text(self, link):
        youtube = YoutubeToText()
        return youtube.get_text(link)

    def __get_text_data(self, filename):
        text = ""
        text += (filename.read().decode('UTF-8'))
        return text

    def __get_pdf_data(self, filename):
        text = extract_text(io.BytesIO(filename.read()))

        return text.strip()


    def __parsed_data(self, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, features="html.parser")

        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()

        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def __get_text_from_image(self, filename):
        text = ""
        img = Image.open(filename)
        text += tess.image_to_string(img)

        return text

    def __get_docs_data(self, file):
        text = docx2txt.process(file)
        return text
