from prettytable import PrettyTable
from Grammar import *
import sys

DFA = []
DFA_end = []
trans = []
dot_g = []

def dot():
    global extend_grammar
    global dot_g
    notT = init_notT()
    j = 0
    for i in range(0,len(notT)):
        temp = [notT[i]]
        while j < len(extend_grammar):
            sa = extend_grammar[j].split("->")
            if sa[0] == notT[i] :
                if sa[1] != "%":
                    temp.append(sa[0] + "->" + "·" + sa[1])
                else:
                    temp.append(sa[0] + "->" + "·" )
                j += 1
            else :
                break
        dot_g.append(temp)
    print(dot_g)

def generate_node(str):
    #print("=====generate=====")
    global DFA
    node = [str]
    notT = init_notT()
    i = 0
    while i < len(node):
        g = node[i].split("->")
        temp = g[1].split("·")
        if temp[1] != "": #如果·不在最后
            index = find_notT(temp[1], notT)
            if index != -1:
                for j in range(1, len(dot_g[index])):
                    if node.count(dot_g[index][j]) == 0:
                        node.append(dot_g[index][j])
        i += 1
    node_end = [0]*len(node)
    DFA.append(node)
    DFA_end.append(node_end)
    trans.append([])
    # print( "new node:", node)
    # print("==========")

def add_gen(id,str):
    global DFA
    node = [str]
    DFA[id].append(str)
    DFA_end[id].append(0)
    notT = init_notT()
    i = 0
    while i < len(node):
        g = node[i].split("->")
        temp = g[1].split("·")
        if temp[1] != "": #如果·不在最后
            index = find_notT(temp[1], notT)
            if index != -1:
                for j in range(1, len(dot_g[index])):
                    if DFA[id].count(dot_g[index][j]) == 0:
                        node.append(dot_g[index][j])
                        DFA[id].append(dot_g[index][j])
                        DFA_end[id].append(0)
        i += 1


def move(s,mark,notT):
    # print("=====move=====")
    # print(s)
    s = s.split("->")  #s = S~ ,·S
    index = s[1].find("·")
    x = find_notT(s[1][index+1:],notT)
    if index == 0 :
        if x == -1:
            if len(s[1][index+1:]) > 1:
                res = s[0] + "->" + s[1][1] + "·" + s[1][2:]
            else:
                res = s[0] + "->" + s[1][1] + "·"
        else:
            if len(s[1][index+1:]) > len(notT[x]):
                res = s[0] + "->" + s[1][1:len(notT[x])+1] + "·" + s[1][len(notT[x])+1:]
            else:
                res = s[0] + "->" + s[1][1:len(notT[x]) + 1] + "·"
    else:
        if x == -1:
            if len(s[1][index + 1:]) > 1:
                res = s[0] + "->" + s[1][0:index] + s[1][index + 1:index + 2] + "·" + s[1][index + 2:]
            else:
                res = s[0] + "->" + s[1][0:index] + s[1][index + 1:index + 2] + "·"
        else:
            if len(s[1][index + 1:]) > len(notT[x]):
                res = s[0] + "->" + s[1][0:index] + s[1][index + 1:index + 1 + len(notT[x])] + "·" + s[1][index + 1 + len(notT[x]):]
            else:
                res = s[0] + "->" + s[1][0:index] + s[1][index + 1:index + 1 + len(notT[x])] + "·"
    # print(res)
    # print("=======")
    return res

def check_node(str):
    global DFA
    flag = 0
    for i in range(0,len(DFA)):
        for j in range(0,len(DFA[i])):
            if DFA[i][j] == str:
                return i
            else :
                flag = 1
    if flag == 1:
        return -1


def create_DFA():
    global DFA
    global DFA_end
    global trans
    notT = init_notT()
    generate_node(dot_g[0][1])

    i = 0
    while i < len(DFA):
        if DFA_end[i].count(0) != 0:
            j = 0
            while j < len(DFA[i]) :
                sent = DFA[i][j].split("->")
                index = sent[1].find("·")
                if index + 1 == len(sent[1]): #·已经在最后了
                    DFA_end[i][j] = 1
                else:
                    mark = find_notT(sent[1][index + 1:], notT)  # 找到·之后的第一个符号，返回非终结符脚标
                    str = move(DFA[i][j], mark, notT)  # 生成·移动后的式子
                    if mark != -1:
                        x = notT[mark]
                    else:
                        spot = sent[1].find("·")
                        x = sent[1][spot + 1]  # 确定·后面的符号

                    if trans[i].count(x) != 0:  # 检查trans中是否已经有这个转换
                        id = trans[i].index(x)
                        id = trans[i][id - 1]
                        #add_gen(id, str)  # 将对应的式子加入目标DFA
                        if DFA[id].count(str) == 0:
                            add_gen(id, str)
                        DFA_end[i][j] = 1
                    else:
                        res = check_node(str)  # trans中没有这个转换 检查是否有包含这个式子的结点
                        if res != -1:
                            trans[i].append(res)
                            trans[i].append(x)
                            DFA_end[i][j] = 1
                        else:  # trans中没有这个转换  也没有包含这个式子的结点 生成新的结点
                            generate_node(str)
                            trans[i].append(len(DFA) - 1)
                            trans[i].append(x)
                            DFA_end[i][j] = 1
                j += 1
                # print(DFA)
                # print(DFA_end)
        i += 1

def chart():
    notT = init_notT()
    T = []
    res = []
    for i in range(0,len(extend_grammar)):
        sa =  extend_grammar[i].split("->")
        for j in range(0,len(sa[1])):
            if sa[1][j] != "'"and sa[1][j] != "%" and notT.count(sa[1][j]) == 0 and T.count(sa[1][j]) == 0:
                T.append(sa[1][j])
    T.append("$")
    row = T + notT
    res = [""]*(len(DFA))
    for i in range(0,len(res)):
        res[i] = [""]*len(row)

    for i in range(0,len(trans),1):
        flag = 0
        for j in range(0, len(DFA[i])):
            if DFA[i][j].endswith("·"):
                flag = 1
                break
        if flag:
            sa = DFA[i][j].split("->")
            if sa[1] == "·":
                s = sa[0] + "->" + "%"
            else:
                s = DFA[i][j][:len(DFA[i][j]) - 1]
            index = extend_grammar.index(s)
            if index != 0 :
                for j in range(0, len(T)):
                    if res[i][j] == "":
                        res[i][j] = "r" + str(index)
                    else:
                        print("conflict grammar")
                        sys.exit()

        if len(trans[i]) != 0:
            for j in range(0, len(trans[i]), 2):
                index = row.index(trans[i][j + 1])
                if index < len(T):
                    if res[i][index] == "":
                        res[i][index] = "s" + str(trans[i][j])
                    else:
                        print("conflict grammar")
                        sys.exit()
                else:
                    if res[i][index] == "":
                        res[i][index] = trans[i][j]
                    else:
                        print("conflict grammar")
                        sys.exit()
    res[1][len(T) - 1] = "acc"
    reschart = [" "] + row
    x = PrettyTable(reschart)
    for i in range(0,len(res)):
        temp = [i] + res[i]
        x.add_row(temp)
    print(x)
    return res

def count(str):
    notT = init_notT()
    num = 0
    while len(str) != 0:
        index = find_notT(str, notT)
        if index == -1:
            str = str[1:]
            num += 1
        else:
            str = str[len(notT[index]):]
            num += 1
    return num


def check(s,res):
    global extend_grammar
    stack_anyl = []
    stack_input = []
    notT = init_notT()
    stack_anyl.append("$")
    stack_anyl.append("s0")
    point = 0
    stack_input.append('$')
    for i in range(0,len(s)):
        stack_input.append(s[len(s) - i - 1])
    print(stack_anyl)
    print(stack_input)
    error_flag = 0
    flag = 1
    while 1 :
        if res[point].count("acc") == 1:
            index = 0
            sa = extend_grammar[index].split("->")
            l = count(sa[1])  # 得到撒sa1的长度
            for i in range(0, l * 2):
                stack_anyl.pop()
            stack_anyl.append(notT[0])
            break
        else:
            if len(trans[point]) == 0 or trans[point].count(stack_input[-1]) == 0:
                index = int(res[point][0][1:])
                sa = extend_grammar[index].split("->")
                l = count(sa[1])  # 得到撒sa1的长度
                for i in range(0, l * 2):
                    stack_anyl.pop()
                point = int(stack_anyl[-1][1:])
                index = trans[point].index(sa[0]) - 1
                stack_anyl.append(sa[0])
                stack_anyl.append("s" + str(trans[point][index]))
                point = trans[point][index]
            else:
                if trans[point].count(stack_input[-1]) != 0:
                    stack_anyl.append(stack_input[-1])
                    index = trans[point].index(stack_input[-1]) - 1
                    point = trans[point][index]
                    stack_anyl.append("s" + str(point))
                    stack_input.pop()
        error_flag += 1
        print("分析：",stack_anyl,"输入：",stack_input)
        if error_flag >len(s)*2+1 :
            print("error")
            flag = 0
            break
    if flag :
        if len(stack_input) > 1:
            print("error")
        else:
            print("final 分析：", stack_anyl, "输入：", stack_input)
            print("accept")




def main():
    global grammar
    wenfa=input()
    while wenfa!='0':
        grammar.append(wenfa)
        wenfa=input()
    print("所有文法：",grammar)
    # normalleft()
    # for i in range(0,len(grammar)):
    #     del_leftfact(i)
    extend()
    print("扩展文法：",extend_grammar)
    print("extend_index:",extend_index)
    dot()
    create_DFA()
    print("DFA:")
    for i in range(0, len(DFA)):
        print("结点内容：",DFA[i],"链接：",trans[i])
    print("================")
    print("chart")
    res = chart()
    s = input()
    check(s,res)




if __name__=='__main__':
    main();


"""
S->aA
A->cA|d
0


S->A|B
A->aAb|c
B->aBd|d
0

acb
aaddd
"""
