from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import sys

from PIL import Image
import requests


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        # initial data
        self.longitude = "52.340178"
        self.latitude = "54.887520"
        self.z = "12"
        self.l = 'map'
        self.params = {
            "z": self.z,
            "ll": self.longitude + ',' + self.latitude,
            "l": self.l,
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b"
        }
        geocoder_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_server, params=self.params)
        with open("map.png", "wb") as file:
            file.write(response.content)
        self.image_label = QLabel(self)
        self.image_label.resize(500, 500)
        self.image_label.setPixmap(QPixmap("map.png"))
        # find button
        self.find_button.clicked.connect(self.find_toponym)
        self.error_label.hide()

    def find_toponym(self):
        request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode" \
            f"={self.request_line.text()}&format=json"
        response = requests.get(request)
        if not response:
            self.error_label.show()
        else:
            self.error_label.hide()
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            self.longitude, self.latitude = toponym_coodrinates.split()
            self.update_map()

    def keyPressEvent(self, event):
        if event.key() == 16777238:
            # Page_up
            self.z = str(min(19, int(self.z) + 1))
        elif event.key() == 16777239:
            # page_down
            self.z = str(max(2, int(self.z) - 1))
        elif event.key() == 16777234:
            # left
            self.longitude = str(float(self.longitude) - 1)
        elif event.key() == 16777235:
            # up
            self.latitude = str(float(self.latitude) + 1)
        elif event.key() == 16777236:
            # right
            self.longitude = str(float(self.longitude) + 1)
        elif event.key() == 16777237:
            # down
            self.latitude = str(float(self.latitude) - 1)
        else:
            return
        self.update_map()

    def update_map(self):
        self.params = {
            "z": self.z,
            "ll": self.longitude + ',' + self.latitude,
            "l": self.l,
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b"
        }
        geocoder_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_server, params=self.params)
        with open("map.png", "wb") as file:
            file.write(response.content)
        self.image_label.setPixmap(QPixmap("map.png"))

    def change_l(self):
        choices = {
            'схема': "map",
            'спутник': 'sat',
            'гибрид': 'sat,skl',
        }
        st = input('Введите переключатель слоёв карты ').strip()
        try:
            self.l = choices[st]
        except Exception:
            print("Не существует такого слоя карты")
            return
        self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())