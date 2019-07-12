from pyrolite.geochem.ind import common_elements, common_oxides
from .common import *

__els__ = common_elements(as_set=True)
__ox__ = common_oxides(as_set=True)


def default_units(var):
    """
    Get the default unit for a particular variable. If unknown return :code:`None`.

    Parameters
    -----------
    var : :class:`str`
        Variable name (e.g. :code:`'Al'`, :code:`'Al2O3'`).

    Returns
    ---------
    :class:`str`
    """
    if var in __els__:
        return "ppm"
    elif var in __ox__:
        return "pct"
    else:
        return None


def GeochemFunctionAxisX(name, function, log=False):
    return Element(
        "GeochemFunctionAxisX", name=str(name), function=function, log=str(log).lower()
    )


def GeochemFunctionAxisY(name, function, log=False):
    return Element(
        "GeochemFunctionAxisY", name=str(name), function=function, log=str(log).lower()
    )


def XYDiagram(
    xvar,
    yvar,
    logscalex=False,
    logscaley=False,
    logxdata=False,
    logydata=False,
    bounds=None,
    comments=[],
    references=[],
):
    """
    Todo
    -------

        * split ratios to determine true variables and functions, and their units
    """
    diagram = Element("XYDiagram", name="{} vs. {}".format(yvar, xvar))
    vars = []
    for v in [xvar, yvar]:
        if "/" in v:
            vars += v.split("/")
        else:
            vars.append(v)
    vars = set(vars)
    if len(vars) > 2:
        diagram.set("variateMode", "Multi")
    info = {
        v: {"code": l, "unit": default_units(v)}
        for v, l in zip(vars, ["A", "B", "C", "D"])
    }
    xf, yf = xvar, yvar
    for v, d in info.items():
        xf = xf.replace(v, d["code"])
        yf = yf.replace(v, d["code"])

    diagram.extend(
        [
            GeochemFunctionAxisX(
                ["{}", "log({})"][logxdata].format(xvar),
                ["{}", "log({})"][logxdata].format(xf),
                log=logscalex,
            ),
            GeochemFunctionAxisY(
                ["{}", "log({})"][logydata].format(yvar),
                ["{}", "log({})"][logydata].format(yf),
                log=logscaley,
            ),
        ]
    )
    diagram.extend([Variable(v, d["code"], unit=d["unit"]) for v, d in info.items()])

    if bounds is not None:
        diagram.extend(bounds)
    if comments:
        diagram.extend([Comment(c) for c in comments])
    if references:
        diagram.extend([Reference(r) for r in references])
    return diagram
