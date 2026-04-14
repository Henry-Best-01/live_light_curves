import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

username=os.getenv('SLED_USERNAME')
password=os.getenv('SLED_PASSWORD')

if username is None or password is None:
    print("please store your SLED_ID and SLED_PASSWORD as environment variables")
    print("in your .bashrc or .zshrc file, try adding the line 'export SLED_ID=[your id]'")
    print("and 'export SLED_PASSWORD=[your password]' then restart your shell")


# parameters to export
query_pars =  {'download-lens_options': ['name', 'ra', 'dec', 'mugshot', 'n_img', 'image_sep', 'score'],
               "download-related": ["redshift","catalogue"],
               'lens-flag':['CONFIRMED'],
               'lens-source_type': ['QUASAR']}
print("Querying SLED...")
r = requests.post("https://sled.amnh.org/api/query-lenses-full/",
                data=json.dumps(query_pars),
                headers={'Content-Type':'application/json', 'User-Agent':'SLED-api/1.0'},
                auth=HTTPBasicAuth(username,password))

if r.status_code != 200:
    print(f"Error: {r.status_code}")
    print(r.text)
    sys.exit(1)

lenses = json.loads(r.text)['lenses']
print('Downloaded', len(lenses), 'lenses')

output_file = os.path.join(os.path.dirname(__file__), 'lenses.json')
print(f"Saving to {output_file}...")
with open(output_file, 'w') as f:
    json.dump(lenses, f, indent=4)

csv_output_file = os.path.join(os.path.dirname(__file__), 'lenses.csv')
print(f"Saving to {csv_output_file}...")

def get_dist(c):
    try:
        val = c.get('distance')
        return float(val) if val is not None else 999.0
    except (ValueError, TypeError):
        return 999.0

for lens in lenses:
    cats = sorted(lens.get('catalogue', []), key=get_dist)
    lens['Gmag'] = next((c.get('mag') for c in cats if c.get('band') == 'G' and c.get('mag') is not None), None)
    lens['RPmag'] = next((c.get('mag') for c in cats if c.get('band') == 'RP' and c.get('mag') is not None), None)
    lens['BPmag'] = next((c.get('mag') for c in cats if c.get('band') == 'BP' and c.get('mag') is not None), None)
    
    lens['z_lens'] = None
    lens['z_lens_type'] = None
    lens['z_source'] = None
    lens['z_source_type'] = None
    
    for z in lens.get('redshift', []):
        tag = z.get('tag')
        if tag == 'LENS' and lens['z_lens'] is None:
            lens['z_lens'] = z.get('value')
            lens['z_lens_type'] = z.get('method')
        elif tag == 'SOURCE' and lens['z_source'] is None:
            lens['z_source'] = z.get('value')
            lens['z_source_type'] = z.get('method')
            
    lens.pop('catalogue', None)
    lens.pop('redshift', None)

df = pd.DataFrame(lenses)

if 'score' in df.columns:
    df = df.drop(columns=['score'])
if 'mugshot' in df.columns:
    df = df.drop(columns=['mugshot'])

df = df.dropna(axis=1, how='all')

df['LEGACY SURVEY'] = "https://www.legacysurvey.org/viewer?ra=" + df['ra'].astype(str) + "&dec=" + df['dec'].astype(str) + "&layer=ls-dr10&zoom=16&gaia-edr3"

if 'name' in df.columns:
    cols = df.columns.tolist()
    cols.insert(0, cols.pop(cols.index('name')))
    df = df[cols]

df.to_csv(csv_output_file, index=False)

print("Done.")
