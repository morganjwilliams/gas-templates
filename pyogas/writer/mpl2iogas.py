"""
Submodule for creating Iogas XML templates from matplotlib axes.
"""
import numpy as np
from lxml.etree import ElementTree
from pyrolite.util.text import int_to_alpha
from pyrolite.util.plot import get_contour_paths
from pyrolite.util.meta import subkwargs

from ..util.xml import prettify_xml
from .common import Poly, Polygon, RegionPolygon
from . import freediagram
from . import geochemdiagram
from . import freeternary

from pyrolite.geochem.ind import common_elements, common_oxides

__els__ = common_elements(as_set=True)
__ox__ = common_oxides(as_set=True)
__chem__ = __els__ | __ox__


def contours_to_XYDiagram(
    ax,
    xvar="X",
    yvar="Y",
    logscalex=False,
    logscaley=False,
    logxdata=False,
    logydata=False,
    filename="element.xml",
    contournames=None,
    allow_free_func=True,
    resolution=100,
    description_prefix="",
    encoding="utf-8",
):
    """
    Take the contour lines from an axis and convert them to an iogas xml diagram
    template.

    Parameters
    ------------

    Note
    ------

        The polygons need not return to the same point.

        If the diagram is for log, the coordinates need to be log.
    """
    filename = str(filename)
    if all([i in __chem__ for i in xvar.split("/")]) and all(
        [i in __chem__ for i in yvar.split("/")]
    ):
        dg = geochemdiagram.XYDiagram
        poly = Poly
    else:
        dg = freediagram.XYDiagram
        if allow_free_func and any(["/" in v for v in [xvar, yvar]]):
            poly = RegionPolygon
        else:
            poly = Poly
    sk = subkwargs(
        dict(
            logscalex=logscalex,
            logscaley=logscaley,
            logxdata=logxdata,
            logydata=logydata,
            allow_free_func=allow_free_func,
        ),
        dg,
    )
    diagram = dg(xvar, yvar, **sk)
    cpaths, cnames, styles = get_contour_paths(ax, resolution=resolution)
    if contournames is not None:
        assert len(contournames) == len(cpaths)
        cnames = contournames
    # create contours
    contours = []
    for ix, (p, name, sty) in enumerate(zip(cpaths, cnames, styles)):
        for six, subpath in enumerate(p):
            if logxdata:
                subpath[0] = np.log(subpath[0])
            if logydata:
                subpath[1] = np.log(subpath[1])
            if len(p) != 1:
                suffix = "-" + int_to_alpha(six)
            else:
                suffix = ""
            cname = ["Countour-{}".format(name), "Countour-{}".format(ix)][
                name is None
            ] + suffix
            c = poly(
                subpath,
                color=sty["color"],
                name=str(name),
                description=description_prefix,
            )
            contours.append(c)
    diagram.extend(contours)
    version_poly = Polygon(
        name="_ v6.1 required to open diagram _",
        visible="true",
        xpoints=[30, 200, 200, 30],
        ypoints=[30, 30, 40, 40],
    )

    diagram.extend([version_poly])
    ElementTree(diagram).write(filename, method="xml", encoding=encoding)
    return prettify_xml(diagram)


def contours_to_FreeTernaryDiagram():
    pass
