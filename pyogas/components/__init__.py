"""
A submodule for reading and representing Iogas XML templates.
"""
from xml.etree.ElementTree import ElementTree, Element, parse
from pathlib import Path
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

from .axes import *
from .diagrams import *
from .points import *
from .text import *
from .variables import *
from .vector import *

# mapping between xml elements and python classes
__mapping__ = {
    "GeochemXYDiagram": GeochemXYDiagram,
    "FreeXYDiagram": FreeXYDiagram,
    "FreeTernaryDiagram": FreeTernaryDiagram,
    "GeochemFunctionAxisX": GeochemFunctionAxisX,
    "GeochemFunctionAxisY": GeochemFunctionAxisY,
    "FreeFunctionAxisX": FreeFunctionAxisX,
    "FreeFunctionAxisY": FreeFunctionAxisY,
    "FreeAxisA": FreeAxisA,
    "FreeAxisB": FreeAxisB,
    "FreeAxisC": FreeAxisC,
    "Variable": Variable,
    "Poly": Poly,
    "Reference": Reference,
    "Comment": Comment,
    "Label": Label,
    "Colour": Colour,
    "LabelAngle": LabelAngle,
    "LabelPos": LabelPos,
    "Boundary3": Boundary3,
    "Boundary": Boundary,
    "Linear": Linear,
    "BezierPoint": BezierPoint,
    "Polygon": Polygon,
    "RegionPolygon": RegionPolygon,
    "Point": Point,
    "TPoint": TPoint,
    "Bounds": Bounds,
    "PointFeature": PointFeature,
    "FreeVariable": FreeVariable,
    "Description": Description,
}


def xml2pyogas(xmlelement):
    """
    Return a python class representation of an Iogas template xml element.

    Parameters
    -----------
    xmlelement : :class:`xml.etree.ElementTree.Element`
        Element to convert a class representation.
    """

    if xmlelement.tag not in __mapping__:
        logger.warning("XML Element not Known")
    cls = __mapping__[xmlelement.tag]
    return cls(xmlelement=xmlelement, text=xmlelement.text, **xmlelement.attrib)


def pyogas2xml(el):
    """
    Create an xml document from a class representation of Iogas xml elements.

    Parameters
    --------------
    el : :class:`IogasXMLObject`
    """
    elxml = el.to_xml()
    if el.children:
        c = [pyogas2xml(i) for i in el.children]
        elxml.extend(c)
    return elxml


def import_iogas_diagram(filepath):
    tree = parse(filepath)
    root = tree.getroot()
    form = root.tag
    assert form in ["GeochemXYDiagram", "FreeXYDiagram", "FreeTernaryDiagram"]
    return xml2pyogas(root)
