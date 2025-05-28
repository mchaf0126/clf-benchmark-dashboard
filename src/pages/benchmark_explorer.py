import textwrap
import base64
from pathlib import Path
import plotly.express as px
import pandas as pd
from dash import html, dcc, callback, Input, Output, State, register_page, ALL, Patch, ctx
import dash_bootstrap_components as dbc
from src.components.dropdowns import create_dropdown
from src.components.toggle import create_toggle
from src.components.radio_items import create_radio_items
from src.components.tooltip import create_tooltip
from src.components.checklists import create_checklist
from src.components.datatable import create_datatable, \
    create_float_table_entry, create_string_table_entry, create_int_table_entry
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

floor_area_radio_yaml = config.get('floor_area_normalization_byob')
assert floor_area_radio_yaml is not None, 'The config for floor area norm. could not be set'

sort_box_radio_yaml = config.get('sort_box_plot_byob')
assert sort_box_radio_yaml is not None, 'The config for box plot sorting could not be set'

field_name_map = config.get('field_name_map')
assert field_name_map is not None, 'The config for field names could not be set'

category_order_map = config.get('category_order_map')
assert category_order_map is not None, 'The config for category orders could not be set'


byob_figure = px.box(
    color_discrete_sequence=["#FFB71B"],
    height=600,
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
        "cat_filter": []
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

    categorical_filter = html.Div(
        [
            dbc.Label(
                [
                    "Categorical values to filter",
                    html.Span(
                        ' 🛈',
                        id='cat_filter_tooltip_id'
                    )
                ]
            ),
            dcc.Dropdown(
                id={"type": "other", "id": 'cat_filter'},
                value=state.get('cat_filter'),
                multi=True,
                clearable=False,
                persistence=True,
                optionHeight=80,
                placeholder='If enabled, please select a filter'
            ),
        ],
        className='mb-4'
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
                    categorical_dropdown,
                    categorical_tooltip,
                    enable_filters_toggle,
                    categorical_filter
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
                    outlier_tooltip
                ],            
                title="Additional Filters",
                item_id='addl_filters'
            ),
        ],
        start_collapsed=True,
        always_open=True,
        active_item=['axis_controls', 'proj_filters', 'addl_filters'],
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
                        style={'max-height': '700px'}
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(figure=byob_figure, id="byob_graph"),
                            html.Div([
                                dbc.Button(
                                    "Download Table Contents",
                                    color='primary',
                                    id="btn-download-tbl-byob",
                                    active=True,
                                    className='my-2 fw-bold'
                                ),
                                dcc.Download(id="download-tbl-byob"),
                            ]),
                            html.Div(id='help_div')
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
            & (metadata_df['bldg_prim_use'] != "Parking")
        ]
        return metadata_df[category_x].dropna().unique(), metadata_df[category_x].unique()[0]


@callback(
    Output('byob_data', 'data'),
    [
        Input({"type": "control", "id": 'categorical_dropdown_byob'}, 'value'),
        Input({"type": "control", "id": 'total_impact_dropdown_byob'}, 'value'),
        Input({"type": "control", "id": 'floor_area_normal_byob'}, 'value'),
        Input({"type": "control", "id": 'scope_checklist'}, 'value'),
        Input({"type": "control", "id": 'proj_type_checklist'}, 'value'),
        Input({"type": "control", "id": "lcs_checklist"}, 'value'),
        Input({"type": "control", "id": 'outlier_toggle_byob'}, 'value'),
        Input('sort_box_plot_byob', 'value'),
        Input({"type": "other", "id": 'cat_filter'}, 'value')
    ]
)
def update_data_for_byob(category_x: str,
                         objective: str,
                         cfa_gfa_type: str,
                         scope: list,
                         proj_type: list,
                         lcs: list,
                         outlier_toggle_byob: list,
                         sort_box_byob: str,
                         cat_filter: list):
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

    # # turn checklists into workable lists
    # lcs = sum(lcs, [])
    # scope = sum(scope, [])

    # new construction filter
    metadata_df = metadata_df[
        (metadata_df['bldg_proj_type'].isin(proj_type))
        & (metadata_df['bldg_prim_use'] != "Parking")
    ]

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

    # filter based on LCS and omniclass element
    new_impacts = impacts_by_lcs_scope_df.loc[
        ((impacts_by_lcs_scope_df['life_cycle_stage'].isin(lcs))
        & (impacts_by_lcs_scope_df)['omniclass_element'].isin(scope)), :
    ]

    # create impacts and intensity metric
    new_impacts_gb = new_impacts.groupby('project_index')[intensity_metric_map.get(objective)].sum()
    final_impacts = metadata_df[['project_index', category_x, cfa_gfa_type]].set_index('project_index').merge(
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

    # wrap text for formatting
    def customwrap(s, width=25):
        if type(s) is not float:
            return "<br>".join(textwrap.wrap(s, width=width))
    final_impacts[category_x] = final_impacts[category_x].map(customwrap)
    final_impacts = final_impacts.drop(columns=[intensity_metric_map.get(objective), cfa_gfa_type])

    # category orders
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
        category_order = list(reversed(category_order))
        category_order = [customwrap(s) for s in category_order]

    return {
        'byob_data': final_impacts.to_dict(),
        'sort': category_order
    }

    
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

    patched_figure = Patch()
    patched_figure["data"][0]["x"] = df[values].values
    patched_figure["data"][0]["y"] = df[categories].values

    patched_figure["layout"]["annotations"] = annotations
    patched_figure["layout"]["xaxis"]["title"]["text"] = f"{values} {units_map.get(values)}"
    patched_figure["layout"]["xaxis"]["range"] = [0, max_of_df+xshift]
    patched_figure["layout"]["xaxis"]["tickformat"] = tickformat_decimal
    patched_figure["layout"]["yaxis"]["title"]["text"] = field_name_map.get(categories)
    patched_figure["layout"]["yaxis"]["categoryarray"] = category_order
    patched_figure["layout"]["yaxis"]["categoryorder"] = "array"
    patched_figure["layout"]["font"]["family"] = "Source Sans Pro"

    return patched_figure


@callback(
    Output('help_div', 'children'),
    Input('byob_figure', 'figure')
)
def test_one(figure_data):
    return json.dumps(figure_data, indent=2)


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
