from dash import html
import dash_bootstrap_components as dbc


def create_checklist(label: str,
                     checklist: list,
                     first_item: str,
                     checklist_id: str,
                     tooltip_id: str) -> html.Div:
    """_summary_

    Args:
        labe (str): _description_
        dropdown_list (list): _description_
        first_item (str): _description_
        id (str): _description_

    Returns:
        html.Div: _description_
    """

    checklist = html.Div(
        [
            dbc.Label(
                [
                    label,
                    html.Span(
                        ' 🛈',
                        id=tooltip_id
                    )
                ]
            ),
            dbc.Checklist(
                options=checklist,
                value=first_item,
                id=checklist_id,
                persistence=False,
                inputCheckedClassName="border border-primary bg-primary",
                inline=True
            ),
        ],
        className='mb-4'
    )
    return checklist