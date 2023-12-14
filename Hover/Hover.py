import sys
from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QLabel, QVBoxLayout, QToolTip
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint


class HoverDetailWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Hover Detail Widget')

        self.main_layout = QVBoxLayout(self)

        # Add image
        self.image_label = QLabel(self)
        pixmap = QPixmap('Hover/screen.jpg')  # Replace with the path to your image

        # Resize the pixmap to a custom size (e.g., 200x200)
        pixmap = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
        
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMouseTracking(True)  # Enable mouse tracking for the image label
        self.main_layout.addWidget(self.image_label)

        # Add label for mouse coordinates
        self.label = QLabel(self)
        self.main_layout.addWidget(self.label)

        self.card_widget = CardWidget(self)
        self.card_widget.hide()

        self.setLayout(self.main_layout)

        self.setMouseTracking(True)  # Enable mouse tracking for hover events

    def mouseMoveEvent(self, event):
        x_global, y_global = event.globalX(), event.globalY()
        pos_relative_to_image = self.image_label.mapFromGlobal(QPoint(x_global, y_global))
        x_relative, y_relative = pos_relative_to_image.x(), pos_relative_to_image.y()

        self.label.setText(f'Mouse Hovering at Image: ({x_relative}, {y_relative})')
        self.label.setAlignment(Qt.AlignCenter)

        self.show_tooltip(f'Mouse Hovering at Image: ({x_relative}, {y_relative})')
        self.show_card(f'({x_relative}, {y_relative})', x_relative + 25, y_relative + 10)

    def show_card(self, text, x, y):
        self.card_widget.set_text(text)
        self.card_widget.move(x, y)
        self.card_widget.show()

    def show_tooltip(self, text):
        QToolTip.showText(self.mapToGlobal(QPoint(0, 0)), text)

    def eventFilter(self, obj, event):
        if obj == self.image_label and event.type() == Qt.QEvent.MouseMove:
            x, y = event.x(), event.y()
            self.label.setText(f'Mouse Hovering at Image: ({x}, {y})')
            self.label.setAlignment(Qt.AlignCenter)
        return super().eventFilter(obj, event)

class CardWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #ffffff")
        self.setFixedSize(150, 50)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

    def set_text(self, text):
        self.label.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    hover_widget = HoverDetailWidget()
    hover_widget.show()
    sys.exit(app.exec_())
