import sys
import requests
import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow


move_range = {1: 2, 2: 1.5, 3: 1, 4: 1, 5: 0.9, 6: 0.9, 7: 0.5, 8: 0.5, 9: 0.1, 10: 0.1, 11: 0.09,
              12: 0.05, 13: 0.01, 14: 0.01, 15: 0.009, 16: 0.005, 17: 0.001, 18: 0.001, 19: 0.0005}


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.btn_run.clicked.connect(self.run)
        self.run()

    def initUi(self):
        self.setupUi(self)
        self.setWindowTitle('Map_observer')

    def getImage(self):
        map_request = self.url_creator()
        print(map_request)
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
        lon, lat, zoom = self.line_lon.text(), self.line_lat.text(), self.spin_zoom.value()
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

    def keyReleaseEvent(self, event):
        # масштаб карты
        if event.key() == Qt.Key_PageUp:
            if self.spin_zoom.value() + 1 <= 19:
                self.spin_zoom.setValue(self.spin_zoom.value() + 1)
                self.run()
        if event.key() == Qt.Key_PageDown:
            if self.spin_zoom.value() - 1 >= 1:
                self.spin_zoom.setValue(self.spin_zoom.value() - 1)
                self.run()
        # движение по карте
        if event.key() == Qt.Key_Right:
            self.line_lon.setText(str(float(self.line_lon.text()) + move_range[self.spin_zoom.value()]))
            self.run()
        if event.key() == Qt.Key_Left:
            self.line_lon.setText(str(float(self.line_lon.text()) - move_range[self.spin_zoom.value()]))
            self.run()
        if event.key() == Qt.Key_Up:
            self.line_lat.setText(str(float(self.line_lat.text()) + move_range[self.spin_zoom.value()] / 2))
            self.run()
        if event.key() == Qt.Key_Down:
            self.line_lat.setText(str(float(self.line_lat.text()) - move_range[self.spin_zoom.value()] / 2))
            self.run()

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
