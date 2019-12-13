import sys
from PyQt5.QtWidgets import *

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Kalkulator Kwot'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 400
        self.initUI()



    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #label
        self.label = QLabel("Podaj kwotę brutto:", self)
        self.label.setGeometry(40,10,200,15)  # (x, y, width, height)

        #list
        self.listwidget = QListWidget(self)
        self.listwidget.setGeometry(40, 150, 200, 200)  # (x, y, width, height)


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
        self.show()



    def on_click_addamount(self):
        textboxValue = self.textbox.text()
        self.listwidget.insertItem(0,textboxValue)
        self.textbox.clear()



    def on_click_calculate(self):
       pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

