# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%


import os
import pandas as pd
import numpy  as np
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def mirror_uv(df):
    """T1 <-> T2 => u, v -> -u, -v; amp  -> amp, phase -> -phase.
    Returns new array with the additive inverse of the phase, u, v
    and swapped T1 and T2 indexes
    """
    # deepcopy ensures anti-aliasing but check if necessary as it is in different scope.
    df2=df.copy()
    col_list=list(df2)
    # TODO: adjust for column name ( something like for elem in column if U in elem then....)

    col_list[1], col_list[2] = col_list[2], col_list[1]
    # TODO: integrate this with U V and phase
    # TODO: Use YAML file
    df2.columns=col_list
    df2["U(lambda)"]*=-1
    df2["V(lambda)"]*=-1
    df2["Iphase(d)"]*=-1
    return df2


csv_fields= [a.strip() for a in """time(UTC),T1,T2,U(lambda),
V(lambda),Iamp(Jy),Iphase(d),Isigma(Jy),sqrtu2v2""".split(',')]
file_list=[]
for root, dirs, files in os.walk('./csvfiles'):
    for file in files:
        if file.endswith('.csv'):
            file_list.append(os.path.join(root, file))

            

#
# df = pd.concat( map (lambda file : pd.DataFrame(eh.obsdata.load_uvfits(file).avg_coherent(inttime=300).
# unpack(['time_utc', 't1', 't2', 'u', 'v', 'amp', 'phase', 'sigma']))\
# ,file_list) )
print(file_list)
print(os)
df = pd.concat( map(lambda file: pd.read_csv(file,names=['time_utc', 't1', 't2', 'u', 'v', 'amp', 'phase', 'sigma'],skiprows=2),["uv1a.csv","uv1b.csv","uv2a.csv","uv2b.csv"]))

df['r'] = np.sqrt(df.u**2 + df.v**2)
df.columns=csv_fields
with open('./yaml_files/locations.yaml', 'r') as f:
    uvfitscode_color = yaml.load(f)
    
# auto load the csv headers into the hovertool
df=df.assign(colors="black")
for sites,color in uvfitscode_color.items():
    df.loc[((df["T1"] == sites[0]) |         (df["T1"] == sites[1])) & ((df["T2"] == sites[0]) |             (df["T2"] == sites[1])),"colors"]=color
    
df_final=pd.concat([df,mirror_uv(df)])
df_1=df_final

pd.eval("D = df1['U(lambda)']**2 + df1.['V(lambda)'] **2", target=df_1)
plt.scatter(df_1["D"],df_1["Iamp(Jy)"])
plt.show()
plt.scatter(df_final["U(lambda)"],df_final["V(lambda)"],c=df_final["colors"])
plt.title("u vs v visibility domain plot")
plt.xlabel("U(lambda)")
plt.ylabel("V(lambda)")


plt.show()

plt.scatter(df_final["sqrtu2v2"],df_final["Iamp(Jy)"],c=df_final["colors"])

plt.title("r vs Amplitude ( log scaled) scatterplot and regression line")
plt.xlabel("r(Baseline GLambda)")
plt.ylabel("Spectral Irradiance amplitude(Jy)")
plt.yscale("log")
plt.figure()
plt.show()


# %%


df_final['log_phase']=np.log10(df_final["Iamp(Jy)"])
sns.regplot("sqrtu2v2","log_phase",df_final)
plt.title("r vs Amplitude ( log scaled) scatterplot and regression line")


plt.show()


# %%



# %%


plt.scatter(df_final["time(UTC)"],df_final["Isigma(Jy)"],c=df_final["colors"])
plt.title(" time vs ")
plt.xlabel("time(UTC)")
plt.ylabel("Spectral Irradiance (Jy)")
plt.show()


# The jansky (symbol Jy, plural janskys) is a non-SI unit of spectral flux density,[1] or spectral irradiance, used especially in radio astronomy. It is equivalent to 10−26 watts per square metre per hertz.


# %%



