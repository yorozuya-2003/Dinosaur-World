# Dinosaur-World

## Overview

This project is a data visualization tool built using Plotly Dash, allowing users to explore various aspects of dinosaur data, including period, diet, type, and geographical distribution.

## Directory Structure

| Directory       | Description                                                  |
|-----------------|--------------------------------------------------------------|
| `analysis`      | Files related to data analysis                               |
| `app`           | Files related to the Plotly Dash application                 |
| `explore`       | Files related to data exploration                             |
| `residuals`       | Old, unused and partially used files                             |

### Analysis Directory

| File/Directory          | Description                                            |
|-------------------------|--------------------------------------------------------|
| `analysis.py`           | Python script for data analysis dash app               |
| `app.py`                | Python script for the analysis application             |
| `assets`                | Assets for the analysis application                    |
| `config.py`             | Configuration file for the analysis application       |
| `data_preprocessed.csv` | Preprocessed data for analysis                         |
| `data_preprocessing`    | Directory for data preprocessing                       |
| `diet_tab.py`           | Python script for the diet tab                         |
| `overview_tab.py`       | Python script for the overview tab                     |
| `period_tab.py`         | Python script for the period tab                       |
| `type_tab.py`           | Python script for the type tab                         |
| `iso_mapping.json`      | JSON file for mapping ISO codes                        |

### Explore Directory

| File/Directory             | Description                                      |
|----------------------------|--------------------------------------------------|
| `app.py`                   | Python script for the exploration application    |
| `assets`                   | Assets for the exploration application           |
| `data_preprocessed.csv`    | Preprocessed data for exploration                |
| `data_preprocessing_and_testing` | Directory for data preprocessing and testing |
| `explore.py`               | Python script for data exploration               |
| `index.py`                 | Python script for the exploration dash app   |

### App Directory

| File/Directory          | Description                                          |
|-------------------------|------------------------------------------------------|
| `analysis.py`           | Python script for analysis functionality            |
| `analysis_data.csv`     | Analysis data file                                   |
| `app.py`                | Python script for the main Dash application          |
| `assets`                | Assets for the Dash application                      |
| `config.py`             | Configuration file for the Dash application          |
| `diet_tab.py`           | Python script for the diet tab                       |
| `discover.py`           | Python script for discover page                     |
| `ETOPO1_Ice_g_gdal.grd` | Elevation data file for 3D globe visualization       |
| `explore.py`            | Python script for the exploration functionality      |
| `explore_data.csv`      | Exploration data file                                |
| `home.py`               | Python script for the home page                      |
| `iso_mapping.json`      | JSON file for mapping ISO codes                      |
| `main.py`               | Main entry point for running the Dash application    |
| `overview_tab.py`       | Python script for the overview tab                   |
| `period_tab.py`         | Python script for the period tab                     |
| `type_tab.py`           | Python script for the type tab                       |
| `world.py`              | Python script for the 3D globe visualization        |

## Running the App
To run the app locally, follow these steps:
1. Clone the repository:
```{bash}
git clone https://github.com/yorozuya-2003/Dinosaur-World.git
```
2. Install Python:  
Download and install Python from [python.org](https://www.python.org/downloads/).

3. Download the `ETOPO1_Ice_g_gdal.grd` file from this [link](https://drive.google.com/drive/folders/1v-2-lihXYj4v6goGP2eZVR27SCCvGeGF) and add it to the `app` directory of the cloned repository.

4. Install dependencies from `requirements.txt`:
```{bash}
cd Dinosaur-World
pip install -r requirements.txt
```

5. Change directory to the `app` directory:
```{bash}
cd app
```

6. Run `main.py` to open the Dash app:
```{bash}
python main.py
```

After running `main.py`, the Dash app should be accessible locally in your web browser.


## Authors
- [Rishav Aich](mailto:aich.1@iitj.ac.in) (B.Tech. Artificial Intelligence & Data Science)  
- [Tanish Pagaria](mailto:pagaria.2@iitj.ac.in) (B.Tech. Artificial Intelligence & Data Science)

(IIT Jodhpur Undergraduates)