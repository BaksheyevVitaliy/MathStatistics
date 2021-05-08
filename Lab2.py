from scipy.stats import norm, cauchy, laplace, poisson, uniform
import numpy as np
import csv
def sample_mean(sample):
    return np.mean(sample)
def sample_median(sample):
    return np.median(sample)
def sample_median(sample):
    return np.median(sample)
def z_R(variational_series):
    return (variational_series[0] + variational_series[variational_series.size - 1]) / 2

def z_p(variational_series, p):
    pn = p * variational_series.size
    if (pn == int(pn)):
        return variational_series[int(pn)]
    return variational_series[int(pn) + 1]

def z_Q(variational_series):
    return (z_p(variational_series, 1/4) + z_p(variational_series, 3/4)) / 2
def trim_mean(variational_series):
    n = variational_series.size
    r = int(n/4)
    sum = 0.
    for i in range(r + 1, n - r + 1):
        sum += variational_series[i]
    return sum / (n - 2*r)
def sample_variance(sample):
    return np.std(sample)**2

def mean_estimation(E, D):
    return E - D ** 0.5, E + D ** 0.5

print(mean_estimation(0.111, 0.2))
number_of_experiments = 1000
units = [10, 100, 1000]
E = []
D = []
E_est = []
for u_num in units:
    samples_means = []
    samples_medians = []
    samples_z_Rs = []
    samples_z_Qs = []
    samples_z_trs = []
    for i in range(number_of_experiments):
        sample = norm.rvs(scale=1, loc=0, size= u_num)
        samples_means.append(sample_mean(sample))
        samples_medians.append(sample_median(sample))
        sample.sort()
        samples_z_Rs.append(z_R(sample))
        samples_z_Qs.append(z_Q(sample))
        samples_z_trs.append(trim_mean(sample))
    val_lists = [samples_means, samples_medians, samples_z_Rs, samples_z_Qs, samples_z_trs]
    E_s = [round(sample_mean(val_list), 6) for val_list in val_lists]
    D_s = [round(sample_variance(val_list), 6) for val_list in val_lists]
    E_est_s = [mean_estimation(E_s[i], D_s[i]) for i in range(len(val_lists))]
    E_est_s = [[round(E_est_s[i][0],6), round(E_est_s[i][1],6)] for i in range(len(val_lists))]
    print(E_s)
    print(D_s)
    print(E_est_s)
    print('\n')
    E.append(E_s)
    D.append(D_s)
    E_est.append(E_est_s)
#Создание таблицы
with open('normalChs.tex','w', newline = '') as f:
    writer = csv.writer(f, delimiter = '&')
    filler_row = [" " for j in range(5)]
    filler_row.append(r" \\")
    hline = "\hline\n"
    for i in range(3):
        row_1 = [" " for j in range(4)]
        row_1.append(r" \\")
        row_1.insert(0, "Normal $n$ = " + str(units[i]))
        writer.writerow(row_1)
        if i == 0:
            row_2 = [" ", "$\overline{x}\;\eqref{mean}$", "$med\;x\;\eqref{med}$", "$z_R\;\eqref{exhfsum}$",
                "$z_Q\;\eqref{hfsum}$", r"$z_{tr}\;\eqref{trmean}$\\"]
        else:
            row_2 = [" ", "$\overline{x}$", "$med\;x$", "$z_R$",
                "$z_Q$", r"$z_{tr}$\\"]
        f.write(hline)
        writer.writerow(row_2)
        E[i][len(E[i]) - 1] = str(E[i][len(E[i]) - 1]) + r"\\"
        if i == 0:
            str_to_ins = "$E(z)\;\eqref{mean_formula}$"
        else:
            str_to_ins = "$E(z)$"
        E[i].insert(0, str_to_ins)
        f.write(hline)
        writer.writerow(E[i])
        if i == 0:
            str_to_ins = "$D(z)\;\eqref{variance_formula}$"
        else:
            str_to_ins = "$D(z)$"
        D[i][len(D[i]) - 1] = str(D[i][len(D[i]) - 1]) + r"\\"
        D[i].insert(0, str_to_ins)
        f.write(hline)
        writer.writerow(D[i])
        if i == 0:
            str_to_ins = "$E(z)\pm\sqrt{D(z)}\;\eqref{confint}$"
        else:
            str_to_ins = "$E(z)\pm\sqrt{D(z)}$"
        E_est[i] = ["(" + str(E_est[i][j][0]) + r",\newline" + str(E_est[i][j][1]) + ")" for j in range(len(E_est[i]))]
        replacement = E_est[i][len(E_est[i]) - 1] + r"\\"
        E_est[i].pop(len(E_est[i]) - 1)
        E_est[i].append(replacement)
        E_est[i].insert(0, str_to_ins)
        f.write(hline)
        writer.writerow(E_est[i])
        if (i != 2):
            f.write(hline)
            writer.writerow(filler_row)
        f.write(hline)
def create_table(E, D, distribution_name, E_est, undefined_mean=False, undefined_z_r=False):
    with open(distribution_name + 'Chs.tex','w', newline = '') as f:
        writer = csv.writer(f, delimiter = '&')
        filler_row = [" " for j in range(5)]
        filler_row.append(r" \\")
        hline = "\hline\n"
        for i in range(3):
            row_1 = [" " for j in range(4)]
            row_1.append(r" \\")
            row_1.insert(0, distribution_name + " $n$ = " + str(units[i]))
            writer.writerow(row_1)
            row_2 = [" ", "$\overline{x}$", "$med\;x$", "$z_R$",
                    "$z_Q$", r"$z_{tr}$\\"]
            f.write(hline)
            writer.writerow(row_2)
            E[i][len(E[i]) - 1] = str(E[i][len(E[i]) - 1]) + r"\\"
            str_to_ins = "$E(z)$"
            E[i].insert(0, str_to_ins)
            f.write(hline)
            writer.writerow(E[i])
            str_to_ins = "$D(z)$"
            D[i][len(D[i]) - 1] = str(D[i][len(D[i]) - 1]) + r"\\"
            D[i].insert(0, str_to_ins)
            f.write(hline)
            writer.writerow(D[i])
            str_to_ins = "$E(z)\pm\sqrt{D(z)}$"
            E_est[i] = ["(" + str(E_est[i][j][0]) + r",\newline" + str(E_est[i][j][1]) + ")" for j in range(len(E_est[i]))]
            replacement = E_est[i][len(E_est[i]) - 1] + r"\\"
            E_est[i].pop(len(E_est[i]) - 1)
            E_est[i].append(replacement)
            E_est[i].insert(0, str_to_ins)
            if undefined_mean:
                E_est[i].pop(1)
                E_est[i].insert(1,"$-$")
            if undefined_z_r:
                E_est[i].pop(3)
                E_est[i].insert(3,"$-$")
            f.write(hline)
            writer.writerow(E_est[i])
            if i != 2:
                f.write(hline)
                writer.writerow(filler_row)
            f.write(hline)
E = []
D = []
E_est = []
for u_num in units:
    samples_means = []
    samples_medians = []
    samples_z_Rs = []
    samples_z_Qs = []
    samples_z_trs = []
    for i in range(number_of_experiments):
        sample = cauchy.rvs(scale=1, loc=0, size=u_num)
        samples_means.append(sample_mean(sample))
        samples_medians.append(sample_median(sample))
        sample.sort()
        samples_z_Rs.append(z_R(sample))
        samples_z_Qs.append(z_Q(sample))
        samples_z_trs.append(trim_mean(sample))
    val_lists = [samples_means, samples_medians, samples_z_Rs, samples_z_Qs, samples_z_trs]
    E_s = [round(sample_mean(val_list), 6) for val_list in val_lists]
    D_s = [round(sample_variance(val_list), 6) for val_list in val_lists]
    E_est_s = [mean_estimation(E_s[i], D_s[i]) for i in range(len(val_lists))]
    E_est_s = [[round(E_est_s[i][0],6), round(E_est_s[i][1],6)] for i in range(len(val_lists))]
    print(E_s)
    print(D_s)
    print(E_est_s)
    print('\n')
    E.append(E_s)
    D.append(D_s)
    E_est.append(E_est_s)
create_table(E, D, 'Cauchy', E_est, undefined_mean=True, undefined_z_r=True)
E = []
D = []
E_est = []
for u_num in units:
    samples_means = []
    samples_medians = []
    samples_z_Rs = []
    samples_z_Qs = []
    samples_z_trs = []
    for i in range(number_of_experiments):
        sample = laplace.rvs(scale=2 ** (-0.5), loc=0, size=u_num)
        samples_means.append(sample_mean(sample))
        samples_medians.append(sample_median(sample))
        sample.sort()
        samples_z_Rs.append(z_R(sample))
        samples_z_Qs.append(z_Q(sample))
        samples_z_trs.append(trim_mean(sample))
    val_lists = [samples_means, samples_medians, samples_z_Rs, samples_z_Qs, samples_z_trs]
    E_s = [round(sample_mean(val_list), 6) for val_list in val_lists]
    D_s = [round(sample_variance(val_list), 6) for val_list in val_lists]
    E_est_s = [mean_estimation(E_s[i], D_s[i]) for i in range(len(val_lists))]
    E_est_s = [[round(E_est_s[i][0],6), round(E_est_s[i][1],6)] for i in range(len(val_lists))]
    print(E_s)
    print(D_s)
    print(E_est_s)
    print('\n')
    E.append(E_s)
    D.append(D_s)
    E_est.append(E_est_s)
create_table(E, D, 'Laplace', E_est)
E = []
D = []
E_est = []
for u_num in units:
    samples_means = []
    samples_medians = []
    samples_z_Rs = []
    samples_z_Qs = []
    samples_z_trs = []
    for i in range(number_of_experiments):
        sample = poisson.rvs(10, size=u_num)
        samples_means.append(sample_mean(sample))
        samples_medians.append(sample_median(sample))
        sample.sort()
        samples_z_Rs.append(z_R(sample))
        samples_z_Qs.append(z_Q(sample))
        samples_z_trs.append(trim_mean(sample))
    val_lists = [samples_means, samples_medians, samples_z_Rs, samples_z_Qs, samples_z_trs]
    E_s = [round(sample_mean(val_list), 6) for val_list in val_lists]
    D_s = [round(sample_variance(val_list), 6) for val_list in val_lists]
    E_est_s = [mean_estimation(E_s[i], D_s[i]) for i in range(len(val_lists))]
    E_est_s = [[round(E_est_s[i][0],6), round(E_est_s[i][1],6)] for i in range(len(val_lists))]
    print(E_s)
    print(D_s)
    print(E_est_s)
    print('\n')
    E.append(E_s)
    D.append(D_s)
    E_est.append(E_est_s)
create_table(E, D, 'Poisson', E_est)
E = []
D = []
E_est = []
for u_num in units:
    samples_means = []
    samples_medians = []
    samples_z_Rs = []
    samples_z_Qs = []
    samples_z_trs = []
    for i in range(number_of_experiments):
        sample = uniform.rvs(loc=-3**0.5, scale=2*3**0.5,size=u_num)
        samples_means.append(sample_mean(sample))
        samples_medians.append(sample_median(sample))
        sample.sort()
        samples_z_Rs.append(z_R(sample))
        samples_z_Qs.append(z_Q(sample))
        samples_z_trs.append(trim_mean(sample))
    val_lists = [samples_means, samples_medians, samples_z_Rs, samples_z_Qs, samples_z_trs]
    E_s = [round(sample_mean(val_list), 6) for val_list in val_lists]
    D_s = [round(sample_variance(val_list), 6) for val_list in val_lists]
    E_est_s = [mean_estimation(E_s[i], D_s[i]) for i in range(len(val_lists))]
    E_est_s = [[round(E_est_s[i][0],6), round(E_est_s[i][1],6)] for i in range(len(val_lists))]
    print(E_s)
    print(D_s)
    print(E_est_s)
    print('\n')
    E.append(E_s)
    D.append(D_s)
    E_est.append(E_est_s)
create_table(E, D, 'Uniform', E_est)
