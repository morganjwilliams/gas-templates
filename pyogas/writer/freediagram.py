import sys
from .common import *
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def FreeFunctionAxisX(name, function):
    return IGElement("FreeFunctionAxisX", name=name, function=function)


def FreeFunctionAxisY(name, function):
    return IGElement("FreeFunctionAxisY", name=name, function=function)


def FreeXYDiagram(xvar, yvar, logx=False, logy=False):
    diagram = IGElement("FreeXYDiagram", name="XY Diagram")
    diagram.extend(
        [
            FreeFunctionAxisX(xvar, ["A", "log(A)"][logx]),
            FreeFunctionAxisY(yvar, ["B", "log(B)"][logy]),
            FreeVariable(xvar, "A"),
            FreeVariable(xvar, "B"),
        ]
    )
    return diagram
