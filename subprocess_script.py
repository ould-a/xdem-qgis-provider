import sys
import xdem

def run_xdem_algorithms(algorithm, dem1_path, dem2_path, output_path):
    # DEMs configuration
    dem1 = xdem.DEM(dem1_path)
    dem1.info()
    try:
        dem2 = xdem.DEM(dem2_path)
        dem2.info()
    except:
        pass

    # Terrain Attributes
    if algorithm == 'Aspect':
        res = dem1.aspect()
    if algorithm == 'Hillshade':
        res = dem1.hillshade()
    if algorithm == 'Slope':
        res = dem1.slope()
    
    # Coregistration
    coreg = None
    if algorithm == 'ICP':
        coreg = xdem.coreg.ICP()
    if algorithm == 'LZD':
        coreg = xdem.coreg.LZD()
    if algorithm == 'NuthKaab':
        coreg = xdem.coreg.NuthKaab()
    if coreg != None:
        coreg.fit(dem1, dem2)
        res = coreg.apply(dem1)
    
    res.to_file(output_path)

# Main
qgis_algorithm = sys.argv[1]
qgis_dem1_path = sys.argv[2]
qgis_dem2_path = sys.argv[3]
qgis_output_path = sys.argv[4]

run_xdem_algorithms(algorithm=qgis_algorithm,
                    dem1_path=qgis_dem1_path,
                    dem2_path=qgis_dem2_path,
                    output_path=qgis_output_path)