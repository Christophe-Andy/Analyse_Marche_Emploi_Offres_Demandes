import scrapy
from scrapy.crawler import CrawlerProcess
import data_cleaning as dc
import horo_format as hf
import persist as ps
import string_transform as st


class RekSmartSpider(scrapy.Spider):

    # Définition des caractéristiques de départ du robot
    name = 'rek_smart_epider'
    allowed_domains = ['www.rekrute.com']
    start_urls = ['https://www.rekrute.com/offres-emploi-maroc.html']

    # Définition de la fonction de parsing
    def parse(self, response):

        # print("N°  JOUR   MOIS   ANNEE   DATE   REGION  SECTEUR   NIVEAU   COMPAGNIE  DESCRIPTION  LIEN")
        # print("______________________________________________________________________")

        # Collecte des données pertinentes
        # Extraction des dates
        dates_emploi = response.css("i.fa.fa-clock-o + span::text").extract()
        #dates_emploi = dc.replace_by_na_if_none_list(dates_emploi_x,10)

        jour_emploi = hf.date_to_jjmmaaa_list(dates_emploi,'/')['days']
        mois_emploi = hf.date_to_jjmmaaa_list(dates_emploi,'/')['months']
        annee_emploi = hf.date_to_jjmmaaa_list(dates_emploi,'/')['years']
        dates_emploi = hf.date_to_jjmmaaa_list(dates_emploi,'/')['dates']

        # Extraction des régions
        regions_emploi_x = response.css("div.section h2 a::text").extract()
        regions_emploi_x = dc.replace_by_na_if_none_list(regions_emploi_x,len(dates_emploi))

        # Suppression du séparateur puis suppression du suffixe maroc
        regions_emploi = dc.keep_since_word_list(regions_emploi_x,'|')
        # J'ajouterais \ si la fonction keep_until_word_list aurait utilisé une autre fonction qui reconnais le symbôle | comme  caractère spécial Python
        # je devrais donc l'echapper
        regions_emploi = dc.keep_until_word_list(regions_emploi,"(Maroc)")
        regions_emploi = st.capitalize_list(regions_emploi)
        regions_emploi = st.replace_sep_list(regions_emploi, '/', ', ')

        # Extraction du secteur
        secteurs_emploi = response.css("div.info ul li:first-child a::text").extract()
        secteurs_emploi = dc.replace_by_na_if_none_list(secteurs_emploi,len(dates_emploi))
        secteurs_emploi = dc.strip_list(secteurs_emploi)
        secteurs_emploi = st.replace_sep_list(secteurs_emploi, ' /', ',')

        # Extraction du niveau d'etudes requis
        niveaux_emploi_x = response.css("div.info ul li:nth-child(4) a::text").extract()
        niveaux_emploi = dc.replace_by_na_if_none_list(niveaux_emploi_x,len(dates_emploi))
        niveaux_emploi = dc.strip_list(niveaux_emploi)
        niveaux_emploi = st.del_first_space_list(niveaux_emploi)


        # Extraction des compagnies
        compagnies_emploi_x = response.css("div.col-sm-2.col-xs-12 a img::attr(alt)").extract()
        compagnies_emploi = dc.replace_by_na_if_none_list(compagnies_emploi_x,len(dates_emploi))
        compagnies_emploi = dc.strip_list(compagnies_emploi)
        compagnies_emploi = st.capitalize_list(compagnies_emploi)

        # Extraction des descriptions
        descs_emploi_x = response.css("i.fa.fa-binoculars + span::text").extract()
        descs_emploi = dc.replace_by_na_if_none_list(descs_emploi_x,len(dates_emploi))
        descs_emploi = dc.strip_list(descs_emploi)

        # Extraction des liens
        links_level = response.css("div.section h2 a::attr(href)").extract()
        links_level = st.add_concat_list('https://www.rekrute.com',links_level)

        # Récupération en boucle de l'enregistrement suivant dans un dictionnaire
        for item in zip(jour_emploi,mois_emploi,annee_emploi,dates_emploi,regions_emploi,secteurs_emploi,niveaux_emploi,compagnies_emploi,descs_emploi,links_level):
            group_data = {
                'Jour': item[0],
                'Mois': item[1],
                'Annee': item[2],
                'Date': item[3],
                'Region': item[4],
                'Secteur': item[5],
                'Niveau': item[6],
                'Compagnie': item[7],
                'Description': item[8],
                'Lien': item[9],
            }
            # print(group_data)
            # Envoi d'un enregistrement à Scrapy
            yield group_data

            next_page = response.css('div.section a.next::attr("href")').get()

            if next_page is not None:
                next_page = 'https://www.rekrute.com' + next_page
                print('URL page courante : ',next_page)
                # Appel par recursivité de la fonction pour extraire les enregistrements des pages suivantes
                yield response.follow(next_page, self.parse)


# Exportation de l'ensemble des enregistrements effectués par le robot
date_of_today = hf.current_date()
hour_of_today = hf.current_hour()

path_csv = "file:///S:/rekrut_data_" + date_of_today + "_" + hour_of_today + "_csv.csv"

process = CrawlerProcess({
    'FEED_FORMAT': "csv",
    'FEED_URI': path_csv,
})

process.crawl(RekSmartSpider)
process.start()

date_of_today_f = hf.current_date()
hour_of_today_f = hf.current_hour()

hf.show_log_period(date_of_today, hour_of_today, date_of_today_f, hour_of_today_f)

path_excel = "S:\\rekrut_data_" + date_of_today + "_" + hour_of_today + "_excel.xlsx"

ps.save_csv_to_excel(path_csv,path_excel)



