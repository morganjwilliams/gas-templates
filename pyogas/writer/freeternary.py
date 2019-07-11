from .common import *


def TPoint(a, b, c=None, strfmt="{:.5f}"):
    """
    Ternary point defined by a and b axes.
    """
    return IGElement("TPoint", a=strfmt.format(a), b=strfmt.format(b))


def FreeAxisA(name, log=False):
    return IGElement("FreeAxisA", name=str(name), log=str(log).lower())


def FreeAxisB(name, log=False):
    return IGElement("FreeAxisB", name=str(name), log=str(log).lower())


def FreeAxisC(name, log=False):
    return IGElement("FreeAxisC", name=str(name), log=str(log).lower())


def FreeTernaryDiagram(name, avar, bvar, cvar, bounds=None, comments=[], references=[]):
    diagram = IGElement(
        "FreeTernaryDiagram", name="{} - {} - {}".format(avar, bvar, cvar)
    )
    diagram.extend([FreeAxisA(avar), FreeAxisB(bvar), FreeAxisC(cvar)])
    if bounds is not None:
        diagram.extend(bounds)
    if comments:
        diagram.extend([Comment(c) for c in comments])
    if references:
        diagram.extend([Reference(r) for r in references])
    version_poly = Polygon(name="_ v6.1 required to open diagram _", visible="true")
    version_poly.extend(
        [Point(x=x, y=y) for x, y in [[30, 30], [200, 30], [200, 40], [30, 40]]]
    )
    diagram.extend([version_poly])
    return diagram
