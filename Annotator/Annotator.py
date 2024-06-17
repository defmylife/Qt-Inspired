import sys, math, os, logging, shutil
from PyQt5.QtWidgets import QApplication, QStackedWidget, QWidget, QLabel, QStyleOption, QStyle, QHBoxLayout, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QObject, QPoint, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QCursor, QPixmap, QPainter, QIcon
from rich import print

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Popup(QWidget):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        # self.setFixedSize(180, 40)
        self.setStyleSheet("background-color: white; border-radius: 8px;")

        self.currentPos = tuple()
        self.is_activated = False

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setStyleSheet("margin: 0px;")
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.hide()

        # First page
        page1 = QWidget()
        page1_layout = QHBoxLayout()
        self.label = QLabel(page1)
        self.label.setStyleSheet("font-size: 10pt;")
        self.conf = QLabel(page1)
        self.conf.setStyleSheet("font-size: 9pt;")
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        page1_layout.addWidget(self.label)
        page1_layout.addWidget(self.conf)
        page1_layout.addItem(spacer)
        page1.setLayout(page1_layout)

        # Second page
        page2 = QWidget()
        page2_layout = QHBoxLayout()
        self.line_edit = QLineEdit(page2)
        self.line_edit.setStyleSheet("font-size: 10pt;")
        self.push_button = QPushButton("", page2)
        self.push_button.setFixedSize(24, 24)  # Adjust the size as needed
        self.push_button.setIcon(QIcon("Annotator/checkmark.png"))
        self.push_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                margin: 0px;
                padding: 0px;
            }
            QPushButton:hover {
                background: rgba(2, 188, 125, 50);
            }
        """)
        self.push_button.setToolTip('Submit')
        self.push_button.clicked.connect(self.submit)
        page2_layout.addWidget(self.line_edit)
        page2_layout.addWidget(self.push_button)
        page2.setLayout(page2_layout)

        # Third page
        page3 = QWidget()
        page3_layout = QHBoxLayout()
        self.finished_label = QLabel("Thank you for feedback :)", page3)
        self.finished_label.setStyleSheet("color: rgb(2, 188, 125); font-size: 9pt;")
        page3_layout.addWidget(self.finished_label)
        page3.setLayout(page3_layout)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(page1)
        self.stacked_widget.addWidget(page2)
        self.stacked_widget.addWidget(page3)

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
        self.hide()
    
    @pyqtSlot(str, QPoint, bool)
    def activate(self, text: str, pos :QPoint, is_done: bool) -> None:
        self.label.setText(text)
        self.line_edit.setText(text)
        self.activated_sender :AnnotatedPoint = self.sender()

        offset_x = 30
        offset_y = -20

        if self.parentWidget().width() - pos.x() < self.width() + offset_x:
            offset_x = -self.width() -offset_x +20 # 20 is AnnotatedPoint size

        newPos = (pos.x() + offset_x, pos.y() + offset_y)

        if is_done:
            self.stacked_widget.setCurrentIndex(2)
            super().show()

        elif not self.is_activated:
            # print('show popup...')
            self.currentPos = newPos
        
            self.move(self.currentPos[0], self.currentPos[1])
            self.raise_()
            self.line_edit.setFocus()
            self.is_activated = True
            self.stacked_widget.setCurrentIndex(1)
            super().show()

        else: 
            self.is_activated = False
            self.stacked_widget.setCurrentIndex(0)
            # self.hide()

    @pyqtSlot(str, float, QPoint, bool)
    def show(self, text: str, conf: float, pos :QPoint, is_done: bool) -> None:
        self.label.setText(text)
        self.line_edit.setText(text)
        self.conf.setText(f' {conf * 100:.0f}%')
        if conf > 0.9:
            self.conf.setStyleSheet('color: rgb(2, 188, 125);')
        elif conf > 0.5:
            self.conf.setStyleSheet('color: orange;')
        else:
            self.conf.setStyleSheet('color: red;')

        offset_x = 30
        offset_y = -20

        if self.parentWidget().width() - pos.x() < self.width() + offset_x:
            offset_x = -self.width() -offset_x +20 # 20 is AnnotatedPoint size

        newPos = (pos.x() + offset_x, pos.y() + offset_y)

        if self.isHidden() or self.currentPos != newPos:
            self.currentPos = newPos
        
            self.move(self.currentPos[0], self.currentPos[1])
            self.raise_()
            self.is_activated = False
            self.stacked_widget.setCurrentIndex(0)
            if is_done:
                self.label.setStyleSheet('color: rgb(2, 188, 125); font-size: 10pt;')
            else:
                self.label.setStyleSheet('color: black; font-size: 10pt;')
            super().show()

        elif not self.is_activated: 
            self.hide()
    
    def submit(self):
        print('Submit')
        self.activated_sender.is_done = True
        self.activated_sender.is_done = True

        self.stacked_widget.setCurrentIndex(2)

    def paintEvent(self, event):
        '''Accoriding to this Qt Wiki article:
        https://wiki.qt.io/How_to_Change_the_Background_Color_of_QWidget
        
        you must implement paintEvent in a custom QWidget subclass in order to use stylesheets.'''
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)
        super().paintEvent(event)

class AnnotatedPoint(QWidget):
    clickedInfo = pyqtSignal(str, QPoint, bool)
    hoveredInfo = pyqtSignal(str, float, QPoint, bool)
    
    def __init__(self, parent: QWidget | None, 
            classname: str, 
            conf: float, 
            size: int = 20, 
            pos :QPoint = None, 
            image_path: str = '',
            margin: int = 2,
        ) -> None:
        super().__init__(parent)

        self.is_done = False
        self.classname = classname
        self.conf = conf
        self.position = pos
        self.image_path = image_path
        self.setStyleSheet(f"""\
        QWidget [
            background-color: red; 
            border-radius: {math.floor(size/2) - margin}px;
            margin: {margin}px;
        ]
        QWidget :hover [
            background-color: yellow; 
            border-radius: {math.floor(size/2)}px;
            margin: 0px;
        ]
        """.replace('[','{').replace(']','}'))

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.show()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.clickedInfo.emit(self.classname, self.pos(), self.is_done)

            print("AnnotatedPoint clicked at:", self.pos())

    def enterEvent(self, event):
        self.hoveredInfo.emit(self.classname, self.conf, self.pos(), self.is_done)
        print("AnnotatedPoint hovered at:", self.pos())

    def leaveEvent(self, event):
        self.hoveredInfo.emit(self.classname, self.conf, self.pos(), self.is_done)
        print("AnnotatedPoint hovered at:", self.pos())

    def paintEvent(self, event):
        '''Accoriding to this Qt Wiki article:
        https://wiki.qt.io/How_to_Change_the_Background_Color_of_QWidget
        
        you must implement paintEvent in a custom QWidget subclass in order to use stylesheets.'''
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, option, painter, self)
        super().paintEvent(event)

class Screen(QWidget):
    def __init__(self, parent: QObject | None, 
            background_img: str,
            size: tuple = (1000, 640),
            saved_crop_paths_and_pos: list = [], # [('path_to_img', (center_x, center_y)), ...]
        ):
        super().__init__(parent)
        size = (int(size[0]), int(size[1]))
        self.setWindowTitle('Click to create Annotator')
        self.setFixedSize(size[0], size[1])
        self.setCreateMode(False)

        self.saved_crop_paths_and_pos = saved_crop_paths_and_pos

        # Option 1: Set a solid background color
        # self.setStyleSheet("background-color: lightblue;")
        
        # Option 2: Create QLabel and set the pixmap
        self.image_path = background_img
        pixmap = QPixmap(self.image_path)
        
        self.background_label = QLabel(self)
        self.background_label.setPixmap(pixmap.scaled(size[0], size[1])) # Qt.KeepAspectRatio
        self.background_label.setScaledContents(True)  # Ensure the image scales to the size of the label
        self.background_label.setAlignment(Qt.AlignCenter)
        
        self.popUpWidget = Popup(self)

        self.show()

    def setCreateMode(self, is_create_mode: bool): 
        self._CREATE_MODE = is_create_mode
        if self._CREATE_MODE: self.setCursor(QCursor(Qt.CrossCursor))
        else:                 self.setCursor(QCursor(Qt.ArrowCursor))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            clicked_widget = self.childAt(event.pos())
            
            if not isinstance(clicked_widget, Popup):

                if self._CREATE_MODE:
                    self.createAnnotatedPoint(event.pos(), classname='Classname')

    def createAnnotatedPoint(self, 
            position: QPoint | tuple,
            classname: str,
            conf: float = 1.0,
            image_path: str = '',
        ):
        # annotated_point = QWidget(self)
        size = 20 # size of point

        if isinstance(position, tuple): # change to QPoint
            x, y = position
            position = QPoint(int(x), int(y))
            
        annotated_point = AnnotatedPoint(self, classname=classname, conf=conf, size=size, pos=position, image_path=image_path)
        annotated_point.setGeometry(position.x() - size//2, position.y() - size//2, size, size)

        annotated_point.clickedInfo.connect(self.popUpWidget.activate)
        annotated_point.hoveredInfo.connect(self.popUpWidget.show)

        logging.debug('AnnotatedPoint created at', position)

        # self.add
        # self._children.add(annotated_point)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    parent = QWidget()

    window = Screen(parent,
        background_img='Annotator/traffic.png')
    window.setCreateMode(True)

    window.createAnnotatedPoint((355, 217), classname='White car', conf=0.99)
    window.createAnnotatedPoint((560, 171), classname='White car', conf=0.8)
    window.createAnnotatedPoint((688, 279), classname='Black car', conf=0.5)

    window.show()
    parent.show()
    sys.exit(app.exec_())
