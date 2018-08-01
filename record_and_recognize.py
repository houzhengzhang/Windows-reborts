import re


def get_instruction(sentence):
    # try:
    pattern = r"(下[\u4e00-\u9fa5]{0,3}?首(歌曲)*)|(上[\u4e00-\u9fa5]{0,3}?首(歌曲)*)|(暂[\u4e00-\u9fa5]{0,1}?停(歌曲|歌子)?|(重新[\u4e00-\u9fa5]{0,3}?开始(这)*(首)*(歌曲)*)|(开始(播放)*[\u4e00-\u9fa5]{0,3}?(歌曲)*))"

    p = re.compile(pattern)
    all = p.findall(sentence)
    # print(len(all))
    if len(all) == 0:
        return 10
    tar = all[len(all) - 1]

    # print(tar[0])
    """
    差指
    """
    for t in tar:
        if "暂停" in t:
            print("暂停")
            return 1
        elif "暂停歌曲" in t:
            print("暂")
            return 4
        elif "暂停歌子" in t:
            print("暂停")
            return 4
        elif "上" in t:
            print("上")
            return 3
        elif "下" in t:
            print("下")
            return 2
        elif "重" in t:
            print("重新开始")
            return 5
        elif "开" in t:
            print("开始")
            return 0
