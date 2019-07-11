from pathlib import Path
import matplotlib.pyplot as plt
from pyrolite.util.synthetic import test_df
from pyrolite.ext.iogas import mpl2iogas

df = test_df()
subdf = df.iloc[:, :2] * 100
ax = subdf.pyroplot.density(
    bins=100, contours=[0.5, 0.95], logx=True, logy=True, relim=False
)

print(
    mpl2iogas.contours_to_FreeXYDiagram(
        ax,
        *subdf.columns,
        filename=Path("./examples/") /"FreeDiagramExample.xml",
        contournames=["50%", "95%"],
        resolution=10
    )
)
