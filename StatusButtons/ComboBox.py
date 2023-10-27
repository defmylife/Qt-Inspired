# -*- coding: utf-8 -*-
import typing
from PyQt5 import QtCore, QtGui, QtWidgets

class CustomComboBox(QtWidgets.QWidget):
    activated = QtCore.pyqtSignal(str)
    
    def __init__(self, 
        parent: typing.Optional[QtWidgets.QWidget] = ...,
        init: str = "No Connection"
    ) -> None: 
        super(QtWidgets.QWidget, self).__init__(parent)

        self.DOT_STYLE = ("QWidget {\n"
            "border-radius: 6px;\n"
            "background-color: {OPTION};\n"
            "}")

        self.setupUi(init)

    def setupUi(self, initial_text: str = "No Connection"):

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(0, 30))

        self.setStyleSheet("QComboBox {\n"
"background-color: #FFF;\n"
"color: #B5BFC6; \n"
"border-radius: 14px;\n"
"text-align: center; \n"
"\n"
"selection-background-color: #FFF; /*ECECEC*/\n"
"selection-color: #0F5BCD;\n"
"outline: 0;\n"
"padding-left: 8px;\n"
"}\n"
"QComboBox:hover {\n"
"    background-color: #F8F9FB; \n"
"}\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    color: #B5BFC6\n"
"}\n"
"QComboBox::drop-down {\n"
"border: 0px;\n"
"padding-right: 5px;\n"
"}\n"
"QComboBox::down-arrow {\n"
"/* image: url(:/icons/icons/edit.png); width: 16px; height: 16px; */\n"
"}\n"
"\n"
"QComboBox QListView {\n"
"background-color: #F8F9FB;\n"
"color: #B5BFC6; \n"
"border-radius: 8px;\n"
"padding: 5px; margin-top: 5px;\n"
"outline: 1px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    selection-background-color: #EDF0F6;\n"
"    selection-color: #4487EB;\n"
"}\n"
"\n")
        self.setObjectName("comboBoxFrame")

        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))

        #########################
        #         Layout        #
        #########################
        self.__layout = QtWidgets.QHBoxLayout(self)
        self.__layout.setContentsMargins(12, 0, 0, 0)
        self.__layout.setSpacing(4)
        self.__layout.setObjectName("layout")

        #########################
        #       Status Dot      #
        #########################
        self.__dot = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.__dot.sizePolicy().hasHeightForWidth())
        self.__dot.setSizePolicy(sizePolicy)
        self.__dot.setMinimumSize(QtCore.QSize(12, 12))
        self.__dot.setMaximumSize(QtCore.QSize(12, 12))
        self.__dot.setObjectName("dot")
        self.__layout.addWidget(self.__dot)
        self.setStatusIdle()
    
        #########################
        #        ComboBox       #
        #########################
        self.comboBox = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))

        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.comboBox.setFont(font)

        self.comboBox.addItem(initial_text)
        self.comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox.setObjectName("comboBox")
        self.__layout.addWidget(self.comboBox)
    
    def setStatusIdle(self) -> None: self.__dot.setStyleSheet( 
            self.DOT_STYLE.replace('{OPTION}', '#B5BFC6') 
        )
    def setStatusConnected(self) -> None: self.__dot.setStyleSheet( 
            self.DOT_STYLE.replace('{OPTION}', '#04B56E') 
        )
    def setStatusConnecting(self) -> None: self.__dot.setStyleSheet( 
            self.DOT_STYLE.replace('{OPTION}', '#F99500') 
        )
    def setStatusDisconnected(self) -> None: self.__dot.setStyleSheet( 
            self.DOT_STYLE.replace('{OPTION}', '#F25858') 
        )


    def addItem(self, text: str, userData: typing.Any = ...) -> None: 
        self.comboBox.addItem(text, userData)
    def addItems(self, texts: typing.Iterable[str]) -> None:
        self.comboBox.addItems(texts)
    def clear(self) -> None: 
        self.comboBox.clear()


if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    
    window = QtWidgets.QWidget()
    window.setStyleSheet("QWidget {background-color: #FFF;}")

    layout = QtWidgets.QHBoxLayout(window)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(12)
    layout.setObjectName("layout")

    #TUTORIAL ######################################
    statusBox1 = CustomComboBox(window)

    statusBox1.addItem("Connection A")
    statusBox1.addItems(
        ["Connection B", "Connection C"])
    
    statusBox1.comboBox.activated.connect(print) # Print the index after comboBox get clicked

    statusBox2 = CustomComboBox(window, init="Connecting")
    statusBox2.setStatusConnecting()

    statusBox3 = CustomComboBox(window, init="Connected")
    statusBox3.setStatusConnected()

    statusBox4 = CustomComboBox(window, init="Error")
    statusBox4.setStatusDisconnected()

    layout.addWidget(statusBox1)
    layout.addWidget(statusBox2)
    layout.addWidget(statusBox3)
    layout.addWidget(statusBox4)
    window.update()
    ################################################

    spacer = QtWidgets.QSpacerItem(261, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
    layout.addItem(spacer)
    window.show()
    app.exec_()