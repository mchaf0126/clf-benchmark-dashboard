from dash import html, dcc
import dash_bootstrap_components as dbc


def create_dropdown(label: str, tooltip_id: str, dropdown_list: list, first_item: str, dropdown_id: str) -> html.Div:
    """_summary_

    Args:
        labe (str): _description_
        dropdown_list (list): _description_
        first_item (str): _description_
        id (str): _description_

    Returns:
        html.Div: _description_
    """

    dropdown = html.Div(
        [
            dbc.Label(
                [
                    label,
                    html.Img(
                        src='assets/info.jpg',
                        height="25px",
                        id=tooltip_id,
                        className='mb-1'
                    )
                ]
            ),
            dcc.Dropdown(
                options=dropdown_list,
                value=first_item,
                id=dropdown_id,
                clearable=False,
                persistence=False,
                optionHeight=60
            ),
        ],
        className='mb-4'
    )
    return dropdown


def create_multi_dropdown(label: str,
                          tooltip_id: str, 
                          dropdown_id: str,
                          placeholder: str,
                          dropdown_list: list = [],
                          first_item: str = None) -> html.Div:
    """_summary_

    Args:
        labe (str): _description_
        dropdown_list (list): _description_
        first_item (str): _description_
        id (str): _description_

    Returns:
        html.Div: _description_
    """

    dropdown = html.Div(
        [
            dbc.Label(
                [
                    label,
                    html.Img(
                        src='assets/info.jpg',
                        height="25px",
                        id=tooltip_id,
                        className='mb-1'
                    )
                ]
            ),
            dcc.Dropdown(
                options=dropdown_list,
                value=first_item,
                id=dropdown_id,
                multi=True,
                clearable=False,
                persistence=False,
                optionHeight=60,
                placeholder=placeholder
            ),
        ],
        className='mb-4'
    )
    return dropdown

