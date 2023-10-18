# -*- coding: utf-8 -*-
import typing
from PyQt5 import QtCore, QtGui, QtWidgets

class Style:
    def __init__(self) -> None:

        self.IDLE = ("QProgressBar {\n"
"background-color: #F8F9FB;\n"
"border: 1px solid #EDF0F6; color: #B5BFC6; \n"
"border-radius: 16px;\n"
"text-align: center; \n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"background-color: #F8F9FB;\n"
"border-radius: 14px;\n"
"}")

        self.PROCESS = ("QProgressBar {\n"
"background-color: #FFF;\n"
"border: 1px solid #4487EB; color: #4487EB; \n"
"border-radius: 16px;\n"
"text-align: center; \n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"background-color: #DAE7FB;\n"
"border-radius: 14px;\n"
"}")

        self.DONE = ("QProgressBar {\n"
"background-color: #DDF7E3;\n"
"border: 1px solid #04B56E; color: #04B56E; \n"
"border-radius: 16px;\n"
"text-align: center; \n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"background-color: #DDF7E3;\n"
"border-radius: 14px;\n"
"}")

class CustomProgressBar(QtWidgets.QProgressBar):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None: 
        super(QtWidgets.QProgressBar, self).__init__(parent)

        self.STYLE = Style()

        self.setupUi()

    def setupUi(self):

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(200, 40))

        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)

        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))

        self.setStyleSheet( self.STYLE.IDLE )
        
        # self.setMinimum(0)
        # self.setMaximum(80)
        self.setProperty("value", 0)

        self.setInvertedAppearance(False)
        self.setObjectName("progressBar")
    
    def setStatus(self,
        current :int = None,
        maximum :int = None,
        text    :str = None,
    ):
        if current is not None: self.setProperty("value", current)
        if maximum is not None: self.setMaximum(maximum)

        if self.value() == 0:                       # IDLE State
            self.setStyleSheet( self.STYLE.IDLE )
            self.setFormat("Idle" if text is None else text)
        
        elif self.value() == self.maximum():        # DONE State
            self.setStyleSheet( self.STYLE.DONE )
            self.setFormat("Done" if text is None else text)
        
        else:                                       # IN PROGRESS State
            self.setStyleSheet( self.STYLE.PROCESS )
            self.setFormat(f"Processing... (%v / {self.maximum()})" if text is None else text)


if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    
    window = QtWidgets.QWidget()
    window.setStyleSheet("QWidget {background-color: #FFF;}")

    layout = QtWidgets.QVBoxLayout(window)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(12)
    layout.setObjectName("layout")

    #TUTORIAL ######################################
    progressbar1 = CustomProgressBar(window)
    progressbar1.setStatus(
        current=0, maximum=20, text='Waiting'
    )

    progressbar2 = CustomProgressBar(window)
    progressbar2.setStatus(
        current=15, maximum=20
    )

    progressbar3 = CustomProgressBar(window)
    progressbar3.setStatus(
        current=20, maximum=20
    )

    layout.addWidget(progressbar1)
    layout.addWidget(progressbar2)
    layout.addWidget(progressbar3)
    ################################################

    window.show()
    app.exec_()