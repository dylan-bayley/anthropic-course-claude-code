from markitdown import MarkItDown, StreamInfo
from io import BytesIO
import os
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Path to the PDF or DOCX file to convert")
) -> str:
    """Convert PDF or DOCX file to markdown format.

    Takes a file path to a PDF or DOCX document, reads the file, and converts
    its contents to markdown-formatted text using the MarkItDown library.

    When to use:
    - When you have a file path to a document that needs conversion
    - When you want to extract and format document contents as markdown
    - For processing local PDF or DOCX files

    When not to use:
    - When you already have binary document data (use binary_document_to_markdown instead)
    - For file types other than PDF or DOCX

    Examples:
    >>> document_path_to_markdown("/path/to/document.pdf")
    "# Document Title\\n\\nDocument content in markdown format..."
    >>> document_path_to_markdown("/path/to/presentation.docx") 
    "## Slide 1\\n\\nPresentation content..."
    """
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")
    
    # Extract and validate file extension
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext not in ['.pdf', '.docx']:
        raise ValueError(f"Unsupported file type: {ext}. Only .pdf and .docx files are supported.")
    
    # Remove the dot from extension for MarkItDown
    file_type = ext[1:]  # Remove the leading dot
    
    try:
        # Read file binary data
        with open(file_path, 'rb') as file:
            binary_data = file.read()
        
        # Use existing function to convert
        return binary_document_to_markdown(binary_data, file_type)
    
    except PermissionError:
        raise PermissionError(f"Permission denied reading file: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error converting document: {str(e)}")
