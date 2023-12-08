from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QToolButton, QMenu, QAction, QActionGroup, QCheckBox
import sys
import pandas as pd

class CustomQTableWidget(QTableWidget):
    def __init__(self, df, parent=None):
        super().__init__(parent)
        self.df = df
        self.current_sort_order = 'ascending'  # Initial sort order
        self.pandas_to_qtablewidget(self.df, _setup=True)

    def pandas_to_qtablewidget(self, df=None, _setup=False):
        if df is not None: self.df = df

        if _setup:
        
            # Set the number of rows and columns
            self.setRowCount(self.df.shape[0])
            self.setColumnCount(self.df.shape[1])

            # Set column headers
            self.setHorizontalHeaderLabels(self.df.columns)

            # Apply style
            style = """
            QWidget {
                background-color: rgb(255, 255, 255);
                font: 63 10pt "Montserrat SemiBold";
                color: #B5BFC6;
            }
            QHeaderView::section { 
                background-color:#FFF;  
                border: 0px;
                padding-left: 16px;
                padding-top: 6px; padding-bottom: 6px;
            }
            QTableWidget {
                font: 11pt "Montserrat";
                color: #4A535F;
                selection-background-color: #DAE7FB;
                selection-color: #4A535F;
                outline: 0;
                border: 0px;
            }
            QTableWidget::item {
                border-bottom: 1px solid #EDF0F6;
                padding-left: 16px;
                selection-background-color: #DAE7FB;
                outline: 0;
            }
            QScrollBar:vertical {
                border: none;
                background: #FFF;
                width: 12px;
                margin: 0px 3px 0px 3px;
                border-radius: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: #FFF;
                height: 12px;
                margin: 3px 0px 3px 0px;
                border-radius: 0px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {    
                background-color: #EDF0F6;
                min-height: 0px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover{    
                background-color: #B5BFC6;
            }
            QScrollBar::handle:vertical:pressed, QScrollBar::handle:horizontal:pressed {    
                background-color: #B5BFC6;
            }
            QScrollBar::sub-line:vertical, QScrollBar::sub-line:horizontal {
                border: none;
                background-color:#FFF;
                height: 15px; width: 15px;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:vertical, QScrollBar::add-line:horizontal {
                border: none;
                background-color: #FFF;
                height: 15px; width: 15px;
                border-bottom-left-radius: 7px;
                border-bottom-right-radius: 7px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            """
            self.setStyleSheet(style)

        # Populate the table with data
        for i in range(self.df.shape[0]):
            for j in range(self.df.shape[1]):
                item = QTableWidgetItem(str(self.df.iloc[i, j]))
                self.setItem(i, j, item)

    def create_sort_button(self, init_action='Patient_ID'):
        self.current_sort_action = init_action

        # Create Sort button
        sort_button = QToolButton()
        sort_button.setText("Sort by "+init_action)
        sort_button.setPopupMode(QToolButton.MenuButtonPopup)

        sort_button.setStyleSheet("""
        QToolButton {
            background-color: #FFF;
            color: #B5BFC6; 
            border-radius: 14px;
            text-align: center; 
            font: 63 10pt "Montserrat SemiBold";
            
            selection-background-color: #FFF; /*ECECEC*/
            selection-color: #0F5BCD;
            outline: 0;
            padding: 8px;
            padding-right: 16px;
        }
        QToolButton:hover {
            background-color: #F8F9FB; 
        }
        """)

        # Create Sort options menu
        sort_menu = QMenu()

        sort_menu.setStyleSheet("""
        QMenu {
            background-color: white;
            margin: 2px; /* some spacing around the menu */
        }

        QMenu::item {
            font: 63 10pt "Montserrat SemiBold";
            padding: 6px 25px 6px 20px;
            border: 1px solid transparent; /* reserve space for selection border */
        }

        QMenu::item:selected {
            background: #DAE7FB;
        }

        QMenu::separator {
            height: 2px;
            background: lightblue;
            margin-left: 10px;
            margin-right: 5px;
        }

        QMenu::indicator {
            width: 13px;
            height: 13px;
        }
        """)

        # Group to ensure only one item is checked at a time
        group = QActionGroup(sort_menu)
        group.setExclusive(True)  # Only one action can be checked at a time

        def update_button_text(action=None):
            if action is not None: self.current_sort_action = action.text()
            
            sort_button.setText("Sort by "+self.current_sort_action)

            # Toggle between ascending and descending sort order
            if self.current_sort_order == 'ascending':
                self.current_sort_order = 'descending'
            else:
                self.current_sort_order = 'ascending'

            # Sort DataFrame by the selected column name and current sort order
            self.df.sort_values(by=self.current_sort_action, inplace=True, ascending=(self.current_sort_order == 'ascending'))

            # Update the table with the sorted data
            self.pandas_to_qtablewidget()
        
        sort_button.clicked.connect(lambda: update_button_text())

        # Add checklist items to the menu
        for column in self.df.columns:
            action = QAction(column, sort_menu)
            action.setCheckable(True)
            action.setChecked(True if column==init_action else False)
            group.addAction(action)
            sort_menu.addAction(action)
            action.triggered.connect(lambda checked, action=action: update_button_text(action))

        sort_button.setMenu(sort_menu)

        return sort_button

# Example usage with the DataFrame created earlier
app = QApplication(sys.argv)
window = QWidget()
window.setGeometry(100, 100, 800, 600)

layout = QVBoxLayout()

# Creating a DataFrame
data = {
    'Patient_ID': [1, 2, 3, 4, 5],
    'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Williams', 'Charlie Brown'],
    'Age': [42, 35, 28, 50, 65],
    'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
    'Blood_Pressure': [120/80, 130/85, 118/75, 125/82, 140/90],
    'Heart_Rate': [75, 82, 68, 92, 78],
    'Temperature': [98.6, 98.2, 98.9, 99.5, 98.0],
    'BMI': [22.5, 26.1, 24.3, 28.7, 29.5]
}
df = pd.DataFrame(data)

custom_table_widget = CustomQTableWidget(df)
sort_button = custom_table_widget.create_sort_button()

layout.addWidget(sort_button)
layout.addWidget(custom_table_widget)

window.setLayout(layout)
window.setStyleSheet("""
QWidget {background-color: #FFF}""")
window.show()

sys.exit(app.exec_())
