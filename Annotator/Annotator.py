import sys, math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QStyleOption, QStyle
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QCursor, QPixmap, QPainter

class Popup(QWidget):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setFixedSize(180, 40)
        self.setStyleSheet("background-color: white; border-radius: 16px;")

        self.currentPos = tuple()

        self.label = QLabel(self)
        self.label.setStyleSheet("margin: 8px; font-size: 10pt;")
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.hide()
    
    def show(self, text: str, pos :QPoint) -> None:
        self.label.setText(text)

        offset_x = 30
        offset_y = -20

        if self.parentWidget().width() - pos.x() < self.width() + offset_x:
            offset_x = -self.width() -offset_x +20 # 20 is AnnotatedPoint size

        newPos = (pos.x() + offset_x, pos.y() + offset_y)

        if self.isHidden() or self.currentPos != newPos:
            # print('show popup...')
            self.currentPos = newPos
        
            self.move(self.currentPos[0], self.currentPos[1])
            self.raise_()
            super().show()

        else: self.hide()

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
    clickedInfo = pyqtSignal(str, QPoint)
    
    def __init__(self, parent: QWidget | None = ..., size: int = 20, margin: int = 2) -> None:
        super().__init__(parent)

        self.setStyleSheet(f"""\
        QWidget [
            background-color: green; 
            border-radius: {math.floor(size/2) - margin}px;
            margin: {margin}px;
        ]
        QWidget :hover [
            background-color: red; 
            border-radius: {math.floor(size/2)}px;
            margin: 0px;
        ]
        """.replace('[','{').replace(']','}'))

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.show()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.clickedInfo.emit(f'AnnotatedPoint {self.x(), self.y()}', self.pos())

            print("AnnotatedPoint clicked at:", self.pos())

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
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Click to create Annotator')
        self.setFixedSize(800, 600)

        # Option 1: Set a solid background color
        # self.setStyleSheet("background-color: lightblue;")
        
        # Option 2: Create QLabel and set the pixmap
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap('Annotator/traffic.png'))
        self.background_label.setFixedSize(800, 600)
        self.background_label.setScaledContents(True)  # Ensure the image scales to the size of the label
        
        self.popUpWidget = Popup(self)

        # self._children = set()
        self.setCursor(QCursor(Qt.CrossCursor))
        self.show()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            clicked_widget = self.childAt(event.pos())
            
            if not isinstance(clicked_widget, Popup):
                self.createAnnotatedPoint(event.pos())

    def createAnnotatedPoint(self, position: QPoint):
        # annotated_point = QWidget(self)
        size = 20
        annotated_point = AnnotatedPoint(self, size=size)
        annotated_point.setGeometry(position.x() - size//2, position.y() - size//2, size, size)

        annotated_point.clickedInfo.connect(self.popUpWidget.show)

        print('AnnotatedPoint created at', position)
        annotated_point.show()

        # self.add
        # self._children.add(annotated_point)

def main():
    app = QApplication(sys.argv)
    window = Screen()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
