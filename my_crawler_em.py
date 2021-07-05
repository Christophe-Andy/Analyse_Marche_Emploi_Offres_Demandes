import scrapy
from scrapy.crawler import CrawlerProcess
import data_cleaning as dc
import horo_format as hf
import persist as ps
import string_transform as st

class EmpSmartSpider(scrapy.Spider):

    # Définition des caractéristiques de départ du robot
    name = 'emp_smart_spider'
    allowed_domains = ['www.emploi.ma']
    start_urls = ['https://www.emploi.ma/recherche-jobs-maroc']

    # Définition de la fonction de parsing
    def parse(self, response, **kwargs):

        #print("N°  JOUR   MOIS   ANNEE   DATE   REGION  SECTEUR NIVEAU COMPAGNIE  DESCRIPTION  LIEN")
        #print("_____________________________________________________________________")

        # Collecte des données pertinentes
        # Extraction des dates
        dates_emploi = response.css("p.job-recruiter::text").extract()
        #dates_emploi = dc.replace_by_na_if_none_list(dates_emploi_x,10)
        dates_emploi = dc.keep_until_word_list(dates_emploi,'|')
        # J'ajouterais \ si la fonction keep_until_word_list aurait utilisé une autre fonction qui reconnais le symbôle | comme  caractère spécial Python
        # je devrais donc l'echapper
        jour_emploi = hf.date_to_jjmmaaa_list(dates_emploi, '.')['days']
        mois_emploi = hf.date_to_jjmmaaa_list(dates_emploi, '.')['months']
        annee_emploi = hf.date_to_jjmmaaa_list(dates_emploi, '.')['years']
        dates_emploi = hf.date_to_jjmmaaa_list(dates_emploi, '.')['dates']

        # Extraction des régions
        regions_emploi_x = response.css("div.search-description + p::text").extract()
        regions_emploi_x = dc.replace_by_na_if_none_list(regions_emploi_x,len(dates_emploi))
        regions_emploi = dc.keep_since_word_list(regions_emploi_x,":")
        regions_emploi = st.replace_sep_list(regions_emploi,' - ',', ')

        # Extraction des compagnies
        compagnies_emploi_x = response.css("p.job-recruiter b *::text").extract()
        compagnies_emploi = dc.replace_by_na_if_none_list(compagnies_emploi_x,len(dates_emploi))
        compagnies_emploi = dc.strip_list(compagnies_emploi)
        compagnies_emploi = st.capitalize_list(compagnies_emploi)

        # Extraction des descriptions
        descs_emploi_x = response.css("div.search-description::text").extract()
        descs_emploi = dc.replace_by_na_if_none_list(descs_emploi_x,len(dates_emploi))
        descs_emploi = dc.strip_list(descs_emploi)

        # Extraction des liens
        links_level = response.css("h5 a::attr(href)").extract()
        links_level = st.add_concat_list('https://www.emploi.ma',links_level)

        for i in range(len(links_level)):
            url = links_level[i]

            yield scrapy.Request(
                url,
                callback=self.parse_sec_niv,
                meta={'Jour': jour_emploi[i],
                      'Mois': mois_emploi[i],
                      'Annee': annee_emploi[i],
                      'Date': dates_emploi[i],
                      'Region': regions_emploi[i],
                      'Compagnie': compagnies_emploi[i],
                      'Description': descs_emploi[i],
                      'Lien': links_level[i],
                      }
            )
        # secteurs_emploi,niveaux_emploi,

        next_page_f = response.css('li.pager-next.active.last a::attr("href")').get()
        if next_page_f is not None:
            next_page_f = 'https://www.emploi.ma' + next_page_f
            print('URL page courante : ',next_page_f)
            # Appel par recursivité de la fonction pour extraire les enregistrements suivants
            #yield response.follow(next_page_f, self.parse)
            yield scrapy.Request(next_page_f, self.parse)


        # Definition de la fonction de niveau 2
    def parse_sec_niv(self,response):

        donnees_partielles = response.meta
        secteur_emploi = "N/A"
        niveau_emploi = "N/A"

        if response is not None:
            #if donnees_partielles is not None:

            # Extraction du secteur
            secteur_emploi = response.css("div.field.field-name-field-offre-secteur.field-type-taxonomy-term-reference.field-label-hidden div.field-items div.field-item.even::text").extract_first()
            secteur_emploi = dc.replace_by_na_if_none(secteur_emploi)

           # Extraction du niveau
            niveau_emploi = response.css("div.field.field-name-field-offre-niveau-etude.field-type-taxonomy-term-reference.field-label-hidden div.field-items div.field-item.even::text").extract_first()
            niveau_emploi = dc.replace_by_na_if_none(niveau_emploi)

        # Ajout aux donnees partielles précédentes, le secteur et le niveau
        ligne_emploi = {'Jour': donnees_partielles['Jour'],
                   'Mois': donnees_partielles['Mois'],
                   'Annee': donnees_partielles['Annee'],
                   'Date': donnees_partielles['Date'],
                   'Region': donnees_partielles['Region'],
                   'Secteur': secteur_emploi,
                   'Niveau': niveau_emploi,
                   'Compagnie': donnees_partielles['Compagnie'],
                   'Description': donnees_partielles['Description'],
                   'Lien': donnees_partielles['Lien'],
                   }
        # print(ligne_emploi)
        # Envoi d'un enregistrement à Scrapy
        yield ligne_emploi

# Exportation de l'ensemble des enregistrements effectués par le robot
date_of_today = hf.current_date()
hour_of_today = hf.current_hour()

path_csv = "file:///S:/employ_data_" + date_of_today + "_" + hour_of_today + "_csv.csv"

process = CrawlerProcess({
    'FEED_FORMAT': "csv",
    'FEED_URI': path_csv,
})

process.crawl(EmpSmartSpider)
process.start()

date_of_today_f = hf.current_date()
hour_of_today_f = hf.current_hour()

#Affichage des moments initial et final
hf.show_log_period(date_of_today, hour_of_today, date_of_today_f, hour_of_today_f)

path_excel = "S:\employ_data_" + date_of_today + "_" + hour_of_today + "_excel.xlsx"

ps.save_csv_to_excel(path_csv,path_excel)


