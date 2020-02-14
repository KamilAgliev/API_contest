from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap
import sys
from PIL import Image
import requests

SCREEN_SIZE = [500, 500]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.longitude = "52.340178"
        self.latitude = "54.887520"
        self.z = "12"
        self.params = {
            "z": self.z,
            "ll": self.longitude + ',' + self.latitude,
            "l": "map",
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b"
        }
        geocoder_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_server, params=self.params)
        with open("map.png", "wb") as file:
            file.write(response.content)
        self.image_label = QLabel(self)
        self.image_label.resize(500, 500)
        self.image_label.setPixmap(QPixmap("map.png"))

    def keyPressEvent(self, event):
        if event.key() == 16777238:
            self.z = str(min(19, int(self.z) + 1))
        if event.key() == 16777239:
            self.z = str(max(2, int(self.z) - 1))
        self.params = {
            "z": self.z,
            "ll": self.longitude + ',' + self.latitude,
            "l": "map",
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b"
        }
        self.update_map()

    def update_map(self):
        geocoder_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_server, params=self.params)
        print(response.url)
        with open("map.png", "wb") as file:
            file.write(response.content)
        self.image_label.setPixmap(QPixmap("map.png"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
