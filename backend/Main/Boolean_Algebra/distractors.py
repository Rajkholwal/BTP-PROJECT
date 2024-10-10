import random
from QM_method import *
from booleanAlgebraFinal import *

# flip sign
def bit_flip_var(x):
    var_list = []
    for i in range(len(x)):
        if(random.randint(0,1)==0):
            if x[i] == '0':
                var_list.append(chr(i+65))
            elif x[i] == '1':
                var_list.append(chr(i+65)+"'")
        else:
            if x[i] == '0':
                var_list.append(chr(i+65)+"'")
            elif x[i] == '1':
                var_list.append(chr(i+65))
    return var_list


def print_QM_distract(mt, dc):
    mt.sort()
    minterms = mt+dc
    minterms.sort()
    size = len(bin(minterms[-1]))-2
    groups,all_pi = {},set()

    for minterm in minterms:
        try:
            groups[bin(minterm).count('1')].append(bin(minterm)[2:].zfill(size))
        except KeyError:
            groups[bin(minterm).count('1')] = [bin(minterm)[2:].zfill(size)]

    while True:
        tmp = groups.copy()
        groups,m,marked,should_stop = {},0,set(),True
        l = sorted(list(tmp.keys()))
        for i in range(len(l)-1):
            for j in tmp[l[i]]:
                for k in tmp[l[i+1]]:
                    res = compare(j,k)
                    if res[0]:
                        try:
                            groups[m].append(j[:res[1]]+'-'+j[res[1]+1:]) if j[:res[1]]+'-'+j[res[1]+1:] not in groups[m] else None
                        except KeyError:
                            groups[m] = [j[:res[1]]+'-'+j[res[1]+1:]]
                        should_stop = False
                        marked.add(j)
                        marked.add(k)
            m += 1
        local_unmarked = set(flatten(tmp)).difference(marked)
        all_pi = all_pi.union(local_unmarked)
        if should_stop:
            break

    sz = len(str(mt[-1]))
    chart = {}

    for i in all_pi:
        merged_minterms,y = findminterms(i),0

        for j in refine(merged_minterms,dc):
            x = mt.index(int(j))*(sz+1)
            y = x+sz
            try:
                chart[j].append(i) if i not in chart[j] else None
            except KeyError:
                chart[j] = [i]

    EPI = findEPI(chart)
    removeTerms(chart,EPI)

    if(len(chart) == 0):
        final_result = [bit_flip_var(i) for i in EPI]
    else:
        P = [[bit_flip_var(j) for j in chart[i]] for i in chart]
        while len(P)>1:
            P[1] = multiply(P[0],P[1])
            P.pop(0)
        final_result = [min(P[0],key=len)]
        final_result.extend(bit_flip_var(i) for i in EPI)
    return "{0}".format('F = '+' + '.join(''.join(i) for i in final_result))


def manipulate_minterms(table):
        mt, num_vars = table_to_minterms(table)
        for i in range (len(table)):
            if i not in mt and random.randint(0,6)<=1:
                mt.append(i)
        return mt

def manipulate_dc(table):
        dc=[]
        mt, num_vars = table_to_minterms(table)
        for i in range (len(table)):
            if i not in mt and random.randint(0,6)<=1:
                dc.append(i)
        return dc


