## CLF WBLCA Benchmark Study v2 - Dataset
This is a public repository containing the code required to run the Life Cycle Lab Dashboard as part of the CLF WBLCA Benchmark Study V2.

## About this study
In 2017, the Carbon Leadership Forum (CLF) at the University of Washington published the [Embodied Carbon Benchmark Study V1](https://carbonleadershipforum.org/lca-benchmark-database/) and [Visualization Tool](https://carbonleadershipforum.org/embodied-carbon-benchmark-study-data-visualization/). Since then, the practice of whole-building life cycle assessment (WBLCA) has grown rapidly, and it became clear that more robust and reliable benchmarks are critical for advancing work in thisfield. This project fills a critical gap and helps enable architects, engineers, policy makers, and the entire design community to work towards realistic and measurable embodied carbon reductionsat the building scale. The [WBLCA Benchmark Study V2](https://carbonleadershipforum.org/clf-wblca-v2/) began while the Carbon Leadership Forum (CLF) was hosted at the University of Washington (UW). After the CLF became an independent nonprofit in the spring of 2024, the study continued as a collaboration between the UW’s newly named Life Cycle Lab and CLF.

## About the dashboard
There are currently two types of graphs available:
*  **Box plot** - the traditional benchmarking graph. This plot shows environmental impacts based on categorical variables (e.g. building use, number of stories or location). All environmental impacts are inclusiveof life cycle stages A-C.
*  **Scatter plot** - good for analyzing relationships.This plot shows environmental impacts compared to continuousvariables (e.g. floor area, window-to-wall ratio or column spacing). All environmental impacts are inclusiveof life cycle stages A-C.

## Data Structure
**Please refer to the data descriptor article for full details, descriptions, and usage notes regarding the dataset and its structure.**

The **buildings_metadata.xlsx** file is structured so that each row of data reflects a single project. It contains 72 features organized by feature types including site context, building design, structural design, LCA methods, and calculated summaries. 

The **full_lca_results.xlsx** file is structured in a novel way that enables high-resolution data filtering and comparison-making. It is similar to the non-aggregated LCA tool output formats of Tally and One Click LCA where each row of data reflects a single material and life cycle stage from an individual project and contains the materials associated classifications, inventory data, and impacts. It contains 21 features organized by feature types for LCA classifications, LCI results, LCIA results, and calculated summaries. The two dataset files can be merged or joined using unique primary keys (project_index) that are assigned to each project to facilitate a wide range of uses and types of analysis. 

## Versioning
Versions on this repository are tracked using Releases on GitHub. 

## How to cite
For any dashboard related citations, please use: 
- Chafart, M., Benke, B., Simonen, K. (2025). WBLCA Benchmark Study v2 Dashboard (Version 1.0) \[Computer Software]. Life Cycle Lab, https://wblca-benchmark-v2.lifecyclelab.org/

For citations relating to the dataset, please cite both the Data Descriptor and the specific data version used:
- **Data Descriptor:** Benke, B., Chafart, M., Shen, Y., Ashtiani, M., Carlisle, S., and Simonen, K.  *A Harmonized Dataset of High-Resolution Whole Building Life Cycle Assessment Results in North America.* In Review. Preprint available at https://doi.org/10.21203/rs.3.rs-6108016/v1
- **Dataset:** Refer to the latest version on Figshare https://doi.org/10.6084/m9.figshare.28462145.v1

## Additional Project Resources
- [WBLCA Benchmark Study V2 Project Page - Carbon Leadership Forum](https://carbonleadershipforum.org/clf-wblca-v2/)
- [WBLCA Benchmark Study V2 Project Page - Life Cycle Lab at University of Washington](https://www.lifecyclelab.org/projects/)
- [Data Descriptor - A Harmonized Dataset of High-Resolution Whole Building Life Cycle Assessment Results in North America](https://doi.org/10.21203/rs.3.rs-6108016/v1)
- [California Carbon Report](https://carbonleadershipforum.org/california-carbon/)
- [Material Use Intensity Paper - Material Use and Embodied Carbon Intensity of New Construction Buildings in North America](https://doi.org/10.21203/rs.3.rs-6315460/v1)
- [Data Entry Template](https://hdl.handle.net/1773/51286)
- [Data Collection User Guide](https://hdl.handle.net/1773/51285)

## How to Use Locally

### 1. Clone the repository

```bash
git clone https://github.com/Life-Cycle-Lab/wblca-benchmark-v2-dashboard.git
cd wblca-benchmark-v2-dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the dashboard

```bash
cd src
python app.py
```

## Acknowledgements
We would like to thank the Alfred P. Sloan Foundation, the ClimateWorks Foundation, and the Breakthrough Energy Foundation for supporting this research project. 

We thank this study’s participating design practitioners (data contributors) who provided substantial time and effort in recording and submitting building project data and sharing feedback with the research team. These companies included: Arrowstreet Architects, Arup, BranchPattern, Brightworks Sustainability, Buro Happold, BVH Architecture, DCI Engineers, EHDD, Ellenzweig, Gensler, GGLO, Glumac, Group 14 Engineering, Ha/f Climate Design, HOK, KieranTimberlake, KPFF Consulting Engineers, Lake|Flato, LMN Architects, Mahlum Architects, Mead & Hunt, Inc., Mithun, Perkins&Will, reLoad Sustainable Design Inc., SERA Architects, Stok, The Green Engineer Inc., The Miller Hull Partnership, LLP., Walter P Moore, and ZGF Architects LLP.
