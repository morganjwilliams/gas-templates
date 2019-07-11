import sys
from xml.etree.ElementTree import Element
from lxml.etree import Element
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def IGElement(tag, *args, **kwargs):
    """
    Return an xml element which should preserve attribute order.
    """
    cfg = {k: str(v) for k, v in kwargs.items() if v is not None}
    E = Element(tag, *args)
    for k, v in cfg.items():
        E.set(k, v)
    return E


def get_color(color):
    r, g, b, a = [str(i) for i in color]
    return IGElement("Colour", r=r, g=g, b=b)


def Variable(component, letter, unit=None):
    """
    Parameters
    ----------
    component : :class:`str`
        Component to register as a variable.
    letter : :class:`str`
        Letter to assign to the variable, for use in functions.
    unit : :class:`str`
        Unit to assign to the variable, if any.

    Returns
    ---------
    :class:`xml.etree.ElementTree.Element`
    """
    cfg = dict(letter=letter, element=component, unit=unit)
    return IGElement("Variable", **{k: str(v) for k, v in cfg.items() if v is not None})


def FreeVariable(name, letter):
    """
    Parameters
    ----------
    name : :class:`str`
        Column name of the variable.
    letter : :class:`str`
        Letter to assign to the variable, for use in functions.

    Returns
    ---------
    :class:`xml.etree.ElementTree.Element`
    """
    return IGElement("FreeVariable", letter="A", columnName=name)


def Bounds(x, y, width=1.0, height=1.0):
    """
    <Bounds x="-0.021973616" y="-0.04849591" w="1.0688399" h="1.1006972" />

    Returns
    ---------
    :class:`xml.etree.ElementTree.Element`
    """
    return IGElement(
        "Bounds",
        x="{:.5f}".format(x),
        y="{:.5f}".format(y),
        w="{:.5f}".format(width),
        h="{:.5f}".format(height),
    )


def Comment(text):
    c = IGElement("Comment")
    c.text = text
    return c


def Reference(text):
    r = IGElement("Reference")
    r.text = text
    return r


def Label(name, xy=(0, 0), color=None, labelangle=0.0, visible=True, strfmt="{:.5f}"):
    x, y = xy
    label = IGElement(
        "Label",
        name=name,
        visible=str(visible).lower(),
        x=strfmt.format(x),
        y=strfmt.format(y),
    )
    if color is not None:
        label.append(get_color(color))
    label.append(IGElement("LabelAngle", angle=str(labelangle)))
    return label


def PointFeature(
    name,
    xy=(0.0, 0.0),
    pixelradius=5.0,
    color=None,
    labelangle=0.0,
    visible=True,
    strfmt="{:.5f}",
):
    x, y = xy
    pf = IGElement(
        "PointFeature",
        name=str(name),
        visible=str(visible).lower(),
        x=strfmt.format(x),
        y=strfmt.format(y),
        pixelRadius=strfmt.format(pixelradius),
    )
    if color is not None:
        pf.append(get_color(color))
    pf.append(IGElement("LabelAngle", angle=str(labelangle)))
    return pf


def Polygon(xpoints, ypoints, name="", visible=True, strfmt="{:.5f}"):
    """
    Polygon defined by point verticies.
    """
    polygon = IGElement("Polygon", name=str(name), visible=str(visible).lower())
    polygon.extend(
        [
            IGElement("Point", x=strfmt.format(x), y=strfmt.format(y))
            for x, y in zip(xpoints, ypoints)
        ]
    )
    return polygon


def Boundary(xpoints, ypoints):
    """
    Boundary polygon defined by point verticies.
    """
    boundary = IGElement("Boundary")
    boundary.extend(
        [
            IGElement("Point", x="{:.5f}".format(x), y="{:.5f}".format(y))
            for (x, y) in zip(xpoints, ypoints)
        ]
    )
    return boundary


def BiezerPoint(x, y, sectionEnd=False, strfmt="{:.5f}"):
    """
    Biezer Curve Control point.

    Parameters
    ----------
    x, y : :class:`float`
        Location of the control point.
    sectionEnd : :class:`bool`, :code:`False`
        Whether the control point is an end point (for non-closed paths).
    strfmt : :class:`str`
        Float formatting string.

    Notes
    ------

        * Line segments which have only two points have <sectionEnd="true>
    """
    return IGElement(
        "BezierPoint",
        x=strfmt.format(x),
        y=strfmt.format(y),
        sectionEnd=str(sectionEnd).lower(),
    )


def Boundary3(xpoints, ypoints, sectionend=False, strfmt="{:.5f}"):
    """
    Boundary defined by segments.

    Parameters
    ----------
    xpoints, ypoints : :class:`numpy.ndarray`
        Location of the control points.


    """
    boundary3 = IGElement("Boundary3")
    segs = [IGElement("Linear") for (x, y) in zip(xpoints, ypoints)]
    for ix, s in enumerate(segs):
        s.append(BiezerPoint(xpoints[ix], ypoints[ix], strfmt=strfmt))
    boundary3.extend(segs)
    return boundary3


def Poly(
    name,
    boundary3,
    labelpos=(41.465637, -7.38374),
    labelangle=0.0,
    color=None,
    closed=True,
    visible=True,
    endArrow=False,
    strfmt="{:.5f}",
):
    poly = IGElement(
        "Poly",
        name=name,
        visible=str(visible).lower(),
        closed=str(closed).lower(),
        endArrow=str(endArrow).lower(),
    )
    if color is not None:
        poly.append(get_color(color))
    poly.append(IGElement("LabelAngle", angle=str(labelangle)))
    lx, ly = labelpos
    poly.append(IGElement("LabelPos", x=strfmt.format(lx), y=strfmt.format(ly)))
    poly.append(boundary3)
    return poly


def RegionPolygon(boundary, name="", color=None, description=None):
    c = IGElement("RegionPolygon", name=name, visible="true")
    sub = []
    if color is not None:
        sub.append(get_color(color))
    if description is not None:
        sub.append(IGElement("Description", name=description))
    sub.append(boundary)
    c.extend(sub)
    return c
