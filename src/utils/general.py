import yaml
import textwrap
from pathlib import Path
import plotly.express as px


def read_yaml(file_path: Path) -> dict:
    """Read yaml files for general use.

    Args:
        file_path (Path): file path of yaml to read

    Raises:
        PermissionError: Raised if function does not have permission to access file
        IOError: Raised if file cannot be read
        Exception: General exception just in case

    Returns:
        dict: dictionary with yaml information or None if error occurs
        str: Logged information in form of Exception or string
    """
    try:
        with open(file=file_path, mode="r", encoding="utf-8") as file:
            yaml_dict = yaml.safe_load(file)
    except PermissionError as pe:
        raise PermissionError("Try closing out the file you are trying to read") from pe
    except IOError as io:
        raise IOError("Trouble reading yaml file") from io
    except Exception as e:
        raise Exception("An unknown error has occured") from e

    return yaml_dict


def create_graph_xshift(max_value: float) -> int:
    """_summary_

    Args:
        max_value (float): _description_

    Returns:
        int: _description_
    """
    if max_value <= 1:
        return 0.1
    elif 1 < max_value <= 25:
        return 2
    elif 25 < max_value <= 50:
        return 5
    elif 50 < max_value <= 100:
        return 10
    elif 100 < max_value <= 1000:
        return 25
    elif 1000 < max_value <= 10000:
        return 100
    elif 10000 < max_value <= 50000:
        return 1000
    elif 50000 < max_value <= 100000:
        return 5000
    else:
        return 20000


def create_basic_figure() -> px.box:
    """_summary_

    Args:
        max_value (float): _description_

    Returns:
        px.box: _description_
    """
    byob_figure = (
        px.box(
            color_discrete_sequence=["#FFB71B"],
            height=600,
            orientation="h",
            points="all",
        )
        .update_xaxes(title="", type="linear")
        .update_traces(
            quartilemethod="inclusive",
            boxmean=True,
            hovertemplate="Impact = %{x}<extra></extra>",
            jitter=0.5,
        )
        .update_layout(
            margin={"pad": 10},
            font={"family": "Source Sans Pro"},
            legend_traceorder="reversed",
            boxgroupgap=0.4,
        )
        .add_vline(x=0, line_color="white", layer="below")
    )
    return byob_figure

    # wrap text for formatting


def customwrap(s, width=25):
    if type(s) is not float:
        return "<br>".join(textwrap.wrap(s, width=width))
