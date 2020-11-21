import yaml
# default yaml file converter
uvfitscode_color={
    ('AA', 'AP'): "red",
('AA', 'AZ'): "green",
('AA', 'JC'): "blue",
('AA', 'LM'): "yellow",
('AA', 'PV'): "pink",
('AA', 'SM'): "grey",
('AP', 'AZ'): "purple",
('AP', 'JC'): "coral",
('AP', 'LM'): "darkgreen",
('AP', 'PV'): "darkorange",
('AP', 'SM'): "darkslateblue",
('AZ', 'JC'): "orangered",
('AZ', 'LM'): "plum",
('AZ', 'PV'): "slateblue",
('AZ', 'SM'): "slateblue",
('JC', 'LM'): "peachpuff",
('JC', 'PV'): "rosybrown",
('JC', 'SM'): "indigo",
('LM', 'PV'): "lavender",
('LM', 'SM'): "darkcyan",
('PV', 'SM'): "lime"
}

import yaml
f = open('meta.yaml', 'w+')
yaml.dump(uvfitscode_color, f, allow_unicode=True)



palette = d3['Category10'][len(df['cat'].unique())]
