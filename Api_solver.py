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
        self.command_btn.clicked.connect(self.run_command_menu)
        self.enter_btn.clicked.connect(self.run)
        self.curr_mark = 2
        self.prev_mark = 1
        self.ret_btn.clicked.connect(self.return_to_initial)

    def find_toponym(self):
        request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode" \
                  f"={self.request_line.text()}&format=json"
        response = requests.get(request)
        if not response:
            self.error_label.show()
        else:
            self.error_label.hide()
            json_response = response.json()
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
        if send == 'PgUp':
            # Page_up
            self.z = str(min(19, int(self.z) + 1))
        elif send == 'PgDn':
            # page_down
            self.z = str(max(2, int(self.z) - 1))
        elif send == '<-':
            # left
            self.longitude = str(
                float(self.longitude) - ((20.0 - int(self.z)) / 200))
        elif send == '↑':
            # up
            self.latitude = str(
                float(self.latitude) + ((20. - int(self.z)) / 200))
        elif send == '->':
            # right
            self.longitude = str(
                float(self.longitude) + ((20.0 - int(self.z)) / 200))
        elif send == '↓':
            # down
            self.latitude = str(
                float(self.latitude) - ((20. - int(self.z)) / 200))
        else:
            return
        self.update_map()

    def update_map(self):
        self.params = {
            "z": self.z,
            "ll": self.longitude + ',' + self.latitude,
            "l": self.l,
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "pt": self.marks[:-1]
        }
        geocoder_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_server, params=self.params)
        with open("map.png", "wb") as file:
            file.write(response.content)
        self.image_label.setPixmap(QPixmap("map.png"))

    def change_l(self, st):
        choices = {
            'схема': "map",
            'спутник': 'sat',
            'гибрид': 'sat,skl',
        }
        try:
            self.l = choices[st]
        except Exception:
            print("Не существует такого слоя карты")
            return
        self.update_map()

    def run_command_menu(self):
        self.curr_com = self.command_line.text()
        if self.curr_com == "1":
            self.what_to_input.setText(
                "Введите слой карты (схема/спутник/гибрид)")
        elif self.curr_com == "2":
            self.what_to_input.setText(
                "Нажмите на кнопку \'enter\', меню ввода появится в консоли")

    def run(self):
        text = self.second_enter_line.text()
        if self.curr_com == '1':
            self.change_l(text)
            self.what_to_input.setText("")
        elif self.curr_com == "2":
            self.create_mark()

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
        geocoder_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_server, params=self.params)
        with open("map.png", "wb") as file:
            file.write(response.content)
        self.image_label = QLabel(self)
        self.image_label.resize(500, 500)
        self.image_label.setPixmap(QPixmap("map.png"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
