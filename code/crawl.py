#Import modul python
from bs4 import BeautifulSoup
import requests
from datetime import datetime,timedelta
import string


linkRaw= "https://www.antaranews.com/indeks/"

hari = datetime.today()

halaman =1
limithalaman=100

print('Sedang Diproses...')
with open('../data/link/link.txt','w') as file:

    while halaman < limithalaman:
        raws=f'{linkRaw}{hari.strftime("%d-%m-%Y")}'
        url=BeautifulSoup(requests.get(raws).text.encode("utf-8"),"html.parser")

        #mengambil konten dari subtautan dan membersihkannya dari tag HTML
        for i in url.select(".simple-post"):
            tautan=i.find ("a")['href']
            file.write(tautan+'\n')
            sublink=BeautifulSoup(requests.get(tautan).text.encode("utf-8"),"html.parser")

            #membuang googletagpush
            for isiScript in sublink(['script','style']):
                isiScript.decompose()
            try:
                isiBerita=sublink.select_one(".post-content").getText().strip().translate(str.maketrans('','',string.punctuation))
                title = sublink.select_one('.post-title').getText().strip().translate(str.maketrans('','',string.punctuation))
            except AttributeError:
                pass
            #memasukkan kedalam folder data
            file = open(f'../data/crawling/doc{halaman}.txt','w')
            file.write(f'{title}\n{isiBerita}')
            if halaman is limithalaman:
                break
            halaman+=1
        else:
            hari+=timedelta(days=-1) 
        print(f'selesai {halaman} berita')



