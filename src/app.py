from pathlib import Path
import pandas as pd
from dash import Dash, html, page_container, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from src.components.header import create_header

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
)
server = app.server

load_figure_template('bootstrap')

header = create_header()

app.layout = dbc.Container(
    [
        dcc.Store(
            id='byob_data',
            storage_type='memory',
        ),
        dbc.Row(
            html.Header(
                dbc.Row(
                    dbc.Col(
                        header,
                        className='mb-2',
                        xs=12, sm=12, md=12, lg=12, xl=10, xxl=10
                    ),
                    justify='center'
                ),
            )
        ),
        dbc.Row(
            page_container
        )
    ],
    fluid=True,
    className='dbc'
)


if __name__ == "__main__":
    app.run(debug=True)
