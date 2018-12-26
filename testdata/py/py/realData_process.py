# author  hjh



def str_add(pro1, pro2):
    if pro1 >= pro2:
        return pro1 + '\t' + pro2
    return pro2 + '\t' + pro1

def twadn(path_ori, path_twa):
    fr = open(path_ori)
    title = fr.readline()
    confident_dict = []
    for each in fr.readlines():
        info = each.strip().split('\t')
        interactor_a = info[0].split(':')[1]
        database1 = info[0].split(':')[0]
        interactor_b = info[1].split(':')[1]
        database2 = info[1].split(':')[0]
        # remove the protein with EBI begin
        if database1 != 'uniprotkb' or database2 != 'uniprotkb':
            continue
        confident_val = info[-1][-4:]
        confident_dict.append([confident_val, str_add(interactor_a, interactor_b)])
    fr.close()
    confident_dict.sort(reverse=True)
    fw = open(path_twa, 'w')
    pre = ''
    for each in confident_dict:
        if each[1] != pre:
            fw.write(each[0] + '\t' + each[1] + '\n')
            pre = each[1]
    fw.close()

if __name__ == '__main__':
    path = 'F:\my_study\IntAct\lastest_network\dynamic\\'
    twadn(path + 'original\\taxidA_960.txt', path + 'twadn\\twadn_960.txt')