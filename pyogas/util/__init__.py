"""
Minor utilities for working with Iogas templates.
"""
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

from . import xml

__all__ = ["xml"]
