import sys
from .common import *
from pyrolite.util.text import int_to_alpha
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
    bounds=None,
    allow_free_func=False,
    comments=[],
    references=[],
):
    diagram = Element("FreeXYDiagram", name="{} vs. {}".format(yvar, xvar))
    diagram.set("variateMode", "Multi")
    if allow_free_func:
        dvars, vars = [], []
        for v in [xvar, yvar]:
            if "/" in v:
                vars += v.split("/")
            else:
                vars.append(v)
        vars = set(vars)
        info = {
            v: {"code": l}
            for v, l in zip(vars, [int_to_alpha(ix).upper() for ix in range(len(vars))])
        }
        xf, yf = xvar, yvar
        for v, d in info.items():
            xf = xf.replace(v, d["code"])
            yf = yf.replace(v, d["code"])

        xax = FreeFunctionAxisX(
            ["{}", "log({})"][logxdata].format(xvar),
            ["{}", "log({})"][logydata].format(xf),
            log=logscalex,
        )
        yax = FreeFunctionAxisY(
            ["{}", "log({})"][logxdata].format(yvar),
            ["{}", "log({})"][logydata].format(yf),
            log=logscaley,
        )
        dvars = [FreeVariable(v, d["code"]) for v, d in info.items()]
        diagram.extend([xax, yax])
        diagram.extend(dvars)
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
