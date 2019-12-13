import sys
import scraper
from PyQt5.QtWidgets import *



class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Kalkulator Kwot'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 400
        self.calculated = False
        self.initUI()
        self.show()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #label
        self.label = QLabel("Podaj kwotę brutto:", self)
        self.label.setGeometry(40,10,200,15)  # (x, y, width, height)

        #labelbrutto
        self.label1 = QLabel("Kwota brutto", self)
        self.label1.setGeometry(40, 115, 200, 15)  # (x, y, width, height)

        #labelnetto
        self.label2 = QLabel("Kwota netto", self)
        self.label2.setGeometry(145, 115, 200, 15)  # (x, y, width, height)

        #lista brutto
        self.listwidget = QListWidget(self)
        self.listwidget.setGeometry(40, 130, 100, 200)  # (x, y, width, height)

        #lista netto
        self.listwidget2 = QListWidget(self)
        self.listwidget2.setGeometry(145, 130, 100, 200)  # (x, y, width, height)


        #inputbox
        self.textbox = QLineEdit(self)
        self.textbox.move(40, 30)
        self.textbox.resize(210, 20)

        #button
        self.button = QPushButton('Dodaj kwote', self)
        self.button.move(40, 60)
        self.button.clicked.connect(self.on_click_addamount)

        #button1
        self.button1 = QPushButton('Pokaz netto', self)
        self.button1.move(150, 60)
        self.button1.clicked.connect(self.on_click_calculate)

        # button3
        self.button3 = QPushButton('Pokaz wykres', self)
        self.button3.move(40, 340)
        self.button3.clicked.connect(self.on_click_graph)



    def on_click_addamount(self):
        textboxValue = self.textbox.text()
        try:
            float(textboxValue)
            self.listwidget.insertItem(0, textboxValue)
            self.textbox.clear()
        except ValueError:
            QMessageBox.question(self, 'Niepoprawna kwota!', "Wprowadź poprawną kwotę", QMessageBox.Ok,QMessageBox.Ok)
            self.textbox.clear()


    def on_click_calculate(self):
        list=[]
        for x in range(self.listwidget.count()):
            list.append(float(self.listwidget.item(x).text()))
        for l in list:
            self.listwidget2.insertItem(0, scraper.netto(l))

        print(list)
        self.calculated=True

    def on_click_graph(self):
        if self.calculated == True:
           self.w = GraphWindow()
           self.w.show()
        else:
            QMessageBox.question(self, 'Brak obliczeń!', "Najpierw oblicz kwoty netto!", QMessageBox.Ok, QMessageBox.Ok)


#okno wykresu
class GraphWindow(App):
    def __init__(self):
        super().__init__()


    def initUI(self):
        self.setWindowTitle("wykres")
        self.setGeometry(600, self.top, 400, 440)

        self.button = QPushButton('zamknij', self)
        self.button.move(150, 400)
        self.button.clicked.connect(self.close)

    def close(self):
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

