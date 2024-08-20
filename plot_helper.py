import shapely.geometry as sg  # geometric objects
import plotly.express as px  # plotting
import plotly.graph_objects as po  # plotting
import numpy as np  # array computations


def plot_geom(geom, fig=None, name=None) -> po.Figure:
    """Plot a single shapely object."""

    if fig is None:
        fig = po.Figure()

    match geom:  # decide how to plot depending on type of geometry
        case sg.LineString():
            xy = np.asarray(geom.xy)
            fig.add_scatter(x=xy[0], y=xy[1], name=name, mode="lines")
        case sg.Polygon():
            xy = np.concatenate(
                [
                    np.asarray(geom.exterior.xy),
                    [[np.nan], [np.nan]],
                    *[np.asarray(i.xy) for i in geom.interiors],
                ],
                axis=1,
            )
            fig.add_scatter(x=xy[0], y=xy[1], fill="toself", name=name, mode="lines")

        # for Multi* objects combine all parts into a single one devided by NaN values to create a gap
        case sg.MultiLineString():
            all_xy = [
                np.concatenate([np.asarray(g.xy), [[np.nan], [np.nan]]], axis=1)
                for g in geom.geoms
            ]
            xy = np.concatenate(all_xy, axis=1)
            fig.add_scatter(x=xy[0], y=xy[1], name=name, mode="lines")
        case sg.MultiPolygon():
            all_xy = [
                np.concatenate(
                    [
                        np.asarray(g.exterior.xy),
                        [[np.nan], [np.nan]],
                        *[np.asarray(i.xy) for i in g.interiors],
                        [[np.nan], [np.nan]],
                    ],
                    axis=1,
                )
                for g in geom.geoms
            ]
            xy = np.concatenate(all_xy, axis=1)
            fig.add_scatter(x=xy[0], y=xy[1], fill="toself", name=name, mode="lines")

    fig.update_yaxes(  # set equally scaled axes
        scaleanchor="x",
        scaleratio=1,
    )
    return fig


def plot_geoms(geoms, names=None) -> po.Figure:
    """Plot multiple shapely objects in a single figure."""

    fig = po.Figure()
    if not names:
        names = [None for g in geoms]
    for g, n in zip(geoms, names):
        plot_geom(g, fig, name=n)
    return fig