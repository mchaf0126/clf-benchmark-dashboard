import base64
from itertools import cycle
from pathlib import Path
import pandas as pd
from dash import (
    html,
    dcc,
    callback,
    Input,
    Output,
    State,
    register_page,
    ALL,
    Patch,
    ctx,
)
import dash_bootstrap_components as dbc
from src.components.dropdowns import create_dropdown, create_multi_dropdown
from src.components.toggle import create_toggle
from src.components.radio_items import create_radio_items
from src.components.tooltip import create_tooltip
from src.components.checklists import create_checklist
from src.components.inputs import create_float_input, create_str_input
import src.utils.load_config as app_config
from src.utils.general import create_graph_xshift, create_basic_figure, customwrap
from dash_bootstrap_templates import load_figure_template
import msgpack

# page name and figure template
register_page(__name__, path="/benchmark_explorer")
load_figure_template("pulse")


# load dictionaries from yaml
impact_dropdown_yaml = app_config.impact_dropdown_yaml
impact_type_radio_yaml = app_config.impact_type_radio_yaml
lcs_checklist_yaml = app_config.lcs_checklist_yaml
scope_checklist_yaml = app_config.scope_checklist_yaml
proj_type_checklist_yaml = app_config.proj_type_checklist_yaml
categorical_toggle_one_yaml = app_config.categorical_toggle_one_yaml
categorical_dropdown_one_yaml = app_config.categorical_dropdown_one_yaml
categorical_filter_toggle_one_yaml = app_config.categorical_filter_toggle_one_yaml
categorical_filter_one_yaml = app_config.categorical_filter_one_yaml
categorical_toggle_two_yaml = app_config.categorical_toggle_two_yaml
categorical_dropdown_two_yaml = app_config.categorical_dropdown_two_yaml
categorical_filter_toggle_two_yaml = app_config.categorical_filter_toggle_two_yaml
categorical_filter_two_yaml = app_config.categorical_filter_two_yaml
material_filter_toggle_yaml = app_config.material_filter_toggle_yaml
material_filter_yaml = app_config.material_filter_yaml
floor_area_normalization_radio_yaml = app_config.floor_area_normalization_radio_yaml
sort_values_radio_yaml = app_config.sort_values_radio_yaml
outlier_toggle_yaml = app_config.outlier_toggle_yaml
line_toggle_yaml = app_config.line_toggle_yaml
line_value_yaml = app_config.line_value_yaml
line_name_yaml = app_config.line_name_yaml
field_name_map = app_config.field_name_map
category_order_map = app_config.category_order_map
caption_orders = app_config.caption_orders
material_list = app_config.material_list

# create basic figure which will be updated by callbacks
byob_figure = create_basic_figure()

# create all tooltips
impact_dropdown_tooltip = create_tooltip(
    tooltip_text=impact_dropdown_yaml["tooltip"],
    target_id=impact_dropdown_yaml["tooltip_id"],
)

impact_type_radio_tooltip = create_tooltip(
    tooltip_text=impact_type_radio_yaml["tooltip"],
    target_id=impact_type_radio_yaml["tooltip_id"],
)

lcs_checklist_tooltip = create_tooltip(
    tooltip_text=lcs_checklist_yaml["tooltip"],
    target_id=lcs_checklist_yaml["tooltip_id"],
)

scope_checklist_tooltip = create_tooltip(
    tooltip_text=scope_checklist_yaml["tooltip"],
    target_id=scope_checklist_yaml["tooltip_id"],
)

proj_type_checklist_tooltip = create_tooltip(
    tooltip_text=proj_type_checklist_yaml["tooltip"],
    target_id=proj_type_checklist_yaml["tooltip_id"],
)

categorical_toggle_one_tooltip = create_tooltip(
    tooltip_text=categorical_toggle_one_yaml["tooltip"],
    target_id=categorical_toggle_one_yaml["tooltip_id"],
)

categorical_dropdown_one_tooltip = create_tooltip(
    tooltip_text=categorical_dropdown_one_yaml["tooltip"],
    target_id=categorical_dropdown_one_yaml["tooltip_id"],
)

categorical_filter_toggle_one_tooltip = create_tooltip(
    tooltip_text=categorical_filter_toggle_one_yaml["tooltip"],
    target_id=categorical_filter_toggle_one_yaml["tooltip_id"],
)

categorical_filter_one_tooltip = create_tooltip(
    tooltip_text=categorical_filter_one_yaml["tooltip"],
    target_id=categorical_filter_one_yaml["tooltip_id"],
)

categorical_toggle_two_tooltip = create_tooltip(
    tooltip_text=categorical_toggle_two_yaml["tooltip"],
    target_id=categorical_toggle_two_yaml["tooltip_id"],
)

categorical_dropdown_two_tooltip = create_tooltip(
    tooltip_text=categorical_dropdown_two_yaml["tooltip"],
    target_id=categorical_dropdown_two_yaml["tooltip_id"],
)

categorical_filter_toggle_two_tooltip = create_tooltip(
    tooltip_text=categorical_filter_toggle_two_yaml["tooltip"],
    target_id=categorical_filter_toggle_two_yaml["tooltip_id"],
)

categorical_filter_two_tooltip = create_tooltip(
    tooltip_text=categorical_filter_two_yaml["tooltip"],
    target_id=categorical_filter_two_yaml["tooltip_id"],
)

material_filter_toggle_tooltip = create_tooltip(
    tooltip_text=material_filter_toggle_yaml["tooltip"],
    target_id=material_filter_toggle_yaml["tooltip_id"],
)

material_filter_tooltip = create_tooltip(
    tooltip_text=material_filter_yaml["tooltip"],
    target_id=material_filter_yaml["tooltip_id"],
)

floor_area_normalization_radio_tooltip = create_tooltip(
    tooltip_text=floor_area_normalization_radio_yaml["tooltip"],
    target_id=floor_area_normalization_radio_yaml["tooltip_id"],
)

sort_values_radio_tooltip = create_tooltip(
    tooltip_text=sort_values_radio_yaml["tooltip"],
    target_id=sort_values_radio_yaml["tooltip_id"],
)

outlier_toggle_tooltip = create_tooltip(
    tooltip_text=outlier_toggle_yaml["tooltip"],
    target_id=outlier_toggle_yaml["tooltip_id"],
)

line_toggle_tooltip = create_tooltip(
    tooltip_text=line_toggle_yaml["tooltip"], target_id=line_toggle_yaml["tooltip_id"]
)

line_value_tooltip = create_tooltip(
    tooltip_text=line_value_yaml["tooltip"], target_id=line_value_yaml["tooltip_id"]
)

line_name_tooltip = create_tooltip(
    tooltip_text=line_name_yaml["tooltip"], target_id=line_name_yaml["tooltip_id"]
)


def layout(state: str = None):
    """Home page layout

    It takes in a keyword arguments defined in `routing_callback_inputs`:
    * state (serialised state in the URL hash), it does not trigger re-render.
    This function is used to serialize and read the hash from URL, otherwise uses defaults.
    """
    # Define default state values
    defaults = {
        impact_dropdown_yaml["dropdown_id"]: impact_dropdown_yaml["first_item"],
        impact_type_radio_yaml["radio_id"]: impact_type_radio_yaml["first_item"],
        lcs_checklist_yaml["checklist_id"]: lcs_checklist_yaml["first_item"],
        scope_checklist_yaml["checklist_id"]: scope_checklist_yaml["first_item"],
        proj_type_checklist_yaml["checklist_id"]: proj_type_checklist_yaml[
            "first_item"
        ],
        categorical_toggle_one_yaml["toggle_id"]: categorical_toggle_one_yaml[
            "first_item"
        ],
        categorical_dropdown_one_yaml["dropdown_id"]: categorical_dropdown_one_yaml[
            "first_item"
        ],
        categorical_filter_toggle_one_yaml[
            "toggle_id"
        ]: categorical_filter_toggle_one_yaml["first_item"],
        categorical_filter_one_yaml["dropdown_id"]: [],
        categorical_toggle_two_yaml["toggle_id"]: categorical_toggle_two_yaml[
            "first_item"
        ],
        categorical_dropdown_two_yaml["dropdown_id"]: [],
        categorical_filter_toggle_two_yaml[
            "toggle_id"
        ]: categorical_filter_toggle_two_yaml["first_item"],
        categorical_filter_two_yaml["dropdown_id"]: [],
        material_filter_toggle_yaml["toggle_id"]: material_filter_toggle_yaml[
            "first_item"
        ],
        material_filter_yaml["dropdown_id"]: [],
        floor_area_normalization_radio_yaml[
            "radio_id"
        ]: floor_area_normalization_radio_yaml["first_item"],
        sort_values_radio_yaml["radio_id"]: sort_values_radio_yaml["first_item"],
        outlier_toggle_yaml["toggle_id"]: outlier_toggle_yaml["first_item"],
        line_toggle_yaml["toggle_id"]: line_toggle_yaml["first_item"],
        line_value_yaml["input_id"]: 0,
        line_name_yaml["input_id"]: "",
    }

    # Decode the state from the hash
    state = defaults | (
        msgpack.unpackb(base64.urlsafe_b64decode(state)) if state else {}
    )

    # create all options for sidebar
    impact_dropdown = create_dropdown(
        label=impact_dropdown_yaml["label"],
        tooltip_id=impact_dropdown_yaml["tooltip_id"],
        dropdown_list=impact_dropdown_yaml["dropdown_list"],
        first_item=state.get(impact_dropdown_yaml["dropdown_id"]),
        dropdown_id={"type": "control", "id": impact_dropdown_yaml["dropdown_id"]},
    )

    impact_type_radio = create_radio_items(
        label=impact_type_radio_yaml["label"],
        tooltip_id=impact_type_radio_yaml["tooltip_id"],
        radio_list=impact_type_radio_yaml["radio_list"],
        first_item=state.get(impact_type_radio_yaml["radio_id"]),
        radio_id={"type": "control", "id": impact_type_radio_yaml["radio_id"]},
    )

    lcs_checklist = create_checklist(
        label=lcs_checklist_yaml["label"],
        checklist=lcs_checklist_yaml["checklist"],
        first_item=state.get(lcs_checklist_yaml["checklist_id"]),
        checklist_id={"type": "control", "id": lcs_checklist_yaml["checklist_id"]},
        tooltip_id=lcs_checklist_yaml["tooltip_id"],
    )

    scope_checklist = create_checklist(
        label=scope_checklist_yaml["label"],
        checklist=scope_checklist_yaml["checklist"],
        first_item=state.get(scope_checklist_yaml["checklist_id"]),
        checklist_id={"type": "control", "id": scope_checklist_yaml["checklist_id"]},
        tooltip_id=scope_checklist_yaml["tooltip_id"],
    )

    proj_type_checklist = create_checklist(
        label=proj_type_checklist_yaml["label"],
        checklist=proj_type_checklist_yaml["checklist"],
        first_item=state.get(proj_type_checklist_yaml["checklist_id"]),
        checklist_id={
            "type": "control",
            "id": proj_type_checklist_yaml["checklist_id"],
        },
        tooltip_id=proj_type_checklist_yaml["tooltip_id"],
    )

    categorical_toggle_one = create_toggle(
        toggle_list=categorical_toggle_one_yaml["toggle_list"],
        first_item=state.get(categorical_toggle_one_yaml["toggle_id"]),
        toggle_id={"type": "control", "id": categorical_toggle_one_yaml["toggle_id"]},
        tooltip_id=categorical_toggle_one_yaml["tooltip_id"],
    )

    categorical_dropdown_one = create_dropdown(
        label=categorical_dropdown_one_yaml["label"],
        tooltip_id=categorical_dropdown_one_yaml["tooltip_id"],
        dropdown_list=categorical_dropdown_one_yaml["dropdown_list"],
        first_item=state.get(categorical_dropdown_one_yaml["dropdown_id"]),
        dropdown_id={
            "type": "control",
            "id": categorical_dropdown_one_yaml["dropdown_id"],
        },
    )

    categorical_filter_toggle_one = create_toggle(
        toggle_list=categorical_filter_toggle_one_yaml["toggle_list"],
        first_item=state.get(categorical_filter_toggle_one_yaml["toggle_id"]),
        toggle_id={
            "type": "control",
            "id": categorical_filter_toggle_one_yaml["toggle_id"],
        },
        tooltip_id=categorical_filter_toggle_one_yaml["tooltip_id"],
    )

    categorical_filter_one = create_multi_dropdown(
        label=categorical_filter_one_yaml["label"],
        tooltip_id=categorical_filter_one_yaml["tooltip_id"],
        dropdown_id={
            "type": "control",
            "id": categorical_filter_one_yaml["dropdown_id"],
        },
        placeholder=categorical_filter_one_yaml["placeholder"],
    )

    categorical_toggle_two = create_toggle(
        toggle_list=categorical_toggle_two_yaml["toggle_list"],
        first_item=state.get(categorical_toggle_two_yaml["toggle_id"]),
        toggle_id={"type": "control", "id": categorical_toggle_two_yaml["toggle_id"]},
        tooltip_id=categorical_toggle_two_yaml["tooltip_id"],
    )

    categorical_dropdown_two = create_dropdown(
        label=categorical_dropdown_two_yaml["label"],
        tooltip_id=categorical_dropdown_two_yaml["tooltip_id"],
        dropdown_list=categorical_dropdown_two_yaml["dropdown_list"],
        first_item=state.get(categorical_dropdown_two_yaml["dropdown_id"]),
        dropdown_id={
            "type": "control",
            "id": categorical_dropdown_two_yaml["dropdown_id"],
        },
    )

    categorical_filter_toggle_two = create_toggle(
        toggle_list=categorical_filter_toggle_two_yaml["toggle_list"],
        first_item=state.get(categorical_filter_toggle_two_yaml["toggle_id"]),
        toggle_id={
            "type": "control",
            "id": categorical_filter_toggle_two_yaml["toggle_id"],
        },
        tooltip_id=categorical_filter_toggle_two_yaml["tooltip_id"],
    )

    categorical_filter_two = create_multi_dropdown(
        label=categorical_filter_two_yaml["label"],
        tooltip_id=categorical_filter_two_yaml["tooltip_id"],
        dropdown_id={
            "type": "control",
            "id": categorical_filter_two_yaml["dropdown_id"],
        },
        placeholder=categorical_filter_two_yaml["placeholder"],
    )

    material_filter_toggle = create_toggle(
        toggle_list=material_filter_toggle_yaml["toggle_list"],
        first_item=state.get(material_filter_toggle_yaml["toggle_id"]),
        toggle_id={"type": "control", "id": material_filter_toggle_yaml["toggle_id"]},
        tooltip_id=material_filter_toggle_yaml["tooltip_id"],
    )

    material_filter = create_multi_dropdown(
        label=material_filter_yaml["label"],
        tooltip_id=material_filter_yaml["tooltip_id"],
        dropdown_id={"type": "control", "id": material_filter_yaml["dropdown_id"]},
        placeholder=material_filter_yaml["placeholder"],
    )

    floor_area_normalization_radio = create_radio_items(
        label=floor_area_normalization_radio_yaml["label"],
        tooltip_id=floor_area_normalization_radio_yaml["tooltip_id"],
        radio_list=floor_area_normalization_radio_yaml["radio_list"],
        first_item=state.get(floor_area_normalization_radio_yaml["radio_id"]),
        radio_id={
            "type": "control",
            "id": floor_area_normalization_radio_yaml["radio_id"],
        },
    )

    sort_values_radio = create_radio_items(
        label=sort_values_radio_yaml["label"],
        tooltip_id=sort_values_radio_yaml["tooltip_id"],
        radio_list=sort_values_radio_yaml["radio_list"],
        first_item=state.get(sort_values_radio_yaml["radio_id"]),
        radio_id={"type": "control", "id": sort_values_radio_yaml["radio_id"]},
    )

    outlier_toggle = create_toggle(
        toggle_list=outlier_toggle_yaml["toggle_list"],
        first_item=state.get(outlier_toggle_yaml["toggle_id"]),
        toggle_id={"type": "control", "id": outlier_toggle_yaml["toggle_id"]},
        tooltip_id=outlier_toggle_yaml["tooltip_id"],
    )

    line_toggle = create_toggle(
        toggle_list=line_toggle_yaml["toggle_list"],
        first_item=state.get(line_toggle_yaml["toggle_id"]),
        toggle_id={"type": "control", "id": line_toggle_yaml["toggle_id"]},
        tooltip_id=line_toggle_yaml["tooltip_id"],
    )

    line_value = create_float_input(
        label=line_value_yaml["label"],
        placeholder=line_value_yaml["placeholder"],
        input_id={"type": "control", "id": line_value_yaml["input_id"]},
        tooltip_id=line_value_yaml["tooltip_id"],
        first_item=state.get(line_value_yaml["input_id"]),
    )

    line_name = create_str_input(
        label=line_name_yaml["label"],
        placeholder=line_name_yaml["placeholder"],
        input_id={"type": "control", "id": line_name_yaml["input_id"]},
        tooltip_id=line_name_yaml["tooltip_id"],
        first_item=state.get(line_name_yaml["input_id"]),
    )

    # create sidebar accordion
    controls_byob = dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    impact_dropdown,
                    impact_dropdown_tooltip,
                    impact_type_radio,
                    impact_type_radio_tooltip,
                    lcs_checklist,
                    lcs_checklist_tooltip,
                    scope_checklist,
                    scope_checklist_tooltip,
                    proj_type_checklist,
                    proj_type_checklist_tooltip,
                ],
                title="Impact Controls",
                item_id="proj_filters",
            ),
            dbc.AccordionItem(
                [
                    categorical_toggle_one,
                    categorical_toggle_one_tooltip,
                    categorical_dropdown_one,
                    categorical_dropdown_one_tooltip,
                    categorical_filter_toggle_one,
                    categorical_filter_toggle_one_tooltip,
                    categorical_filter_one,
                    categorical_filter_one_tooltip,
                    categorical_toggle_two,
                    categorical_toggle_two_tooltip,
                    categorical_dropdown_two,
                    categorical_dropdown_two_tooltip,
                    categorical_filter_toggle_two,
                    categorical_filter_toggle_two_tooltip,
                    categorical_filter_two,
                    categorical_filter_two_tooltip,
                    material_filter_toggle,
                    material_filter_toggle_tooltip,
                    material_filter,
                    material_filter_tooltip,
                ],
                title="Categorical Controls",
                item_id="axis_controls",
            ),
            dbc.AccordionItem(
                [
                    floor_area_normalization_radio,
                    floor_area_normalization_radio_tooltip,
                    sort_values_radio,
                    sort_values_radio_tooltip,
                    outlier_toggle,
                    outlier_toggle_tooltip,
                ],
                title="Additional Filters",
                item_id="addl_filters",
            ),
            dbc.AccordionItem(
                [
                    line_toggle,
                    line_toggle_tooltip,
                    line_value,
                    line_value_tooltip,
                    line_name,
                    line_name_tooltip,
                ],
                title="Reference Line",
                item_id="ref_line",
            ),
        ],
        start_collapsed=True,
        always_open=True,
        active_item=["axis_controls", "proj_filters", "addl_filters", "ref_line"],
        class_name="overflow-scroll h-100",
    )

    return html.Div(
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [controls_byob],
                        xs=4,
                        sm=4,
                        md=4,
                        lg=4,
                        xl=3,
                        xxl=3,
                        style={"max-height": "800px"},
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(figure=byob_figure, id="byob_graph"),
                            html.Div(id="caption"),
                            html.Div(
                                [
                                    dbc.Button(
                                        "Download Table Contents",
                                        color="primary",
                                        id="btn-download-tbl-byob",
                                        className="my-2 fw-bold",
                                    ),
                                    dcc.Download(id="download-tbl-byob"),
                                ]
                            ),
                            html.Div(id="help_div"),
                        ],
                        xs=8,
                        sm=8,
                        md=8,
                        lg=8,
                        xl=7,
                        xxl=7,
                    ),
                ],
                justify="center",
                className="mb-4",
            ),
        ],
    )


### Glossary of symbols for variables
# c = category
# ch = checklist
# d = dropdown
# f = filter
# fl = floor
# i = impact
# ln = line
# m = material
# nm = name
# no = normalization
# t = toggle
# typ = type
# p = project
# lcs = life cycle stage
# out = outlier
# sc = scope
# sort = sort
# v = values


@callback(
    [
        Output({"type": "control", "id": "c_f_t_1"}, "options"),
        Output({"type": "control", "id": "c_t_2"}, "options"),
        Output({"type": "control", "id": "c_f_t_2"}, "options"),
    ],
    [
        Input({"type": "control", "id": "c_t_1"}, "value"),
        Input({"type": "control", "id": "c_t_2"}, "value"),
    ],
)
def enable_filters(cat_selection_toggle: list, second_cat_selection_toggle: list):
    if cat_selection_toggle == [1]:
        enable_filters_toggle = [{"label": "Enable 1st categorical filter", "value": 1}]
        second_cat_selection = [
            {"label": "Enable 2nd categorical variable", "value": 1}
        ]
        if second_cat_selection_toggle == [1]:
            second_cat_filter_toggle = [
                {"label": "Enable 2nd categorical filter", "value": 1}
            ]
        else:
            second_cat_filter_toggle = [
                {"label": "Enable 2nd categorical filter", "value": 1, "disabled": True}
            ]
        return enable_filters_toggle, second_cat_selection, second_cat_filter_toggle
    else:
        enable_filters_toggle = [
            {"label": "Enable 1st categorical filter", "value": 1, "disabled": True}
        ]
        second_cat_selection = [
            {"label": "Enable 2nd categorical variable", "value": 1, "disabled": True}
        ]
        second_cat_filter_toggle = [
            {"label": "Enable 2nd categorical filter", "value": 1, "disabled": True}
        ]
        return enable_filters_toggle, second_cat_selection, second_cat_filter_toggle


@callback(
    [
        Output({"type": "control", "id": "c_d_1"}, "disabled"),
        Output({"type": "control", "id": "c_f_1"}, "disabled"),
        Output({"type": "control", "id": "c_d_2"}, "disabled"),
        Output({"type": "control", "id": "c_f_2"}, "disabled"),
    ],
    [
        Input({"type": "control", "id": "c_t_1"}, "value"),
        Input({"type": "control", "id": "c_f_t_1"}, "value"),
        Input({"type": "control", "id": "c_t_2"}, "value"),
        Input({"type": "control", "id": "c_f_t_2"}, "value"),
    ],
)
def enable_or_disable_cat_dropdowns_and_filters(
    cat_selection_toggle: list,
    enable_filters_toggle: list,
    second_cat_selection_toggle: list,
    second_cat_filter_toggle: list,
):
    if cat_selection_toggle == [1]:
        if enable_filters_toggle == [1]:
            if second_cat_selection_toggle == [1]:
                if second_cat_filter_toggle == [1]:
                    return False, False, False, False
                else:
                    return False, False, False, True
            else:
                return False, False, True, True
        else:
            if second_cat_selection_toggle == [1]:
                if second_cat_filter_toggle == [1]:
                    return False, False, False, False
                else:
                    return False, False, False, True
            else:
                return False, True, True, True
    else:
        return True, True, True, True


@callback(
    Output({"type": "control", "id": "m_f"}, "disabled"),
    Input({"type": "control", "id": "m_t"}, "value"),
)
def enable_or_disable_material_filter(material_filter_toggle):
    if material_filter_toggle == []:
        return True
    else:
        return False


@callback(
    Output({"type": "control", "id": "fl_no"}, "options"),
    Input({"type": "control", "id": "i_typ"}, "value"),
)
def enable_or_disable_floor_norm_radio(impact_type_value):
    if impact_type_value == 1:
        disabled_option = False
    else:
        disabled_option = True
    return [
        {
            "label": "Built Floor Area",
            "value": "bldg_cfa",
            "disabled": disabled_option,
        },
        {
            "label": "Gross Internal Floor Area",
            "value": "bldg_gfa",
            "disabled": disabled_option,
        },
    ]


@callback(
    [
        Output({"type": "control", "id": "ln_v"}, "disabled"),
        Output({"type": "control", "id": "ln_nm"}, "disabled"),
    ],
    Input({"type": "control", "id": "ln_t"}, "value"),
)
def enable_or_disable_ref_line(enable_line_toggle):
    if enable_line_toggle == []:
        return True, True
    else:
        return False, False


@callback(
    [
        Output({"type": "control", "id": "c_d_2"}, "options"),
        Output({"type": "control", "id": "c_d_2"}, "value"),
    ],
    [
        Input({"type": "control", "id": "c_t_2"}, "value"),
        Input({"type": "control", "id": "c_d_1"}, "value"),
        Input({"type": "control", "id": "c_d_1"}, "options"),
    ],
)
def create_second_categorical_dropdown_values(
    cat_filters_toggle: list, category_x: str, category_x_options: dict
):
    if cat_filters_toggle == []:
        return ([], None)
    else:
        reduced_options = [
            option for option in category_x_options if option.get("value") != category_x
        ]
        return reduced_options, reduced_options[0].get("value")


@callback(
    [
        Output({"type": "control", "id": "c_f_2"}, "options"),
        Output({"type": "control", "id": "c_f_2"}, "value"),
    ],
    [
        Input({"type": "control", "id": "c_f_t_2"}, "value"),
        Input({"type": "control", "id": "c_t_2"}, "value"),
        Input({"type": "control", "id": "c_d_2"}, "value"),
    ],
)
def create_second_categorical_filter_values(
    second_cat_filters_toggle: list,
    second_cat_selection_toggle: list,
    second_category_x: str,
):
    if second_cat_filters_toggle == []:
        return ([], None)
    if second_cat_selection_toggle == []:
        return ([], None)
    else:
        # path to directories of files
        current_file_path = Path(__file__)
        main_directory = current_file_path.parents[2]
        metadata_directory = main_directory.joinpath("data/buildings_metadata.pkl")
        metadata_df = pd.read_pickle(metadata_directory)
        return (
            metadata_df[second_category_x].dropna().unique(),
            metadata_df[second_category_x].unique()[0],
        )


@callback(
    [
        Output({"type": "control", "id": "c_f_1"}, "options"),
        Output({"type": "control", "id": "c_f_1"}, "value"),
    ],
    [
        Input({"type": "control", "id": "c_f_t_1"}, "value"),
        Input({"type": "control", "id": "c_d_1"}, "value"),
    ],
)
def create_first_categorical_filter_values(cat_filters_toggle: list, category_x: str):
    if cat_filters_toggle == []:
        return [], None
    else:
        # path to directories of files
        current_file_path = Path(__file__)
        main_directory = current_file_path.parents[2]
        metadata_directory = main_directory.joinpath("data/buildings_metadata.pkl")
        metadata_df = pd.read_pickle(metadata_directory)
        return (
            metadata_df[category_x].dropna().unique(),
            metadata_df[category_x].unique()[0],
        )


@callback(
    [
        Output({"type": "control", "id": "m_f"}, "options"),
        Output({"type": "control", "id": "m_f"}, "value"),
    ],
    [
        Input({"type": "control", "id": "m_t"}, "value"),
    ],
)
def create_material_filter_values(mat_filters_toggle: list):
    if mat_filters_toggle == []:
        return ([], None)
    else:
        return material_list, "Concrete"


@callback(
    Output("byob_data", "data"),
    [
        Input({"type": "control", "id": "c_d_1"}, "value"),
        Input({"type": "control", "id": "i_d"}, "value"),
        Input({"type": "control", "id": "fl_no"}, "value"),
        Input({"type": "control", "id": "sc_c"}, "value"),
        Input({"type": "control", "id": "p_typ_c"}, "value"),
        Input({"type": "control", "id": "lcs_c"}, "value"),
        Input({"type": "control", "id": "c_t_1"}, "value"),
        Input({"type": "control", "id": "i_typ"}, "value"),
        Input({"type": "control", "id": "c_t_2"}, "value"),
        Input({"type": "control", "id": "c_d_2"}, "value"),
        Input({"type": "control", "id": "c_f_t_2"}, "value"),
        Input({"type": "control", "id": "c_f_2"}, "value"),
        Input({"type": "control", "id": "m_t"}, "value"),
        Input({"type": "control", "id": "m_f"}, "value"),
        Input({"type": "control", "id": "out_t"}, "value"),
        Input({"type": "control", "id": "sort_v"}, "value"),
        Input({"type": "control", "id": "c_f_1"}, "value"),
        Input({"type": "control", "id": "ln_t"}, "value"),
        Input({"type": "control", "id": "ln_v"}, "value"),
        Input({"type": "control", "id": "ln_nm"}, "value"),
    ],
)
def update_data_for_graphs_and_tables(
    category_x: str,
    objective: str,
    cfa_gfa_type: str,
    scope: list,
    proj_type: list,
    lcs: list,
    cat_selection_toggle: list,
    impact_type: int,
    second_cat_selection_toggle: list,
    second_cat_value: str,
    second_cat_filter_toggle: list,
    second_cat_filter: list,
    mat_filter_toggle: list,
    mat_filter: list,
    outlier_toggle_byob: list,
    sort_box_byob: str,
    cat_filter: list,
    ref_line_toggle: list,
    ref_line_number: float,
    ref_line_name: str,
):
    # path to directories of files
    current_file_path = Path(__file__)
    main_directory = current_file_path.parents[2]
    metadata_directory = main_directory.joinpath("data/buildings_metadata.pkl")
    impacts_directory = main_directory.joinpath(
        "data/impacts_grouped_by_lcs_and_scope.parquet"
    )

    intensity_metric_value_map = impact_dropdown_yaml.get("value_map")
    objective = intensity_metric_value_map.get(objective)

    lcs_value_map = lcs_checklist_yaml.get("value_map")
    lcs = [lcs_value_map.get(item) for item in lcs]

    scope_value_map = scope_checklist_yaml.get("value_map")
    scope = [scope_value_map.get(item) for item in scope]

    proj_type_value_map = proj_type_checklist_yaml.get("value_map")
    proj_type = [proj_type_value_map.get(item) for item in proj_type]

    # intensity metric map
    intensity_metric_map = {
        "Global Warming Potential": "gwp",
        "Material Use": "inv_mass",
        "Eutrophication Potential": "ep",
        "Acidification Potential": "ap",
        "Smog Formation Potential": "sfp",
        "Ozone Depletion Potential": "odp",
        "Non Renewable Energy Demand": "nred",
    }

    # read files
    metadata_df = pd.read_pickle(metadata_directory)
    impacts_by_lcs_scope_df = pd.read_parquet(impacts_directory)

    # new construction filter
    metadata_df = metadata_df[(metadata_df["bldg_proj_type"].isin(proj_type))]

    # cat selection toggle
    if cat_selection_toggle == [1]:
        # cat_value_filter
        if cat_filter is None:
            cat_filter = []
        elif len(cat_filter) == 0:
            cat_filter = []
        elif isinstance(cat_filter, str):
            cat_filter = [cat_filter]
            metadata_df = metadata_df[metadata_df[category_x].isin(cat_filter)]
        else:
            metadata_df = metadata_df[metadata_df[category_x].isin(cat_filter)]

    if (second_cat_filter_toggle == [1]) & (cat_selection_toggle == [1]):
        # cat_value_filter
        if second_cat_filter is None:
            second_cat_filter = []
        elif len(second_cat_filter) == 0:
            second_cat_filter = []
        elif isinstance(second_cat_filter, str):
            second_cat_filter = [second_cat_filter]
            metadata_df = metadata_df[
                metadata_df[second_cat_value].isin(second_cat_filter)
            ]
        else:
            metadata_df = metadata_df[
                metadata_df[second_cat_value].isin(second_cat_filter)
            ]

    # material selection toggle
    if mat_filter_toggle == [1]:
        # mat_value_filter
        if mat_filter is None:
            mat_filter = []
        elif len(mat_filter) == 0:
            mat_filter = []
        elif isinstance(mat_filter, str):
            mat_filter = [mat_filter]
            impacts_by_lcs_scope_df = impacts_by_lcs_scope_df[
                impacts_by_lcs_scope_df["mat_group"].isin(mat_filter)
            ]
        else:
            impacts_by_lcs_scope_df = impacts_by_lcs_scope_df[
                impacts_by_lcs_scope_df["mat_group"].isin(mat_filter)
            ]

    # filter based on LCS and omniclass element
    new_impacts = impacts_by_lcs_scope_df.loc[
        (
            (impacts_by_lcs_scope_df["life_cycle_stage"].isin(lcs))
            & (impacts_by_lcs_scope_df)["omniclass_element"].isin(scope)
        ),
    ]

    # create impacts and intensity metric
    new_impacts_gb = new_impacts.groupby("project_index")[
        intensity_metric_map.get(objective)
    ].sum()
    if cat_selection_toggle == [1]:
        if second_cat_selection_toggle == [1]:
            metadata_gb = metadata_df[
                ["project_index", category_x, second_cat_value, cfa_gfa_type]
            ]
        else:
            metadata_gb = metadata_df[["project_index", category_x, cfa_gfa_type]]
    else:
        metadata_gb = metadata_df[["project_index", cfa_gfa_type]]

    final_impacts = metadata_gb.set_index("project_index").merge(
        new_impacts_gb, how="left", left_index=True, right_index=True
    )
    if impact_type == 1:
        final_impacts[objective] = (
            final_impacts[intensity_metric_map.get(objective)]
            / final_impacts[cfa_gfa_type]
        )
    else:
        final_impacts[objective] = final_impacts[intensity_metric_map.get(objective)]

    # remove outliers
    if outlier_toggle_byob == [1]:
        Q1 = final_impacts[objective].quantile(0.25)
        Q3 = final_impacts[objective].quantile(0.75)
        IQR = Q3 - Q1
        final_impacts = final_impacts[
            (final_impacts[objective] < Q3 + 3 * IQR)
            & (final_impacts[objective] > Q1 - 3 * IQR)
        ]

    # set reference line visibility
    ref_line_toggle_boolean = False
    if ref_line_toggle == [1]:
        ref_line_toggle_boolean = True

    if cat_selection_toggle == [1]:
        final_impacts[category_x] = final_impacts[category_x].map(customwrap)
    final_impacts = final_impacts.drop(
        columns=[intensity_metric_map.get(objective), cfa_gfa_type]
    )

    # category orders
    if cat_selection_toggle == [1]:
        if sort_box_byob == "median":
            grouped_medians = (
                final_impacts[[objective, category_x]]
                .groupby(by=category_x)
                .median()
                .sort_values(by=objective, ascending=True)
            )
            category_order = grouped_medians.index.to_list()
        elif sort_box_byob == "sample_size":
            grouped_medians = (
                final_impacts[[objective, category_x]]
                .groupby(by=category_x)
                .count()
                .sort_values(by=objective, ascending=True)
            )
            category_order = grouped_medians.index.to_list()
        else:
            category_order = category_order_map.get(category_x)
            category_order = [
                item
                for item in category_order
                if item in list(final_impacts[category_x].unique())
            ]
            category_order = list(reversed(category_order))
            category_order = [customwrap(s) for s in category_order]
    else:
        category_order = []

    return {
        "byob_data": final_impacts.to_dict(),
        "impact_type": impact_type,
        "sort": category_order,
        "v_line": ref_line_toggle_boolean,
        "v_line_location": ref_line_number,
        "v_line_text": ref_line_name,
    }


@callback(
    Output("caption", "children"),
    [
        Input({"type": "control", "id": "c_d_1"}, "value"),
        Input({"type": "control", "id": "c_t_1"}, "value"),
        Input({"type": "control", "id": "c_f_1"}, "value"),
        Input({"type": "control", "id": "c_t_2"}, "value"),
        Input({"type": "control", "id": "c_d_2"}, "value"),
        Input({"type": "control", "id": "c_f_2"}, "value"),
        Input({"type": "control", "id": "m_t"}, "value"),
        Input({"type": "control", "id": "m_f"}, "value"),
        Input({"type": "control", "id": "i_d"}, "value"),
        Input({"type": "control", "id": "i_typ"}, "value"),
        Input({"type": "control", "id": "fl_no"}, "value"),
        Input({"type": "control", "id": "sc_c"}, "value"),
        Input({"type": "control", "id": "p_typ_c"}, "value"),
        Input({"type": "control", "id": "lcs_c"}, "value"),
        Input({"type": "control", "id": "out_t"}, "value"),
        Input({"type": "control", "id": "sort_v"}, "value"),
    ],
)
def create_notes_below_graph(
    category_x: str,
    cat_selection_toggle: list,
    cat_filter,
    sec_cat_selection_toggle: list,
    sec_cat_x: str,
    second_cat_filter,
    mat_filter_toggle: list,
    mat_filter,
    objective: str,
    impact_type: str,
    cfa_gfa_type: str,
    scope: list,
    proj_type: list,
    lcs: list,
    outlier_toggle_byob: list,
    sort_box_byob: str,
):

    lcs_value_map = lcs_checklist_yaml.get("value_map")
    lcs = [lcs_value_map.get(item) for item in lcs]

    scope_value_map = scope_checklist_yaml.get("value_map")
    scope = [scope_value_map.get(item) for item in scope]

    proj_type_value_map = proj_type_checklist_yaml.get("value_map")
    proj_type = [proj_type_value_map.get(item) for item in proj_type]
    if cat_selection_toggle == [1]:
        if cat_filter is None:
            cat_selection_one_text = f"- **{field_name_map.get(category_x)}**: All"
        elif len(cat_filter) == 0:
            cat_selection_one_text = f"- **{field_name_map.get(category_x)}**: All"
        elif isinstance(cat_filter, str):
            cat_selection_one_text = (
                f"- **{field_name_map.get(category_x)}**: {cat_filter}"
            )
        else:
            cat_selection_one_text = (
                f'- **{field_name_map.get(category_x)}**: {", ".join(cat_filter)}'
            )
    else:
        cat_selection_one_text = ""

    if sec_cat_selection_toggle == [1]:
        if second_cat_filter is None:
            cat_selection_two_text = f"- **{field_name_map.get(sec_cat_x)}**: All"
        elif len(second_cat_filter) == 0:
            cat_selection_two_text = f"- **{field_name_map.get(sec_cat_x)}**: All"
        elif isinstance(second_cat_filter, str):
            cat_selection_two_text = (
                f"- **{field_name_map.get(sec_cat_x)}**: {second_cat_filter}"
            )
        else:
            cat_selection_two_text = (
                f'- **{field_name_map.get(sec_cat_x)}**: {", ".join(second_cat_filter)}'
            )
    else:
        cat_selection_two_text = ""

    if mat_filter_toggle == [1]:
        if mat_filter is None:
            mat_text = "- **Material Data**: All"
        elif len(mat_filter) == 0:
            mat_text = "- **Material Data**: All"
        elif isinstance(mat_filter, str):
            mat_text = f"- **Material Data**: {mat_filter} only"
        else:
            mat_text = f'- **Material Data**: {", ".join(mat_filter)}'
    else:
        mat_text = "- **Material Data**: All"

    sorted_lcs = ", ".join(sorted(lcs))
    sorted_scope = [item for item in caption_orders.get("scope_order") if item in scope]
    sorted_proj_type = [
        item for item in caption_orders.get("proj_type_order") if item in proj_type
    ]
    sorted_scope = ", ".join(sorted_scope)
    sorted_proj_type = ", ".join(proj_type)
    if outlier_toggle_byob == [1]:
        crop_option = "have been"
    else:
        crop_option = "have not been"

    if impact_type == 1:
        impact_type_information = f"normalized by {field_name_map.get(cfa_gfa_type)}"
    else:
        impact_type_information = "not normalized by floor area"

    intensity_metric_value_map = impact_dropdown_yaml.get("value_map")
    objective = intensity_metric_value_map.get(objective)

    return [
        dcc.Markdown(
            f"""
            This box plot represents the projects plotted by {objective}. 
            The environmental metric is {impact_type_information}. The boxes are sorted 
            by {field_name_map.get(sort_box_byob)}, and outliers {crop_option} cropped. A subset of the data 
            is being displayed that represents:
            - **Life Cycle Stage(s)**: {sorted_lcs}
            - **Element Scope(s)**: {sorted_scope}
            - **Project Type(s)**: {sorted_proj_type}
            {mat_text}
            {cat_selection_one_text}
            {cat_selection_two_text}
        
            """
        )
    ]


@callback(
    Output("byob_graph", "figure"),
    Input("byob_data", "data"),
)
def update_chart(byob_data: dict):
    units_map = {
        "Global Warming Potential": "(kgCO<sub>2</sub>e)",
        "Material Use": "(kg)",
        "Eutrophication Potential": "(kgNe)",
        "Acidification Potential": "(kgSO<sub>2</sub>e)",
        "Smog Formation Potential": "(kgO<sub>3</sub>e)",
        "Ozone Depletion Potential": "(kgCFC-11e)",
        "Non Renewable Energy Demand": "(MJ)",
    }
    if byob_data.get("impact_type") == 1:
        units_map = {
            key: value.replace(")", "") + "/m<sup>2</sup>)"
            for key, value in units_map.items()
        }

    starting_df = pd.DataFrame.from_dict(byob_data.get("byob_data"))
    df = starting_df.copy()
    category_order = byob_data.get("sort")
    column_list = list(df.columns)
    if len(column_list) == 1:
        values = column_list[0]
        categories = "All"
        df[categories] = categories
    elif len(column_list) == 2:
        categories = column_list[0]
        values = column_list[1]
    else:
        categories = column_list[0]
        color_col = column_list[1]
        values = column_list[2]

    annotations = []
    max_of_df = df[values].max()
    xshift = create_graph_xshift(max_value=max_of_df)
    for s in df[categories].unique():
        if len(df[df[categories] == s]) > 0:
            annotation = {
                "showarrow": False,
                "text": f"n={str(len(df[df[categories]==s][categories]))}",
                "x": max_of_df + xshift,
                "y": str(s),
            }
            annotations.append(annotation)

    if values in [
        "Eutrophication Potential Intensity",
        "Acidification Potential Intensity",
        "Smog Formation Potential Intensity",
    ]:
        tickformat_decimal = ",.2f"
    elif values == "Ozone Depletion Potential Intensity":
        tickformat_decimal = ",.8f"
    else:
        tickformat_decimal = ",.0f"

    ref_line_location = byob_data.get("v_line_location")
    if byob_data.get("v_line_location", None) is None:
        ref_line_location = 0

    shape = {
        "label": {
            "textangle": 0,
            "textposition": "end",
            "text": byob_data.get("v_line_text"),
        },
        "line": {"color": "#AA182C", "dash": "dot"},
        "type": "line",
        "x0": ref_line_location,
        "x1": ref_line_location,
        "xref": "x",
        "y0": 0,
        "y1": 1,
        "yref": "y domain",
    }
    no_shape = {
        "line": {
            "color": "white",
        },
        "x0": 0,
        "x1": 0,
        "xref": "x",
        "y0": 0,
        "y1": 1,
        "yref": "y domain",
        "type": "line",
        "layer": "below",
    }
    grouped_boxes = []
    colors_for_grouped_boxes = [
        "#FFB71B",
        "#6E6F72",
        "#8DC6EB",
        "#AA182C",
        "#0075A9",
        "#E47E3D",
        "#4A9462",
        "#414042",
        "#31006F",
    ]
    if len(column_list) > 2:
        for unique_value, repeated_color in zip(
            df[color_col].unique(), cycle(colors_for_grouped_boxes)
        ):
            temp_box = {
                "alignmentgroup": "True",
                "boxpoints": "all",
                "hovertemplate": "Impact=%{x}<extra></extra>",
                "legendgroup": unique_value,
                "marker": {"color": repeated_color},
                "name": unique_value,
                "notched": False,
                "offsetgroup": unique_value,
                "orientation": "h",
                "showlegend": True,
                "x": df[df[color_col] == unique_value][values].values,
                "xaxis": "x",
                "y": df[df[color_col] == unique_value][categories].values,
                "yaxis": "y",
                "type": "box",
            }
            grouped_boxes.append(temp_box)
    else:
        box_list = [
            {
                "alignmentgroup": "True",
                "boxpoints": "all",
                "hovertemplate": "Impact = %{x}<extra></extra>",
                "legendgroup": "",
                "marker": {"color": "#FFB71B"},
                "name": "",
                "notched": False,
                "offsetgroup": "",
                "orientation": "h",
                "showlegend": False,
                "x0": " ",
                "xaxis": "x",
                "y0": " ",
                "yaxis": "y",
                "type": "box",
                "boxmean": True,
                "jitter": 0.5,
                "quartilemethod": "inclusive",
                "x": df[values].values,
                "y": df[categories].values,
            }
        ]

    patched_figure = Patch()
    if len(column_list) > 2:
        patched_figure["data"] = list(reversed(grouped_boxes))
    else:
        patched_figure["data"] = box_list

    patched_figure["layout"]["annotations"] = annotations
    patched_figure["layout"]["title"][
        "text"
    ] = f"{values} of {field_name_map.get(categories)}"
    patched_figure["layout"]["xaxis"]["title"][
        "text"
    ] = f"{values} {units_map.get(values)}"
    patched_figure["layout"]["xaxis"]["range"] = [0, max_of_df + xshift]
    patched_figure["layout"]["xaxis"]["tickformat"] = tickformat_decimal
    patched_figure["layout"]["yaxis"]["title"]["text"] = field_name_map.get(categories)
    patched_figure["layout"]["yaxis"]["categoryarray"] = category_order
    patched_figure["layout"]["yaxis"]["categoryorder"] = "array"
    if byob_data.get("v_line"):
        patched_figure["layout"]["shapes"][0] = shape
    else:
        patched_figure["layout"]["shapes"][0] = no_shape

    return patched_figure


@callback(
    Output("download-tbl-byob", "data"),
    [
        Input("btn-download-tbl-byob", "n_clicks"),
        State("byob_data", "data"),
    ],
    prevent_initial_call=True,
)
def create_download_table(n_clicks, byob_data):
    starting_df = pd.DataFrame.from_dict(byob_data.get("byob_data"))
    df = starting_df.copy()
    column_list = list(df.columns)
    if len(column_list) == 1:
        values = column_list[0]
        categories = "All"
        df[categories] = categories
    elif len(column_list) == 2:
        categories = column_list[0]
        values = column_list[1]
    else:
        categories = column_list[0]
        color_col = column_list[1]
        values = column_list[2]

    if len(column_list) > 2:
        groupby_cols = [categories, color_col]
    else:
        groupby_cols = categories

    tbl_df = (
        df.groupby(groupby_cols, as_index=False)[values]
        .describe()
        .rename(columns={"25%": "Q1", "50%": "median", "75%": "Q3"})
    )

    if len(column_list) > 2:
        tbl_df = tbl_df[
            [
                categories,
                color_col,
                "count",
                "std",
                "min",
                "Q1",
                "median",
                "mean",
                "Q3",
                "max",
            ]
        ]
    else:
        tbl_df = tbl_df[
            [categories, "count", "std", "min", "Q1", "median", "mean", "Q3", "max"]
        ]

    if len(column_list) > 2:
        grouped_text = f" grouped by {color_col}"
    else:
        grouped_text = ""

    return dcc.send_data_frame(
        tbl_df.to_csv, f"{categories} values by {values}{grouped_text}.csv", index=False
    )


@callback(
    Output("main-url", "hash"),
    Input({"type": "control", "id": ALL}, "value"),
)
def update_hash(_values):
    """Update the hash in the URL Location component to represent the app state.

    The app state is json serialised then base64 encoded and is treated with the
    reverse process in the layout function.
    """
    # print({inp["id"]["id"]: inp["value"] for inp in ctx.inputs_list[0]})
    if len({inp["id"]["id"]: inp["value"] for inp in ctx.inputs_list[0]}) == 0:
        return ""
    return "#" + base64.urlsafe_b64encode(
        msgpack.packb({inp["id"]["id"]: inp["value"] for inp in ctx.inputs_list[0]})
    ).decode("utf-8")
