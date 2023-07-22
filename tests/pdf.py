from src.gcloud.pdfparser2 import parsePDF
from transformers import GPT2Tokenizer

def test_pdf_parser():
    file_path = '/home/aryan/Downloads/FinTech Hackcelerator Project Coordinator (Events).pdf'
    chunks = parsePDF(file_path)
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    assert len(chunks) > 0
    for c in chunks:
        assert len(tokenizer.encode(c)) <= 4096
    

