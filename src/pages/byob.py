import textwrap
from pathlib import Path
import plotly.express as px
import pandas as pd
from dash import html, dcc, callback, Input, Output, State, register_page, ALL, Patch
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

config = app_config

register_page(__name__, path='/byob')
load_figure_template('pulse')

categorical_dropdown_yaml = config.get('categorical_dropdown_byob')
assert categorical_dropdown_yaml is not None, 'The config for cat. dropdowns could not be set'

total_impact_dropdown_yaml = config.get('total_impact_dropdown_byob')
assert total_impact_dropdown_yaml is not None, 'The config for total impacts could not be set'

lcs_checklist_yaml = config.get('lcs_checklist')
assert lcs_checklist_yaml is not None, 'The config for lcs checklist could not be set'

scope_checklist_yaml = config.get('scope_checklist')
assert scope_checklist_yaml is not None, 'The config for scope checklist could not be set'

new_constr_toggle_yaml = config.get('new_constr_toggle_byob')
assert new_constr_toggle_yaml is not None, 'The config for new construction could not be set'

outlier_toggle_yaml = config.get('outlier_toggle_byob')
assert outlier_toggle_yaml is not None, 'The config for outlier toggle could not be set'

floor_area_radio_yaml = config.get('floor_area_normalization_byob')
assert floor_area_radio_yaml is not None, 'The config for floor area norm. could not be set'

# sort_box_radio_yaml = config.get('sort_box_plot_cat')
# assert sort_box_radio_yaml is not None, 'The config for box plot sorting could not be set'

field_name_map = config.get('field_name_map')
assert field_name_map is not None, 'The config for field names could not be set'

# category_order_map = config.get('category_order_map')
# assert category_order_map is not None, 'The config for category orders could not be set'

# cfa_gfa_map = config.get('cfa_gfa_map')
# assert cfa_gfa_map is not None, 'The config for cfa/gfa map could not be set'

categorical_dropdown = create_dropdown(
    label=categorical_dropdown_yaml['label'],
    tooltip_id=categorical_dropdown_yaml['tooltip_id'],
    dropdown_list=categorical_dropdown_yaml['dropdown_list'],
    first_item=categorical_dropdown_yaml['first_item'],
    dropdown_id=categorical_dropdown_yaml['dropdown_id']
)

categorical_tooltip = create_tooltip(
    tooltip_text=categorical_dropdown_yaml['tooltip'],
    target_id=categorical_dropdown_yaml['tooltip_id']
)

lcs_checklist = create_checklist(
    label=lcs_checklist_yaml['label'],
    checklist=lcs_checklist_yaml['checklist'],
    first_item=lcs_checklist_yaml['first_item'],
    checklist_id={"type": "lcs", "id": 'lcs_checklist'}
)

scope_checklist = create_checklist(
    label=scope_checklist_yaml['label'],
    checklist=scope_checklist_yaml['checklist'],
    first_item=scope_checklist_yaml['first_item'],
    checklist_id={"type": "scope", "id": 'scope_checklist'}
)

total_impact_dropdown = create_dropdown(
    label=total_impact_dropdown_yaml['label'],
    tooltip_id=total_impact_dropdown_yaml['tooltip_id'],
    dropdown_list=total_impact_dropdown_yaml['dropdown_list'],
    first_item=total_impact_dropdown_yaml['first_item'],
    dropdown_id=total_impact_dropdown_yaml['dropdown_id']
)

total_impact_tooltip = create_tooltip(
    tooltip_text=total_impact_dropdown_yaml['tooltip'],
    target_id=total_impact_dropdown_yaml['tooltip_id']
)

new_constr_toggle = create_toggle(
    toggle_list=new_constr_toggle_yaml['toggle_list'],
    first_item=new_constr_toggle_yaml['first_item'],
    toggle_id=new_constr_toggle_yaml['toggle_id'],
    tooltip_id=new_constr_toggle_yaml['tooltip_id'],
)

new_constr_tooltip = create_tooltip(
    tooltip_text=new_constr_toggle_yaml['tooltip'],
    target_id=new_constr_toggle_yaml['tooltip_id']
)

outlier_toggle = create_toggle(
    toggle_list=outlier_toggle_yaml['toggle_list'],
    first_item=outlier_toggle_yaml['first_item'],
    toggle_id=outlier_toggle_yaml['toggle_id'],
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
    first_item=floor_area_radio_yaml['first_item'],
    radio_id=floor_area_radio_yaml['radio_id']
)

floor_area_tooltip = create_tooltip(
    tooltip_text=floor_area_radio_yaml['tooltip'],
    target_id=floor_area_radio_yaml['tooltip_id']
)

# sort_box_radio = create_radio_items(
#     label=sort_box_radio_yaml['label'],
#     tooltip_id=sort_box_radio_yaml['tooltip_id'],
#     radio_list=sort_box_radio_yaml['radio_list'],
#     first_item=sort_box_radio_yaml['first_item'],
#     radio_id=sort_box_radio_yaml['radio_id']
# )

# sort_box_tooltip = create_tooltip(
#     tooltip_text=sort_box_radio_yaml['tooltip'],
#     target_id=sort_box_radio_yaml['tooltip_id']
# )

controls_byob = dbc.Accordion(
    [
        dbc.AccordionItem(
            [
                categorical_dropdown,
                categorical_tooltip,
                total_impact_dropdown,
                total_impact_tooltip,
            ],
            title="Axis Controls",
            item_id='axis_controls'
        ),
        dbc.AccordionItem(
            [
                lcs_checklist,
                scope_checklist,
            ],            
            title="Project Filters",
            item_id='proj_filters'
        ),
        dbc.AccordionItem(
            [
                floor_area_radio,
                floor_area_tooltip,
                # sort_box_radio,
                # sort_box_tooltip,
                # new_constr_toggle,
                # new_constr_tooltip,
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

byob_figure = px.box(
    color_discrete_sequence=["#ffc700"],
    height=600,
).update_xaxes(
    tickformat=',.0f',
    title='',
    type='linear'
).update_traces(
    quartilemethod='inclusive',
).update_layout(
    margin={'pad': 10},
)
# table = create_datatable(table_id='results_table_cat')

layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        controls_byob
                    ], xs=4, sm=4, md=4, lg=4, xl=3, xxl=3,
                    style={'max-height': '800px'}
                ),
                dbc.Col(
                    [
                        dcc.Graph(figure=byob_figure, id="byob_graph"),
                    ], xs=8, sm=8, md=8, lg=8, xl=7, xxl=7,
                ),
            ],
            justify='center',
            className='mb-4'
        ),
#         dbc.Row(
#             dbc.Col(
#                 html.Div([
#                     dbc.Button(
#                         "Download Table Contents",
#                         color='primary',
#                         id="btn-download-tbl-box",
#                         active=True,
#                         className='my-2 fw-bold'
#                     ),
#                     dcc.Download(id="download-tbl-box"),
#                     table,
#                 ]),
#                 xs=12, sm=12, md=12, lg=12, xl=8, xxl=8,
#             ),
#             justify='center',
#             className='mb-4'
#         )
    ],
)


@callback(
    Output('byob_data', 'data'),
    [
        Input('categorical_dropdown_byob', 'value'),
        Input('total_impact_dropdown_byob', 'value'),
        Input('floor_area_normal_byob', 'value'),
        Input({'type': 'lcs', 'id': ALL}, 'value'),
        Input({'type': 'scope', 'id': ALL}, 'value'),
        Input('outlier_toggle_byob', 'value')
    ]
)
def update_data_for_byob(category_x: str,
                         objective: str,
                         cfa_gfa_type: str,
                         lcs: list,
                         scope: list,
                         outlier_toggle_byob: list):
    # path to directories of files
    current_file_path = Path(__file__)
    main_directory = current_file_path.parents[2]
    metadata_directory = main_directory.joinpath('data/buildings_metadata.pkl')
    impacts_directory = main_directory.joinpath('data/impacts_grouped_by_lcs_and_scope.parquet')

    # read files
    metadata_df = pd.read_pickle(metadata_directory)
    impacts_by_lcs_scope_df = pd.read_parquet(impacts_directory)

    # turn checklists into workable lists
    lcs = sum(lcs, [])
    scope = sum(scope, [])

    # new construction filter
    # if new_constr_toggle_byob == [1]:
    metadata_df = metadata_df[metadata_df['bldg_proj_type'] == 'New Construction']

    # filter based on LCS and omniclass element
    new_impacts = impacts_by_lcs_scope_df.loc[
        ((impacts_by_lcs_scope_df['life_cycle_stage'].isin(lcs))
        & (impacts_by_lcs_scope_df)['omniclass_element'].isin(scope)), :
    ]

    # create impacts and intensity metric
    new_impacts_gb = new_impacts.groupby('project_index')[objective].sum()
    final_impacts = metadata_df[['project_index', category_x, cfa_gfa_type]].set_index('project_index').merge(
        new_impacts_gb,
        how='left',
        left_index=True,
        right_index=True
    )
    final_impacts['intensity'] = final_impacts[objective] / final_impacts[cfa_gfa_type]

    # remove outliers
    if outlier_toggle_byob == [1]:
        Q1 = final_impacts['intensity'].quantile(0.25)
        Q3 = final_impacts['intensity'].quantile(0.75)
        IQR = Q3 - Q1
        final_impacts = final_impacts[
            (final_impacts['intensity'] < Q3 + 3 * IQR)
            & (final_impacts['intensity'] > Q1 - 3 * IQR)
        ]

    # wrap text for formatting
    def customwrap(s, width=25):
        if type(s) is not float:
            return "<br>".join(textwrap.wrap(s, width=width))
    final_impacts[category_x] = final_impacts[category_x].map(customwrap)
    final_impacts = final_impacts.drop(columns=[objective, cfa_gfa_type])

    return {'byob_data': final_impacts.to_dict()}
    
@callback(
    Output('byob_graph', 'figure'),
    Input('byob_data', 'data'),
)
def update_chart(byob_data: dict):
    # if new_constr_toggle_cat == [1]:
    #     df = df[df['bldg_proj_type'] == 'New Construction']
    # units_map = {
    #     'eci': '(kgCO<sub>2</sub>e/m<sup>2</sup>)',
    #     'epi': '(kgNe/m<sup>2</sup>)',
    #     'api': '(kgSO<sub>2</sub>e/m<sup>2</sup>)',
    #     'sfpi': '(kgO<sub>3</sub>e/m<sup>2</sup>)',
    #     'odpi': '(CFC-11e/m<sup>2</sup>)',
    #     'nredi': '(MJ/m<sup>2</sup>)',
    #     'ec_per_occupant': '(kgCO<sub>2</sub>e/occupant)',
    #     'ec_per_res_unit': '(kgCO<sub>2</sub>e/residential unit)',
    # }
#     cfa_gfa_mapping = cfa_gfa_map.get(cfa_gfa_type)
#     # cfa_gfa_name_for_annotation = cfa_gfa_mapping.get('name')
#     objective_for_graph = cfa_gfa_mapping.get(objective)

#     if sort_type == 'median':
#         grouped_medians = (
#             df[[category_x, objective_for_graph]]
#             .groupby(by=category_x)
#             .median()
#             .sort_values(
#                 by=objective_for_graph,
#                 ascending=False
#             )
#         )
#         category_order = grouped_medians.index.to_list()
#     else:
#         category_order = category_order_map.get(category_x)

    df = pd.DataFrame.from_dict(byob_data.get('byob_data'))    
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
    # wrapped_category_order = [customwrap(s) for s in category_order]

    patched_figure = Patch()
    patched_figure["data"][0]["x"] = df[values].values
    patched_figure["data"][0]["y"] = df[categories].values
    patched_figure["data"][0]["orientation"] = 'h'

    patched_figure["layout"]["annotations"] = annotations
    patched_figure["layout"]["xaxis"]["title"]["text"] = values
    patched_figure["layout"]["yaxis"]["title"]["text"] = field_name_map.get(categories)
    patched_figure["layout"]["xaxis"]["range"] = [0, max_of_df+xshift]

    return patched_figure


@callback(
    Output("download-tbl-box", "data"),
    [
        Input("btn-download-tbl-box", "n_clicks"),
        State('byob_data', 'data'),
    ],
    prevent_initial_call=True,
)
def func(n_clicks,
         byob_data):
    if n_clicks > 0:
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
                    '25%': 'Q1',
                    '50%': 'median',
                    '75%': 'Q3'
                }
            ).drop(
                columns='count'
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
