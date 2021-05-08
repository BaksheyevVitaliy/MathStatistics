from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg','pdf')

from scipy.stats import norm, cauchy, laplace, poisson, uniform
import numpy as np
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import codecs
import csv
from statsmodels.distributions.empirical_distribution import ECDF
sns.set_style('whitegrid')
units = [20, 60, 100]
cont_segment = (-4, 4)
discr_segment = (6, 14)
bw_adjust_coefs = [.5, 1, 2]
def bw_title(n, factor):
    if factor == .5:
        return r'$h=0.5h_{' + str(n) + r'}$'
    if factor == 1:
        return r'$h=h_{' + str(n) + r'}$'
    else:
        return r'$h=2 h_{' + str(n) + r'}$'
def get_truncated_sample(segment, distribution, sample_size):
    sample = []
    while len(sample) < sample_size:
        to_add = list(distribution.rvs(size=sample_size - len(sample)))
        to_add = [x for x in to_add if x>=segment[0] and x<=segment[1]]
        sample = sample + to_add
    return sample
def z_p(variational_series, p):
    pn = p * variational_series.size
    if (pn == int(pn)):
        return variational_series[int(pn)]
    return variational_series[int(pn) + 1]
ecdf_fig, axs = plt.subplots(ncols=len(units), figsize=(12,4))
x = np.linspace(cont_segment[0], cont_segment[1], 1000)
y = norm.cdf(x)
for i in range(len(units)):
    axs[i].plot(x,y, color='blue')
    ecdf = ECDF(norm.rvs(size=units[i]))
    axs[i].plot(x,ecdf(x), color='black')
    axs[i].set(xlabel='x', ylabel = "$F(x)$")
    axs[i].set_title(r"Normal $n$ = " + str(units[i]))
ecdf_fig.subplots_adjust(wspace=0.3)
ecdf_fig.savefig("normalECDF.pdf")
x = np.linspace(cont_segment[0], cont_segment[1], 1000)
y = norm.pdf(x)
for i in range(len(units)):
    kernel_fig, axs = plt.subplots(ncols=len(bw_adjust_coefs), figsize=(12,3))
    for j in range(len(bw_adjust_coefs)):
        axs[j].plot(x, y, color='blue')
        sns.kdeplot(data=norm.rvs(size=units[i]), bw_method='silverman', bw_adjust=bw_adjust_coefs[j], ax=axs[j], color='black')
        axs[j].add_artist(AnchoredText(bw_title(units[i], bw_adjust_coefs[j]),loc=2))
    kernel_fig.suptitle(r'Normal $n$ = ' + str(units[i]))
    kernel_fig.subplots_adjust(wspace=0.3)
    kernel_fig.savefig("normalKde" + str(units[i]) + ".pdf")
ecdf_fig, axs = plt.subplots(ncols=len(units), figsize=(12,4))
x = np.linspace(cont_segment[0], cont_segment[1], 1000)
y = cauchy.cdf(x)
for i in range(len(units)):
    axs[i].plot(x,y, color='blue')
    ecdf = ECDF(cauchy.rvs(size=units[i]))
    axs[i].plot(x,ecdf(x), color='black')
    axs[i].set(xlabel='x', ylabel = "$F(x)$")
    axs[i].set_title(r"Cauchy $n$ = " + str(units[i]))
ecdf_fig.subplots_adjust(wspace=0.3)
ecdf_fig.savefig("cauchyECDF.pdf")
#x = np.linspace(cont_segment[0], cont_segment[1], 10000)
#y = cauchy.pdf(x)
for i in range(len(units)):
    kernel_fig, axs = plt.subplots(ncols=len(bw_adjust_coefs), figsize=(12,3))
    for j in range(len(bw_adjust_coefs)):
        sample = cauchy.rvs(size=units[i])
        sample.sort()
        x = np.linspace(min(min(sample),cont_segment[0]),max(max(sample),cont_segment[1]), 10000)
        y = cauchy.pdf(x)
        Q_1 = z_p(sample, 1/4)
        Q_3 = z_p(sample, 3/4)
        X_1 = Q_1 - 1.5 * (Q_3 - Q_1)
        X_2 = Q_3 + 1.5 * (Q_3 - Q_1)
        sample_truncated = [x for x in sample if x >= X_1 and x <= X_2]
        sns.kdeplot(data=sample, bw_method='silverman',
                    bw_adjust=bw_adjust_coefs[j], ax=axs[j], color='black')
        #axs[j].set_xlim(cont_segment)
        axs[j].add_artist(AnchoredText(bw_title(units[i], bw_adjust_coefs[j]),loc=2))
        axs[j].plot(x, y, color='blue')
    kernel_fig.suptitle(r'Cauchy $n$ = ' + str(units[i]))
    kernel_fig.subplots_adjust(wspace=0.3)
    kernel_fig.savefig("cauchyKde" + str(units[i]) + ".pdf")
sample1 = cauchy.rvs(size=11)
print(sample1)
sample1 = sample + [1]
print(sample1)

ecdf_fig, axs = plt.subplots(ncols=len(units), figsize=(12,4))
x = np.linspace(cont_segment[0], cont_segment[1], 1000)
y = laplace(scale=2 ** (-0.5), loc=0).cdf(x)
for i in range(len(units)):
    axs[i].plot(x,y, color='blue')
    ecdf = ECDF(laplace.rvs(scale=2 ** (-0.5), loc=0, size=units[i]))
    axs[i].plot(x,ecdf(x), color='black')
    axs[i].set(xlabel='x', ylabel = "$F(x)$")
    axs[i].set_title(r"Laplace $n$ = " + str(units[i]))
ecdf_fig.subplots_adjust(wspace=0.3)
ecdf_fig.savefig("laplaceECDF.pdf")
x = np.linspace(cont_segment[0], cont_segment[1], 1000)
y = laplace(scale=2 ** (-0.5), loc=0).pdf(x)
for i in range(len(units)):
    kernel_fig, axs = plt.subplots(ncols=len(bw_adjust_coefs), figsize=(12,3))
    for j in range(len(bw_adjust_coefs)):
        axs[j].plot(x, y, color='blue')
        sns.kdeplot(data=laplace.rvs(scale=2 ** (-0.5), loc=0,size=units[i]), bw_method='silverman', bw_adjust=bw_adjust_coefs[j], ax=axs[j], color='black')
        axs[j].add_artist(AnchoredText(bw_title(units[i], bw_adjust_coefs[j]),loc=2))
    kernel_fig.suptitle(r'Laplace $n$ = ' + str(units[i]))
    kernel_fig.subplots_adjust(wspace=0.3)
    kernel_fig.savefig("laplaceKde" + str(units[i]) + ".pdf")
ecdf_fig, axs = plt.subplots(ncols=len(units), figsize=(12,4))
x = np.linspace(discr_segment[0], discr_segment[1], 1000)
y = poisson(10).cdf(x)
for i in range(len(units)):
    line1, = axs[i].plot(x,y, color='blue')
    ecdf = ECDF(poisson.rvs(10, size=units[i]))
    line2, = axs[i].plot(x,ecdf(x), color='black')
    axs[i].set(xlabel='x', ylabel = "$F(x)$")
    axs[i].set_title(r"Poisson $n$ = " + str(units[i]))
    axs[i].legend((line1, line2),(r"$F_X(x)$",r'$F_{'+ str(units[i]) + r'}^{*}(x)$'))
ecdf_fig.subplots_adjust(wspace=0.3)
ecdf_fig.savefig("poissonECDF.pdf")

x = np.linspace(discr_segment[0], discr_segment[1], discr_segment[1] - discr_segment[0] + 1)
y = poisson(10).pmf(x)
for i in range(len(units)):
    kernel_fig, axs = plt.subplots(ncols=len(bw_adjust_coefs), figsize=(12,3))
    for j in range(len(bw_adjust_coefs)):
        axs[j].plot(x, y, color='blue')
        sns.kdeplot(data=poisson.rvs(10, size=units[i]), bw_method='silverman', bw_adjust=bw_adjust_coefs[j], ax=axs[j], color='black')
        axs[j].add_artist(AnchoredText(bw_title(units[i], bw_adjust_coefs[j]),loc=3))
        axs[j].set_xlim(discr_segment)
    kernel_fig.suptitle(r'Poisson $n$ = ' + str(units[i]))
    kernel_fig.subplots_adjust(wspace=0.3)
    kernel_fig.savefig("poisKde" + str(units[i]) + ".pdf")
ecdf_fig, axs = plt.subplots(ncols=len(units), figsize=(12,4))
x = np.linspace(cont_segment[0], cont_segment[1], 1000)
y = uniform(loc=-3**0.5, scale=2*3**0.5).cdf(x)
for i in range(len(units)):
    axs[i].plot(x,y, color='blue')
    ecdf = ECDF(uniform.rvs(loc=-3**0.5, scale=2*3**0.5, size=units[i]))
    axs[i].plot(x,ecdf(x), color='black')
    axs[i].set(xlabel='x', ylabel = "$F(x)$")
    axs[i].set_title(r"Uniform $n$ = " + str(units[i]))
ecdf_fig.subplots_adjust(wspace=0.3)
ecdf_fig.savefig("uniformECDF.pdf")
x = np.linspace(cont_segment[0], cont_segment[1], 1000)
y = uniform(loc=-3**0.5, scale=2*3**0.5).pdf(x)
for i in range(len(units)):
    kernel_fig, axs = plt.subplots(ncols=len(bw_adjust_coefs), figsize=(12,3))
    for j in range(len(bw_adjust_coefs)):
        axs[j].plot(x, y, color='blue')
        sns.kdeplot(data=uniform.rvs(loc=-3**0.5, scale=2*3**0.5, size=units[i]), bw_method='silverman', bw_adjust=bw_adjust_coefs[j], ax=axs[j], color='black')
        axs[j].add_artist(AnchoredText(bw_title(units[i], bw_adjust_coefs[j]),loc=2))
        axs[j].set_xlim(cont_segment)
    kernel_fig.suptitle(r'Uniform $n$ = ' + str(units[i]))
    kernel_fig.subplots_adjust(wspace=0.3)
    kernel_fig.savefig("unifKde" + str(units[i]) + ".pdf")
