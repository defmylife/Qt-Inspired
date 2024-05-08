from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, pyqtSlot

import sys, os
DIR = os.path.dirname(os.path.realpath(__file__))

class RotatedWidget(QtWidgets.QGraphicsProxyWidget):
    hovered_pos = pyqtSignal(int, int, str) # (global_x, global_y, description)

    def __init__(self,
            x :int,     # center x
            y :int,     # center y
            w :int,
            h :int,
            r :int = 0, # rotation (deg.)
            description :str = '',

        parent=None) -> None:
        super().__init__(parent)
        self.desc = description
        # self.setStyleSheet('''
        # QWidget {background-color: transparent;}
        # ''')

        label = QtWidgets.QLabel()
        label.setGeometry(x, y, w, h)
        label.setStyleSheet('''
        QLabel {
            margin: 2px;
            background-color: transparent;
            border: 1px solid rgb(255,255,255),
        }
        QLabel::hover {
            background-color: rgba(255,255,255,100);
            border: 2px solid rgb(255,255,255),
        }
        ''')
        self.setWidget(label)

        self.setPos(x - w//2, y - h//2)
        self.setTransformOriginPoint(self.boundingRect().center())
        self.setRotation(r)

    def hoverMoveEvent(self, event):
        # Get the mouse cursor position relative to the proxy widget
        mouse_pos_relative = event.pos()
        # Convert relative position to scene coordinates
        mouse_pos_scene = self.mapToScene(mouse_pos_relative)

        self.hovered_pos.emit(int(mouse_pos_scene.x()), int(mouse_pos_scene.y()), self.desc)
        super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event):
        # Handle leave event 
        self.hovered_pos.emit(-1, -1, self.desc)
        super().hoverLeaveEvent(event)


class CardWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(150, 60)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        layout = QtWidgets.QVBoxLayout(self)

        self.desc = QtWidgets.QLabel(self)
        self.desc.setStyleSheet('''
        QLabel {
            border-radius           : 2px;
            border-top-left-radius  : 0px;
            border                  : 0px;
            background-color        : #FFF;
            color                   : #4A535F;
            font                    : 63 10pt "Montserrat Medium";
            padding                 : 2px;
        }''')
        layout.addWidget(self.desc)

        self.pos_label = QtWidgets.QLabel(self)
        self.pos_label.setStyleSheet('''
        QLabel {
            border-radius           : 2px;
            border-top-left-radius  : 0px;
            border                  : 0px;
            background-color        : transparent;
            color                   : #4A535F;
            font                    : 63 10pt "Montserrat Medium";
            padding                 : 1px;
        }''')
        layout.addWidget(self.pos_label)
    
    @pyqtSlot(int, int, str)
    def show_card(self, x:int, y:int, desc:str):
        if x>=0 and y>=0:
            self.desc.setText(desc)
            self.pos_label.setText(str((x, y)))
            self.move(x + 0, y - 32)
            self.show()

        else: # x = -1, y = -1
            self.hide()


class Window(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Create a background pixmap
        # 
        # Reference image from https://www.aviva.com/newsroom/news-releases/2023/09/the-15-minutes-of-the-day-you-are-most-likely-to-have-a-car-collision/
        # 
        background_pixmap = QtGui.QPixmap(os.path.join(DIR, "traffic.png"))
        desired_size = QtCore.QSize(1000, 640)  
        background_pixmap = background_pixmap.scaled(desired_size, QtCore.Qt.IgnoreAspectRatio)
        background_brush = QtGui.QBrush(background_pixmap)

        self.graphicsview = QtWidgets.QGraphicsView()
        self.graphicsview.setFixedSize(desired_size.width(), desired_size.height())
        self.scene = QtWidgets.QGraphicsScene(self.graphicsview)
        self.graphicsview.setScene(self.scene)

        # Set the background brush for the scene
        self.scene.setBackgroundBrush(background_brush)
        self.scene.setSceneRect(0, 0, desired_size.width()-2, desired_size.height()-2)

        # Align the scene both horizontally and vertically within the view
        self.graphicsview.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.graphicsview)
        self.setFixedSize(desired_size)
        self.show()

        self.card_widget = CardWidget(self)
        self.card_widget.hide()
    
    def addSceneWidget(self, widget :RotatedWidget) -> None:
        self.scene.addItem(widget)
        widget.hovered_pos.connect(self.card_widget.show_card)
    

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setOverrideCursor(Qt.CrossCursor) 
    window = Window()

    window.addSceneWidget(
        RotatedWidget(
            x=350,
            y=225,
            w=180,
            h=80,
            r=-11,
            description='White Van Id-001'
        )
    )
    window.addSceneWidget(
        RotatedWidget(
            x=550,
            y=175,
            w=175,
            h=75,
            r=-8,
            description='White Car Id-002'
        )
    )
    window.addSceneWidget(
        RotatedWidget(
            x=680,
            y=282,
            w=180,
            h=75,
            r=-5,
            description='Black Car Id-001'
        )
    )
    window.addSceneWidget(
        RotatedWidget(
            x=775,
            y=175,
            w=180,
            h=75,
            r=-6,
            description='Black Van Id-001'
        )
    )
    window.addSceneWidget(
        RotatedWidget(
            x=90,
            y=330,
            w=310,
            h=130,
            r=-9,
            description='Yellow Bus Id-001'
        )
    )
    window.addSceneWidget(
        RotatedWidget(
            x=412,
            y=436,
            w=450,
            h=120,
            r=-5,
            description='Yellow Bus Id-002'
        )
    )

    sys.exit(app.exec_())