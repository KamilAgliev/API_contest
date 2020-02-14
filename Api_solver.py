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
        self.change_l()

    def keyPressEvent(self, event):
        if event.key() == 16777238:
            # Page_up
            self.z = str(min(19, int(self.z) + 1))
        if event.key() == 16777239:
            # page_down
            self.z = str(max(2, int(self.z) - 1))
        if event.key() == 16777234:
            # left
            self.longitude = str(float(self.longitude) - 1)
        if event.key() == 16777235:
            # up
            self.latitude = str(float(self.latitude) + 1)
        if event.key() == 16777236:
            # right
            self.longitude = str(float(self.longitude) + 1)
        if event.key() == 16777237:
            # down
            self.latitude = str(float(self.latitude) - 1)

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
        print(response.url)
        with open("map.png", "wb") as file:
            file.write(response.content)
        self.image_label.setPixmap(QPixmap("map.png"))

    def change_l(self):
        dic = {
            'схема': "map",
            'спутник': 'sat',
            'гибрид': 'sat,skl',
        }
        st = input('Введите переключатель слоёв карты')
        self.l = dic[st]
        self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
