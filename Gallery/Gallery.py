import sys, os
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QCursor
from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QRadioButton, QButtonGroup, QSizePolicy, QSpacerItem

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
        self.buttonFrame = QFrame()
        self.buttonFrame.setFixedWidth(155)
        self.buttonFrame.setLayout(vbox)
        self.buttonFrame.setStyleSheet("background-color: #EDF0F6; border-radius: 16px; margin: 12px;")

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
        mainLayout.addWidget(self.buttonFrame)

        # Set the main layout to the window
        self.setLayout(mainLayout)
        self.setWindowTitle('Gallery App')

        self.additionalUI()
        self.resize(700, 400)

    def additionalUI(self):
        # Add drop button
        self.dropButton = QPushButton(self)
        self.dropButton.setStyleSheet("""
            QPushButton {
                background-color: #EDF0F6;
                border-radius: 12px;
                padding: 12px;
                image: url(:/Gallery/bin.png);
            }
            QPushButton:hover {
                background-color: #F25858;
                border-radius: 12px;
                padding: 12px;
                image: url(:/Gallery/bin-activated.png);
            }
        """.replace(':/Gallery', os.path.dirname(__file__).replace('\\','/')))
        
        self.dropButton.setToolTip('Delete image')
        self.dropButton.setFixedSize(42, 42)
        self.dropButton.clicked.connect(lambda: self.drop(self.stackedWidget.currentIndex()))

        self.dropButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.dropButton.raise_()

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

    def drop(self, index :int):
        if 0 <= index < len(self.image_paths):
            # Remove the image path from the list
            self.image_paths.pop(index)
            
            # Remove the widget from the stacked widget
            widget = self.stackedWidget.widget(index)
            self.stackedWidget.removeWidget(widget)
            widget.deleteLater()
            
            # Remove the corresponding radio button
            button = self.buttonGroup.buttons()[index]
            self.buttonGroup.removeButton(button)
            self.buttonLayout.removeWidget(button)
            button.deleteLater()
            
            # Update the remaining buttons' click connections
            for i, button in enumerate(self.buttonGroup.buttons()):
                button.clicked.disconnect()
                button.clicked.connect(lambda _, x=i: self.stackedWidget.setCurrentIndex(x))
                
            # Set the first radio button checked by default if any remain
            if self.buttonGroup.buttons():
                self.buttonGroup.buttons()[index if index<len(self.buttonGroup.buttons()) else -1].setChecked(True)

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

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Position the drop button at the top-right corner of the stacked widget
        widgetPos = self.stackedWidget.mapToParent(self.stackedWidget.rect().topRight())
        newPos = widgetPos - self.dropButton.rect().topRight()
        self.dropButton.move(newPos.x() + 6, newPos.y() + 18)


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

    # Drop an image
    # galleryApp.drop(2)  # This will remove the third image (index 2)

    sys.exit(app.exec_())