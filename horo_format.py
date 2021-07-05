import time
import data_cleaning as dc

def current_date():
    date_of_today = time.strftime("%d/%m/%Y", time.localtime())
    date_of_today = date_of_today.replace('/', '-')
    return date_of_today

def current_hour():
    hour_of_today = time.strftime("%H:%M:%S", time.localtime())
    hour_of_today = hour_of_today.split(':')
    hour_of_today = hour_of_today[0] + 'h' + hour_of_today[1] + 'm' + hour_of_today[2] + 's'
    return hour_of_today

def show_log_period(date_of_today, hour_of_today, date_of_today_f, hour_of_today_f):
    print("\nJOURNAL")
    print("\n_________________")
    print("Debut Spider :")
    print(date_of_today)
    print(hour_of_today)
    print("\n_________________")
    print("Fin Spider :")
    print(date_of_today_f)
    print(hour_of_today_f)

def date_to_jjmmaaa(elem,sep):

    date_dico = {}
    date_split = elem.split(sep)

    annee = date_split[2]
    mois = date_split[1]
    jour = date_split[0]
    date = jour + '-' + mois + '-' + annee

    date_dico["year"] = annee
    date_dico["month"] = mois
    date_dico["day"] = jour
    date_dico["date"] = date

    return date_dico

def date_to_jjmmaaa_list(list,sep):

    annees = ['']*len(list)
    mois = ['']*len(list)
    jours = ['']*len(list)
    dates = ['']*len(list)

    dates_dico = {}
    i=0
    for e in list:
        date = e.split(sep)
        annees[i] = date[2]
        mois[i] = date[1]
        jours[i] = date[0]
        dates[i] = jours[i] + '-' + mois[i] + '-' + annees[i]
        i += 1

    dates_dico["years"] = annees
    dates_dico["months"] = mois
    dates_dico["days"] = jours
    dates_dico["dates"] = dates

    return dates_dico

'''
d = ["25.06.2021 | ihjljl","29.12.2015 | ljlkjk"]
print(dc.keep_until_word_list(d,' | '))
print('**********')
a = dc.keep_until_word_list(d,' | ')
x = date_to_jjmmaaa_list(a,'.')['years']
y = date_to_jjmmaaa_list(a,'.')['months']
z = date_to_jjmmaaa_list(a,'.')['days']
o = date_to_jjmmaaa_list(a,'.')['dates']
print(x)
print(y)
print(z)
print(o)
'''