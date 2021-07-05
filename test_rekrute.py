from requests import get
from scrapy import Selector

def catch_URL(URL) :
    url_rekrute = URL
    response_rekrute = get(url_rekrute)
    source_rekrute = None

    if response_rekrute.status_code == 200 :
        source_rekrute = response_rekrute.text
        return source_rekrute

def catch_data(sourceRekrute) :
    if sourceRekrute :

        # Si le code source existe
        selector_rekrute = Selector(text=source_rekrute)
        contenus_rekrute = selector_rekrute.css("div.col-sm-10.col-xs-12")
        print("N°    DATE            INTITULE            COMPAGNIE            DESCRIPTION              LIEN")
        print("_________________________________________________________")
        cmp = 1
        for contenu in contenus_rekrute:
            if cmp < 3 :
                # Extraction de la date
                date_rekrute = contenu.css("i.fa.fa-clock-o + span::text").extract_first()

                # Extraction de la region
                region_rekrute_x = contenu.css("div.section h2 a::text").extract_first()
                region_rekrute = region_rekrute_x.rsplit(' | ')[1].strip()

                # Extraction du secteur
                secteur_rekrute = contenu.css("div.info ul li:first-child a::text").extract_first()

                # Extraction du niveau d'etudes requis
                niveau_rekrute_x = contenu.css("div.info ul li:nth-child(4) a::text").extract_first()
                niveau_rekrute = niveau_rekrute_x.strip()

                # Extraction de la compagnie
                compagnie_rekrute_x = contenu.css("i.fa.fa-industry + span::text").extract_first()
                compagnie_rekrute = compagnie_rekrute_x.strip()

                # Extraction de la description
                description_rekrute_x = contenu.css("i.fa.fa-binoculars + span::text").extract_first()
                description_rekrute = description_rekrute_x.strip()

                lien_rekrute = contenu.css("div.section h2 a::attr(href)").extract_first()

                #print(cmp, " ",date_rekrute," ",region_rekrute," ",secteur_rekrute," ", niveau_rekrute," ",compagnie_rekrute," ",description_rekrute," ",lien_rekrute)

                print(cmp,".")
                print("date : ",date_rekrute)
                print("region : ",region_rekrute)
                print("secteur : ",secteur_rekrute)
                print("niveau : ",niveau_rekrute)
                print("compagnie : ",compagnie_rekrute)
                print("description : ",description_rekrute)
                print("lien : ",lien_rekrute)

                cmp+=1

        return contenus_rekrute




RekruteURL = "https://www.rekrute.com/offres-emploi-metiers-de-l-it.html"

source_rekrute = catch_URL(RekruteURL)
data_rekrute = catch_data(source_rekrute)