#from selenium import webdriver
import horo_format as hf
import data_cleaning as dc
from requests import get
from scrapy import Selector
import time
import re


def catch_URL(URL):
    url_emploi = URL
    response_emploi = get(url_emploi)
    source_emploi = None

    if response_emploi.status_code == 200:
        source_emploi = response_emploi.text
        return source_emploi

def catch_sec_niv(source):
    if source:
        # Si le code source existe
        selector_emploi = Selector(text=source)
        contenus_emploi = selector_emploi.css("body")
        print("DATE DE MAJ - ID - TYPES DE METIER - NIVEAU EXP - SECTEURS - COMPETENCES - VILLE - NIVEAU - ETUDE")
        print("_________________________________________________________________________________")

        date_of_today = hf.current_date()
        hour_of_today = hf.current_hour()

        #driver = webdriver.Chrome(r"S:\Talence\Documents PFE\chromedriver.exe")
        #driver.get('http://www.gutenberg.org/ebooks/search/%3Fsort_order%3Drelease_date')

        for contenu in contenus_emploi:
            #date_emploi = driver.find_elements_by_xpath("//div[@class='field-items']/div[@class='field-item']/label[contains(text(),'mise à jour')]/parent::*/text()")
            #date_emploi = contenu.css("div.candidate-more-info div.candidate-more-info div.field-items div:nth-of-type(5)").extract_first()
            #date_emploi = contenu.xpath("//div[@class='candidate-more-info']/div[@class='candidate-more-info']/div[@class='field-items']/div[@class='field-item'][5]/label/parent::div/text()").extract()
            #date_emploi = contenu.xpath("//div[@class='candidate-more-info']/div[@class='candidate-more-info']/div[@class='field-items']/div[@class='field-item'][5]/text()[not(ancestor::label)]").extract()
            date_emploi = contenu.xpath("//div[@class='candidate-more-info']/div[@class='candidate-more-info']/div[@class='field-items']/div[@class='field-item'][5]/text()").extract()
            date_emploi = ''.join(date_emploi).strip()

            ville_emploi = contenu.xpath("//div[@class='candidate-more-info']/div[@class='candidate-more-info']/div[@class='field-items']/div[@class='field-item'][3]/text()").extract()
            ville_emploi = ' '.join(ville_emploi).strip()

            mobilite_emploi = contenu.xpath("//div[@class='candidate-more-info']/div[@class='candidate-more-info']/div[@class='field-items']/div[@class='field-item'][2]/span[@class='regions-items']//text()").extract()
            mobilite_emploi = ' '.join(mobilite_emploi).strip()
            mobilite_emploi = ', '.join(mobilite_emploi.split('-'))

            id_emploi = contenu.css("section#main-content h1.title::text").extract_first()
            id_emploi = dc.keep_since_word(id_emploi,'N°')

            types_emploi = contenu.xpath("//div[@class='candidate-job-categories']/div[@class='field-items']/div[@class='job-item']/div[@class='field field-name-field-candidat-metier field-type-taxonomy-term-reference field-label-hidden']/div[@class='field-items']/div[@class='field-item even']//text()").extract()
            types_emploi = dc.keep_since_word_list(types_emploi,"»")
            types_emploi = ', '.join(types_emploi)

            competences_emploi = contenu.xpath("//div[@class='candidate-skills']/div[@class='field-item']//text()").extract()
            competences_emploi = ' '.join(competences_emploi).strip()

            secteurs_emploi = contenu.xpath("//div[@class='candidate-professional-experience']/div[@class='field-items']/div[@class='field-item'][2]/div[@class='industry-item']//div[@class='industries-item']/text()").extract()
            secteurs_emploi = dc.keep_since_word_list(secteurs_emploi, "» ")
            secteurs_emploi = ', '.join(secteurs_emploi)

            niveau_etudes_emploi = contenu.xpath("//div[@class='candidate-education']/div[@class='candidate-education-info']/div[@class='field-items']/div[@class='field-item'][1]/text()").extract()
            niveau_etudes_emploi = ' '.join(niveau_etudes_emploi).strip()

            lien_emploi = contenu.css("div.col-lg-5.col-md-5.col-sm-7.col-xs-12.job-title h5 a::attr(href)").extract_first()

            print("date : ", date_emploi)
            print("id : ", id_emploi)
            print("ville : ", ville_emploi)
            print("mobilité : ", mobilite_emploi)
            print("type : ", types_emploi)
            print("competence : ", competences_emploi)
            print("secteur : ", secteurs_emploi)
            print("niveau d'etudes : ", niveau_etudes_emploi)
            print("lien : ", lien_emploi)

            print(type(date_emploi))
            print(type(types_emploi))
        return contenus_emploi

#url_emploi = "https://www.emploi.ma/recrutement-maroc-cv/5842650"
url_emploi = "https://www.emploi.ma/recrutement-maroc-cv/5839879"

source_emploi_ma = catch_URL(url_emploi)
data_emploi_ma = catch_sec_niv(source_emploi_ma)

print(data_emploi_ma)
