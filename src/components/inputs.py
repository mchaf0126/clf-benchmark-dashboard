from dash import html, dcc
import dash_bootstrap_components as dbc


def create_str_input(label: str, tooltip_id: str, placeholder: str, input_id: str, first_item: str = "") -> html.Div:
    """_summary_

    Args:
        label (str): _description_
        tooltip_id (list): _description_
        placeholder (str): _description_
        input_id (str): _description_

    Returns:
        html.Div: _description_
    """

    dbc_input = html.Div(
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
            dbc.Input(
                placeholder=placeholder,
                value=first_item,
                type='text',
                id=input_id,
                persistence=False,
                maxlength=30
            ),
        ],
        className='mb-2'
    )
    return dbc_input


def create_float_input(label: str, tooltip_id: str, placeholder: str, input_id: str, first_item: int = 0) -> html.Div:
    """_summary_

    Args:
        label (str): _description_
        tooltip_id (list): _description_
        placeholder (str): _description_
        input_id (str): _description_

    Returns:
        html.Div: _description_
    """

    dbc_input = html.Div(
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
            dbc.Input(
                placeholder=placeholder,
                value=first_item,
                type='number',
                id=input_id,
                persistence=False,
                maxlength=10,
                min=0
            ),
        ],
        className='mb-2'
    )
    return dbc_input