import pickle
import numpy as np
import sys


def calc_ent(x):
    """
        calculate shanno ent of x
    """

    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]
        logp = np.log2(p)
        ent -= p * logp

    return ent


def calc_nor_ent(x):
    """
        calculate normalized shanno ent of x
    """

    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]
        logp = np.log2(p)
        ent -= p * logp
    if len(x_value_list) == 1:
        return 0
    return ent / float(np.log2(len(x_value_list)))


def mean_entropy(go_path, ali_path):
    dic = open(go_path, 'rb')
    go_dic = pickle.load(dic)
    fr = open(ali_path)

    entropy = []
    for each in fr.readlines():
        go_list = []
        for pro in each.strip().split('\t'):
            if pro in go_dic.keys():
                for go in go_dic[pro]:
                    go_list.append(go)
        if len(go_list) != 0:
            match_set = np.array(go_list)
            ent = calc_ent(match_set)
            # print(ent, go_list)
            entropy.append(ent)
    fr.close()
    np_entropy = np.array(entropy)
    print('mean entropy:', np_entropy.mean())
    return np_entropy.mean()


def normalized_mean_ent(go_path, ali_path):
    dic = open(go_path, 'rb')
    go_dic = pickle.load(dic)
    fr = open(ali_path)

    entropy = []
    for each in fr.readlines():
        go_list = []
        for pro in each.strip().split('\t'):
            if pro in go_dic.keys():
                for go in go_dic[pro]:
                    go_list.append(go)
        if len(go_list) != 0:
            match_set = np.array(go_list)
            ent = calc_nor_ent(match_set)
            # print(ent, go_list)
            entropy.append(ent)
    fr.close()
    np_entropy = np.array(entropy)
    print('normalized mean entropy:', np_entropy.mean())
    return np_entropy.mean()

# go_P = 'F:\my_study\GO\prepared go\go_dick.txt'
# ali_i = 'F:\my_study\GO\\test_coverage\\Res_test1.txt'
# ali_m = 'F:\my_study\GO\\test_coverage\\Res_test1_CIQ_10_100_100.txt'
# ali_0 = 'F:\my_study\GO\\test_coverage\\testr_beta0.ali'
# ali_8 = 'F:\my_study\GO\\test_coverage\\testr_beta0.8.ali'
# ali_9 = 'F:\my_study\GO\\test_coverage\\testr_beta0.9.ali'
# ali_Ne = 'F:\my_study\GO\\test_coverage\\Result1.ali'
# # mean_entropy(go_P, ali_i)
# # normalized_mean_ent(go_P, ali_i)
# # print('iso' + '\n')
#
# mean_entropy(go_P, ali_m)
# normalized_mean_ent(go_P, ali_m)
# print('multiMAGNA++' + '\n')
#
# mean_entropy(go_P, ali_Ne)
# normalized_mean_ent(go_P, ali_Ne)
# print('NetCoffee beta mean' + '\n')
#
# mean_entropy(go_P, ali_0)
# normalized_mean_ent(go_P, ali_0)
# print('NetCoffee beta 0' + '\n')
#
# mean_entropy(go_P, ali_8)
# normalized_mean_ent(go_P, ali_8)
# print('NetCoffee beta 0.8' + '\n')
#
# mean_entropy(go_P, ali_9)
# normalized_mean_ent(go_P, ali_9)
# print('NetCoffee beta 0.9' + '\n')

if '__name__' == '__main__':
    go_path = sys.argv[1]
    ali_path = sys.argv[2]
    # print(ali_path)
    mean_entropy(go_path, ali_path)
    normalized_mean_ent(go_path, ali_path)
    print('\n')
