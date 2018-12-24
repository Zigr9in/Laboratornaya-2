import sys, re, urllib, html2text
from urllib import request
# Импортируем наш интерфейс
from newsform import *
from PyQt5 import QtCore, QtGui, QtWidgets

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.newsurl=[]
        self.Parse()
        

        # Здесь прописываем событие нажатия на кнопку                     
        self.ui.pushButton.clicked.connect(self.AllNews)

    # Пока пустая функция которая выполняется
    # при нажатии на кнопку

    def Parse(self): #Функция которая парсит наш сайт
        s='http://russian.rt.com/news'
        doc=urllib.request.urlopen(s).read().decode('utf-8',errors='ignore') #html страничка сайта
        doc=doc.replace('\n','') #убираем переносы строк в коде для правильного парсинга
        zagolovky=re.findall('<a class="link link_color" href="(.+?)</a>',doc)
        for x in zagolovky:
            self.newsurl.append(x.split('">')[0])
            self.ui.listWidget.addItem(x.split('">')[1].strip()) # разделяем ссылку и название строки
    def AllNews(self): # открывает новость подробнее
        n=self.ui.listWidget.currentRow() #номер строки на которую мы нажали
        u='https://russian.rt.com'+self.newsurl[n] #вытаскиваем ссылку с соответствующим номером
        doc=urllib.request.urlopen(u).read().decode('utf-8',errors='ignore')
        h=html2text.HTML2Text()
        h.ignore_links=True
        h.body_width=False
        h.ignory_images=True
        doc=h.handle(doc) #Преобразовываем из HTML в text
        mas=doc.split('\n')
        stroka=''
        del mas[mas.index('Ошибка в тексте? Выделите её и нажмите «Ctrl + Enter»'):-1]
        for x in mas:
            if(len(x)>100):
                stroka=stroka+x+'\n\n'
        self.ui.textEdit.setText(stroka)
    
        
if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
