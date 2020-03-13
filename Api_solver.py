from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import sys
import requests
 
 
class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        # initial data
        self.longitude = "52.340178"
        self.latitude = "54.887520"
        self.z = "12"
        self.l = ['map', 'png']
        self.params = {
            "z": self.z,
            "ll": self.longitude + ',' + self.latitude,
            "l": self.l,
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b"
        }
        self.postal = False
        geocoder_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_server, params=self.params)
        with open("map.png", "wb") as file:
            file.write(response.content)
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
        self.postal_code.toggled.connect(self.change_postal)
        self.curr_mark = 2
        self.prev_mark = 1
        self.ret_btn.clicked.connect(self.return_to_initial)
        self.maps = {
            'схема': ["map", 'png'],
            'спутник': ['sat', 'jpeg'],
            'гибрид': ['sat,skl', 'jpeg']
        }
        request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode" \
                  f"={'Альметьевск'}&format=json"
        response = requests.get(request)
        json_response = response.json()
 
        self.toponym = \
            json_response["response"]["GeoObjectCollection"][
                "featureMember"][
                0]["GeoObject"]
        self.lower_corner = self.toponym['boundedBy']['Envelope']['lowerCorner'].split()
        self.upper_corner = self.toponym['boundedBy']['Envelope']['upperCorner'].split()
 
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
            self.toponym = \
                json_response["response"]["GeoObjectCollection"][
                    "featureMember"][
                    0]["GeoObject"]
            self.lower_corner = self.toponym['boundedBy']['Envelope']['lowerCorner'].split()
            self.upper_corner = self.toponym['boundedBy']['Envelope']['upperCorner'].split()
            toponym_coodrinates = self.toponym["Point"]["pos"]
            self.longitude, self.latitude = toponym_coodrinates.split()
            metka = f'{",".join(toponym_coodrinates.split())},pm'
            metka += 'wt'
            metka += 's' + str(self.curr_mark) + '~'
            self.prev_mark = self.curr_mark
            self.curr_mark += 1
            self.marks += metka
            self.update_map()
            self.show_adress()
 
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
        self.l = self.maps[self.sender().text()]
        self.update_map()
 
    def update_map(self):
        self.params = {
            "z": self.z,
            "ll": self.longitude + ',' + self.latitude,
            "l": self.l[0],
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "pt": self.marks[:-1]
        }
        geocoder_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_server, params=self.params)
        print(response.url)
        with open(f"map.{self.l[1]}", "wb") as file:
            file.write(response.content)
        self.image_label.setPixmap(QPixmap(f"map.{self.l[1]}"))
 
    def return_to_initial(self):
        self.longitude = "52.340178"
        self.latitude = "54.887520"
        self.z = "12"
        self.params = {
            "z": self.z,
            "ll": self.longitude + ',' + self.latitude,
            "l": self.l,
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "pt": self.marks[:-1]
        }
        self.update_map()
        self.adress_label.setText("Адрес: Россия, Альметьевск")
 
    def show_adress(self):
        if self.postal:
            try:
                postal_code = \
                    self.toponym['metaDataProperty']['GeocoderMetaData'][
                        'Address'][
                        'postal_code']
            except Exception:
                postal_code = ""
        else:
            postal_code = ""
        self.adress_label.setText(
            f"Адрес: {self.toponym['metaDataProperty']['GeocoderMetaData']['text']}, {postal_code}")
 
    def change_postal(self):
        self.postal = not self.postal
        self.show_adress()
 
    def mousePressEvent(self, event):
        self.point = event.pos()
        if 0 < self.point.x() < 600 and 10 < self.point.y() < 460:
            print(self.lower_corner)
            print(self.upper_corner)
            x_koof = (float(self.upper_corner[0]) - float(self.lower_corner[0])) / 600
            y_koof = (float(self.upper_corner[1]) - float(self.lower_corner[1])) / 450
            print(y_koof, x_koof)
            x_coord = self.point.x() * x_koof + float(self.lower_corner[0])
            y_coord = (self.point.y() - 10) * y_koof + float(self.lower_corner[1])
            print(x_coord, y_coord)
            self.longitude = str(x_coord)
            self.latitude = str(y_coord)
            self.update_map()
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
