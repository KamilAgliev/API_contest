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
        self.marks = self.longitude + ',' + self.latitude + '~'
        self.up.clicked.connect(self.Change_buttons)
        self.down.clicked.connect(self.Change_buttons)
        self.left.clicked.connect(self.Change_buttons)
        self.right.clicked.connect(self.Change_buttons)
        self.PgUp.clicked.connect(self.Change_buttons)
        self.PgDn.clicked.connect(self.Change_buttons)
        self.radioButton.toggled.connect(self.l_change)
        self.radioButton_2.toggled.connect(self.l_change)
        self.radioButton_3.toggled.connect(self.l_change)
        self.curr_mark = 2
        self.prev_mark = 1
        self.ret_btn.clicked.connect(self.return_to_initial)
        self.maps = {
            'схема': "map",
            'спутник': 'sat',
            'гибрид': 'sat,skl',
        }

    def find_toponym(self):
        request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode" \
            f"={self.request_line.text()}&format=json"
        response = requests.get(request)
        if not response:
            self.error_label.show()
        else:
            self.error_label.hide()
            json_response = response.json()
            if len(json_response["response"]["GeoObjectCollection"][
                       "featureMember"]) == 0:
                self.error_label.show()
                return
            toponym = \
                json_response["response"]["GeoObjectCollection"][
                    "featureMember"][
                    0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            self.longitude, self.latitude = toponym_coodrinates.split()
            metka = f'{",".join(toponym_coodrinates.split())},pm'
            metka += 'wt'
            metka += 's' + str(self.curr_mark) + '~'
            self.prev_mark = self.curr_mark
            self.curr_mark += 1
            self.marks += metka
            self.update_map()

    def Change_buttons(self):
        send = self.sender().text()
        k = (19. - int(self.z)) * (19. - int(self.z)) / 3000
        if send == 'PgUp':
            # Page_up
            self.z = str(min(19, int(self.z) + 1))
        elif send == 'PgDn':
            # page_down
            self.z = str(max(2, int(self.z) - 1))
        elif send == '<-':
            # left
            self.longitude = str(
                float(self.longitude) - k)
        elif send == '↑':
            # up
            self.latitude = str(
                float(self.latitude) + k)
        elif send == '->':
            # right
            self.longitude = str(
                float(self.longitude) + k)
        elif send == '↓':
            # down
            self.latitude = str(
                float(self.latitude) - k)
        else:
            return
        self.update_map()

    def l_change(self):
        for btn in ex.buttonGroup.buttons():
            if btn.isChecked():
                self.l = self.maps[btn.text()]
        self.update_map()

    def update_map(self):
        for btn in ex.buttonGroup.buttons():
            if btn.isChecked():
                self.l = self.maps[btn.text()]
        self.params = {
            "z": self.z,
            "ll": self.longitude + ',' + self.latitude,
            "l": self.l,
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "pt": self.marks[:-1]
        }
        geocoder_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_server, params=self.params)
        print(response.url)
        with open("map.png", "wb") as file:
            file.write(response.content)
        self.image_label.setPixmap(QPixmap("map.png"))

    def return_to_initial(self):
        self.longitude = "52.340178"
        self.latitude = "54.887520"
        self.z = "12"
        self.l = 'map'
        self.params = {
            "z": self.z,
            "ll": self.longitude + ',' + self.latitude,
            "l": self.l,
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "pt": self.marks[:-1]
        }
        self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
