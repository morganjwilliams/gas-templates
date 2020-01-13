from .common import *
from pyrolite.util.text import int_to_alpha
import re
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def TPoint(a, b, c=None, strfmt="{:.5f}"):
    """
    Ternary point defined by a and b axes.
    """
    return Element("TPoint", a=strfmt.format(a), b=strfmt.format(b))


def FreeAxisA(name):
    return Element("FreeAxisA", name=str(name), log=False)


def FreeAxisB(name):
    return Element("FreeAxisB", name=str(name), log=False)


def FreeAxisC(name):
    return Element("FreeAxisC", name=str(name), log=False)


def FreeFunctionAxisA(name, function):
    return Element("FreeFunctionAxisA", name=str(name), function=function, log=False)


def FreeFunctionAxisB(name, function):
    return Element("FreeFunctionAxisB", name=str(name), function=function, log=False)


def FreeFunctionAxisC(name, function):
    return Element("FreeFunctionAxisC", name=str(name), function=function, log=False)


def FreeTernaryDiagram(
    avar,
    bvar,
    cvar,
    bounds=None,
    comments=[],
    references=[],
    delim=r"[/+*-]",
    allow_free_func=True,
):
    diagram = Element(
        "FreeTernaryDiagram", name="{} - {} - {}".format(avar, bvar, cvar)
    )
    if allow_free_func:
        dvars, vars = [], []
        for v in [avar, bvar, cvar]:
            if re.findall(delim, v):
                vars += [i for i in re.split(delim, v) if not i.isnumeric()]
            else:
                vars.append(v)
        vars = set(vars)
        info = {
            v: {"code": l}
            for v, l in zip(vars, [int_to_alpha(ix).upper() for ix in range(len(vars))])
        }
        af, bf, cf = avar, bvar, cvar
        for v, d in info.items():
            af = af.replace(v, d["code"])
            bf = bf.replace(v, d["code"])
            cf = cf.replace(v, d["code"])

        aax = FreeFunctionAxisA(avar, af)
        bax = FreeFunctionAxisB(bvar, bf)
        cax = FreeFunctionAxisC(cvar, cf)
        dvars = [FreeVariable(v, d["code"]) for v, d in info.items()]
        diagram.extend([aax, bax, cax])
        diagram.extend(dvars)
    else:
        diagram.extend([FreeAxisA(avar), FreeAxisB(bvar), FreeAxisC(cvar)])

    if bounds is not None:
        diagram.extend(bounds)
    if comments:
        diagram.extend([Comment(c) for c in comments])
    if references:
        diagram.extend([Reference(r) for r in references])
    return diagram
