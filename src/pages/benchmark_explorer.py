import textwrap
import base64
from pathlib import Path
import plotly.express as px
import pandas as pd
from dash import html, dcc, callback, Input, Output, State, register_page, ALL, Patch, ctx
import dash_bootstrap_components as dbc
from src.components.dropdowns import create_dropdown, create_multi_dropdown
from src.components.toggle import create_toggle
from src.components.radio_items import create_radio_items
from src.components.tooltip import create_tooltip
from src.components.checklists import create_checklist
from src.components.inputs import create_float_input, create_str_input
from src.utils.load_config import app_config
from src.utils.general import create_graph_xshift
from dash_bootstrap_templates import load_figure_template
import json

config = app_config

register_page(__name__, path='/benchmark_explorer')
load_figure_template('pulse')

categorical_dropdown_yaml = config.get('categorical_dropdown_byob')
assert categorical_dropdown_yaml is not None, 'The config for cat. dropdowns could not be set'

enable_filters_toggle_yaml = config.get('enable_filters_toggle')
assert enable_filters_toggle_yaml is not None, 'The config for cat. dropdowns could not be set'

total_impact_dropdown_yaml = config.get('total_impact_dropdown_byob')
assert total_impact_dropdown_yaml is not None, 'The config for total impacts could not be set'

lcs_checklist_yaml = config.get('lcs_checklist')
assert lcs_checklist_yaml is not None, 'The config for lcs checklist could not be set'

scope_checklist_yaml = config.get('scope_checklist')
assert scope_checklist_yaml is not None, 'The config for scope checklist could not be set'

proj_type_checklist_yaml = config.get('proj_type_checklist')
assert proj_type_checklist_yaml is not None, 'The config for proj_type checklist could not be set'

new_constr_toggle_yaml = config.get('new_constr_toggle_byob')
assert new_constr_toggle_yaml is not None, 'The config for new construction could not be set'

outlier_toggle_yaml = config.get('outlier_toggle_byob')
assert outlier_toggle_yaml is not None, 'The config for outlier toggle could not be set'

cat_selection_toggle_yaml = config.get('cat_selection_toggle_byob')
assert cat_selection_toggle_yaml is not None, 'The config for categorical selection toggle could not be set'

cat_filter_yaml = config.get('cat_filter')
assert cat_filter_yaml is not None, 'The config for cat filters could not be set'

mat_filter_toggle_yaml = config.get('mat_filter_toggle_byob')
assert mat_filter_toggle_yaml is not None, 'The config for material filter toggle could not be set'

mat_filter_yaml = config.get('mat_filter')
assert mat_filter_yaml is not None, 'The config for material filters could not be set'

floor_area_radio_yaml = config.get('floor_area_normalization_byob')
assert floor_area_radio_yaml is not None, 'The config for floor area norm. could not be set'

sort_box_radio_yaml = config.get('sort_box_plot_byob')
assert sort_box_radio_yaml is not None, 'The config for box plot sorting could not be set'

field_name_map = config.get('field_name_map')
assert field_name_map is not None, 'The config for field names could not be set'

category_order_map = config.get('category_order_map')
assert category_order_map is not None, 'The config for category orders could not be set'

line_toggle_byob_yaml = config.get("line_toggle_byob")
assert line_toggle_byob_yaml is not None, "The config for line toggle could not be set"

line_number_input_yaml = config.get("line_number_input")
assert line_number_input_yaml is not None, "The config for line number input could not be set"

line_name_input_yaml = config.get("line_name_input")
assert line_name_input_yaml is not None, "The config for line name input could not be set"

caption_orders = config.get("caption_orders")
assert caption_orders is not None, "The config for caption orders could not be set"

material_list = config.get("material_list")
assert material_list is not None, "The config for caption orders could not be set"


byob_figure = px.box(
    color_discrete_sequence=["#FFB71B"],
    height=550,
    orientation='h',
    points='all',
).update_xaxes(
    title='',
    type='linear'
).update_traces(
    quartilemethod='inclusive',
    boxmean=True,
    hovertemplate='Impact = %{x}<extra></extra>',
    jitter=0.5
).update_layout(
    margin={'pad': 10},
    font={'family': 'Source Sans Pro'}
).add_vline(
    x=0,
    line_color='white',
    layer='below'
)
# table = create_datatable(table_id='results_table_cat')

def layout(state: str = None):
    """Home page layout

    # It takes in a keyword arguments defined in `routing_callback_inputs`:
    # * state (serialised state in the URL hash), it does not trigger re-render
    # """
    # Define default state values
    defaults = {
        categorical_dropdown_yaml['dropdown_id']: categorical_dropdown_yaml['first_item'],
        lcs_checklist_yaml['checklist_id']: lcs_checklist_yaml['first_item'],
        scope_checklist_yaml['checklist_id']: scope_checklist_yaml['first_item'],
        proj_type_checklist_yaml['checklist_id']: proj_type_checklist_yaml['first_item'],
        total_impact_dropdown_yaml['dropdown_id']: total_impact_dropdown_yaml['first_item'],
        enable_filters_toggle_yaml['toggle_id']: enable_filters_toggle_yaml['first_item'],
        outlier_toggle_yaml['toggle_id']: outlier_toggle_yaml['first_item'],
        floor_area_radio_yaml['radio_id']: floor_area_radio_yaml['first_item'],
        line_toggle_byob_yaml['toggle_id']: line_toggle_byob_yaml['first_item'],
        cat_filter_yaml['dropdown_id']: [],
        cat_selection_toggle_yaml['toggle_id']: cat_selection_toggle_yaml['first_item'],
        mat_filter_toggle_yaml['toggle_id']: mat_filter_toggle_yaml['first_item']
    }
    # Decode the state from the hash
    state = defaults | (json.loads(base64.b64decode(state)) if state else {})

    categorical_dropdown = create_dropdown(
        label=categorical_dropdown_yaml['label'],
        tooltip_id=categorical_dropdown_yaml['tooltip_id'],
        dropdown_list=categorical_dropdown_yaml['dropdown_list'],
        first_item=state.get(categorical_dropdown_yaml['dropdown_id']),
        dropdown_id={"type": "control", "id": categorical_dropdown_yaml['dropdown_id']}
    )

    categorical_tooltip = create_tooltip(
        tooltip_text=categorical_dropdown_yaml['tooltip'],
        target_id=categorical_dropdown_yaml['tooltip_id']
    )

    lcs_checklist = create_checklist(
        label=lcs_checklist_yaml['label'],
        checklist=lcs_checklist_yaml['checklist'],
        first_item=state.get(lcs_checklist_yaml['checklist_id']),
        checklist_id={"type": "control", "id": lcs_checklist_yaml['checklist_id']}
    )

    scope_checklist = create_checklist(
        label=scope_checklist_yaml['label'],
        checklist=scope_checklist_yaml['checklist'],
        first_item=state.get(scope_checklist_yaml['checklist_id']),
        checklist_id={"type": "control", "id": scope_checklist_yaml['checklist_id']}
    )

    proj_type_checklist = create_checklist(
        label=proj_type_checklist_yaml['label'],
        checklist=proj_type_checklist_yaml['checklist'],
        first_item=state.get(proj_type_checklist_yaml['checklist_id']),
        checklist_id={"type": "control", "id": proj_type_checklist_yaml['checklist_id']}
    )

    total_impact_dropdown = create_dropdown(
        label=total_impact_dropdown_yaml['label'],
        tooltip_id=total_impact_dropdown_yaml['tooltip_id'],
        dropdown_list=total_impact_dropdown_yaml['dropdown_list'],
        first_item=state.get(total_impact_dropdown_yaml['dropdown_id']),
        dropdown_id={"type": "control", "id": total_impact_dropdown_yaml['dropdown_id']}
    )

    total_impact_tooltip = create_tooltip(
        tooltip_text=total_impact_dropdown_yaml['tooltip'],
        target_id=total_impact_dropdown_yaml['tooltip_id']
    )

    enable_filters_toggle = create_toggle(
        toggle_list=enable_filters_toggle_yaml['toggle_list'],
        first_item=state.get(enable_filters_toggle_yaml['toggle_id']),
        toggle_id={"type": "control", "id": enable_filters_toggle_yaml['toggle_id']},
        tooltip_id=enable_filters_toggle_yaml['tooltip_id'],
    )

    outlier_toggle = create_toggle(
        toggle_list=outlier_toggle_yaml['toggle_list'],
        first_item=state.get(outlier_toggle_yaml['toggle_id']),
        toggle_id={"type": "control", "id": outlier_toggle_yaml['toggle_id']},
        tooltip_id=outlier_toggle_yaml['tooltip_id'],
    )

    outlier_tooltip = create_tooltip(
        tooltip_text=outlier_toggle_yaml['tooltip'],
        target_id=outlier_toggle_yaml['tooltip_id']
    )

    cat_selection_toggle = create_toggle(
        toggle_list=cat_selection_toggle_yaml['toggle_list'],
        first_item=state.get(cat_selection_toggle_yaml['toggle_id']),
        toggle_id={"type": "control", "id": cat_selection_toggle_yaml['toggle_id']},
        tooltip_id=cat_selection_toggle_yaml['tooltip_id'],
    )

    mat_filter_toggle = create_toggle(
        toggle_list=mat_filter_toggle_yaml['toggle_list'],
        first_item=state.get(mat_filter_toggle_yaml['toggle_id']),
        toggle_id={"type": "other", "id": mat_filter_toggle_yaml['toggle_id']},
        tooltip_id=mat_filter_toggle_yaml['tooltip_id'],
    )

    floor_area_radio = create_radio_items(
        label=floor_area_radio_yaml['label'],
        tooltip_id=floor_area_radio_yaml['tooltip_id'],
        radio_list=floor_area_radio_yaml['radio_list'],
        first_item=state.get(floor_area_radio_yaml['radio_id']),
        radio_id={"type": "control", "id": floor_area_radio_yaml['radio_id']}
    )

    floor_area_tooltip = create_tooltip(
        tooltip_text=floor_area_radio_yaml['tooltip'],
        target_id=floor_area_radio_yaml['tooltip_id']
    )

    sort_box_radio = create_radio_items(
        label=sort_box_radio_yaml['label'],
        tooltip_id=sort_box_radio_yaml['tooltip_id'],
        radio_list=sort_box_radio_yaml['radio_list'],
        first_item=sort_box_radio_yaml['first_item'],
        radio_id=sort_box_radio_yaml['radio_id']
    )

    sort_box_tooltip = create_tooltip(
        tooltip_text=sort_box_radio_yaml['tooltip'],
        target_id=sort_box_radio_yaml['tooltip_id']
    )

    line_toggle_byob = create_toggle(
        toggle_list=line_toggle_byob_yaml['toggle_list'],
        first_item=state.get(line_toggle_byob_yaml['toggle_id']),
        toggle_id=line_toggle_byob_yaml['toggle_id'],
        tooltip_id=line_toggle_byob_yaml['tooltip_id'],
    )

    line_number_input = create_float_input(
        label=line_number_input_yaml["label"],
        placeholder=line_number_input_yaml["placeholder"],
        input_id=line_number_input_yaml["input_id"],
        tooltip_id=line_number_input_yaml["tooltip_id"]
    )

    line_name_input = create_str_input(
        label=line_name_input_yaml["label"],
        placeholder=line_name_input_yaml["placeholder"],
        input_id=line_name_input_yaml["input_id"],
        tooltip_id=line_name_input_yaml["tooltip_id"]
    )

    categorical_filter = create_multi_dropdown(
        label=cat_filter_yaml["label"],
        tooltip_id=cat_filter_yaml["tooltip_id"],
        dropdown_id={"type": "other", "id": cat_filter_yaml["dropdown_id"]},
        placeholder="If enabled, please select a filter"
    )

    material_filter = create_multi_dropdown(
        label=mat_filter_yaml["label"],
        tooltip_id=mat_filter_yaml["tooltip_id"],
        dropdown_id={"type": "other", "id": mat_filter_yaml["dropdown_id"]},
        placeholder="If enabled, please select a filter"
    )

    controls_byob = dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    total_impact_dropdown,
                    total_impact_tooltip,
                    lcs_checklist,
                    scope_checklist,
                    proj_type_checklist
                ],            
                title="Impact Controls",
                item_id='proj_filters'
            ),
            dbc.AccordionItem(
                [
                    cat_selection_toggle,
                    categorical_dropdown,
                    categorical_tooltip,
                    enable_filters_toggle,
                    categorical_filter,
                    mat_filter_toggle,
                    material_filter
                ],
                title="Categorical Controls",
                item_id='axis_controls'
            ),
            dbc.AccordionItem(
                [
                    floor_area_radio,
                    floor_area_tooltip,
                    sort_box_radio,
                    sort_box_tooltip,
                    outlier_toggle,
                    outlier_tooltip,
                    
                ],            
                title="Additional Filters",
                item_id='addl_filters'
            ),
            dbc.AccordionItem(
                [
                    line_toggle_byob,
                    line_number_input,
                    line_name_input
                ],
                title="Reference Line",
                item_id='ref_line'
            )
        ],
        start_collapsed=True,
        always_open=True,
        active_item=['axis_controls', 'proj_filters', 'addl_filters', 'ref_line'],
        class_name='overflow-scroll h-100',
    )

    return html.Div(
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            controls_byob
                        ], xs=4, sm=4, md=4, lg=4, xl=3, xxl=3,
                        style={'max-height': '750px'}
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(figure=byob_figure, id="byob_graph"),
                            html.Div(id='help_div'),
                            html.Div([
                                dbc.Button(
                                    "Download Table Contents",
                                    color='primary',
                                    id="btn-download-tbl-byob",
                                    active=True,
                                    className='my-2 fw-bold'
                                ),
                                dcc.Download(id="download-tbl-byob"),
                            ])
                        ], xs=8, sm=8, md=8, lg=8, xl=7, xxl=7,
                    ),
                ],
                justify='center',
                className='mb-4'
            ),
        ],
    )


@callback(
    Output({"type": "other", "id": 'cat_filter'}, 'disabled'),
    Input({"type": "control", "id": 'enable_filters_toggle'}, 'value')
)
def enable_filters(enable_filters_toggle):
    if enable_filters_toggle == []:
        return True
    else:
        return False
    

@callback(
    Output({"type": "other", "id": 'mat_filter'}, 'disabled'),
    Input({"type": "other", "id": 'mat_filter_toggle_byob'}, 'value')
)
def enable_filters(enable_filters_toggle):
    if enable_filters_toggle == []:
        return True
    else:
        return False
    

@callback(
    [
        Output('line_number_input', 'disabled'),
        Output('line_name_input', 'disabled'),
    ],
    Input("ref_line_toggle", 'value')
)
def enable_filters(enable_filters_toggle):
    if enable_filters_toggle == []:
        return True, True
    else:
        return False, False


@callback(
    [
        Output({"type": "other", "id": 'cat_filter'}, 'options'),
        Output({"type": "other", "id": 'cat_filter'}, 'value')
    ],
    [
        Input({"type": "control", "id": 'enable_filters_toggle'}, 'value'),
        Input({"type": "control", "id": 'categorical_dropdown_byob'}, 'value')
    ]
)
def add_filter_dropdown(cat_filters_toggle: list,
                        category_x: str):
    if cat_filters_toggle == []:
        return ([], None)
    else:
        # path to directories of files
        current_file_path = Path(__file__)
        main_directory = current_file_path.parents[2]
        metadata_directory = main_directory.joinpath('data/buildings_metadata.pkl')
        metadata_df = pd.read_pickle(metadata_directory)
        metadata_df = metadata_df[
            (metadata_df['bldg_proj_type'] == 'New Construction')
        ]
        return metadata_df[category_x].dropna().unique(), metadata_df[category_x].unique()[0]


@callback(
    [
        Output({"type": "other", "id": 'mat_filter'}, 'options'),
        Output({"type": "other", "id": 'mat_filter'}, 'value')
    ],
    [
        Input({"type": "other", "id": 'mat_filter_toggle_byob'}, 'value'),
    ]
)
def add_filter_dropdown(mat_filters_toggle: list):
    if mat_filters_toggle == []:
        return ([], None)
    else:
        return material_list, "Concrete"


@callback(
    Output('byob_data', 'data'),
    [
        Input({"type": "control", "id": 'categorical_dropdown_byob'}, 'value'),
        Input({"type": "control", "id": 'total_impact_dropdown_byob'}, 'value'),
        Input({"type": "control", "id": 'floor_area_normal_byob'}, 'value'),
        Input({"type": "control", "id": 'scope_checklist'}, 'value'),
        Input({"type": "control", "id": 'proj_type_checklist'}, 'value'),
        Input({"type": "control", "id": "lcs_checklist"}, 'value'),
        Input({"type": "control", "id": "cat_selection_toggle_byob"}, "value"),
        Input({"type": "other", "id": "mat_filter_toggle_byob"}, "value"),
        Input({"type": "other", "id": "mat_filter"}, "value"),
        Input({"type": "control", "id": 'outlier_toggle_byob'}, 'value'),
        Input('sort_box_plot_byob', 'value'),
        Input({"type": "other", "id": 'cat_filter'}, 'value'),
        Input("ref_line_toggle", 'value'),
        Input("line_number_input", 'value'),
        Input("line_name_input", 'value')
    ]
)
def update_data_for_byob(category_x: str,
                         objective: str,
                         cfa_gfa_type: str,
                         scope: list,
                         proj_type: list,
                         lcs: list,
                         cat_selection_toggle: list,
                         mat_filter_toggle: list,
                         mat_filter: list,
                         outlier_toggle_byob: list,
                         sort_box_byob: str,
                         cat_filter: list,
                         ref_line_toggle: list,
                         ref_line_number: float,
                         ref_line_name: str
                         ):
    # path to directories of files
    current_file_path = Path(__file__)
    main_directory = current_file_path.parents[2]
    metadata_directory = main_directory.joinpath('data/buildings_metadata.pkl')
    impacts_directory = main_directory.joinpath('data/impacts_grouped_by_lcs_and_scope.parquet')

    # intensity metric map
    intensity_metric_map = {
        "Embodied Carbon Intensity": "gwp",
        "Eutrophication Potential Intensity": "ep",
        "Acidification Potential Intensity": "ap",
        "Smog Formation Potential Intensity": "sfp",
        "Ozone Depletion Potential Intensity": "odp",
        "Natural Resource Depletion Intensity": "nred",
    }

    # read files
    metadata_df = pd.read_pickle(metadata_directory)
    impacts_by_lcs_scope_df = pd.read_parquet(impacts_directory)

    # new construction filter
    metadata_df = metadata_df[
        (metadata_df['bldg_proj_type'].isin(proj_type))
    ]

    # cat selection toggle
    if cat_selection_toggle == [1]:
        # cat_value_filter
        if cat_filter is None:
            cat_filter = []
        elif len(cat_filter) == 0:
            cat_filter = []
        elif isinstance(cat_filter, str):
            cat_filter = [cat_filter]
            metadata_df = metadata_df[
                metadata_df[category_x].isin(cat_filter)
            ]
        else: 
            metadata_df = metadata_df[
                metadata_df[category_x].isin(cat_filter)
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
        ((impacts_by_lcs_scope_df['life_cycle_stage'].isin(lcs))
        & (impacts_by_lcs_scope_df)['omniclass_element'].isin(scope)), 
    ]

    # create impacts and intensity metric
    new_impacts_gb = new_impacts.groupby('project_index')[intensity_metric_map.get(objective)].sum()
    if cat_selection_toggle == [1]:
        metadata_gb = metadata_df[['project_index', category_x, cfa_gfa_type]]
    else: 
        metadata_gb =  metadata_df[['project_index', cfa_gfa_type]]

    final_impacts = metadata_gb.set_index('project_index').merge(
        new_impacts_gb,
        how='left',
        left_index=True,
        right_index=True
    )
    final_impacts[objective] = final_impacts[intensity_metric_map.get(objective)] / final_impacts[cfa_gfa_type]

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
    

    # wrap text for formatting
    def customwrap(s, width=25):
        if type(s) is not float:
            return "<br>".join(textwrap.wrap(s, width=width))
    if cat_selection_toggle == [1]:
        final_impacts[category_x] = final_impacts[category_x].map(customwrap)
    final_impacts = final_impacts.drop(columns=[intensity_metric_map.get(objective), cfa_gfa_type])

    # category orders
    if cat_selection_toggle == [1]:
        if sort_box_byob == 'median':
            grouped_medians = (
                final_impacts.groupby(by=category_x)
                .median()
                .sort_values(
                    by=objective,
                    ascending=True
                )
            )
            category_order = grouped_medians.index.to_list()
        elif sort_box_byob == 'sample_size':
            grouped_medians = (
                final_impacts.groupby(by=category_x)
                .count()
                .sort_values(
                    by=objective,
                    ascending=True
                )
            )
            category_order = grouped_medians.index.to_list()
        else:
            category_order = category_order_map.get(category_x)
            category_order = [item for item in category_order if item in list(final_impacts[category_x].unique())]
            category_order = list(reversed(category_order))
            category_order = [customwrap(s) for s in category_order]
    else:
        category_order = []
    

    return {
        'byob_data': final_impacts.to_dict(),
        'sort': category_order,
        'v_line': ref_line_toggle_boolean,
        'v_line_location': ref_line_number,
        'v_line_text': ref_line_name
    }


@callback(
    Output('help_div', 'children'),
    [
        Input({"type": "control", "id": 'categorical_dropdown_byob'}, 'value'),
        Input({"type": "control", "id": 'total_impact_dropdown_byob'}, 'value'),
        Input({"type": "control", "id": 'floor_area_normal_byob'}, 'value'),
        Input({"type": "control", "id": 'scope_checklist'}, 'value'),
        Input({"type": "control", "id": 'proj_type_checklist'}, 'value'),
        Input({"type": "control", "id": "lcs_checklist"}, 'value'),
        Input({"type": "control", "id": 'outlier_toggle_byob'}, 'value'),
        Input('sort_box_plot_byob', 'value'),
    ]
)
def create_notes_below_graph(category_x: str,
                             objective: str,
                             cfa_gfa_type: str,
                             scope: list,
                             proj_type: list,
                             lcs: list,
                             outlier_toggle_byob: list,
                             sort_box_byob: str,):
    
    sorted_lcs = ", ".join(sorted(lcs))
    sorted_scope = [item for item in caption_orders.get('scope_order') if item in scope]
    sorted_proj_type = [item for item in caption_orders.get('proj_type_order') if item in proj_type]
    sorted_scope = ", ".join(sorted_scope)
    sorted_proj_type = ", ".join(proj_type)
    if outlier_toggle_byob == [1]:
        crop_option = "have been"
    else:
        crop_option = "have not been"
    
    return [
        dcc.Markdown(
            f"""
            This box plot represents the {field_name_map.get(category_x)} plotted by {objective}. 
            The environmental metric is normalized by {field_name_map.get(cfa_gfa_type)}. The boxes are sorted 
            by {field_name_map.get(sort_box_byob)}, and outliers {crop_option} cropped. The following
            additional metrics have been selected:
            - **Life Cycle Stages**: {sorted_lcs}
            - **Element Scopes**: {sorted_scope}
            - **Project Types**: {sorted_proj_type}
            """
        )
    ]


    
@callback(
    Output('byob_graph', 'figure'),
    Input('byob_data', 'data'),
)
def update_chart(byob_data: dict):
    units_map = {
        "Embodied Carbon Intensity": '(kgCO<sub>2</sub>e/m<sup>2</sup>)',
        "Eutrophication Potential Intensity": '(kgNe/m<sup>2</sup>)',
        "Acidification Potential Intensity": '(kgSO<sub>2</sub>e/m<sup>2</sup>)',
        "Smog Formation Potential Intensity": '(kgO<sub>3</sub>e/m<sup>2</sup>)',
        "Ozone Depletion Potential Intensity": '(CFC-11e/m<sup>2</sup>)',
        "Natural Resource Depletion Intensity": '(MJ/m<sup>2</sup>)',
        # 'ec_per_occupant': '(kgCO<sub>2</sub>e/occupant)',
        # 'ec_per_res_unit': '(kgCO<sub>2</sub>e/residential unit)',
    }

    df = pd.DataFrame.from_dict(byob_data.get('byob_data'))
    category_order = byob_data.get('sort')
    column_list = list(df.columns)
    if len(column_list) == 1:
        values = column_list[0]
        categories = "All"
        df[categories] = categories
    else:
        categories = column_list[0]
        values = column_list[1]
    
    annotations = []
    max_of_df = df[values].max()
    xshift = create_graph_xshift(max_value=max_of_df)
    for s in df[categories].unique():
        if len(df[df[categories] == s]) > 0:
            annotation = {
                'showarrow': False,
                'text': f'n={str(len(df[df[categories]==s][categories]))}',
                'x': max_of_df+xshift,
                'y': str(s),
            }
            annotations.append(annotation)
    
    if values in [
        'Eutrophication Potential Intensity',
        'Acidification Potential Intensity',
        'Smog Formation Potential Intensity'
    ]:
        tickformat_decimal =',.2f'
    elif values == 'Ozone Depletion Potential Intensity':
        tickformat_decimal =',.8f'
    else:
        tickformat_decimal =',.0f'

    ref_line_location = byob_data.get("v_line_location")
    if byob_data.get("v_line_location", None) is None:
        ref_line_location = 0
        
    shape = {
        "label": {
          "textangle": 0,
          "textposition": "end",
          "text": byob_data.get("v_line_text")
        },
        "line": {
          "color": "#AA182C",
          "dash": "dot"
        },
        "type": "line",
        "x0": ref_line_location,
        "x1": ref_line_location,
        "xref": "x",
        "y0": 0,
        "y1": 1,
        "yref": "y domain"
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
        "layer": "below"
    }

    patched_figure = Patch()
    patched_figure["data"][0]["x"] = df[values].values
    patched_figure["data"][0]["y"] = df[categories].values

    patched_figure["layout"]["annotations"] = annotations
    patched_figure["layout"]["title"]["text"] = f"{values} of {field_name_map.get(categories)}"
    patched_figure["layout"]["xaxis"]["title"]["text"] = f"{values} {units_map.get(values)}"
    patched_figure["layout"]["xaxis"]["range"] = [0, max_of_df+xshift]
    patched_figure["layout"]["xaxis"]["tickformat"] = tickformat_decimal
    patched_figure["layout"]["yaxis"]["title"]["text"] = field_name_map.get(categories)
    patched_figure["layout"]["yaxis"]["categoryarray"] = category_order
    patched_figure["layout"]["yaxis"]["categoryorder"] = "array"
    if byob_data.get('v_line'):
        patched_figure["layout"]["shapes"][0] = shape
    else: 
        patched_figure["layout"]["shapes"][0] = no_shape

    return patched_figure


# @callback(
#     Output('help_div', 'children'),
#     Input('byob_graph', 'figure')
# )
# def test_one(figure_data):
#     print(json.dumps(figure_data, indent=2))
#     return json.dumps(figure_data, indent=2)


@callback(
    Output("download-tbl-byob", "data"),
    [
        Input("btn-download-tbl-byob", "n_clicks"),
        State('byob_data', 'data'),
    ],
    prevent_initial_call=True,
)
def create_download_table(n_clicks,
                          byob_data):
    df = pd.DataFrame.from_dict(byob_data.get('byob_data'))    
    column_list = list(df.columns)
    categories = column_list[0]
    values = column_list[1]

    tbl_df = (
        df.groupby(
            categories, as_index=False
        )[values]
        .describe()
        .rename(
            columns={
                '50%': 'median',
            }
        ).drop(
            columns=[
                'count',
                '25%',
                '75%'
            ]
        )
    )

    tbl_df = pd.merge(
        left=tbl_df,
        right=df[categories].value_counts(),
        how='left',
        left_on=categories,
        right_on=categories
    )
    tbl_df = pd.merge(
        left=tbl_df,
        right=df.groupby(categories)[values].quantile(0.2).rename('20%'),
        how='left',
        left_on=categories,
        right_on=categories
    )
    tbl_df = pd.merge(
        left=tbl_df,
        right=df.groupby(categories)[values].quantile(0.25).rename('Q1'),
        how='left',
        left_on=categories,
        right_on=categories
    )
    tbl_df = pd.merge(
        left=tbl_df,
        right=df.groupby(categories)[values].quantile(0.75).rename('Q3'),
        how='left',
        left_on=categories,
        right_on=categories
    )
    tbl_df = pd.merge(
        left=tbl_df,
        right=df.groupby(categories)[values].quantile(0.8).rename('80%'),
        how='left',
        left_on=categories,
        right_on=categories
    )
    tbl_df = tbl_df[
        [
            categories,
            'count',
            'std',
            'min',
            '20%',
            'Q1',
            'median',
            'mean',
            'Q3',
            '80%',
            'max'
        ]
    ]

    return dcc.send_data_frame(
        tbl_df.to_csv,
        f"{categories} values by {values}.csv",
        index=False
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
    return "#" + base64.urlsafe_b64encode(
        json.dumps({inp["id"]["id"]: inp["value"] for inp in ctx.inputs_list[0]})
        .encode("utf-8")
    ).decode("utf-8")
