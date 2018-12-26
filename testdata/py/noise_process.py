import os
import random
import collections


def str_add(pro1, pro2):
    if pro1 >= pro2:
        return pro1 + '\t' + pro2
    return pro2 + '\t' + pro1


def delete_pro(original, del_list):
    return [f for f in original if f not in del_list]


def count_interaction(dyna_dict):
    cnt = 0
    for key in dyna_dict.keys():
        cnt += len(dyna_dict[key])
    return cnt

'''

'''
def noise_process(path, name, noise_level):
    i = int(noise_level * 10)
    fr = open(os.path.join(path, name))
    dyna_dict = collections.OrderedDict()
    for each in fr.readlines():
        info = each.strip().split('\t')
        if info[0] not in dyna_dict.keys():
            dyna_dict[info[0]] = []
            dyna_dict[info[0]].append('\t'.join(info[1:]))
        else:
            dyna_dict[info[0]].append('\t'.join(info[1:]))
    fr.close()
    
    for key in dyna_dict.keys():
        picked = random.sample(dyna_dict[key], int(len(dyna_dict[key]) * noise_level))
        dyna_dict[key] = delete_pro(dyna_dict[key], picked)
        for each in picked:
            changed = random.sample(dyna_dict.keys(), 1)[0]
            dyna_dict[changed].append(each)
    
    print('noise level%s:' % noise_level)
    for key in dyna_dict.keys():
        print('len', key, len(dyna_dict[key]))
    print(count_interaction(dyna_dict))

    fw = open(os.path.join(path + '/noise%s' % i, ('noise%s_' % i) + name), 'w')
    for key in dyna_dict.keys():
        for each in dyna_dict[key]:
            add_each = each.split('\t')
            fw.write(key + '\t' + add_each[0] + '_noise_%s'% i + '\t' +
                     add_each[1] + '_noise_%s'% i + '\n')
    fw.close()


def noise_process_structure(path, name, noise_level):
    i = int(noise_level * 10)
    fr = open(os.path.join(path, name))
    dyna_dict = collections.OrderedDict()
    for each in fr.readlines():
        info = each.strip().split('\t')
        if info[0] not in dyna_dict.keys():
            dyna_dict[info[0]] = []
            dyna_dict[info[0]].append(str_add(info[1], info[2]))
        else:
            dyna_dict[info[0]].append(str_add(info[1], info[2]))
    fr.close()
    
    for key in dyna_dict.keys():
        for interaction in dyna_dict[key]:
            if random.uniform(0, 1) > noise_level:
                continue
            picked = random.sample(dyna_dict[key], 1)[0]
            u, v = interaction.split('\t')
            _u, _v = picked.split('\t')
            if u != _v and _u != v:
                if str_add(u, _v) not in dyna_dict[key] and str_add(_u, v) not in dyna_dict[key]:
                    dyna_dict[key].remove(interaction)
                    dyna_dict[key].remove(picked)
                    dyna_dict[key].append(str_add(u, _v))
                    dyna_dict[key].append(str_add(_u, v))
    
    print('noise level%s:' % noise_level)
    for key in dyna_dict.keys():
        print('len', key, len(dyna_dict[key]))
    print(count_interaction(dyna_dict))
    
    if not os.path.exists(path + '/noise%s' % i):
        os.mkdir(os.path.join(path + '/noise%s' % i))
    fw = open(os.path.join(path + '/noise%s' % i, ('noise%s_struct_' % i) + name), 'w')
    for key in dyna_dict.keys():
        for each in dyna_dict[key]:
            add_each = each.split('\t')
            fw.write(key + '\t' + add_each[0] + '_noise_%s'% i + '\t' +
                     add_each[1] + '_noise_%s'% i + '\n')
    fw.close()
            

if __name__ == '__main__':
    path = '/home/hjh/桌面/workshop/my_study/lastNetCoffee2/twadn/testdata/read_data_dynamic/net_9606'
    #noise_process_structure(path, 'net_722.txt', 1)
    noise_process_structure(path, 'net_960.txt', 1)
    #for i in range(10):
       # noise_process(path, 'net_960.txt', i / 10.0)
       # print(i)
