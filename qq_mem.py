import re
import argparse


def paras():
    paraser = argparse.ArgumentParser()
    paraser.add_argument('file', help="core file you wanna analyse")
    paraser.add_argument('-s', '--strict', help="use chat box content(may can't find some string)",
                         action="store_true")
    paraser.add_argument('-n', '--norep', help="output not repeating string",
                         action="store_true")
    args = paraser.parse_args()

    return args.file, args.strict, args.norep


def main():
    filename, strict, norep = paras()

    # 聊天框字体匹配等
    pat_chat = br'\x20\x00\x28\x0a\x30\x00\x38\x86\x01\x40\x02\x4a\x06' \
               br'[\x00-\xff][\x00-\xff][\x00-\xff][\x00-\xff][\x00-\xff][\x00-\xff][\x00-\xff]'
    # 直接匹配字符串
    pat_str = br'[\x00-\xff]\x0a[\x00-\xff]\x0a[\x00-\xff]'
    if strict:
        pat = re.compile(pat_chat + pat_str)
        offset = 20 + 5
    else:
        pat = re.compile(pat_str)
        offset = 5
    count = 0
    readed = []
    with open(filename, "rb") as f:
        bins = f.read()
        for m in pat.finditer(bins):
            if m.group()[-5] - 4 == m.group()[-3] - 2 == m.group()[-1]:
                cur_bstr = bins[m.start() + offset:m.start() + offset + m.group()[-1]]
                try:
                    cur_str = cur_bstr.decode('utf-8')
                except:
                    cur_str = "解码失败"
                if norep:
                    if cur_str not in readed:
                        print("0x{:x}".format(m.start() + 5), cur_str)
                        readed.append(cur_str)
                        count += 1
                else:
                    print("0x{:x}".format(m.start() + 5), cur_str)
                    count += 1
    print("find {} record".format(count))


if __name__ == '__main__':
    main()
