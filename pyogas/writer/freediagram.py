import sys
from .common import *
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def FreeFunctionAxisX(name, function):
    return Element("FreeFunctionAxisX", name=name, function=function)


def FreeFunctionAxisY(name, function):
    return Element("FreeFunctionAxisY", name=name, function=function)


def FreeXYDiagram(xvar, yvar, logx=False, logy=False):
    diagram = Element("FreeXYDiagram", name="XY Diagram")
    diagram.extend(
        [
            FreeFunctionAxisX(xvar, ["A", "log(A)"][logx]),
            FreeFunctionAxisY(yvar, ["B", "log(B)"][logy]),
            FreeVariable(xvar, "A"),
            FreeVariable(xvar, "B"),
        ]
    )
    return diagram
