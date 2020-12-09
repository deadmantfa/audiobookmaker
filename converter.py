import PyPDF2
from gtts import gTTS
import Tkinter

book = open('pdf/Business_Law_I_Essentials_-_WEB.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(book)
pages = pdfReader.numPages
page = pdfReader.getPage(12)
text = page.extractText()
file = "file.mp3"
# initialize tts, create mp3 and play
tts = gTTS(text=text, lang='en', slow=False, lang_check=False)
tts.save(file)
# os.system("mpg321 " + file)
