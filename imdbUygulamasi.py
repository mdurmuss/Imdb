from bs4 import BeautifulSoup
import sys,requests
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QVBoxLayout,QTextEdit,QHBoxLayout,QLineEdit,QLabel

class film():
    def __init__(self):
        url = "https://www.imdb.com/chart/top"
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content,"html.parser")
        self.film_isimleri = soup.find_all("td",{"class":"titleColumn"})
        self.rating = soup.find_all("td",{"class":"ratingColumn imdbRating"})

    def list(self,rating):
        a = list()
        for self.baslik,self.reyting in zip(self.film_isimleri,self.rating):
            self.baslik = self.baslik.text
            self.reyting = self.reyting.text

            self.baslik = self.baslik.strip()
            self.baslik = self.baslik.replace("\n","")

            self.reyting = self.reyting.strip()
            self.reyting = self.reyting.replace("\n", "")
            if rating == 0.0:
                a.append(self.baslik+" Rating: "+self.reyting)

            else:
                try:
                   if float(self.reyting) >= float(rating):
                        a.append(self.baslik + " Rating: " + self.reyting)
                except:
                    if ValueError:

                        return "LÜTFEN FLOAT DEĞER GİRİNİZ"
        return a

class urlKopyalama():
    def __init__(self,x):
        self.count = 1
        self.url = "https://www.imdb.com/chart/top"
        self.response = requests.get(self.url)
        self.html_content = self.response.content
        self.soup = BeautifulSoup(self.html_content, "html.parser")
        self.film_isimleri = self.soup.find_all("td", {"class": "titleColumn"}, ("a"))

        for j in self.film_isimleri:
            j = str(j).split("<a hre")
            if self.count == int(x):
                break
            self.count += 1
        j = j[1].split("title")
        j[1].strip()
        self.isim = str(j[1])

        url = "https://www.imdb.com/title" + self.isim
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        film_isimleri = soup.find_all("div", {"class": "inline canwrap"})
        for i in film_isimleri:
            self.storyline = i.text
        self.storyline = self.storyline.strip()
class Pencere(QWidget,film):

    def __init__(self):
        super().__init__() # ÜST SINIFIN İNİT'İNİ ÇAĞIRMAMIZ GEREKİYOR..
        self.init_ui() # KENDİ FONKSİYONUMUZU TANIMLADIK

    def init_ui(self):
        self.ratio = float(8.0) # RATING İÇİN STANDART DEĞER
        self.filmler = film() # FİLM SINIFI İÇİN KULLANILACAK NESNE
        self.yazi_alani = QTextEdit() # LİSTELENECEK ALAN
        self.listele_buton = QPushButton("LISTELE") #LİSTE BUTONU
        self.temizle = QPushButton("TEMIZLE") # TEMİZLE BUTONU
        self.ratingButton = QLabel("RATING AYARI:") # RATING ETİKETİ
        self.line = QLineEdit(str(self.ratio)) # RATING DEĞERİNİN BULUNDUGU ALAN
        self.artiButon = QPushButton("+") # RATING ARTTIRMA
        self.eksiButon = QPushButton("-") # RATING AZALTMA
        self.storyButton = QPushButton("STORY") #KONUYU GÖSTERECEK BUTON
        self.storyLabel = QLabel("Konusunu görmek istediğiniz filmin numarasını yazın ve STORY butonunu kullanın:")
        self.story = QLineEdit()

        h_box = QHBoxLayout()
        h_box.addWidget(self.yazi_alani)

        h_box2 =QHBoxLayout()
        h_box2.addWidget(self.listele_buton)
        h_box2.addWidget(self.temizle)
        h_box2.addStretch()
        h_box2.addWidget(self.ratingButton)
        h_box2.addWidget(self.line)
        h_box2.addWidget(self.artiButon)
        h_box2.addWidget(self.eksiButon)

        h_box3 = QHBoxLayout()
        h_box3.addWidget(self.storyButton)
        h_box3.addWidget(self.storyLabel)
        h_box3.addWidget(self.story)

        v_box = QVBoxLayout()
        v_box.addLayout(h_box)
        v_box.addLayout(h_box2)
        v_box.addLayout(h_box3)

        self.setLayout(v_box)

        self.listele_buton.clicked.connect(self.click)
        self.temizle.clicked.connect(self.click)
        self.artiButon.clicked.connect(self.click)
        self.eksiButon.clicked.connect(self.click)
        self.storyButton.clicked.connect(self.click)

        self.setWindowTitle("IMDB FILMS")
        self.show()

    def click(self): # BU FONKSİYONDA HANGİ BUTONA TIKLANILDIGI VE BUTONLARIN İŞLEVLERİNİ AÇIKLADIM
        sender = self.sender() # TIKLANAN BUTONUN DEĞERİ

        if sender.text() == "LISTELE": # EĞER LİSTELE İSE
            a = self.filmler.list(self.line.text()) # line kısmı rating'i gösteriyor, oradaki değere göre filmler gösteriliyor..
            b = ""                                  # self.filmler nesnesi kullanıldı..
            for i in a:
                 b += (str(i)+"\n")

            self.yazi_alani.setText(b)
        elif sender.text() == "TEMIZLE":
            self.yazi_alani.clear()

        elif sender.text() == "+": # eğer + ' ya tıklandıysa arttırılır 10 olana dek..
            if self.ratio != 10.0:
             self.ratio += 0.5

        elif sender.text() == "-":
            if self.ratio != 8.0: # eğer - ' ye tıklanırsa eksilir.
                self.ratio -= 0.5
        elif sender.text() == "STORY": # evet STORY'E TIKLANIRSA BELİRLİ OLAN FİLMİN KONUSUNU YAZDIRMAK İSTİYORUZ.
            self.konu_goster() # konu göster fonksiyonumuzu çağırdık

        self.line.setText(str(self.ratio)) # rating değeri güncelleniyor..

    def konu_goster(self,):
        urlKopya = urlKopyalama(self.story.text())
        self.yazi_alani.setText(urlKopya.storyline) # yazi alanına filmin konusunu yazmamız gerek..
        self.numara = self.filmler.baslik.split(".")[0]


app = QApplication(sys.argv)

pen = Pencere()

pen.setGeometry(500,10,700,400)

sys.exit(app.exec_())

