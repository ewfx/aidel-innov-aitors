import PyPDF2

class PdfReaderTool:
    """ 
    Reads the contents of a PDF file and returns its text.
    """
    def __init__(self):
        self.name = "pdfReaderTool"
        self.description = "Extracts textual content of the pdf"
    
    def run(self,path="txns.pdf"):
        text = ""
        with open(path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text




# Test function - note that this is not indented under the class.
if __name__ == "__main__":
    pdf_file = "txns.pdf"
    pdfReader = PdfReaderTool()
    extracted_text = pdfReader.run(pdf_file)
    print(extracted_text)
