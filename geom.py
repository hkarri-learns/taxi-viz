import geopandas as gpd
# Read the shapefile
gdf = gpd.read_file("taxi_zones\\taxi_zones.shp")
# Project to WGS84 lat/long
gdf = gdf.to_crs("EPSG:4326")
# Convert geometry to WKT text
gdf["WKT"] = gdf.geometry.apply(lambda geom: geom.wkt)
# Save to CSV (including relevant fields and the WKT)
gdf.to_csv("taxi_zones_wkt.csv",
columns=["LocationID","Borough","Zone","service_zone","WKT"], index=False)