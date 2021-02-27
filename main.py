import sys
import requests
import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.btn_run.clicked.connect(self.run)

    def initUi(self):
        self.setupUi(self)
        self.setWindowTitle('Map_observer')

    def getImage(self):
        map_request = self.url_creator()
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def url_creator(self):
        api_server = 'http://static-maps.yandex.ru/1.x/'
        lon, lat, zoom = self.line_lon.text(), self.line_lat.text(), self.line_zoom.text()
        params = {
            "ll": ",".join([lon, lat]),
            "z": zoom,
            "l": "map"
        }
        return requests.get(api_server, params=params).url

    def run(self):
        try:
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.label_map.setPixmap(self.pixmap)
        except Exception as e:
            self.label_error_msg.setText(f'Произошла ошибка {e.__class__.__name__}')

    def closeEvent(self, event):
        try:
            os.remove(self.map_file)
        except AttributeError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
