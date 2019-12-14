import sys
import scraper
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.use('agg')
from matplotlib.figure import Figure


bruttoplot=[0]
nettoplot=[0]
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
            if textboxValue.startswith("."):
                raise(ValueError)
            float(textboxValue)
            bruttoplot.append(float(textboxValue))
            self.listwidget.insertItem(0, textboxValue)
            self.textbox.clear()
        except ValueError:
            QMessageBox.question(self, 'Niepoprawna kwota!', "Wprowadź poprawną kwotę", QMessageBox.Ok,QMessageBox.Ok)
            self.textbox.clear()


    def on_click_calculate(self):
        self.listwidget2.clear()
        list=[]
        for x in range(self.listwidget.count()):
            list.append(float(self.listwidget.item(x).text()))
        list.reverse()
        for l in list:
            temp = scraper.netto(l)
            nettoplot.append(float(temp))
            self.listwidget2.insertItem(0, temp)
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



