import data_cleaning as dc

def capitalize_list(list):
    list_f = [''] * len(list)

    for i in range(len(list)):
        list_f[i] = list[i].capitalize()

    return list_f

def lower_list(list):
    list_f = [''] * len(list)

    for i in range(len(list)):
        list_f[i] = list[i].lower()

    return list_f

def upper_list(list):
    list_f = [''] * len(list)

    for i in range(len(list)):
        list_f[i] = list[i].upper()

    return list_f

def add_concat(elem1,elem2):
    return str(elem1) + str(elem2)

def add_concat_list(elem,list):
    list_f = [''] * len(list)

    for i in range(len(list)):
        list_f[i] = elem + list[i]

    return list_f

def insert_something_before(chaine,sep,to_insert):
    part1 = dc.keep_until_word(chaine,sep)
    part2 = dc.keep_since_word(chaine,sep)

    if part1 == chaine or part2 == '' :
        chaine_f = chaine
    else:
        chaine_f = str(part1) + str(to_insert) + str(sep) + str(part2)

    return chaine_f

def insert_something_before_list(list,sep,to_insert):
    list_f = [''] * len(list)

    for i in range(len(list)):
        list_f[i] = insert_something_before(list[i],sep,to_insert)

    return list_f

def del_first_space(chaine):
    part1 = dc.keep_until_word(chaine,' ')
    part2 = dc.keep_since_word(chaine,' ')

    if part1 == chaine or part2 == '':
        chaine_f = chaine
    else:
        chaine_f = str(part1) + str(part2)

    return chaine_f

'''
a='Bac +5 et plus'

print(dc.keep_until_word(a,' '))
print(dc.keep_since_word(a,' '))
print(del_first_space(a))
'''

def del_first_space_list(list):
    list_f = [''] * len(list)

    for i in range(len(list)):
        list_f[i] = del_first_space(list[i])

    return list_f

def replace_sep_list(list, sep, instead):
    list_f = [''] * len(list)

    for i in range(len(list)):
        list_f[i] = list[i].replace(sep,instead)

    return list_f


"""
a=['bal','SaLLjjLé','bel']
print(capitalize_list(a))
"""