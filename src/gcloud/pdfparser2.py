from typing import Sequence
import os
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore
from transformers import GPT2Tokenizer

# TODO(developer): Uncomment these variables before running the sample.
project_id = os.environ["PROJECT_ID"]
location = os.environ["LOCATION"] # Format is "us" or "eu"
processor_id = os.environ["PROCESSOR_ID"] # Create processor before running sample
processor_version = "rc" # Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
#file_path = "/home/aryan/Downloads/FinTech Hackcelerator Project Coordinator (Events).pdf"
mime_type = "application/pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types


def parsePDF(
    file_path: str,
) -> Sequence[str]:
    # Online processing request to Document AI
    project_id = os.environ["PROJECT_ID"]
    location = os.environ["LOCATION"]
    processor_id = os.environ["PROCESSOR_ID"]
    processor_version = "rc"
    mime_type = "application/pdf"
    document = process_document(
        project_id, location, processor_id, processor_version, file_path, mime_type
    )

    text = document.text
    chunks = []
    for page in document.pages:
        text_res = create_text_from_blocks(page.blocks, text)
        text_res = chunk_token_limit(text_res)
        for t in text_res:
            chunks.append(t)

    return chunks

def print_page_dimensions(dimension: documentai.Document.Page.Dimension) -> None:
    print(f"    Width: {str(dimension.width)}")
    print(f"    Height: {str(dimension.height)}")


def print_detected_langauges(
    detected_languages: Sequence[documentai.Document.Page.DetectedLanguage],
) -> None:
    print("    Detected languages:")
    for lang in detected_languages:
        code = lang.language_code
        print(f"        {code} ({lang.confidence:.1%} confidence)")


def print_paragraphs(
    paragraphs: Sequence[documentai.Document.Page.Paragraph], text: str
) -> None:
    print(f"    {len(paragraphs)} paragraphs detected:")
    first_paragraph_text = layout_to_text(paragraphs[0].layout, text)
    print(f"        First paragraph text: {repr(first_paragraph_text)}")
    last_paragraph_text = layout_to_text(paragraphs[-1].layout, text)
    print(f"        Last paragraph text: {repr(last_paragraph_text)}")


def print_blocks(blocks: Sequence[documentai.Document.Page.Block], text: str) -> None:
    print(f"    {len(blocks)} blocks detected:")
    for block in blocks:
        first_block_text = layout_to_text(block.layout, text)
        print(f"        First text block: {repr(first_block_text)}")
    
    #last_block_text = layout_to_text(blocks[-1].layout, text)
    #print(f"        Last text block: {repr(last_block_text)}")

def create_text_from_blocks(blocks: Sequence[documentai.Document.Page.Block], text: str,
                            ) -> Sequence[str]:
    texts = []
    for block in blocks:
        block_text = layout_to_text(block.layout, text)
        block_text = block_text.replace("\n", " ")
        texts.append(block_text)

    return texts

def chunk_token_limit(chunks: Sequence[str]) -> Sequence[str]:
    res = []
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    for c in chunks:
        tokens = len(tokenizer.encode(c))
        if tokens > 4096:
            c1 = c[:len(c)/2]
            c2 = c[len(c)/2:]
            res.append(c1)
            res.append(c2)
        else:
            res.append(c)

    return res

def print_lines(lines: Sequence[documentai.Document.Page.Line], text: str) -> None:
    print(f"    {len(lines)} lines detected:")
    first_line_text = layout_to_text(lines[0].layout, text)
    print(f"        First line text: {repr(first_line_text)}")
    last_line_text = layout_to_text(lines[-1].layout, text)
    print(f"        Last line text: {repr(last_line_text)}")


def print_tokens(tokens: Sequence[documentai.Document.Page.Token], text: str) -> None:
    print(f"    {len(tokens)} tokens detected:")
    first_token_text = layout_to_text(tokens[0].layout, text)
    first_token_break_type = tokens[0].detected_break.type_.name
    print(f"        First token text: {repr(first_token_text)}")
    print(f"        First token break type: {repr(first_token_break_type)}")
    last_token_text = layout_to_text(tokens[-1].layout, text)
    last_token_break_type = tokens[-1].detected_break.type_.name
    print(f"        Last token text: {repr(last_token_text)}")
    print(f"        Last token break type: {repr(last_token_break_type)}")


def print_image_quality_scores(
    image_quality_scores: documentai.Document.Page.ImageQualityScores,
) -> None:
    print(f"    Quality score: {image_quality_scores.quality_score:.1%}")
    print("    Detected defects:")

    for detected_defect in image_quality_scores.detected_defects:
        print(f"        {detected_defect.type_}: {detected_defect.confidence:.1%}")


def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    # You must set the `api_endpoint` if you use a location other than "us".
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    # The full resource name of the processor version, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
    # You must create a processor before running this sample.
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
    )

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    return result.document


def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document"s text. This function converts
    offsets to a string.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in layout.text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        response += text[start_index:end_index]
    return response




