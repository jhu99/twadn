import os


def split_confidence(path, name):
    fr = open(os.path.join(path, name))
    fw = open(os.path.join(path, 'dyna_' + name), 'w')
    lines = fr.readlines()
    whole = len(lines)
    start = int(whole * 0.75)
    for i in range(start):
        info = lines[i].strip().split('\t')
        fw.write('dyna_1' + '\t' + '\t'.join(info[1:]) + '\n')

    second = int(whole * 0.80)
    for i in range(second):
        info = lines[i].strip().split('\t')
        fw.write('dyna_2' + '\t' + '\t'.join(info[1:]) + '\n')

    third = int(whole * 0.85)
    for i in range(third):
        info = lines[i].strip().split('\t')
        fw.write('dyna_3' + '\t' + '\t'.join(info[1:]) + '\n')

    fourth = int(whole * 0.90)
    for i in range(fourth):
        info = lines[i].strip().split('\t')
        fw.write('dyna_4' + '\t' + '\t'.join(info[1:]) + '\n')

    fifth = int(whole * 0.95)
    for i in range(fifth):
        info = lines[i].strip().split('\t')
        fw.write('dyna_5' + '\t' + '\t'.join(info[1:]) + '\n')

    sixth = whole
    for i in range(sixth):
        info = lines[i].strip().split('\t')
        fw.write('dyna_6' + '\t' + '\t'.join(info[1:]) + '\n')

    fw.close()
    fr.close()


if __name__ == '__main__':
    path = 'F:\my_study\IntAct\lastest_network\dynamic\\twadn'
    split_confidence(path, 'twadn_960.txt')