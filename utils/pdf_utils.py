
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf):
    raw_text = ''
    with open(pdf, 'rb') as file:
        reader = PdfReader(file)
        
        # Iterate through all pages
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            content = page.extract_text()
            
            if content:
                raw_text += content
    return raw_text


