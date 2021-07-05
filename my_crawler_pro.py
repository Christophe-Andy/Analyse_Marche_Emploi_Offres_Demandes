import scrapy
from scrapy.crawler import CrawlerProcess
import data_cleaning as dc
import horo_format as hf
import persist as ps
import string_transform as st

class ProSmartSpider(scrapy.Spider):

    # Définition des caractéristiques de départ du robot
    name = 'pro_smart_spider'
    allowed_domains = ['www.emploi.ma']
    start_urls = ['https://www.emploi.ma/recherche-base-donnees-cv']

    # Définition de la fonction de parsing
    def parse(self, response, **kwargs):

        #print("N°  JOUR   MOIS   ANNEE   DATE   ID  VILLE  MOBILITE  TYPE  COMPETENCES  SECTEUR  NIVEAU ETUDES  LIEN")
        #print("_____________________________________________________________________")

        # Extraction des liens
        links_level = response.css("h5 a::attr(href)").extract()

        for i in range(len(links_level)):
            url = "https://www.emploi.ma" + links_level[i]

            yield scrapy.Request(
                url,
                callback=self.parse_sec_niv,
                meta={
                      'Lien': links_level[i],
                      }
            )

        next_page_f = response.css('ul.pager li.pager-next.active.last a::attr("href")').get()
        if next_page_f is not None:
            next_page_f = 'https://www.emploi.ma' + next_page_f
            print('URL page courante : ',next_page_f)
            # Appel par recursivité de la fonction pour extraire les enregistrements suivants
            #yield response.follow(next_page_f, self.parse)
            yield scrapy.Request(next_page_f, self.parse)


        # Definition de la fonction de niveau 2
    def parse_sec_niv(self,response):

        donnees_partielles = response.meta

        # Collecte des données pertinentes
        if response is not None:
            # Extraction de la date
            date_profil = response.xpath("//div[@class='candidate-more-info']/div[@class='candidate-more-info']/div[@class='field-items']/div[@class='field-item'][5]/text()").extract()
            date_profil = dc.replace_by_na_if_none(date_profil)
            date_profil = ''.join(date_profil).strip()

            jour_profil = hf.date_to_jjmmaaa(date_profil, '.')['day']
            mois_profil = hf.date_to_jjmmaaa(date_profil, '.')['month']
            annee_profil = hf.date_to_jjmmaaa(date_profil, '.')['year']
            date_profil = hf.date_to_jjmmaaa(date_profil, '.')['date']

            # Extraction de la ville
            ville_profil = response.xpath("//div[@class='candidate-more-info']/div[@class='candidate-more-info']/div[@class='field-items']/div[@class='field-item'][3]/text()").extract()
            ville_profil = dc.replace_by_na_if_none(ville_profil)
            ville_profil = ' '.join(ville_profil).strip()
            ville_profil = ville_profil.capitalize()

            # Extraction de la mobilité
            mobilite_profil = response.xpath("//div[@class='candidate-more-info']/div[@class='candidate-more-info']/div[@class='field-items']/div[@class='field-item'][2]/span[@class='regions-items']//text()").extract()
            mobilite_profil = dc.replace_by_na_if_none(mobilite_profil)
            mobilite_profil = ' '.join(mobilite_profil).strip()
            mobilite_profil = ', '.join(mobilite_profil.split('-'))

            # Extraction de l'ID
            id_profil = response.css("section#main-content h1.title::text").extract_first()
            id_profil = dc.replace_by_na_if_none(id_profil)
            id_profil = dc.keep_since_word(id_profil,'N°')

            # Extraction du type de secteurs recherchés
            types_profil = response.xpath("//div[@class='candidate-job-categories']/div[@class='field-items']/div[@class='job-item']/div[@class='field field-name-field-candidat-metier field-type-taxonomy-term-reference field-label-hidden']/div[@class='field-items']/div[@class='field-item even']//text()").extract()
            types_profil = dc.replace_by_na_if_none(types_profil)
            types_profil = dc.keep_since_word_list(types_profil, "»")
            types_profil = ', '.join(types_profil)

            # Extraction des compétences
            competences_profil = response.xpath("//div[@class='candidate-skills']/div[@class='field-item']//text()").extract()
            competences_profil = dc.replace_by_na_if_none(competences_profil)
            competences_profil = ' '.join(competences_profil).strip()

            # Extraction des secteurs d'expérience
            secteurs_profil = response.xpath("//div[@class='candidate-professional-experience']/div[@class='field-items']/div[@class='field-item'][2]/div[@class='industry-item']//div[@class='industries-item']/text()").extract()
            secteurs_profil = dc.replace_by_na_if_none(secteurs_profil)
            secteurs_profil = dc.keep_since_word_list(secteurs_profil, "» ")
            secteurs_profil = ', '.join(secteurs_profil)

            # Extraction du niveau d'études
            niveau_etudes_profil = response.xpath("//div[@class='candidate-education']/div[@class='candidate-education-info']/div[@class='field-items']/div[@class='field-item'][1]/text()").extract()
            niveau_etudes_profil = dc.replace_by_na_if_none(niveau_etudes_profil)
            niveau_etudes_profil = ' '.join(niveau_etudes_profil).strip()

        # Ajout aux liens précédents, des données du profil
        ligne_profil = {'Jour': jour_profil,
                   'Mois': mois_profil,
                   'Annee': annee_profil,
                   'Date': date_profil,
                   'id': id_profil,
                   'Ville': ville_profil,
                   'Mobilite': mobilite_profil,
                   'Type': types_profil,
                   'Competences': competences_profil,
                   'Secteur': secteurs_profil,
                   'Niveau': niveau_etudes_profil,
                   'Lien': donnees_partielles['Lien'],
                       }
        # print(ligne_profil)
        # Envoi d'un enregistrement à Scrapy
        if int(annee_profil) == 2021 :
            yield ligne_profil

# Exportation de l'ensemble des enregistrements effectués par le robot
date_of_today = hf.current_date()
hour_of_today = hf.current_hour()

path_csv = "file:///S:/pro_data_" + date_of_today + "_" + hour_of_today + "_csv.csv"

process = CrawlerProcess({
    'FEED_FORMAT': "csv",
    'FEED_URI': path_csv,
})

process.crawl(ProSmartSpider)
process.start()

date_of_today_f = hf.current_date()
hour_of_today_f = hf.current_hour()

#Affichage des moments initial et final
hf.show_log_period(date_of_today, hour_of_today, date_of_today_f, hour_of_today_f)

path_excel = "S:\pro_data_" + date_of_today + "_" + hour_of_today + "_excel.xlsx"

ps.save_csv_to_excel(path_csv,path_excel)


