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
    resolution=100,
    contournames=None,
    filename="element.xml",
    allow_free_func=True,
    description_prefix="",
    encoding="utf-8",
):
    """
    Take the contour lines from a bivariate axis and convert them to an
    IoGas(TM) xml diagram template.

    Parameters
    ------------
    ax : :class:`matplotlib.axes.Axes`
        Axes to take contours from.
    xvar : :class:`str`
        X-axis variable name.
    yvar : :class:`str`
        Y-axis variable name.
    logscalex : :class:`bool`
        Whether to render the diagram with a log-scaled x axis.
    logscaley : :class:`bool`
        Whether to render the diagram with a log-scaled y axis.
    logxdata : :class:`bool`
        Whether to log-transform the x coordinates (such that the x variable is
        effectively log(x)).
    logydata : :class:`bool`
        Whether to log-transform the y coordinates (such that the y variable is
        effectively log(y)).
    resolution : :class:`int`
        Resolution of the output contours, which directly controls the number of
        interpolated points.
    contournames : :class:`list`
        Names/labels for contours, optional.
    filename : :class:`str` | :class:`pathlib.Path`
        Filename for output xml diagram.
    allow_free_func : :class:`bool
        Whether to allow free-function axes in the xml template.
    description_prefix : :class:`str`
        Prefix for the diagram description.
    encoding : :class:`str`
        Encoding for the output file, defaults to UTF-8 unicode.

    Returns
    ---------
    :class:`str`
        String-formatted xml template file, output for purposes of quick checking.

    Note
    ------

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


def contours_to_FreeTernaryDiagram(
    ax,
    tvar="A",
    lvar="B",
    rvar="C",
    resolution=100,
    contournames=None,
    filename="element.xml",
    allow_free_func=True,
    description_prefix="",
    encoding="utf-8",
):
    """
    Take the contour lines from a ternary axis and convert them to an
    IoGas(TM) xml diagram template.

    Parameters
    ------------
    ax : :class:`matplotlib.axes.Axes`
        Axes to take contours from.
    tvar : :class:`str`
        Top-axis variable name.
    lvar : :class:`str`
        Left-axis variable name.
    rvar : :class:`str`
        Right-axis variable name.
    resolution : :class:`int`
        Resolution of the output contours, which directly controls the number of
        interpolated points.
    contournames : :class:`list`
        Names/labels for contours, optional.
    filename : :class:`str` | :class:`pathlib.Path`
        Filename for output xml diagram.
    allow_free_func : :class:`bool
        Whether to allow free-function axes in the xml template.
    description_prefix : :class:`str`
        Prefix for the diagram description.
    encoding : :class:`str`
        Encoding for the output file, defaults to UTF-8 unicode.

    Returns
    ---------
    :class:`str`
        String-formatted xml template file, output for purposes of quick checking.
    """
    filename = str(filename)

    if allow_free_func:
        poly = RegionPolygon
    else:
        poly = Poly
        
    diagram = freeternary.FreeTernaryDiagram(
        tvar,
        lvar,
        rvar,
        bounds=None,
        comments=[],
        references=[],
        allow_free_func=allow_free_func,
    )

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
            # might need to transform subpath here
            axis_to_data = ax.transData + ax.transTernaryAxes.inverted()
            subpath = axis_to_data.transform(subpath.T)
            c = poly(
                subpath,
                color=sty["color"],
                name=str(name),
                description=description_prefix,
                mode="ternary",
            )
            contours.append(c)
    diagram.extend(contours)
    ElementTree(diagram).write(filename, method="xml", encoding=encoding)
    return prettify_xml(diagram)
