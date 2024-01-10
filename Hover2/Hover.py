import sys
from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, pyqtSlot


class HoverWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 300, 150)
        self.setWindowTitle('Hover Detail Widget')
        self.layout = QVBoxLayout(self)

        self.mouse_tracking_zone = QLabel(self)
        self.mouse_tracking_zone.setMouseTracking(True)  # Enable mouse tracking for the image label
        self.layout.addWidget(self.mouse_tracking_zone)

        self.setStyleSheet('''
    QWidget {
        background-color        : #FFF;
    }
    QLabel {
        background-color        : #EDF0F6;
        border-radius           : 15px;
        border                  : 0px;
    }''')

        self.card_widget = CardWidget(self)
        self.card_widget.hide()

        self.setLayout(self.layout)

        self.setMouseTracking(True)  # Enable mouse tracking for hover events

    def mouseMoveEvent(self, event):
        x_global, y_global = event.globalX(), event.globalY()
        pos_relative_to_image = self.mouse_tracking_zone.mapFromGlobal(QPoint(x_global, y_global))
        x_relative, y_relative = pos_relative_to_image.x(), pos_relative_to_image.y()

        self.card_widget.show_card(x_relative + 20, y_relative + 15)


class CardWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(150, 50)

        self.label = QLabel(self)
        self.label.setText('What is this?')
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.setStyleSheet('''
    QFrame {
        background-color        : transparent;
    }
    QLabel {
        border-radius           : 15px;
        border-top-left-radius  : 0px;
        border                  : 0px;
        background-color        : #FFF;
        color                   : #4A535F;
        font                    : 63 10pt "Montserrat Medium";
    }''')

    def set_text(self, text):
        self.label.setText(text)
    
    @pyqtSlot(int, int)
    def show_card(self, x:int, y:int):
        self.move(x, y)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    hover_widget = HoverWidget()
    hover_widget.show()
    sys.exit(app.exec_())
