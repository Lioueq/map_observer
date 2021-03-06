import sys
import requests
import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow


move_range = {1: 2, 2: 1.5, 3: 1, 4: 1, 5: 0.9, 6: 0.9, 7: 0.5, 8: 0.5, 9: 0.1, 10: 0.1, 11: 0.09,  # ренж мува по карте
              12: 0.05, 13: 0.01, 14: 0.01, 15: 0.009, 16: 0.005, 17: 0.001, 18: 0.001, 19: 0.0005}
maps = {1: 'map', 2: 'sat', 3: 'sat,skl'}  # режим карты
pt = None  # метка


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.status = 1
        self.initui()
        self.run()

    def initui(self):
        self.setupUi(self)
        self.setWindowTitle('Map_observer')
        self.btn_run.clicked.connect(self.run)
        self.btn_change_map.clicked.connect(self.change_map)
        self.btn_search.clicked.connect(self.search)

    def getImage(self):  # получение карты местности
        map_request = self.url_creator(1)
        print(map_request)
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def url_creator(self, mode):  # создание ссылок
        if mode == 1:  # по координатам
            api_server = 'http://static-maps.yandex.ru/1.x/'
            lon, lat, zoom = self.line_lon.text(), self.line_lat.text(), self.spin_zoom.value()
            if pt:
                params = {
                    "ll": ",".join([lon, lat]),
                    "z": zoom,
                    "l": maps[self.status],
                    'pt': pt
                }
            else:
                params = {
                    "ll": ",".join([lon, lat]),
                    "z": zoom,
                    "l": maps[self.status]
                }
            return requests.get(api_server, params=params).url
        elif mode == 2:  # по названию
            api_server = 'https://search-maps.yandex.ru/v1/'
            lon, lat = self.line_lon.text(), self.line_lat.text()
            search = self.line_search.text()
            params = {
                "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
                'text': search,
                'lang': 'ru_RU',
                "ll": ",".join([lon, lat])
            }
            return requests.get(api_server, params=params).url

    def run(self):  # поиск по координатам
        try:
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.label_map.setPixmap(self.pixmap)
        except Exception as e:
            self.label_error_msg.setText(f'Произошла ошибка {e.__class__.__name__}')

    def change_map(self):  # режим карты
        if self.status + 1 > 3:
            self.status = 1
        else:
            self.status += 1
        self.run()

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
            if float(self.line_lon.text()) + move_range[self.spin_zoom.value()] <= 180:
                self.line_lon.setText(str(float(self.line_lon.text()) + move_range[self.spin_zoom.value()]))
                self.run()
        if event.key() == Qt.Key_Left:
            if float(self.line_lon.text()) - move_range[self.spin_zoom.value()] >= -180:
                self.line_lon.setText(str(float(self.line_lon.text()) - move_range[self.spin_zoom.value()]))
                self.run()
        if event.key() == Qt.Key_Up:
            if float(self.line_lat.text()) + move_range[self.spin_zoom.value()] <= 90:
                self.line_lat.setText(str(float(self.line_lat.text()) + move_range[self.spin_zoom.value()] / 2))
                self.run()
        if event.key() == Qt.Key_Down:
            if float(self.line_lat.text()) - move_range[self.spin_zoom.value()] >= -90:
                self.line_lat.setText(str(float(self.line_lat.text()) - move_range[self.spin_zoom.value()] / 2))
                self.run()

    def search(self):  # поиск по названию
        global pt
        map_request = self.url_creator(2)
        print(map_request)
        response = requests.get(map_request).json()
        print(response)
        lon, lat = response['features'][0]['geometry']['coordinates']
        pt = f'{str(lon)},{str(lat)}'
        self.line_lon.setText(str(lon)), self.line_lat.setText(str(lat))
        self.run()

    def closeEvent(self, event):  # закрытие
        try:
            os.remove(self.map_file)
        except AttributeError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
