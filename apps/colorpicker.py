
import yaml
import os
import pandas as pd
from itertools import permutations
import ehtim as eh
color_file= open("colors.txt", "r")

color_list = []
for line in color_file:
    stripped_line = line.strip()
    color_list.append(stripped_line)

color_file.close()
file_list=[]
for root, dirs, files in os.walk('./uvfitsfiles'):
    for file in files:
        if file.endswith('.uvfits'):
            file_list.append(os.path.join(root, file))



            


df = pd.concat( map (lambda file : pd.DataFrame(eh.obsdata.load_uvfits(file).avg_coherent(inttime=300).
unpack(['time_utc', 't1', 't2', 'u', 'v', 'amp', 'phase', 'sigma']))\
,file_list) )
\



location_list=list(set(df.t1.unique()).union(set(df.t2.unique())))
perm_list=list(permutations(location_list, 2))
for tpl in perm_list:
    if (tpl[1],tpl[0]) in perm_list:
        perm_list.remove((tpl[1],tpl[0]))
location_list=perm_list
color_set=set(color_list)

final_dict=dict()
for loc_tuple in location_list:
    final_dict[loc_tuple]=color_set.pop()
with open('./yaml_files/locations.yaml', 'w') as f:
    yaml.dump(final_dict,f)



