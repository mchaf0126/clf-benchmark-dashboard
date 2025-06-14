from dash import html
import dash_bootstrap_components as dbc


def create_header() -> html.Div:
    """_summary_

    Returns:
        html.Div: _description_
    """
    navbar = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            html.Img(
                                src='assets/CLF WBLCA Benchmark Project Logo_blue (1).png',
                                height="80px",
                            ),
                            href='https://carbonleadershipforum.org/clf-wblca-v2/'
                        ),
                        width=3,
                        align='center'
                    ),
                    dbc.Col(
                        dbc.NavbarBrand(
                            'Benchmark Explorer',
                            href='/benchmark_explorer',
                            className='fs-3 text-white fw-bold text-wrap'
                        ),
                        width=6,
                        class_name='text-center',
                        align='center'
                    ),
                    dbc.Col(
                        dbc.Nav(
                            [
                                dbc.NavItem(
                                        dbc.NavLink(
                                            'Home',
                                            href='/',
                                            className='fs-5 text-white fw-bolder'
                                        ),
                                ),
                            ],
                            horizontal='end'
                        ),
                        align='center',
                        width=3
                    )
                ],
                class_name='p-2'
            ),
        ],
        fluid=True,
        class_name='bg-primary justify-content-between',
    )

    return navbar
