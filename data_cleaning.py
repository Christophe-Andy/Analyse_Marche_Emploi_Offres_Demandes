def replace_by_na_if_none(value):
    if value == None or value == '' or value == ' ':
        return "N/A"
    else :
        return value

def replace_by_na_if_none_list(list,size):
    if list is None :
        list_f = ['']*size
        for i in range(size):
            list_f[i] = "N/A"
    else :
        list_f = ['']*len(list)
        for i in range(len(list)):
            list_f[i] = replace_by_na_if_none(list[i])

    return list_f

def strip_list(list):
    list_f = [''] * len(list)

    for i in range(len(list)):
        list_f[i] = list[i].strip()

    return list_f

def split_list(list,sep):
    list_f = [''] * len(list)

    for i in range(len(list)):
        list_f[i] = list[i].split(sep)

    return list_f

def keep_until_word(elem,sep):
    elem_f = elem.split(sep)[:1]

    for i in range(len(elem_f)):
        elem_f[i].strip()

    elem_f = ' '.join(elem_f)
    return elem_f

def keep_until_word_list(list,sep):
    list_f = list
    for i in range(len(list)):
        list_f[i] = keep_until_word(list[i],sep)

    return list_f

def keep_since_word(elem, sep):
    elem_f = elem.split(sep)[1:]

    for i in range(len(elem_f)):
        elem_f[i].strip()

    elem_f = ' '.join(elem_f)
    return elem_f.strip()


def keep_since_word_list(list, sep):
    list_f = list
    for i in range(len(list)):
        list_f[i] = keep_since_word(list[i],sep)

    return list_f

'''
# Test until et since
a=keep_until_word("azde | azeraz zaraz azer",'\|')
b=keep_since_word("azde | azeraz zaraz azer",'\|')
print("until :",a)
print("since :",b)
'''

'''
l=['a | a (Maroc)','b | b (Maroc)']
l = keep_since_word_list(l, '|')
print(l)
l = keep_until_word_list(l,'(Maroc)')
print(l)
'''