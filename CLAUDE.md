# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies in development mode
uv pip install -e .
```

### Running the Application
```bash
# Start the MCP server
uv run main.py
```

### Testing
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_document.py

# Run specific test class or method
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Architecture

This is an **MCP (Model Context Protocol) server** that exposes document processing and mathematical tools through a FastMCP interface.

### Core Components

- **`main.py`**: Entry point that initializes the FastMCP server and registers tools
- **`tools/`**: Directory containing tool implementations
  - **`math.py`**: Simple mathematical operations (currently just addition)
  - **`document.py`**: Document conversion utilities using MarkItDown library
- **`tests/`**: Test suite with fixtures for document conversion testing

### Tool Architecture

Tools are defined as Python functions and registered with the MCP server using the `@mcp.tool()` decorator pattern:

```python
mcp.tool()(my_function)
```

#### Tool Definition Requirements

All tools should follow these guidelines from the project README:

**Docstring Structure:**
- Begin with a one-line summary
- Provide detailed explanation of functionality  
- Explain when to use (and not use) the tool
- Include usage examples with expected input/output

**Parameter Definitions:**
Use `Field` from pydantic for comprehensive parameter descriptions:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
    """Comprehensive docstring here"""
    # Implementation
```

**Complete Example:**
```python
from pydantic import Field

def add(
    a: float = Field(description="First number to add"),
    b: float = Field(description="Second number to add"),
) -> float:
    """Add two numbers together.

    Takes two numerical inputs and returns their sum. This tool handles
    integers and floating point numbers.

    When to use:
    - When you need to perform simple addition
    - When you need precise numerical calculation

    Examples:
    >>> add(2, 3)
    5.0
    >>> add(2.5, 3.5)
    6.0
    """
    return a + b
```

### Document Processing

The document conversion system uses the MarkItDown library to convert binary document data (DOCX, PDF) to markdown format. The `binary_document_to_markdown` function handles the conversion by creating a BytesIO stream and StreamInfo object for proper file type handling.

### Testing Structure

Tests use pytest with fixture files located in `tests/fixtures/`. The current test structure validates document conversion functionality with real DOCX and PDF files, ensuring proper markdown output formatting.