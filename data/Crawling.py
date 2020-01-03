from bs4 import BeautifulSoup
import requests
from datetime import datetime,timedelta

raw = "https://news.okezone.com/indeks/"

hari = datetime.today()

halaman = 1
limithalaman = 100

print('memproses...')
with open('../data/link/link.txt','w') as file:
    while halaman < limithalaman:
        raws=f'{raw}{hari.strftime("%Y/%m/%d")}'
        url=BeautifulSoup(requests.get(raws).text.encode("utf-8"),"html.parser")

        for i in url.select(".content-hardnews"):
            tautan=i.find ("a")['href']
            file.write (tautan+'\n')

            #mengambil konten dari subtautan
            subtautan=BeautifulSoup(requests.get(tautan).text.encode("utf-8"),"html.parser")
        
            for script in subtautan(['script','style']):
                script.decompose()
            try:
                konten=subtautan.select_one(".read").getText().strip()
            except AttributeError:
                pass

            #hasil scraping dimasukkan ke dalam folder scraping
            file = open(f'../data/crawling/doc{halaman}.txt','w')
            file.write(konten)
            if halaman is limithalaman:
                break
            halaman+=1
        else:
            hari+=timedelta(days=-1) 
        print(f'selesai {halaman} url')
    