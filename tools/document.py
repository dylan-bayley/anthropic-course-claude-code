import logging
from markitdown import MarkItDown, StreamInfo
from io import BytesIO
import os
from pydantic import Field

logger = logging.getLogger(__name__)


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    logger.info(f"Converting binary document of type: {file_type}")
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    logger.info(f"Document conversion completed, output length: {len(result.text_content)} characters")
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
    logger.info(f"Starting document conversion for: {file_path}")
    
    # Validate file exists
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not os.path.isfile(file_path):
        logger.error(f"Path is not a file: {file_path}")
        raise ValueError(f"Path is not a file: {file_path}")
    
    # Extract and validate file extension
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    logger.info(f"File extension: {ext}")
    
    if ext not in ['.pdf', '.docx']:
        logger.error(f"Unsupported file type: {ext}")
        raise ValueError(f"Unsupported file type: {ext}. Only .pdf and .docx files are supported.")
    
    # Remove the dot from extension for MarkItDown
    file_type = ext[1:]  # Remove the leading dot
    
    try:
        # Read file binary data
        logger.info(f"Reading file: {file_path}")
        with open(file_path, 'rb') as file:
            binary_data = file.read()
        
        logger.info(f"File read successfully, size: {len(binary_data)} bytes")
        
        # Use existing function to convert
        result = binary_document_to_markdown(binary_data, file_type)
        logger.info(f"Document conversion completed for: {file_path}")
        return result
    
    except PermissionError as e:
        logger.error(f"Permission denied reading file: {file_path}")
        raise PermissionError(f"Permission denied reading file: {file_path}")
    except Exception as e:
        logger.error(f"Error converting document {file_path}: {str(e)}")
        raise RuntimeError(f"Error converting document: {str(e)}")
