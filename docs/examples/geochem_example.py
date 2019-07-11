import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from pyrolite.util.synthetic import test_df
from pyrolite.util.plot import get_contour_paths
from pyrolite.util.text import int_to_alpha, prettify_xml
from pyrolite.ext.iogas import iogasxml


def contours_to_GeochemXYDiagram(
    ax,
    xvar="X",
    yvar="Y",
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
            xs, ys = subpath
            c = iogasxml.Poly(
                name=str(name),
                children=[
                    iogasxml.Colour(
                        **{l: c for l, c in zip(["r", "g", "b"], sty["color"])}
                    ),
                    iogasxml.LabelAngle(angle=0),
                    iogasxml.LabelPos(x=np.nanmean(xs), y=np.nanmean(ys)),
                    iogasxml.Boundary3(
                        children=[
                            iogasxml.Linear(
                                children=[iogasxml.Point("Point", x=x, y=y)]
                            )
                            for (x, y) in zip(xs, ys)
                        ]
                    ),
                ],
            )
        contours.append(c)
    diagram = iogasxml.GeochemXYDiagram(
        name="{} vs. {}".format(yvar, xvar),
        children=[
            iogasxml.GeochemFunctionAxisX(xvar, function="a"),
            iogasxml.GeochemFunctionAxisY(yvar, function="b"),
            iogasxml.Variable(name=xvar, letter="A"),
            iogasxml.Variable(name=yvar, letter="B"),
        ]
        + contours,
    )
    diagram.export(filename, method="xml", encoding=encoding)
    return prettify_xml(diagram)


df = test_df()
subdf = df.iloc[:, :2] * 100
ax = subdf.pyroplot.density(
    bins=100, contours=[0.5, 0.95], logx=True, logy=True, relim=False
)
ax.figure
print(
    contours_to_GeochemXYDiagram(
        ax,
        *subdf.columns,
        filename=Path("./examples/") / "GeochemXYDiagramExample.xml",
        contournames=["50%", "95%"],
        resolution=10
    )
)
