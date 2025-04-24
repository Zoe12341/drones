import pandas as pd

mrk_file = "/Users/caseymacgibbon/Downloads/October 10th/files/DJI_202410240928_018_ParadisePondBaseWithLeg/DJI_202410240928_018_ParadisePondBaseWithLeg_Timestamp.MRK"

import re

# Load MRK file
with open(mrk_file, "r") as f:
    lines = f.readlines()

# Extract lat/lon only
latlon = []
for line in lines:
    if "Lat" in line and "Lon" in line:
        lat_match = re.search(r"([-+]?\d*\.\d+),Lat", line)
        lon_match = re.search(r"([-+]?\d*\.\d+),Lon", line)

        if lat_match and lon_match:
            lat = float(lat_match.group(1))
            lon = float(lon_match.group(1))
            latlon.append((lat, lon))

import pandas as pd
df_latlon = pd.DataFrame(latlon, columns=["Latitude", "Longitude"])

print(df_latlon.head())

