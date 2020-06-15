def step1():
    fr = open('train_data', 'r', encoding='utf8')
    fw = open('train_data_pure_chinese', 'w', encoding='utf8')

    # 判断是否是纯中文
    def is_all_chinese(strs):
        for i in strs:
            if not '\u4e00' <= i <= '\u9fa5':
                return False
        return True

    for line in fr.readlines():
        # print(line.strip())
        line_list = line.strip().split('\t')
        if len(line_list) != 2:
            continue
        org, dst = line_list
        if is_all_chinese(org) and is_all_chinese(dst):
            fw.write(line)


def step2():
    fr = open('train_data_pure_chinese', 'r', encoding='utf8')
    fw = open('train_data_with_label', 'w', encoding='utf8')
    for line in fr.readlines():
        line_list = line.strip().split('\t')
        if len(line_list) != 2:
            continue
        org, dst = line_list
        if org == dst:
            fw.write(line.strip() + '\t' + ' '.join(["O"] * len(org)) + '\n')
        else:
            tmp_labels = ["O"] * (len(org))
            org_start = 0
            dst_start = 0
            org_end = len(org) - 1
            dst_end = len(dst) - 1
            while org_start < org_end and dst_start < dst_end and org[org_start] == dst[dst_start]:
                org_start += 1
                dst_start += 1
            while org_start < org_end and dst_start < dst_end and org[org_end] == dst[dst_end]:
                org_end -= 1
                dst_end -= 1
            org_diff_len = org_end - org_start + 1
            dst_diff_len = dst_end - dst_start + 1

            # diff 片段如果等长 考虑替换和顺序 S W
            if org_diff_len == dst_diff_len:
                if org_diff_len == 2 and org[org_end] == dst[dst_start] and org[org_start] == dst[dst_end]:
                    tmp_labels[org_start] = 'W'
                    tmp_labels[org_end] = 'W'
                else:
                    for i in range(org_start, org_end + 1):
                        if org[i] != dst[i]:
                            tmp_labels[i] = 'S'

            # diff 片段如果不等长 考虑增删 M R
            else:
                # print(line.strip(), dst_diff_len, org_diff_len)
                # break
                if org_diff_len == 2 and dst_diff_len == 1:
                    tmp_labels[org_start] = 'R'
                elif org_diff_len == 1 and dst_diff_len == 2:
                    # if org == dst[:-1]:
                    #     tmp_labels[org_start + 1] = 'M'
                    # else:
                        tmp_labels[org_start] = 'M'
            fw.write(line.strip() + '\t' + ' '.join(tmp_labels) + '\n')




if __name__ == '__main__':
    # step1 filter pure chinese char
    # step1()

    # mark label
    step2()