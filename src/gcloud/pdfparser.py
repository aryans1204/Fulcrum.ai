from google.cloud import documentai
from google.api_core.client_options import ClientOptions
import os

def parsePDF(file_path: str):
    # You must set the `api_endpoint`if you use a location other than "us".
    project_id = os.environ["PROJECT_ID"]
    location = os.environ["LOCATION"]
    processor_display_name = os.environ["DOCS_PROCESSOR"]
    processor_type = "OCR_PROCESSOR"
    processor_id = os.environ["PROCESSOR_ID"]
    mime_type = "application/pdf"

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location, e.g.:
    # `projects/{project_id}/locations/{location}`
    name = client.processor_path(project_id, location, processor_id)

    # Make GetProcessor request
    processor = client.get_processor(name=name)

    # Print the processor information
    print(f"Processor Name: {processor.name}")

    # Read the file into memory
    with open(file_path, "rb") as doc:
        doc_content = doc.read()

    # Load binary data
    raw_document = documentai.RawDocument(content=doc_content, mime_type=mime_type)

    # Configure the process request
    # `processor.name` is the full resource name of the processor, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}`
    request = documentai.ProcessRequest(name=processor.name, raw_document=raw_document)

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    document = result.document

    # Read the text recognition output from the processor
    print("The document contains the following text:")
    return document.text

if __name__ == "__main__":
    text = parsePDF("/home/aryan/Downloads/FinTech Hackcelerator Project Coordinator (Events).pdf")
    print(text)
