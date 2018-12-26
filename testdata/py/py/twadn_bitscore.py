import os


def str_add(pro1, pro2):
    if pro1 >= pro2:
        return pro1 + '\t' + pro2
    return pro2 + '\t' + pro1


def twadn_bitscore(path, name):
    bit_path = 'F:\my_study\IntAct\evalue_bitscore.txt'
    fr = open(os.path.join(path, name))
    pro_set = set()
    for each in fr.readlines():
        info = each.strip().split('\t')
        pro_set.add(info[1])
        pro_set.add(info[2])
    fr.close()
    print('len pro_set', len(pro_set))
    fw = open(os.path.join(path, 'bit_' + name), 'w')
    fr_bit = open(bit_path)
    bit_dict = {}
    for each in fr_bit.readlines():
        info = each.strip().split('\t')
        if info[0] in pro_set and info[1] in pro_set:
            bit_dict[str_add(info[0], info[1])] = '\t'.join(info[2:])
    fr_bit.close()
    for key in bit_dict.keys():
        pros = key.split('\t')
        fw.write('\t'.join([pros[0], pros[1] + '_dyna_1', bit_dict[key] + '\n']))
        fw.write('\t'.join([pros[1], pros[0] + '_dyna_1', bit_dict[key] + '\n']))
    fw.close()


if __name__ == '__main__':
    path = 'F:\my_study\IntAct\lastest_network\dynamic\\twadn'
    twadn_bitscore(path, 'twadn_960.txt')