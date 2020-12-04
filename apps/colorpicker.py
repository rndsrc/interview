
import yaml
from itertools import permutations
color_file= open("colors.txt", "r")

color_list = []
for line in color_file:
    stripped_line = line.strip()
    color_list.append(stripped_line)

color_file.close()

location_file= open("locations.txt", "r")

location_list = []
for line in location_file:
    stripped_line = line.strip()
    location_list.append(stripped_line)

perm_list=list(permutations(location_list, 2))
location_file.close()
for tpl in perm_list:
    if (tpl[1],tpl[0]) in perm_list:
        perm_list.remove((tpl[1],tpl[0]))
location_list=perm_list
color_set=set(color_list)

final_dict=dict()
for loc_tuple in location_list:
    final_dict[loc_tuple]=color_set.pop()


location_file.close()
with open('./yaml_files/locations.yaml', 'w') as f:
    yaml.dump(final_dict,f)

