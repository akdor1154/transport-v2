#%%
import os

import zipfile
#%%
with open('ENVIRONMENT') as envFile:
    for line in envFile:
        key, val = map(str.strip, line.split('=', 1))
        os.environ[key] = val
#%%
os.makedirs('data', exist_ok=True)
#%%

def download(what: str, where: str):
    import urllib.request

    with(
        urllib.request.urlopen(what) as response,
        open(f'data/{where}', 'wb') as dest
    ):
        while (b := response.read1()) != b'':
            dest.write(b)
#%%

download(
    (
        'https://app.interline.io/osm_extracts/download_latest'
        f"?string_id=melbourne_australia&data_format=pbf&api_token={os.environ['INTERLINE_KEY']}"
    ),
    'melbourne.pbf'
)
#%%
download(
    'http://data.ptv.vic.gov.au/downloads/gtfs.zip',
    'melbourne_gtfs.zip'
)
# %%

# SA1 data
DATA_YEAR = '2016'
if DATA_YEAR == '2016':
    # in gda94 i think
    download(
        'https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa1_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&6F308688D810CEF3CA257FED0013C62D&0&July%202016&12.07.2016&Latest',
        'SA1_2016_AUST_SHP.zip'
    )

    download(
        'https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa1_2016_aust_csv.zip&1270.0.55.001&Data%20Cubes&10E21199BF8C37F7CA257FED0013A4BB&0&July%202016&12.07.2016&Latest',
        'SA1_2016_AUST_CSV.zip'
    )
    download(
        'https://www.abs.gov.au/census/find-census-data/datapacks/download/2016_GCP_SA1_for_VIC_short-header.zip',
        '2016_GCP_SA1_for_VIC_short-header.zip'
    )

    with zipfile.ZipFile('data/SA1_2016_AUST_SHP.zip', 'r') as zf:
        zf.extractall('data/sa1')

    
elif DATA_YEAR == '2021':
    download(
        'https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA1_2021_AUST_SHP_GDA2020.zip',
        'SA1_2021_AUST_SHP_GDA2020.zip'
    )

    with zipfile.ZipFile('data/SA1_2021_AUST_SHP_GDA2020.zip', 'r') as zf:
        zf.extractall('data/sa1')
    # pop stats not yet available, might redo once done.


#%%
# dnz data
download(
    'https://www.abs.gov.au/statistics/people/population/census-population-and-housing-destination-zones/aug-2016/80000_dzn_sa2_2016_aust_csv.zip',
    'dzn_sa2_2016_aust_csv.zip'
)
download(
    'https://www.abs.gov.au/statistics/people/population/census-population-and-housing-destination-zones/aug-2016/80000_dzn_2016_aust_shape.zip',
    'dzn_2016_aust_shape.zip'
)

with zipfile.ZipFile('data/dzn_2016_aust_shape.zip', 'r') as zf:
    zf.extractall('data/dzn')

#%%

from subprocess import run
# for gqis
run(['ogr2ogr', '-f', 'SQLite', 'melbourne.pbf.sqlite', 'melbourne.pbf', '-dsco', 'SPATIALITE=YES'], cwd='data')
# %%
os.makedirs('data/sa1', exist_ok=True)

# %%

os.makedirs('data/sa1_stats', exist_ok=True)
import zipfile
with zipfile.ZipFile('data/2016_GCP_SA1_for_VIC_short-header.zip', 'r') as zf:
    zf.extractall('data/sa1_stats')
# %%
