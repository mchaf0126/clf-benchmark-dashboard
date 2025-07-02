## The CLF Benchmark Explorer
This is a public repository containing the code required to run the CLF Dashboard as part of the CLF WBLCA Benchmark Study V2. This is a fork of the LCL dashboard found [here](https://wblca-benchmark-v2.lifecyclelab.org).

## About this dashboard
The CLF Benchmark Explorer is a tool created by the Carbon Leadership Forum (CLF) to better visualize the data created by the WBLCA Benchmark Study V2. It consists of a set of customizable box and whisker plots for use in design, research, and education. These plots can be used to understand the impacts of building typologies and learn more about the WBLCA Benchmark Study dataset created by the CLF and the University of Washington’s Life Cycle Lab.

To learn how to use the dashboard, refer to the how-to video posted [here]().

## Versioning
Versions of this repository are tracked using Releases on GitHub.

## How to cite
For any dashboard related citations, please use: 
```
Chafart, M., Benke, B., Jensen, A. (2025). CLF Benchmark Explorer (Version 1.0) [Computer Software]. Carbon Leadership Forum, TBD!
```

For citations relating to the dataset, please cite both the Data Descriptor and the specific data version used:
- **Data Descriptor:**
```
Benke, B., Chafart, M., Shen, Y., Ashtiani, M., Carlisle, S., & Simonen, K. (2025). A Harmonized Dataset of High-Resolution Embodied Life Cycle Assessment Results for Buildings in North America. Scientific Data, 12(1), 1085. https://doi.org/10.1038/s41597-025-05216-0
```
- **Dataset:** Refer to the latest version on Figshare https://doi.org/10.6084/m9.figshare.28462145.v1

## Additional Project Resources
- [The Embodied Carbon Benchmark Report](https://carbonleadershipforum.org/de/the-embodied-carbon-benchmark-report/)
- [Public dataset hosted on Figshare](https://doi.org/10.6084/m9.figshare.28462145.v1)
- [A Harmonized Dataset of High-resolution Whole Building Life Cycle Assessment Results in North America](https://www.nature.com/articles/s41597-025-05216-0)
- [The California Carbon Report: An Analysis of the Embodied and Operational Carbon Impacts of 30 Buildings](https://carbonleadershipforum.org/california-carbon/)
- [A Novel Whole-life Carbon Assessment of Thirty Buildings in California](https://www.sciencedirect.com/science/article/pii/S2352710225013117?via%3Dihub)
- [The California Carbon Report: Six Key Takeaways for Policymakers](http://hdl.handle.net/1773/51415)
- [Exploratory Data Analysis of a North American Whole Building Life Cycle Assessment Dataset](https://doi.org/10.2139/ssrn.5197463)
- [Material Use and Embodied Carbon Intensity of New Construction Buildings in North America](https://doi.org/10.21203/rs.3.rs-6315460/v1)

## How to Use Locally

### 1. Clone the repository

```bash
git clone https://github.com/carbon-leadership-forum/wblca-benchmark-explorer.git
cd wblca-benchmark-explorer
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
