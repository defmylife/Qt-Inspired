import sys, os
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QRadioButton, QButtonGroup, QSizePolicy, QSpacerItem

class GalleryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.image_paths = []

        # Main layout
        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        self.setStyleSheet('background-color: white;')

        # Create QStackedWidget
        self.stackedWidget = QStackedWidget()

        # Create a frame and vertical layout for buttons and spacer
        vbox = QVBoxLayout()
        buttonFrame = QFrame()
        buttonFrame.setLayout(vbox)
        buttonFrame.setStyleSheet("background-color: #EDF0F6; border-radius: 16px; margin: 12px;")

        # Create buttons to change the stack index with image previews
        self.buttonLayout = QVBoxLayout()
        self.buttonGroup = QButtonGroup()

        # Add the button layout to the vertical box layout
        vbox.addLayout(self.buttonLayout)
        
        # Add a spacer item to the bottom of the vertical box layout
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer)

        # Add the stacked widget and buttons to the main layout
        mainLayout.addWidget(self.stackedWidget)
        mainLayout.addWidget(buttonFrame)

        # Set the main layout to the window
        self.setLayout(mainLayout)
        self.setWindowTitle('Gallery App')
        self.resize(600, 400)

    def add(self, image_path :str):
        if image_path not in self.image_paths:
            # Add image path to the list
            self.image_paths.append(image_path)

            # Add image to the stacked widget
            pixmap = QPixmap(image_path)
            label = QLabel()
            label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))
            label.setAlignment(Qt.AlignCenter)
            self.stackedWidget.addWidget(label)

            # Create a new radio button with the image preview
            radioButton = QRadioButton()
            radioButton.setIcon(QIcon(image_path))
            radioButton.setIconSize(QSize(75, 75))  # Adjust the size for the previews
            radioButton.setStyleSheet("""
            QRadioButton::indicator::unchecked {
                image: url(:/Gallery/radiobutton_unchecked.png);
            }
            QRadioButton::indicator::unchecked:hover {
                image: url(:/Gallery/radiobutton_hovered.png);
            }
            QRadioButton::indicator::checked {
                image: url(:/Gallery/radiobutton_checked.png);
            }
            """.replace(':/Gallery', os.path.dirname(__file__).replace('\\','/')))

            idx = len(self.image_paths) - 1
            radioButton.clicked.connect(lambda _, x=idx: self.stackedWidget.setCurrentIndex(x))

            self.buttonGroup.addButton(radioButton)
            self.buttonLayout.addWidget(radioButton)

            # Set the first radio button checked by default if it's the only one
            if idx == 0:
                radioButton.setChecked(True)

    def clear(self):
        # Clear the list of image paths
        self.image_paths.clear()
        
        # Clear the stacked widget
        while self.stackedWidget.count() > 0:
            widget = self.stackedWidget.widget(0)
            self.stackedWidget.removeWidget(widget)
            widget.deleteLater()

        # Clear the button group and layout
        for button in self.buttonGroup.buttons():
            self.buttonGroup.removeButton(button)
            self.buttonLayout.removeWidget(button)
            button.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    galleryApp = GalleryApp()
    galleryApp.show()

    # Test the add methods
    galleryApp.add('Gallery/1.jpg')
    galleryApp.add('Gallery/2.jpg')
    galleryApp.add('Gallery/3.jpg')
    galleryApp.add('Gallery/4.jpg')
    galleryApp.add('Gallery/5.jpg')

    sys.exit(app.exec_())