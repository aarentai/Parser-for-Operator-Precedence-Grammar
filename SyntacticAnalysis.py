# 生成FIRSTVT集
# 经验：不能用一个oldFIRSTVT来记录FIRSTVT的旧值，因为oldFIRSTVT就是FIRSTVT，所以一直都是相等的，不能作为循环停止的依据
def firstvt(grammar, grammarnum, vt, vn, FIRSTVT):
    var = 1
    changed = False
    while var == 1:
        changed = False
        for i in range(grammarnum):

            # FIRSTVT(P) = {a|P→a...}
            # grammar[i][1]就是前面的a，symbol就是前面的P，vn.index(symbol)是P在vn列表中的序号
            if grammar[i][1] in vt and grammar[i][1] not in FIRSTVT[vn.index(grammar[i][0])]:
                FIRSTVT[vn.index(grammar[i][0])].append(grammar[i][1])
                changed = True

            # FIRSTVT(P) = {a|P→Qa...}
            if (len(grammar[i]) >= 3):
                if grammar[i][1] in vn and grammar[i][2] in vt and grammar[i][2] not in FIRSTVT[vn.index(grammar[i][0])]:
                    FIRSTVT[vn.index(grammar[i][0])].append(grammar[i][2])
                    changed = True

            # 如果有P→Q...，则FIRSTVT(P)包含FIRSTVT(Q)
            if grammar[i][1] in vn:
                for j in range(len(FIRSTVT[vn.index(grammar[i][1])])):
                    if FIRSTVT[vn.index(grammar[i][1])][j] not in FIRSTVT[vn.index(grammar[i][0])]:
                        FIRSTVT[vn.index(grammar[i][0])].append(FIRSTVT[vn.index(grammar[i][1])][j])
                        changed = True

        # 直到FIRSTVT集不再变化
        if changed == False:
            break

    return FIRSTVT



# 生成LASTVT集
def lastvt(grammar, grammarnum, vt, vn, LASTVT):
    var = 1
    changed = False
    while var == 1:
        changed = False
        for i in range(grammarnum):

            # FIRSTVT(P) = {a|P→...a}
            # grammar[i][-1]就是前面的a，symbol就是前面的P，vn.index(symbol)是P在vn列表中的序号
            if grammar[i][-1] in vt and grammar[i][-1] not in LASTVT[vn.index(grammar[i][0])]:
                LASTVT[vn.index(grammar[i][0])].append(grammar[i][-1])
                changed = True

            # FIRSTVT(P) = {a|P→...aQ}
            if (len(grammar[i]) >= 3):
                if grammar[i][-1] in vn and grammar[i][-2] in vt and grammar[i][-2] not in LASTVT[vn.index(grammar[i][0])]:
                    LASTVT[vn.index(grammar[i][0])].append(grammar[i][-2])
                    changed = True

            # 如果有P→...Q，则LASTVT(P)包含LASTVT(Q)
            if grammar[i][-1] in vn:
                for j in range(len(LASTVT[vn.index(grammar[i][-1])])):
                    if LASTVT[vn.index(grammar[i][-1])][j] not in LASTVT[vn.index(grammar[i][0])]:
                        LASTVT[vn.index(grammar[i][0])].append(LASTVT[vn.index(grammar[i][-1])][j])
                        changed = True

        # 直到LASTVT集不再变化
        if changed == False:
            break

    return LASTVT



# 生成优先表
def priority(PriorityTable, grammar, grammarnum, vt, vn, FIRSTVT, LASTVT):
    for i in range(grammarnum):
        for j in range(1, len(grammar[i]) - 1):

            # 如果产生式中有...ab...，则a = b
            if grammar[i][j] in vt and grammar[i][j + 1] in vt:
                PriorityTable[vt.index(grammar[i][j])][vt.index(grammar[i][j + 1])] = 3

            # 如果产生式中有...aPb...，则a = b
            if j < len(grammar[i]) - 2 and grammar[i][j] in vt and grammar[i][j + 2] in vt and grammar[i][j + 1] in vn:
                PriorityTable[vt.index(grammar[i][j])][vt.index(grammar[i][j + 2])] = 3

            # 如果产生式中有...aP...，则FIRSTVT(P) < a
            if grammar[i][j] in vt and grammar[i][j + 1] in vn:
                for anyvt in FIRSTVT[vn.index(grammar[i][j + 1])]:
                    PriorityTable[vt.index(grammar[i][j])][vt.index(anyvt)] = 2

            # 如果产生式中有...Pa...，则a > LASTVT(P)
            if grammar[i][j] in vn and grammar[i][j + 1] in vt:
                for anyvt in LASTVT[vn.index(grammar[i][j])]:
                    PriorityTable[vt.index(anyvt)][vt.index(grammar[i][j + 1])] = 1

    # 列出FIRSTVT中不重复的终结符
    FIRSTVTwithoutrepeat = []
    for i in range(len(vn)):
        for j in range(len(FIRSTVT[i])):
            if FIRSTVT[i][j] not in FIRSTVTwithoutrepeat:
                FIRSTVTwithoutrepeat.append(FIRSTVT[i][j])

    # 列出LASTVT中不重复的终结符
    LASTVTwithoutrepeat = []
    for i in range(len(vn)):
        for j in range(len(LASTVT[i])):
            if LASTVT[i][j] not in LASTVTwithoutrepeat:
                LASTVTwithoutrepeat.append(LASTVT[i][j])

    # '#' < 所有FIRSTVT中出现过的终结符
    for anyvt in FIRSTVTwithoutrepeat:
        PriorityTable[len(vt)][vt.index(anyvt)] = 2
    # 所有LASTVT中出现过的终结符 > '#'
    for anyvt in LASTVTwithoutrepeat:
        PriorityTable[vt.index(anyvt)][len(vt)] = 1
    # '#' = '#'
    PriorityTable[len(vt)][len(vt)] = 3

    return 0



# 检查是否是算符优先文法
def check(grammar, grammarnum, vt):
    for i in range(grammarnum):
        for j in range(1, len(grammar[i]) - 1):
            if grammar[i][j] in vt and grammar[i][j + 1] in vt:
                return False
    return True



# 归约函数
def reduction(sentence,grammar, grammarnum, vt, vn, PriorityTable):

    # 把所有的产生式中的非终极符都变为N
    newgrammar = [[] for row in range(20)]
    newgrammarnum = 0
    for i in range(grammarnum):
        if not(grammar[i][1] in vn and len(grammar[i][1:]) == 1):
            for j in range(len(grammar[i])):
                if grammar[i][j] in vn:
                    newgrammar[newgrammarnum].append('N')
                else:
                    newgrammar[newgrammarnum].append(grammar[i][j])
            newgrammarnum += 1


    vt.append('#')
    stack = ['#']
    # top是栈顶（其实是离栈顶最近的终结符的位置）
    top = len(stack) - 1
    sentencecnt = 0

    a = sentence[sentencecnt]

    while (1):
        # 如果句子中出现了终结符表中没有的字符，则说明错误
        if a not in vt:
            print('错误：句子中出现了终结符表中没有的字符')
            return False

        # 如果栈顶是非终结符，则top往下移一格，因为比较优先级一定是比较两个终结符的，非终结符没有优先级
        if stack[top] not in vt:
            top = top - 1

        # 如果两个终结符之间没有关系，也就意味着他们不可能紧挨着出现，就是错误的情况
        if PriorityTable[vt.index(stack[top])][vt.index(a)] == 0:
            print('错误：', stack[top], '和', a, '不能连续出现')
            return True

        # 如果栈最上方的终结符 > 即将从句子中读入的下一个终极符a，就要开始往前找第一次出现的<关系，将<...>进行归约
        print('当前的堆栈：', stack, '当前的句子：', sentence[sentencecnt:])
        while (PriorityTable[vt.index(stack[top])][vt.index(a)] == 1):# >
            # j指针负责往前找第一次出现的<关系
            while (1):
                j = top
                Q = stack[j]

                if stack[j - 1] in vt:
                    j = j - 1
                else:
                    j = j - 2
                if PriorityTable[vt.index(stack[j])][vt.index(Q)] == 2:# <
                    break
                if PriorityTable[vt.index(stack[j])][vt.index(Q)] == 3:# =关系的处理与<关系有所区别
                    j -= 1
                    break

            changed = False
            # 归约
            for i in range(newgrammarnum):
                if (newgrammar[i][1:] == stack[j + 1:]):
                    changed = True
                    print(stack[j + 1:], '归约为', 'N')
                    stack[j + 2: ] = []
                    stack[j + 1] = 'N'
                    top = len(stack) - 1
                    if stack[top] not in vt:
                        top -= 1

            #在文法中找了一遍都没找到符合它的文法，就说明该句子语法错误
            if changed ==False:
                print('错误：不存在这样的表达形式 ', str(stack[j + 1:]))
                return False

        # 如果栈最上方的终结符 <或者= 即将从句子中读入的下一个终极符a，就从句子中读入一个字符
        print('当前的堆栈：', stack, '当前的句子：', sentence[sentencecnt:])
        if PriorityTable[vt.index(stack[top])][vt.index(a)] == 2 or PriorityTable[vt.index(stack[top])][vt.index(a)] == 3:# < =
            if sentencecnt >= len(sentence):
                return False
            a = sentence[sentencecnt]
            stack.append(a)
            top = len(stack) - 1
            if sentencecnt + 1 < len(sentence):
                sentencecnt += 1
            a = sentence[sentencecnt]

        # 以下说明语法正确，程序可以终止了
        if a == '#' and stack[0] == '#'and stack[1] == 'N'and stack[2] == '#':
            print('语法正确！')
            return True



def main():

    # 创建非终结符列表和终结符列表
    vn = []
    vt = []

    # 读非终结符
    f = open("grammar.txt")
    linenum = len(open(r"grammar.txt", 'rU').readlines())
    for i in range(linenum):
        str = f.readline().strip()
        if str[0] not in vn:
            vn.append(str[0])
    f.close()
    print('非终结符 = ', vn)

    #读终结符
    f = open("grammar.txt")
    for i in range(linenum):
        str = f.readline().strip()
        for j in range(2, len(str)):
            if str[j] not in vn and str[j] not in vt and str[j] != '|':
                vt.append(str[j])
    f.close()
    print('终结符 = ', vt)

    # 创建文法表
    grammar = [[[] for col in range(10)] for row in range(20)]
    # 读文法
    grammarnum = 0
    f = open("grammar.txt")
    for i in range(linenum):
        str = f.readline().strip()
        for j in range(str.count('|')+1):
            grammar[grammarnum][0] = str[0]
            grammar[grammarnum][1:] = str[2:].split('|')[j]
            grammarnum += 1
    f.close()
    print('文法 = ')
    for i in range(grammarnum):
        print(grammar[i])

    if not check(grammar, grammarnum, vt):
        print('该文法不是算符优先文法，请重新输入')
        return False


    # 创建FIRSTVT和LASTVT集
    FIRSTVT = [[] for row in range(len(vn))]
    LASTVT = [[] for row in range(len(vn))]
    firstvt(grammar, grammarnum, vt, vn, FIRSTVT)
    lastvt(grammar, grammarnum, vt, vn, LASTVT)
    for i in range(len(vn)):
        print(vn[i],'的FIRSTVT集  = ', FIRSTVT[i])
    for i in range(len(vn)):
        print(vn[i],'的LASTVT集   = ', LASTVT[i])

    # 创建优先表
    PriorityTable = [[0 for col in range(len(vt) + 1)] for row in range(len(vt) + 1)]
    priority(PriorityTable, grammar, grammarnum, vt, vn, FIRSTVT, LASTVT)
    print('符号优先表 = ')
    print('     ',vt,'#')
    for i in range(len(vt) + 1):
        if i == len(vt):
            print('#  : ', PriorityTable[i])
        else:
            print(vt[i], ' : ', PriorityTable[i])

    # 读语句
    f = open("sentence.txt")
    sentence = f.readline().strip()
    if sentence[-1] != '#':
        sentence += '#'
    f.close()
    print(sentence)
    reduction(sentence,grammar, grammarnum, vt, vn, PriorityTable)

    return True

if __name__ == '__main__':
    main()