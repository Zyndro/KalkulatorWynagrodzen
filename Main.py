import sys
import scraper
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.use('agg')
from matplotlib.figure import Figure


bruttoplot = [0]
nettoplot = [0]


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Kalkulator Kwot'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 400
        self.calculated = False
        self.cleared = True
        self.init_ui()
        self.show()
        self.umowa = 1

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #label
        self.label = QLabel("Podaj kwotę brutto(14zł minimum):", self)
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
        self.textbox.resize(205, 20)

        #button
        self.button = QPushButton('Dodaj kwote', self)
        self.button.move(40, 60)
        self.button.clicked.connect(self.on_click_addamount)

        #button1
        self.button1 = QPushButton('Pokaz netto', self)
        self.button1.move(145, 60)
        self.button1.clicked.connect(self.on_click_calculate)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(40, 375, 240, 20)

        #button3
        self.button3 = QPushButton('Pokaz wykres', self)
        self.button3.move(40, 340)
        self.button3.clicked.connect(self.on_click_graph)

        #button4
        self.button4 = QPushButton('Wyczysc wszystko', self)
        self.button4.move(145, 340)
        self.button4.clicked.connect(self.clear_all)


        self.cb = QCheckBox('UoP', self)
        self.cb.move(145, 85)
        self.cb.toggle()
        self.cb.stateChanged.connect(self.change_uop)

        self.cb1 = QCheckBox('Uz', self)
        self.cb1.move(190, 85)
        self.cb1.stateChanged.connect(self.change_uz)

        self.cb2 = QCheckBox('UoD', self)
        self.cb2.move(230, 85)
        self.cb2.stateChanged.connect(self.change_uod)




    def change_uop(self, state):
        if state == QtCore.Qt.Checked:
            self.umowa=1
            self.cb1.setChecked(False)
            self.cb2.setChecked(False)

    def change_uz(self, state):
        if state == QtCore.Qt.Checked:
            self.umowa=2
            self.cb.setChecked(False)
            self.cb2.setChecked(False)

    def change_uod(self, state):
        if state == QtCore.Qt.Checked:
            self.umowa=3
            self.cb.setChecked(False)
            self.cb1.setChecked(False)


    def on_click_addamount(self):
        if self.cleared == True:
            textboxValue = self.textbox.text()
            try:
                if textboxValue.startswith(".") or float(textboxValue) < 14.0:
                    raise(ValueError)
                float(textboxValue)
                bruttoplot.append(float(textboxValue))
                self.listwidget.insertItem(0, textboxValue)
                self.textbox.clear()
            except ValueError:
                QMessageBox.question(self, 'Niepoprawna kwota!', "Wprowadź poprawną kwotę", QMessageBox.Ok,QMessageBox.Ok)
                self.textbox.clear()
        else:
            QMessageBox.question(self, 'Wyczyść dane', "Wyczuść dane aby ponownie wykonac obliczenia", QMessageBox.Ok, QMessageBox.Ok)

    def on_click_calculate(self):
        if self.cleared == True:
            self.completed = 0
            self.listwidget2.clear()
            list=[]
            try:
                for x in range(self.listwidget.count()):
                    list.append(float(self.listwidget.item(x).text()))
                list.reverse()
                for l in list:
                    temp = scraper.netto(l,self.umowa)
                    nettoplot.append(float(temp))
                    self.listwidget2.insertItem(0, temp)
                    self.completed += 100/len(list)
                    self.progress.setValue(self.completed)
                self.calculated=True
                self.cleared = False
            except:
                QMessageBox.question(self, 'Błąd połączenia', "Sprawdź internet", QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.question(self, 'Wyczyść dane', "Wyczuść dane aby ponownie wykonac obliczenia", QMessageBox.Ok, QMessageBox.Ok)



    def on_click_graph(self):
        if self.calculated == True:
           self.w = GraphWindow()
           self.w.show()
        else:
            QMessageBox.question(self, 'Brak obliczeń!', "Najpierw oblicz kwoty netto!", QMessageBox.Ok, QMessageBox.Ok)

    def clear_all(self):
        self.listwidget.clear()
        self.listwidget2.clear()
        bruttoplot.clear()
        bruttoplot.append(0.0)
        nettoplot.clear()
        nettoplot.append(0.0)
        self.calculated=False
        self.cleared = True
        self.completed = 0
        QMessageBox.question(self, 'Wyczyszczono', "wyczyszczono!", QMessageBox.Ok, QMessageBox.Ok)


#okno wykresu
class GraphWindow(App):
    def __init__(self):
        super().__init__()

    def init_ui(self):
        self.setWindowTitle("wykres")
        self.setGeometry(600, self.top, 600, 440)

        self.button = QPushButton('zamknij', self)
        self.button.move(250, 400)
        self.button.clicked.connect(self.close)
        m = PlotCanvas(self, width=6, height=4)
        m.move(0, 0)

    def close(self):
        self.hide()


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
        #siatka na wykresie
        for ax in fig.axes:
            ax.grid(True)

    def plot(self):
        brutto = sorted(bruttoplot, key=float)
        netto = sorted(nettoplot, key=float)
        ax = self.figure.add_subplot(111)
        ax.set_xlabel("kwota brutto")
        ax.set_ylabel("kwota netto")
        ax.axis([0, max(brutto)+max(brutto)/3, 0, max(netto)+max(netto)/3])
        ax.plot(brutto, netto, 'b-',brutto, netto, 'ro')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



