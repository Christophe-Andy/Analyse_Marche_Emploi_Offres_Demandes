from requests import get
from scrapy import Selector
import re


def catch_URL(URL):
    url_emploi = URL
    response_emploi = get(url_emploi)
    source_emploi = None

    if response_emploi.status_code == 200:
        source_emploi = response_emploi.text
        return source_emploi


def catch_data(source):
    if source:

        # Si le code source existe
        selector_emploi = Selector(text=source)
        contenus_emploi = selector_emploi.css("div.row")
        print("N°    DATE               REGION               COMPAGNIE              DESCRIPTION")
        print("_________________________________________________________________________________")
        cmp = 1
        for contenu in contenus_emploi:
            if cmp < 2:
                date_emploi_x = contenu.css("p.job-recruiter::text").extract_first()
                if cmp == 1:
                    print(type(date_emploi_x))
                date_emploi = date_emploi_x.split(' | ')[0]
                date_coupee = date_emploi.split('.')
                print(date_coupee)

                jour_emploi = date_coupee[0]
                mois_emploi = date_coupee[1]
                annee_emploi = date_coupee[2]

                region_emploi_x = contenu.css("div.search-description + p::text").extract_first()
                region_emploi = re.split(" : ", region_emploi_x)[1]

                compagnie_emploi = contenu.css("p.job-recruiter b *::text").extract_first()
                desc_emploi = contenu.css("div.search-description::text").extract_first()

                link_level = contenu.css("h5 a::attr(href)").extract_first()

                print(cmp, " | ", jour_emploi, " | ", mois_emploi, " | ", annee_emploi, " | ", region_emploi, " | ", compagnie_emploi, " | ", desc_emploi, " ",
                      link_level)
                cmp += 1

        return contenus_emploi

def catch_sec_niv(source):
    if source:

        # Si le code source existe
        selector_emploi = Selector(text=source)
        contenus_emploi = selector_emploi.css("body")
        print("N°    SECTEUR               NIVEAU D'ETUDES   ")
        print("_________________________________________________________________________________")

        for contenu in contenus_emploi:
            secteur_emploi = contenu.css("div.field.field-name-field-offre-secteur.field-type-taxonomy-term-reference.field-label-hidden div.field-items div.field-item.even::text").extract_first()
            if secteur_emploi == None:
                secteur_emploi = "N/A"

            niveau_emploi = contenu.css("div.field.field-name-field-offre-niveau-etude.field-type-taxonomy-term-reference.field-label-hidden div.field-items div.field-item.even::text").extract_first()
            if niveau_emploi == None :
                niveau_emploi = "N/A"

            print("secteur : ", secteur_emploi)
            print("niveau d'études requis : ", niveau_emploi)
            print(type(secteur_emploi))
            print(type(niveau_emploi))
        return contenus_emploi

url_emploi = "https://www.emploi.ma/offre-emploi-maroc/consultant-securite-informatique-5948742"

source_emploi_ma = catch_URL(url_emploi)
#data_emploi_ma = catch_data(source_emploi_ma)
data_emploi_ma = catch_sec_niv(source_emploi_ma)

print(data_emploi_ma)
