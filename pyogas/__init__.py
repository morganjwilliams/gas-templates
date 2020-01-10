r"""
Methods for generating xml-based plot templates for use in
`IoGas™ <https://reflexnow.com/iogas/>`__ .
"""
import sys
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.captureWarnings(True)

from ._version import get_versions
from .writer.mpl2iogas import contours_to_XYDiagram, contours_to_FreeTernaryDiagram

__version__ = get_versions()["version"]
del get_versions

__all__ = ["contours_to_XYDiagram", "contours_to_FreeTernaryDiagram"]
