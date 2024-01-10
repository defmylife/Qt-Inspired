import sys
from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PIL import Image
import numpy as np, cv2

class HoverWidget(QWidget):
    def __init__(self, parent, x, y, w, h, background_image, label):
        super().__init__(parent)

        self.setGeometry(x, y, w, h)
        self.setParent(parent)
        self.layout = QVBoxLayout(self)

        self.mouse_tracking_zone = QLabel(self)
        self.mouse_tracking_zone.setMouseTracking(True)
        self.layout.addWidget(self.mouse_tracking_zone)

        self.setStyleSheet('''
    QWidget {
        background-color        : transparent;
    }
    QLabel {
        background-color        : transparent;
        border-radius           : 4px;
        border                  : 1px solid #FFF;
    }
    QLabel:hover {
        background-color        : rgba(255, 255, 255, 50);;
    }''')

        self.card_widget = CardWidget(parent, x, y, w, h, background_image, label)
        self.card_widget.hide()

        self.setLayout(self.layout)

        self.setMouseTracking(True)
        # self.move(x, y)

    def enterEvent(self, event):
        self.card_widget.show()

    # def leaveEvent(self, event):
    #     self.card_widget.hide()


class CardWidget(QFrame):
    def __init__(self, parent, x, y, w, h, background_image, label):
        super().__init__(parent)

        scale = 1.2

        self.image = QLabel(self)
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setFixedSize(
            int(w*scale), 
            int(h*scale)
        )

        self.label = QLabel(self)
        self.label.setText(label)
        self.label.setAlignment(Qt.AlignCenter)

        margin = 2

        layout = QVBoxLayout(self)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(0)
        layout.addWidget(self.image)
        layout.addWidget(self.label)

        self.move(
            x - int(w*(scale-1)/2), 
            y - int(h*(scale-1)/2), 
            )
        # self.setFixedSize(w, h)

        # Set background image for HoverWidget
        self.set_background_image(background_image, (x, y, x+w, y+h))

        self.setStyleSheet('''
    QFrame {
        border-radius           : 4px;
        border                  : 0px;
        background-color        : #FFF;
    }
    QLabel {
        border-radius           : 0px;
        border                  : 0px;
        background-color        : #FFF;
        color                   : #4A535F;
        font                    : 63 10pt "Montserrat Medium";
        padding                 : 2px;
    }''')
        self.setLayout(layout)

    def set_background_image(self, background_image, crop_coords):
        img = background_image.crop(crop_coords)
        img = img.resize((self.image.width(), self.image.height()))
        # img.save("geeks.jpg")

        img = np.array(img)
        print(img.shape, self.image.width(), self.image.height())
        # Crop image 
        # x1, y1, x2, y2 = crop_coords
        # img = img[y1:y2, x1:x2] 
        # cv2.imwrite("filename.png", img)

        q_img = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        pixmap = pixmap.scaled(self.image.size(), Qt.IgnoreAspectRatio)
        self.image.setPixmap(pixmap)

    def leaveEvent(self, event):
        self.hide()


class MainWindow(QWidget):
    def __init__(self, w=640, h=480):
        super().__init__()

        self.setGeometry(100, 100, w, h)  # Set fixed resolution
        self.setFixedSize(w, h)
        self.setWindowTitle('Main Window')
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Set background image
        background_image_path = 'Hover2/image1.jpg'
        background_image = Image.open(background_image_path)
        background_image = background_image.resize((w, h))

        background_label = QLabel(self)
        pixmap = QPixmap(background_image_path) 
        pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio)
        background_label.setPixmap(pixmap)
        background_label.setAlignment(Qt.AlignCenter)
        background_label.setGeometry(0, 0, w, h)  # Set fixed resolution
        background_label.setFixedSize(w, h)

        # Create multiple HoverWidget instances with different absolute positions
        hover_widget1 = HoverWidget(background_label,  45,  85, 155, 155, background_image, 'Tool #0')
        hover_widget2 = HoverWidget(background_label, 200, 250, 100, 100, background_image, 'Tool #1')
        hover_widget3 = HoverWidget(background_label, 310, 340, 130, 130, background_image, 'Tool #2')

        self.layout.addWidget(background_label, 0, Qt.AlignTop)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
