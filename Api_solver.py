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
        self.longitude = sys.argv[1]
        self.latitude = sys.argv[2]
        self.spn = sys.argv[3:]
        params = {
            "spn": ",".join(self.spn),
            "ll": self.longitude + ',' + self.latitude,
            "l": "map",
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b"
        }
        geocoder_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_server, params=params)
        print(response.url)
        self.map = "map.png"
        with open("map.png", "wb") as file:
            file.write(response.content)
        self.image_label = QLabel(self)
        self.image_label.resize(500, 500)
        self.image_label.move(0, 0)
        self.image_label.setPixmap(QPixmap("map.png"))
        self.image_label.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
