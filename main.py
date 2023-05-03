import sys
import pandas
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QWidget, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtGui import QIcon

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Películas más taquilleras entre 2007 y 2011')
        self.resize(1200, 400)

        # Importar el dataset
        self.ds = pandas.read_csv('Dataset/movies.csv')

        # Widgets de búsqueda
        self.film = QLineEdit()
        self.genre = QComboBox()
        self.leadStudio = QComboBox()
        #self.audienceScore = QLineEdit()
        #self.profitability = QLineEdit()
        #self.rottenTomatoes = QLineEdit()
        #self.worldwideGross = QLineEdit()
        self.year = QComboBox()

        # Configurar opciones de ComboBox
        self.genre.addItem('Todos')
        self.ds['Genre'] = self.ds['Genre'].astype(str)
        self.genre.addItems(self.ds['Genre'].unique())

        self.leadStudio.addItem('Todos')
        self.ds['Lead Studio'] = self.ds['Lead Studio'].astype(str)
        self.leadStudio.addItems(self.ds['Lead Studio'].unique())

        self.year.addItem('Todos')
        self.ds['Year'] = self.ds['Year'].astype(str)
        self.year.addItems(self.ds['Year'].unique())

        # Botón de búsqueda
        self.searchButton = QPushButton("Buscar")
        self.searchButton.clicked.connect(self.search)

        # Tabla de resultados
        self.resultTable = QTableWidget()
        self.resultTable.setColumnCount(8)
        self.resultTable.setHorizontalHeaderLabels(['Película', 'Género', 'Estudio Principal', 'Puntuación del Público %', 'Rentabilidad', 'Rotten Tomatoes %', 'Bruto mundial', 'Año'])
        self.resultTable.setRowCount(0)

        # Layouts
        search = QVBoxLayout()
        search.addWidget(QLabel('Película:'))
        search.addWidget(self.film)
        search.addWidget(QLabel('Género:'))
        search.addWidget(self.genre)
        search.addWidget(QLabel('Estudio Principal:'))
        search.addWidget(self.leadStudio)
        #search.addWidget(QLabel('Puntuación del Público %:'))
        #search.addWidget(self.audienceScore)
        #search.addWidget(QLabel('Rentabilidad:'))
        #search.addWidget(self.profitability)
        #search.addWidget(QLabel('Rotten Tomatoes %'))
        #search.addWidget(self.rottenTomatoes)
        #search.addWidget(QLabel('Bruto mundial:'))
        #search.addWidget(self.worldwideGross)
        search.addWidget(QLabel('Año:'))
        search.addWidget(self.year)
        search.addWidget(self.searchButton)

        main = QHBoxLayout()
        main.addLayout(search)
        main.addWidget(self.resultTable)

        self.setLayout(main)

    def search(self):
        film = self.film.text().lower()
        genre = self.genre.currentText()
        leadStudio = self.leadStudio.currentText()
        #audienceScore = self.audienceScore.text()
        #profitability = self.profitability.text()
        #rottenTomatoes = self.rottenTomatoes.text()
        #worldwideGross = self.worldwideGross.text()
        year = self.year.currentText()

        # Filtrar el Data Set
        query = f'Film.str.lower().str.contains("{film}")'
        if genre != 'Todos':
            query += f' and Genre == "{genre}"'
        if leadStudio != 'Todos':
            query += f' and "Lead Studio" == "{leadStudio}"'

        # Filtro para ordenar de mayor a menor y visceversa
        #if audienceScore != '':
        #    query += f' and "Audience score %" == {audienceScore}'
        #if profitability != '':
        #    query += f' and Profitability == {profitability}'
        #if rottenTomatoes != '':
        #    query += f' and "Rotten Tomatoes %" == {rottenTomatoes}'
        #if worldwideGross != '':
        #    query += f' and "Worldwide Gross" == {worldwideGross}'

        if year != 'Todos':
            query += f' and Year == "{year}"'

        # Optimizar tabla según filtro
        filtro = self.ds.query(query)
        filtro = filtro.dropna()
        filtro = filtro.reset_index(drop = True)

        # Mostrar los resultados de la tabla
        self.resultTable.setRowCount(len(filtro))
        for i, row in filtro.iterrows():
            filmItem = QTableWidgetItem(row['Film'])
            genreItem = QTableWidgetItem(row['Genre'])
            leadStudioItem = QTableWidgetItem(str(row['Lead Studio']))
            audienceScoreItem = QTableWidgetItem(str(row['Audience score %']))
            profitabilityItem = QTableWidgetItem(str(row['Profitability']))
            rottenTomatoesItem = QTableWidgetItem(str(row['Rotten Tomatoes %']))
            worldwideGrossItem = QTableWidgetItem(str(row['Worldwide Gross']))
            yearItem = QTableWidgetItem(str(row['Year']))

            self.resultTable.setItem(i, 0, filmItem)
            self.resultTable.setItem(i, 1, genreItem)
            self.resultTable.setItem(i, 2, leadStudioItem)
            self.resultTable.setItem(i, 3, audienceScoreItem)
            self.resultTable.setItem(i, 4, profitabilityItem)
            self.resultTable.setItem(i, 5, rottenTomatoesItem)
            self.resultTable.setItem(i, 6, worldwideGrossItem)
            self.resultTable.setItem(i, 7, yearItem)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    icon = QIcon('nota.png')
    ventana.setWindowIcon(icon)
    ventana.show()
    app.exec()
