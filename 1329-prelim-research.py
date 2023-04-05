import audioop
import os
from turtle import color
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# sets constant
bkgnd = 0.833

# functions for data processing
def coeff(dat_d: dict, act_sp: float):
    count_av = {i:round((sum(dat_d[i]) - len(dat_d[i])*bkgnd) / len(dat_d[i]), 2) for i in dat_d if dat_d[i]}
    coef_eff = {i:round(count_av[i]/(i * act_sp), 2)   for i in count_av}
    return count_av, coef_eff

# appricsimating function which uses a pd dates
def approximate(x, y, n):
    xx = list(x)
    yy = list(y)
    zz = np.polyfit(xx, yy, n)
    p = np.poly1d(zz)
    app_date = dict()
    app_date['x'] = np.arange(min(x), max(x), 0.01)
    app_date['y'] = p(app_date['x'])
    app_date['koeff'] = zz
    return app_date

# transform data in DataFrame
def transform(dat, act):
    max_len = len(max(dat.values(), key=len))
    for i in dat.keys():
        if len(dat[i]) < max_len:
            dat[i] = [np.mean(dat[i]) for j in range(max_len)]
    frame = pd.DataFrame(dat).T
    frame.index.name = 'mass'
    frame['activ'] = [round(act * i, 3) for i in frame.index]
    frame['aver_coeff'] = coeff(dat, act)[1]
    frame['count_av'] = coeff(dat, act)[0]
    frame['bkgnd_chen'] = 0
    frame = frame.sort_index()
    return frame 

def add_bk(dat, n):
    for i in dat:
        i += i - n + bkgnd
    return dat



# K-40 COKK-055/05-22
print('K-40 COKK-055/05-22')

# input dates
a_sp_k = 14.4
count_r_k = dict()
count_r_k[0.25] = [1.79, 1.83, 1.81, 1.79, 1.84]
count_r_k[0.2] = [1.67, 1.66, 1.72, 1.64, 1.65]
count_r_k[0.15] = [1.45, 1.45, 1.45, 1.49, 1.43]
count_r_k[0.10] = [1.36, 1.33, 1.34, 1.32, 1.36]
#count_r_k[0.05] = [1.23, 1.24, 1.24, 1.21, 1.19]
count_r_k[0.07] = [1.26, 1.20, 1.18, 1.24, 1.14]
count_r_k[0.03] = [1.07 , 1.02, 1.07, 0.993, 0.980 ]
count_r_k[0.05] = [1.14, 1.12, 1.15, 1.11, 1.05]

frame_k_simpl = transform(count_r_k, a_sp_k)
frame_k_simpl['nukl'] = 'K_simpl_A=14.4'

# K-40 12Bk/g
print('K-40 12Bk/g')
a_sp_k1 = 12
 
count_r_k1 = dict()


count_r_k1[0.2] = [1.38, 1.41, 1.42, 1.36, 1.38]
count_r_k1[0.1] = [1.23, 1.19, 1.15, 1.18, 1.23]
count_r_k1[0.05] = [1.08, 1.07, 1.02, 1.00, 1.05]
count_r_k1[0.35] = [1.79, 1.75, 1.78, 1.66, 1.71]
count_r_k1[0.15] = [1.30, 1.36, 1.31, 1.36, 1.37]
#count_r_k1_shield[0.15] = [1.19, 1.18, 1.14, 1.17, 1.14]



frame_k_10 = transform(count_r_k1, a_sp_k1)
frame_k_10['nukl'] = 'K_10_A=12'

rez_fr = pd.concat([frame_k_simpl, frame_k_10])


# K-40 3.6 Bk/g
print('K-40 3.6 Bk/g')
a_sp_k2 = 3.6
 
count_r_k2 = dict()

count_r_k2[0.1] = [0.952, 0.945, 0.925, 0.957, 0.926]
#count_r_k2[0.05] = [0.888, 0.899, 0.874, 0.881]
count_r_k2[0.05] = add_bk([0.847, 0.878, 0.852, 0.865, 0.885], 0.807)
print('count_r_k2[0.05]', count_r_k2[0.05])


frame_k_02 = transform(count_r_k2, a_sp_k2)
frame_k_02['bkgnd_chen'][0.05] = 0.807
frame_k_02['nukl'] = 'K_02'
rez_fr = pd.concat([rez_fr, frame_k_02])


# Sr-90 14/11
print('Sr-90 14/11') 
a_sp_sr = 18.86     


count_r_sr = dict()
count_r_sr_shield = dict()
count_r_sr[0.2] = [1.53, 1.47, 1.52, 1.54, 1.51]
count_r_sr[0.15] = [1.43, 1.43, 1.38, 1.39, 1.43 ]
count_r_sr[0.1] = [1.23, 1.26, 1.28, 1.21, 1.30]
#count_r_sr[0.07] = [1.12, 1.09, 1.07, 1.18, 1.13]
count_r_sr[0.07] = [1.20, 1.23, 1.17, 1.18, 1.16]
#count_r_sr_shield[0.07] = [1.20, 1.23, 1.17, 1.18, 1.16]

count_r_sr[0.05] = [1.07, 1.10, 1.06, 1.07, 1.12]
count_r_sr[0.02] = [0.973, 0.980, 0.974, 0.933, 0.940]
count_r_sr[0.25] = [1.70, 1.67, 1.71, 1.69, 1.72]
count_r_sr[0.17] = [1.48, 1.45, 1.46, 1.52, 1.52]


frame_sr = transform(count_r_sr, a_sp_sr)

frame_sr['nukl'] = 'Sr_05_A=18.86'
rez_fr = pd.concat([rez_fr, frame_sr])
print(rez_fr)
rez_fr.to_csv('1329-pre.csv')

dat1 = approximate(frame_k_simpl['activ'], frame_k_simpl['aver_coeff'], 2)
dat2 = approximate(frame_k_10['activ'], frame_k_10['aver_coeff'], 2)
dat3 = approximate(frame_sr['activ'], frame_sr['aver_coeff'], 2)
dat4 = approximate(frame_k_02['activ'], frame_k_02['aver_coeff'], 1)

dat_m_1 = approximate(frame_k_simpl.index, frame_k_simpl['aver_coeff'], 2)
dat_m_2 = approximate(frame_k_10.index, frame_k_10['aver_coeff'], 2)
dat_m_3 = approximate(frame_sr.index, frame_sr['aver_coeff'], 2)
dat_m_4 = approximate(frame_k_02.index, frame_k_02['aver_coeff'], 1)

dat_gom_1 = approximate(frame_k_simpl['activ'], frame_k_simpl['count_av'], 2)
dat_gom_2 = approximate(frame_k_10['activ'], frame_k_10['count_av'], 2)
dat_gom_3 = approximate(frame_sr['activ'], frame_sr['count_av'], 2)
dat_gom_4 = approximate(frame_k_02['activ'], frame_k_02['count_av'], 1)

app_coeff = [dat1['koeff'], dat2['koeff'], dat3['koeff']]
print(app_coeff)

# figure container
fig = plt.figure()
fig.set_facecolor('w')

# places the axes on a regular grid
ax1 = fig.add_subplot(221)
ax1.set(
    facecolor = 'white',
    title = 'effectivity',
    #ylim = [0, 200],
    xlabel = 'activity of samples',
    ylabel = 'coeff',
)
ax1.grid(True)


plt.plot(list(frame_k_simpl['activ']), frame_k_simpl['aver_coeff'], '.r', dat1['x'], dat1['y'], '-r', label = 'check sample')
plt.plot(frame_k_10['activ'], frame_k_10['aver_coeff'], '.b', dat2['x'], dat2['y'], '-b', label = 'check sample')
plt.plot(frame_sr['activ'], frame_sr['aver_coeff'], '.c', dat3['x'], dat3['y'], '-c', label = 'check sample')
plt.plot(frame_k_02['activ'], frame_k_02['aver_coeff'], '.y', dat4['x'], dat4['y'], '-y', label = 'K-02')

ax2 = fig.add_subplot(223)
ax2.set(
    facecolor = 'white',
    title = 'effectivity',
    #ylim = [0, 200],
    xlabel = 'activity of samples',
    ylabel = 'coeff',
)
ax2.grid(True)

plt.plot(frame_k_simpl['activ'], frame_k_simpl['count_av'], '.r', dat_gom_1['x'], dat_gom_1['y'], '-r', label = 'check sample')
plt.plot(frame_k_10['activ'], frame_k_10['count_av'], '.b', dat_gom_2['x'], dat_gom_2['y'], '-b', label = 'K-10')
plt.plot(frame_sr['activ'], frame_sr['count_av'], '.c', dat_gom_3['x'], dat_gom_3['y'], '-c', label = 'Sr')
plt.plot(frame_k_02['activ'], frame_k_02['count_av'], '.y', dat_gom_4['x'], dat_gom_4['y'], '-y', label = 'K-02')

ax3 = fig.add_subplot(122)
ax3.set(
    facecolor = 'white',
    title = 'effectivity',
    #ylim = [0, 200],
    xlabel = 'mass of samples',
    ylabel = 'coeff',
)
ax3.grid(True)

plt.plot(frame_k_simpl.index, frame_k_simpl['aver_coeff'], '.r', dat_m_1['x'], dat_m_1['y'], '-r', label = 'check sample')
plt.plot(frame_k_10.index, frame_k_10['aver_coeff'], '.b', dat_m_2['x'], dat_m_2['y'], '-b', label = 'K-10')
plt.plot(frame_sr.index, frame_sr['aver_coeff'], '.c', dat_m_3['x'], dat_m_3['y'], '-c', label = 'Sr')
plt.plot(frame_k_02.index, frame_k_02['aver_coeff'], '.y', dat_m_4['x'], dat_m_4['y'], '-y', label = 'K-02')


plt.legend()
plt.savefig('1329-bullshit.jpeg')


plt.close()