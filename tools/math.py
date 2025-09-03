import logging
from pydantic import Field

logger = logging.getLogger(__name__)


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
    logger.info(f"Adding {a} + {b}")
    result = a + b
    logger.info(f"Addition result: {result}")
    return result
