"""
Submodule for creating Iogas XML templates from matplotlib axes.
"""
import numpy as np
from lxml.etree import ElementTree
from pyrolite.util.text import int_to_alpha
from pyrolite.util.plot import get_contour_paths

from ..util.xml import prettify_xml
from .common import Polygon
from . import freediagram
from . import geochemdiagram
from . import freeternary


def contours_to_FreeXYDiagram(
    ax,
    xvar="X",
    yvar="Y",
    logx=False,
    logy=False,
    filename="element.xml",
    contournames=None,
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
    """
    filename = str(filename)
    diagram = freediagram.FreeXYDiagram(xvar, yvar, logx=logx, logy=logy)
    cpaths, cnames, styles = get_contour_paths(ax, resolution=resolution)
    if contournames is not None:
        assert len(contournames) == len(cpaths)
        cnames = contournames
    # create contours
    contours = []
    for ix, (p, name, sty) in enumerate(zip(cpaths, cnames, styles)):
        for six, subpath in enumerate(p):
            if len(p) != 1:
                suffix = "-" + int_to_alpha(six)
            else:
                suffix = ""
            cname = ["Countour-{}".format(name), "Countour-{}".format(ix)][
                name is None
            ] + suffix
            c = freediagram.RegionPolygon(
                freediagram.Boundary(*subpath),
                color=sty["color"],
                name=cname,
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


def contours_to_GeochemXYDiagram(
    ax,
    xvar="X",
    yvar="Y",
    logx=False,
    logy=False,
    filename="element.xml",
    contournames=None,
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
    """
    filename = str(filename)
    diagram = geochemdiagram.GeochemXYDiagram(xvar, yvar, logx=logx, logy=logy)
    cpaths, cnames, styles = get_contour_paths(ax, resolution=resolution)
    if contournames is not None:
        assert len(contournames) == len(cpaths)
        cnames = contournames
    # create contours
    contours = []
    for ix, (p, name, sty) in enumerate(zip(cpaths, cnames, styles)):
        for six, subpath in enumerate(p):
            if len(p) != 1:
                suffix = "-" + int_to_alpha(six)
            else:
                suffix = ""
            cname = ["Countour-{}".format(name), "Countour-{}".format(ix)][
                name is None
            ] + suffix
            c = geochemdiagram.Poly(
                str(name), geochemdiagram.Boundary3(*subpath), color=sty["color"]
            )
            # boundary

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
