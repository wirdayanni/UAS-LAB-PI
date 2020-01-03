#Import modul python
from bs4 import BeautifulSoup
import requests
from datetime import datetime,timedelta
import string


linkRaw= "https://www.antaranews.com/indeks/"

hari = datetime.today()

#Ba~tasan Crawling
halaman =1
limitHalaman=100

#proses Scraping/Crawling
print('Sedang Diproses...')
with open('../data/link/link.txt','w') as file2:

    while halaman < limitHalaman:
        raws=f'{linkRaw}{hari.strftime("%d-%m-%Y")}'
        url=BeautifulSoup(requests.get(raws).text.encode("utf-8"),"html.parser")

        #mengambil isi berita di sublink dan membersihkannya dari tag HTML
        for i in url.select(".simple-post"):
            linkSemuanya=i.find ("a")['href']
            file2.write(linkSemuanya+'\n')
            sublink=BeautifulSoup(requests.get(linkSemuanya).text.encode("utf-8"),"html.parser")

            #membuang googletagpush
            for isiScript in sublink(['script','style']):
                isiScript.decompose()
            try:
                isiBerita=sublink.select_one(".post-content").getText().strip().translate(str.maketrans('','',string.punctuation))
                title = sublink.select_one('.post-title').getText().strip().translate(str.maketrans('','',string.punctuation))
            except AttributeError:
                pass
            #memasukkan kedalam folder antaraNews
            file = open(f'../data/crawling/berita{halaman}.txt','w')
            file.write(f'{title}\n{isiBerita}')
            if halaman is limitHalaman:
                break
            halaman+=1
        else:
            hari+=timedelta(days=-1) 
        print(f'selesai {halaman} berita')



