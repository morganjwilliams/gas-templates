from pathlib import Path
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_scatter_points
import pyrolite.plot
import numpy as np
import pyogas
import pandas as pd


df = pd.DataFrame(np.array(get_scatter_points(n=100)).T, columns=["TiO2_pct/5", "Cr_ppm+1", "Zr_ppm*2"])
df = df.loc[(df>0.1).all(axis=1), ]
# %%
from pyrolite.util.plot import get_contour_paths

fig, ax = plt.subplots(1, 2, subplot_kw =dict(projection='ternary'), figsize=(10, 4))
df.pyroplot.density(bins=20, ax=ax[0], contours=[0.5, 0.95], label_contours=False)
cpaths, cnames, styles = get_contour_paths(ax[0], resolution=100)
tfm = ax[1].transData + ax[1].transTernaryAxes.inverted()  # ax.transData  + ax.transTernaryAxes.inverted()
for p in cpaths:
    for sp in p:
        tdata = tfm.transform(sp.T)

        ax[1].plot(*tdata.T)
fig

# %%
out = pyogas.contours_to_FreeTernaryDiagram(
    ax[0],
    *df.columns,
    filename=Path("./") / "FreeTernaryDiagramExample.xml",
    contournames=["50%", "95%"],
    resolution=100
)
