# Chicago Neighborhood Desirability Model - Data Download Guide

## 📋 Project Overview
This project builds a machine learning model to predict neighborhood desirability in Chicago using Airbnb pricing, Zillow home values, crime data, 311 complaints, food inspections, and parks data.

**Final Dataset**: 76 Chicago neighborhoods with ~10 features ready for modeling

---

## 📥 Data Sources & Download Instructions

### 1. **Airbnb Data** (Inside Airbnb)
**Source**: http://insideairbnb.com/get-the-data/

**Steps**:
1. Go to http://insideairbnb.com/get-the-data/
2. Find "Chicago, Illinois, United States"
3. Download the latest available date
4. You need these files:
   - `listings.csv` (detailed listing data)
   - `neighbourhoods.csv` (neighborhood boundaries)
   - `neighbourhoods.geojson` (GeoJSON format)

**Files to use**:
- `listings.csv` → Extract: neighborhood name, price, review scores
- `neighbourhoods.csv` → Neighborhood reference table

**Expected size**: ~8-10 MB total

---

### 2. **Zillow Home Value Index (ZHVI)**
**Source**: https://www.zillow.com/research/data/

**Steps**:
1. Go to https://www.zillow.com/research/data/
2. Search for "ZHVI" (Zillow Home Value Index)
3. Download "Zillow Home Value Index - Neighborhoods"
4. Filter to Chicago, Illinois
5. Download as CSV

**File to use**:
- `ZHVI_Neighborhood_Chicago.csv` (or similar name)

**What you get**:
- RegionName (neighborhood name)
- Latest month's median home value
- Historical price data by month

**Expected size**: ~5-15 MB

---

### 3. **Chicago 311 Service Requests**
**Source**: https://data.cityofchicago.org/

**Steps**:
1. Go to https://data.cityofchicago.org/
2. Search "311 Service Requests"
3. Click dataset: https://data.cityofchicago.org/Service-Requests/311-Service-Requests-Chicago-311-Online-Request/v6vf-nrqa
4. Click "Download" → Select "CSV"
5. Download

**File to use**:
- `311_Service_Requests_Chicago.csv`

**Key columns**:
- `COMMUNITYAREA` (numeric ID: 1-77)
- `SR_TYPE` (type of service request)
- `CREATED_DATE`

**Expected size**: **LARGE** (~500 MB+) - but you only need to aggregate by Community Area

---

### 4. **Crimes - Chicago Police Dept**
**Source**: https://data.cityofchicago.org/

**Steps**:
1. Go to https://data.cityofchicago.org/
2. Search "Crimes Chicago"
3. Click dataset: https://data.cityofchicago.org/Public-Safety/Crimes-Chicago-Police-Department/ijzp-q8t2
4. Click "Download" → Select "CSV"
5. Download

**File to use**:
- `Crimes_Chicago.csv`

**Key columns**:
- `Community Area` (numeric ID: 1-77)
- `Primary Type` (crime classification)
- `Date`

**Expected size**: **VERY LARGE** (~300-500 MB) - aggregate by Community Area

**⚠️ TIP**: If file is too large, use the website filters:
- Filter to last 12 months only
- Then download

---

### 5. **Food Inspections**
**Source**: https://data.cityofchicago.org/

**Steps**:
1. Go to https://data.cityofchicago.org/
2. Search "Food Inspections"
3. Click dataset: https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5
4. Click "Download" → Select "CSV"
5. Download

**File to use**:
- `Food_Inspections_Chicago.csv`

**Key columns**:
- `Latitude` / `Longitude` (you'll need to spatially join to Community Area)
- `Risk` (Risk 1 High, Risk 2 Medium, Risk 3 Low)
- `Results` (Pass, Fail, etc.)

**Expected size**: ~20-50 MB

---

### 6. **Parks**
**Source**: https://data.cityofchicago.org/

**Steps**:
1. Go to https://data.cityofchicago.org/
2. Search "Parks Chicago Park District Facilities"
3. Click dataset: https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Facilities-current-/5yyk-qt9y
4. Click "Download" → Select "CSV"
5. Download

**File to use**:
- `Parks_Chicago.csv`

**Key columns**:
- `PARK_CLASS` (type of park)
- `ACRES` (size)
- `ZIP` (ZIP code)

**Expected size**: ~1-5 MB

---

## 🗺️ Geographic Mapping Files (OPTIONAL but USEFUL)

### Community Area Boundaries (Shapefiles)
**Source**: https://data.cityofchicago.org/d/cauq-8yn6

**Purpose**: Spatial join to map lat/lon data to Community Areas

**Download**:
1. Go to https://data.cityofchicago.org/d/cauq-8yn6
2. Click "Download"
3. Choose format:
   - **Shapefile (.shp)** → Use with geopandas (Python)
   - **GeoJSON** → Use with geopandas or web maps
   - **KML** → Use with Google Earth

**File to use**:
- `Boundaries_Community_Areas.shp` (or .geojson)

---

### ZIP Code Boundaries (Shapefiles)
**Source**: https://data.cityofchicago.org/d/gdcf-axmw

**Purpose**: If you want to map ZIP codes to Community Areas

**Download**:
1. Go to https://data.cityofchicago.org/d/gdcf-axmw
2. Click "Download"
3. Choose format (GeoJSON recommended)

**File to use**:
- `Boundaries_ZIP_Codes.geojson`

---

## 📁 Folder Structure (After Download)

```
chicago_project/
├── README.txt (this file)
├── 01_Raw_Data/
│   ├── Airbnb/
│   │   ├── listings.csv
│   │   ├── neighbourhoods.csv
│   │   └── neighbourhoods.geojson
│   ├── Zillow/
│   │   └── ZHVI_Neighborhood_Chicago.csv
│   ├── Chicago_Portal/
│   │   ├── 311_Service_Requests_Chicago.csv
│   │   ├── Crimes_Chicago.csv
│   │   ├── Food_Inspections_Chicago.csv
│   │   └── Parks_Chicago.csv
│   └── Shapefiles/ (OPTIONAL)
│       ├── Boundaries_Community_Areas.geojson
│       └── Boundaries_ZIP_Codes.geojson
├── 02_Processed_Data/
│   ├── airbnb_by_neighborhood.csv
│   ├── zillow_by_neighborhood.csv
│   └── chicago_mapping.csv
├── 03_Master_Dataset/
│   └── master_chicago_neighborhoods.csv
├── 04_Analysis/
│   ├── eda.ipynb
│   └── modeling.ipynb
└── data_download_guide.txt (this file)
```

---

## 🚀 Quick Start

### Step 1: Download All Data
```bash
# Create folder structure
mkdir -p 01_Raw_Data/Airbnb 01_Raw_Data/Zillow 01_Raw_Data/Chicago_Portal

# Download files to appropriate folders
# (see instructions above for each source)
```

### Step 2: Load Data in Python
```python
import pandas as pd

# Load all datasets
df_listings = pd.read_csv('01_Raw_Data/Airbnb/listings.csv', low_memory=False)
df_neighborhoods = pd.read_csv('01_Raw_Data/Airbnb/neighbourhoods.csv')
df_zillow = pd.read_csv('01_Raw_Data/Zillow/ZHVI_Neighborhood_Chicago.csv')
df_311 = pd.read_csv('01_Raw_Data/Chicago_Portal/311_Service_Requests_Chicago.csv', low_memory=False)
df_crimes = pd.read_csv('01_Raw_Data/Chicago_Portal/Crimes_Chicago.csv', low_memory=False)
df_food = pd.read_csv('01_Raw_Data/Chicago_Portal/Food_Inspections_Chicago.csv', low_memory=False)
df_parks = pd.read_csv('01_Raw_Data/Chicago_Portal/Parks_Chicago.csv', low_memory=False)

print("✅ All datasets loaded!")
```

### Step 3: Create Master Dataset
```python
# See main analysis notebook for full processing pipeline
# Result: master_chicago_neighborhoods.csv (76 rows × 10+ columns)
```

---

## 📊 Final Master Dataset Features

After processing, your master dataset will have:

| Feature | Source | Description |
|---------|--------|-------------|
| `Community_Area_ID` | Chicago Portal | 1-77 official ID |
| `Community_Area_Name` | Mapping table | Neighborhood name |
| `Listing_Count` | Airbnb | # of Airbnb listings |
| `Avg_Airbnb_Price` | Airbnb | Average nightly price ($) |
| `Avg_Review_Score` | Airbnb | Average guest rating (0-5) |
| `Median_Home_Value` | Zillow | Median home sales price ($) |
| `Total_311_Calls` | 311 | # of service requests |
| `Total_Crimes` | Crime data | Total crime count |
| `Food_Businesses` | Food Inspections | # of restaurants |
| `Park_Facilities` | Parks | # of parks |

**Target Variable**: `Median_Home_Value`

**Predictors**: All other features

---

## ⚠️ Data Size Notes

| Dataset | Size | Notes |
|---------|------|-------|
| Airbnb | ~10 MB | ✅ Small, easy to work with |
| Zillow | ~5-15 MB | ✅ Small, easy to work with |
| 311 | ~500 MB | ⚠️ Large; filter to recent data or aggregate |
| Crimes | ~300-500 MB | ⚠️ Large; filter to recent data or aggregate |
| Food | ~20-50 MB | ✅ Medium, manageable |
| Parks | ~1-5 MB | ✅ Very small |
| **TOTAL** | **~850 MB** | **Filter large files to make manageable** |

---

## 🛠️ Processing Tips

### For Large Files (311 & Crimes)
Use filters on data.cityofchicago.org BEFORE downloading:
- Filter 311 to "Last 12 months"
- Filter Crimes to "Last 12 months"
- This reduces file size by 50-75%

### For Food Inspections
If you only need recent inspections, filter on website:
- Filter to "Last inspection date > 2024-01-01"

### Python: Read Large Files in Chunks
```python
# Read only needed columns
df_311 = pd.read_csv(
    '311_Service_Requests_Chicago.csv',
    usecols=['COMMUNITYAREA', 'SR_TYPE', 'CREATED_DATE'],
    low_memory=False
)

# Aggregate by Community Area (much smaller!)
df_311_agg = df_311.groupby('COMMUNITYAREA').size().reset_index(name='Total_311_Calls')
```

---

## 🔗 Direct Links (Summary)

| Dataset | Link | Download Format |
|---------|------|-----------------|
| Airbnb | http://insideairbnb.com/get-the-data/ | CSV/GeoJSON |
| Zillow | https://www.zillow.com/research/data/ | CSV |
| 311 | https://data.cityofchicago.org/Service-Requests/311-Service-Requests-Chicago-311-Online-Request/v6vf-nrqa | CSV |
| Crimes | https://data.cityofchicago.org/Public-Safety/Crimes-Chicago-Police-Department/ijzp-q8t2 | CSV |
| Food | https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5 | CSV |
| Parks | https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Facilities-current-/5yyk-qt9y | CSV |
| **Community Areas** | https://data.cityofchicago.org/d/cauq-8yn6 | Shapefile/GeoJSON |
| **ZIP Codes** | https://data.cityofchicago.org/d/gdcf-axmw | Shapefile/GeoJSON |

---

## ✅ Checklist

Before running analysis, verify you have:

- [ ] `listings.csv` (Airbnb)
- [ ] `neighbourhoods.csv` (Airbnb)
- [ ] `ZHVI_Neighborhood_Chicago.csv` (Zillow)
- [ ] `311_Service_Requests_Chicago.csv` (311)
- [ ] `Crimes_Chicago.csv` (Crimes)
- [ ] `Food_Inspections_Chicago.csv` (Food)
- [ ] `Parks_Chicago.csv` (Parks)
- [ ] Community Area mapping table created
- [ ] All files placed in correct folders
- [ ] Ready to run `master_dataset_creation.ipynb`

---

## 📝 Questions?

If a download link is broken or a dataset has moved:
1. Go to https://data.cityofchicago.org/
2. Use the search bar to find the dataset by name
3. Click "Download" and select CSV format

---

**Last Updated**: January 30, 2026
**Project**: Chicago Neighborhood Desirability Model
**Status**: Ready for Data Processing
