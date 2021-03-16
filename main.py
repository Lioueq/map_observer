import sys
import requests
import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow

MOVE_RANGE = {1: 2, 2: 1.5, 3: 1, 4: 1, 5: 0.9, 6: 0.9, 7: 0.5, 8: 0.5, 9: 0.1, 10: 0.1, 11: 0.09,  # ренж мува по карте
              12: 0.05, 13: 0.01, 14: 0.01, 15: 0.009, 16: 0.005, 17: 0.001, 18: 0.001, 19: 0.0005}
MAPS = {1: 'map', 2: 'sat', 3: 'sat,skl'}  # режим карты
pt = None  # метка
index_vision = False  # просмотр индекса


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.status = 1
        self.initUi()
        self.run()

    def initUi(self):
        self.setupUi(self)
        self.setWindowTitle('Map_observer')
        self.btn_run.clicked.connect(self.run)
        self.btn_change_map.clicked.connect(self.change_map)
        self.btn_search.clicked.connect(self.search)
        self.btn_reset.clicked.connect(self.reset)
        self.btn_postal_code.clicked.connect(self.changer)

    def getImage(self):  # получение карты местности
        map_request = self.url_creator(1)
        print(map_request)
        response = requests.get(map_request)
        if not response:
            self.label_error_msg.setText("Http статус:", response.status_code, "(", response.reason, ")")
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
                    "l": MAPS[self.status],
                    'pt': pt
                }
            else:
                params = {
                    "ll": ",".join([lon, lat]),
                    "z": zoom,
                    "l": MAPS[self.status]
                }
            return requests.get(api_server, params=params).url
        elif mode == 2:  # по названию
            api_server = 'https://search-maps.yandex.ru/v1/'
            lon, lat = self.line_lon.text(), self.line_lat.text()
            search = self.line_search.text()
            if lon and lat:
                params = {
                    "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
                    'text': search,
                    'lang': 'ru_RU',
                    "ll": ",".join([lon, lat])
                }
            else:
                params = {
                    "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
                    'text': search,
                    'lang': 'ru_RU',
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
            if float(self.line_lon.text()) + MOVE_RANGE[self.spin_zoom.value()] <= 180:
                self.line_lon.setText(str(float(self.line_lon.text()) + MOVE_RANGE[self.spin_zoom.value()]))
                self.run()
        if event.key() == Qt.Key_Left:
            if float(self.line_lon.text()) - MOVE_RANGE[self.spin_zoom.value()] >= -180:
                self.line_lon.setText(str(float(self.line_lon.text()) - MOVE_RANGE[self.spin_zoom.value()]))
                self.run()
        if event.key() == Qt.Key_Up:
            if float(self.line_lat.text()) + MOVE_RANGE[self.spin_zoom.value()] <= 90:
                self.line_lat.setText(str(float(self.line_lat.text()) + MOVE_RANGE[self.spin_zoom.value()] / 2))
                self.run()
        if event.key() == Qt.Key_Down:
            if float(self.line_lat.text()) - MOVE_RANGE[self.spin_zoom.value()] >= -90:
                self.line_lat.setText(str(float(self.line_lat.text()) - MOVE_RANGE[self.spin_zoom.value()] / 2))
                self.run()

    def search(self):  # поиск по названию
        global pt
        try:
            map_request = self.url_creator(2)
            print(map_request)
            response = requests.get(map_request).json()
            print(response)
            lon, lat = response['features'][0]['geometry']['coordinates']
            pt = f'{str(lon)},{str(lat)}'
            if 'CompanyMetaData' in response['features'][0]['properties']:
                self.label_address.setText(response['features'][0]['properties']['CompanyMetaData']['address'])
            else:
                self.label_address.setText(response['features'][0]['properties']['GeocoderMetaData']['text'])
            self.line_lon.setText(str(lon)), self.line_lat.setText(str(lat))
            self.run()
            if index_vision:
                self.postal_code()
        except Exception as e:
            print(e)

    def reset(self):  # сброс
        global pt
        pt = None
        self.label_address.setText('')
        self.run()

    def postal_code(self):  # почтовый индекс
        try:
            geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                               f"geocode={self.label_address.text()}&format=json"
            response = requests.get(geocoder_request).json()
            print(response)
            if not response:
                self.label_error_msg.setText("Http статус:", response.status_code, "(", response.reason, ")")
                print("Ошибка выполнения запроса:")
                print(geocoder_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
            if 'postal_code' in \
                    response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
                        'GeocoderMetaData']['Address']:
                self.label_address.setText('Индекс: ' + response['response']['GeoObjectCollection']['featureMember'][0]
                ['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code'] + ', ' +
                                           self.label_address.text())
            else:
                self.label_address.setText('Индекс: не найден, ' + self.label_address.text())
        except Exception as e:
            print(e)

    def changer(self):  # кнопка показа индекса
        global index_vision
        if index_vision:
            index_vision = False
            if 'Индекс:' in self.label_address.text().split(', ')[0]:
                var = self.label_address.text().split(', ')
                print(var)
                del var[0]
                self.label_address.setText(', '.join(var))
        else:
            index_vision = True
            if pt:
                self.postal_code()
        print(index_vision)

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
