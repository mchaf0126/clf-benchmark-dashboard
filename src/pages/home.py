from pathlib import Path
import pandas as pd
from dash import html, dcc, register_page
import dash_bootstrap_components as dbc
from src.components.jumbotron import create_jumbotron


register_page(__name__, path="/")

current_file_path = Path(__file__)
main_directory = current_file_path.parents[2]
metadata_directory = main_directory.joinpath("data/buildings_metadata.pkl")
buildings_metadata_df = pd.read_pickle(metadata_directory)

typology_jumbotron = create_jumbotron(
    subtitle="Unique Building Typologies",
    main_text=len(buildings_metadata_df["bldg_prim_use"].unique()),
)

project_number_jumbotron = create_jumbotron(
    subtitle="Projects in Dataset", main_text=buildings_metadata_df.shape[0]
)

avg_impact_jumbotron = create_jumbotron(
    subtitle="Average kgCO2e / m2",
    main_text=round(buildings_metadata_df["eci_a_to_c_gfa"].mean()),
)

layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(
                            """
                            #### **About the dashboard**
                            """
                        ),
                        dcc.Markdown(
                            """
                            The [CLF Benchmark Explorer](/benchmark_explorer) 
                            is a tool created by the Carbon Leadership Forum (CLF) to 
                            better visualize the data created by the 
                            [WBLCA Benchmark Study V2](https://carbonleadershipforum.org/clf-wblca-v2/). It consists 
                            of a set of customizable box and whisker plots for 
                            use in design, research, and education. These plots
                            can be used to understand the impacts of building 
                            typologies and learn more about the WBLCA Benchmark 
                            Study dataset created by the CLF and the University 
                            of Washington’s Life Cycle Lab.
                            """,
                        ),
                        html.Div(
                            [
                                dbc.Button(
                                    "Use the Benchmark Explorer",
                                    color="primary",
                                    href="/benchmark_explorer",
                                    className="d-grid col-4 fw-bold mx-auto",
                                    size="lg",
                                ),
                            ]
                        ),
                        html.Br(),
                        dcc.Markdown(
                            """
                            #### **Relationship to CLF Embodied Carbon Benchmark Report**
                            """
                        ),
                        dcc.Markdown(
                            """
                            This dashboard is meant to enable exploration, research, 
                            and education. While it is a valuable tool for comparison 
                            making and target setting, the CLF does not recommend it 
                            be used to derive carbon limits or budgets for LCA policies
                            or programs. The [CLF Embodied Carbon Benchmark Report]
                            (https://carbonleadershipforum.org/de/the-embodied-carbon-benchmark-report/)
                            serves this purpose by presenting curated benchmarks
                            intended for reference in building-scale policies, 
                            incentives, certification programs, and other real-world
                            applications. In order to be legible and useful for a wide 
                            variety of applications, the embodied carbon budgets (ECBs) 
                            in the CLF Embodied Carbon Benchmark Report were generated 
                            with specific methods that extend beyond what can be assessed 
                            with this dashboard or with the raw dataset alone. Please 
                            note that these additional methods and curated benchmark 
                            figures are not available in the dashboard which is built 
                            directly on the public dataset. 
                            """,
                        ),
                        html.Br(),
                        dcc.Markdown(
                            """
                            #### **Using the Dashboard**
                            """
                        ),
                        dcc.Markdown(
                            """
                            CLF chose box and whisker plots to visualize the benchmarking 
                            dataset to quickly display the variability and distribution 
                            of WBLCA results and provide several helpful key statistics 
                            for use by the industry. Looking at a box and whisker plot, 
                            viewers should be able to quickly understand the range of 
                            typical impacts (indicated by the color bar between quartile
                            1 and 3), typical practice (mean) or (median), “best practice” 
                            (quartile 1), and a conservative upper value (quartile 3). 

                            The specific values that box and whisker plots display are 
                            described in the figure below, which include:

                            - **Mean:** The average value representing the sum of all
                                values divided by the number of values
                            - **Quartile 1 (Q1):** The 25th percentile value of data 
                                points, where 25% of projects fall below this value. 
                            - **Median:** The middle value dividing the upper and lower 
                                half of data points (50th percentile)
                            - **Quartile 3 (Q3):** The 75th percentile value of data 
                                points, where 75% of projects fall below this value
                            - **Interquartile range (IQR):** The middle 50% of data 
                                points, from 25th to 75th percentiles. A smaller IQR 
                                indicates less variability of the data (more similar 
                                values) and a larger IQR indicates more variability 
                                (less similar values).
                            - **Lower whisker:** The lowest 25% of data points, 
                                excluding any outliers, as determined by multiplying 
                                the length of the IQR by 1.5.
                            - **Upper whisker:** The uppermost 25% of data points, 
                                excluding any outliers, as determined by multiplying 
                                the length of the IQR by 1.5.
                            """,
                        ),
                        html.Img(
                            src="assets/boxplot_ex.jpg", className="img-fluid px-4"
                        ),
                        dcc.Markdown(
                            """
                            **Note:** Box and whisker plots cannot be accurately drawn 
                            with sample sizes less than 5. In this dashboard, when 
                            sample sizes are less than 5, approximations of box and 
                            whisker plots will be shown, but they are for information 
                            only so that the user can understand where the small sample 
                            sizes are located in the dataset. 
                            """,
                        ),
                        html.Br(),
                        dcc.Markdown(
                            """
                            #### **About the CLF Benchmark v2 study**
                            """
                        ),
                        dcc.Markdown(
                            """
                            In 2017, the Carbon Leadership Forum at the 
                            University of Washington published the [Embodied 
                            Carbon Benchmark Study V1]
                            (https://carbonleadershipforum.org/lca-benchmark-database/)
                            and [Visualization Tool]
                            (https://carbonleadershipforum.org/embodied-carbon-benchmark-study-data-visualization/). 
                            Since then, the practice of whole-building life 
                            cycle assessment (WBLCA) has grown rapidly, and 
                            it became clear that more robust and reliable 
                            benchmarks were critical for advancing work in this
                            field. This project helps fill this critical gap 
                            by enabling architects, engineers, policy makers, and 
                            the entire design community to work towards 
                            realistic and measurable embodied carbon reductions
                            at the building scale.
                            
                            The [WBLCA Benchmark Study V2]
                            (https://carbonleadershipforum.org/clf-wblca-v2/)
                            began while the Carbon Leadership Forum
                            was hosted at the University 
                            of Washington. After the CLF became an 
                            independent nonprofit in the spring of 2024, the 
                            study continued as a collaboration between the UW’s 
                            newly named Life Cycle Lab and CLF.
                            """,
                        ),
                        html.Br(),
                        dcc.Markdown(
                            """
                            #### **Project Publications**
                            """
                        ),
                        dcc.Markdown(
                            """
                            - [The Embodied Carbon Benchmark Report]
                            (https://carbonleadershipforum.org/de/the-embodied-carbon-benchmark-report/)
                            - [Public dataset hosted on Figshare]
                            (https://doi.org/10.6084/m9.figshare.28462145.v1)
                            - [A Harmonized Dataset of High-resolution Whole 
                            Building Life Cycle Assessment Results in North America]
                            (https://www.nature.com/articles/s41597-025-05216-0)
                            - [The California Carbon Report: An Analysis of the 
                            Embodied and Operational Carbon Impacts of 30 Buildings]
                            (https://carbonleadershipforum.org/california-carbon/)
                            - [A Novel Whole-life Carbon Assessment of 
                            Thirty Buildings in California]
                            (https://www.sciencedirect.com/science/article/pii/S2352710225013117?via%3Dihub)
                            - [The California Carbon Report: Six Key 
                            Takeaways for Policymakers](http://hdl.handle.net/1773/51415)
                            - [Exploratory Data Analysis of a North American 
                            Whole Building Life Cycle Assessment Dataset]
                            (https://doi.org/10.2139/ssrn.5197463)
                            - [Material Use and Embodied Carbon Intensity of New Construction Buildings in North America]
                            (https://doi.org/10.21203/rs.3.rs-6315460/v1)

                            The code for this dashboard can be found at this [Github Repository.]()
                            """,
                        ),
                        html.Br(),
                        dcc.Markdown(
                            """
                            #### **About the Carbon Leadership Forum**
                            """
                        ),
                        dcc.Markdown(
                            """
                            The Carbon Leadership Forum accelerates the transformation 
                            of the building sector to radically reduce the greenhouse 
                            gas emissions attributed to materials (also known as 
                            embodied carbon) used in buildings and infrastructure. 
                            The CLF researches, educates, and fosters cross-collaboration to 
                            bring embodied carbon of buildings and infrastructure down to 
                            zero. CLF envisions a transformed, decarbonized building 
                            industry – better buildings for a better planet.
                            """,
                        ),
                        html.Br(),
                        dcc.Markdown(
                            """
                            #### **Authors**
                            """
                        ),
                        dcc.Markdown(
                            """
                            The individuals from the Carbon Leadership Forum who worked on this
                            dashboard are:
                            - Manuel Chafart, Lead
                            - Aurora Jensen, Senior Manager
                            - Brad Benke, Manager
                            - Meghan Lewis, Program Director

                            [CRediT]
                            (https://www.elsevier.com/researcher/author/policies-and-guidelines/credit-author-statement)
                            authorship contribution: Conceptualization -M.C., A.J., B.B., M.L.;
                            Formal analysis: M.C; Methodology - M.C., A.J.;  Visualization: M.C;
                            Supervision and Funding Acquisition: M.L.
                            """,
                        ),
                        html.Br(),
                        dcc.Markdown(
                            """
                            #### **Acknowledgements**
                            """,
                        ),
                        dcc.Markdown(
                            """
                            We would like to thank the individuals and respective firms
                            who participated in the data collection and quality assurance
                            process, this work would not have been possible without their
                            incredible support and dedication to thisproject. These
                            included: Arrowstreet Architects, Arup, BranchPattern,
                            Brightworks Sustainability, Buro Happold, BVH Architecture,
                            DCI Engineers, EHDD, Ellenzweig, Gensler, GGLO, Glumac,
                            Group 14 Engineering, Ha/f ClimateDesign, HOK, KieranTimberlake,
                            KPFF Consulting Engineers, Lake|Flato, LMN Architects,
                            Mahlum Architects, Mead & Hunt, Inc., Mithun, Perkins&Will,
                            reLoad Sustainable Design Inc., SERA Architects, Stok,
                            The Green Engineer Inc., The Miller Hull Partnership, LLP.,
                            Walter P Moore, and ZGF Architects LLP.
                            """,
                        ),
                        html.Br(),
                        dcc.Markdown(
                            """
                            #### **Citation**
                            """
                        ),
                        dcc.Markdown(
                            """
                            Chafart, M., Jensen, A., Benke, B., Lewis, M. (2025). CLF 
                            Benchmark Explorer (Version 1.0) [Computer Software]. 
                            Carbon Leadership Forum, 
                            https://wblca-benchmark-explorer.carbonleadershipforum.org 
                            """,
                        ),
                        html.Br(),
                        dcc.Markdown(
                            """
                            [(CC BY 4.0)](https://creativecommons.org/licenses/by/4.0)
                            2025
                            """,
                            className="text-center",
                        ),
                    ],
                    xs=9,
                    sm=9,
                    md=9,
                    lg=9,
                    xl=8,
                    xxl=8,
                    class_name="pe-5",
                ),
                dbc.Col(
                    [
                        typology_jumbotron,
                        project_number_jumbotron,
                        avg_impact_jumbotron,
                    ],
                    className="my-4",
                    xs=3,
                    sm=3,
                    md=3,
                    lg=3,
                    xl=2,
                    xxl=2,
                ),
            ],
            justify="center",
            className="m-2",
        ),
    ]
)
