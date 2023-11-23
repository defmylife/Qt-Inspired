# -*- coding: utf-8 -*-
import typing
from PyQt5 import QtCore, QtGui, QtWidgets

class SearchBar(QtWidgets.QLineEdit):
    searchText = QtCore.pyqtSignal(str)

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None: 
        super(QtWidgets.QLineEdit, self).__init__(parent)

        # self.STYLE = Style()

        self.setupUi()

    def setupUi(self):

        self.setObjectName("searchBar")
        self.setPlaceholderText("Search here")

        self.returnPressed.connect(lambda: self.searchText.emit(self.text()) )

        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)

        self.setStyleSheet("#Form {\n"
"    /*font: 11pt \"Montserrat Medium\";\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 16px;\n"
"    border: 1px solid #EDF0F6;*/\n"
"    background-color:  #FFF;\n"
"}\n"
"/*#searchWidget:focus {\n"
"    border: 1px solid #4487EB;\n"
"}*/\n"
"\n"
"#searchBar{\n"
"    font: 11pt \"Montserrat Medium\";\n"
"    border-radius: 16px;\n"
"    border: 1px solid #EDF0F6;\n"
"    background-color: #F8F9FB;\n"
"    padding-left: 46 px;\n"
"    color: #4487EB;\n"
"}\n"
"#searchBar:focus {\n"
"    border: 1px solid #4487EB;\n"
"}\n"
"\n"
"#searchBtn{\n"
"    border-radius: 13px;\n"
"    background: transparent;\n"
"}\n"
"#searchBtn:hover{\n"
"    background: #EDF0F6;\n"
"}")
        
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.setMinimumSize(QtCore.QSize(0, 50))

        ######## BUTTON ########

        self.searchBtn = QtWidgets.QPushButton(self)

        self.searchBtn.clicked.connect(lambda: self.searchText.emit(self.text()) )

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchBtn.sizePolicy().hasHeightForWidth())
        self.searchBtn.setSizePolicy(sizePolicy)
        self.searchBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.searchBtn.setText("")
        self.searchBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("SearchBar/searchBtn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.searchBtn.setIcon(icon)
        self.searchBtn.setObjectName("searchBtn")
        self.searchBtn.move(5, 5)


if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    
    window = QtWidgets.QWidget()
    window.setStyleSheet("QWidget {background-color: #FFF;}")

    layout = QtWidgets.QVBoxLayout(window)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(12)
    layout.setObjectName("layout")

    #TUTORIAL ######################################
    searchBar = SearchBar(window)

    searchBar.searchText.connect(print)
    # searchBar.searchText.connect( ...ADD YOUR SLOT FUNCTION HERE... )

    layout.addWidget(searchBar)
    ################################################

    window.show()
    app.exec_()