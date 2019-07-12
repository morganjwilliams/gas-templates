import sys
from .common import *
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def FreeAxisX(name, log=False):
    return Element("FreeAxisX", name=name, log=str(log).lower())


def FreeAxisY(name, log=False):
    return Element("FreeAxisY", name=name, log=str(log).lower())


def FreeFunctionAxisX(name, function, log=False):
    return Element(
        "FreeFunctionAxisX", name=name, function=function, log=str(log).lower()
    )


def FreeFunctionAxisY(name, function, log=False):
    return Element(
        "FreeFunctionAxisY", name=name, function=function, log=str(log).lower()
    )


def XYDiagram(
    xvar,
    yvar,
    logscalex=False,
    logscaley=False,
    logxdata=False,
    logydata=False,
    functionvar=False,
    bounds=None,
    comments=[],
    references=[],
):
    diagram = Element("FreeXYDiagram", name="{} vs. {}".format(yvar, xvar))
    diagram.set("variateMode", "Multi")
    if functionvar:
        diagram.extend(
            [
                FreeFunctionAxisX(xvar, ["A", "log(A)"][logxdata]),
                FreeFunctionAxisY(yvar, ["B", "log(B)"][logydata]),
                FreeVariable(xvar, "A"),
                FreeVariable(xvar, "B"),
            ]
        )
    else:
        diagram.extend(
            [
                FreeAxisX(["{}", "log({})"][logxdata].format(xvar), log=logscalex),
                FreeAxisY(["{}", "log({})"][logydata].format(yvar), log=logscaley),
            ]
        )
    if bounds is not None:
        diagram.extend(bounds)
    if comments:
        diagram.extend([Comment(c) for c in comments])
    if references:
        diagram.extend([Reference(r) for r in references])
    return diagram
