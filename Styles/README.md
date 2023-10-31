```css
/*----------------------------- Frame -----------------------------*/
QFrame {
    border: 1px solid #EDF0F6;
    border-radius: 16px;
}

/*----------------------------- Header -----------------------------*/
QLabel {
    font: 20pt "Montserrat SemiBold";
    color: #4A535F;
}

/*----------------------------- Subheader -----------------------------*/
QLabel {
    font: 63 10pt "Montserrat SemiBold";
    color: #B5BFC6;
    border: 0px;
}

/*----------------------------- Text -----------------------------*/
QLabel { 
    font: 12pt "Montserrat";
    color: #4A535F;
    border: 0px;
}

/*----------------------------- High Button -----------------------------*/
QPushButton {
    border-radius: 16px;
    border: 0px;
    background-color: #4487EB;
    color: #FFF;
    font: 63 10pt "Montserrat SemiBold";
}
QPushButton:hover {
    background-color: #0F5BCD;
}
QPushButton:pressed {
    background-color: #0F5BCD;
    border: 1px solid #DAE7FB;
} 
QPushButton:!enabled {
    background-color: #EDF0F6;
    color: #B5BFC6;
}

/*----------------------------- Medium Button -----------------------------*/
QPushButton {
    border-radius: 16px;
    border: 1px solid #EDF0F6;
    background-color: #FFF;
    color: #4487EB;
    font: 63 10pt "Montserrat SemiBold";
}
QPushButton:hover {
    background-color: #EDF0F6;
}
QPushButton:pressed {
    background-color: #EDF0F6;
    border-color: #4487EB;
} 
QPushButton:!enabled {
    background-color: #EDF0F6;
    color: #B5BFC6;
}

/*----------------------------- Low Button -----------------------------*/
QPushButton {
    border-radius: 15px;
	border: 1px solid #EDF0F6;
    background-color: #FFF;
    color: #B5BFC6;
    font: 63 10pt "Montserrat Medium";
}
QPushButton:hover {
    background-color: #F8F9FB
}
QPushButton:pressed {
    background-color: #F8F9FB;	
    color: #4487EB;
} 
QPushButton:!enabled {
    border-radius: 15px;
    font: 63 10pt "Montserrat Medium";
}

/*----------------------------- Views -----------------------------*/
QPushButton #view1, #view2, #view3 {
    border: 0px;
    background-color: #FFF;
    color: #B5BFC6;
    font: 63 10pt "Montserrat Medium";
}
QPushButton #view1:checked, #view2:checked, #view3:checked {
	color: #4487EB;
	font: 63 10pt "Montserrat SemiBold";
} 
QWidget #underline1,#underline2,#underline3 {
    border: 0px; 
    border-radius: 1px;
    background-color: #4487EB;
}
QWidget #underline1:!enabled,#underline2:!enabled,#underline3:!enabled {
    background-color: #F8F9FB;
}

/*----------------------------- CheckBox -----------------------------*/
QCheckBox {
    color: #4A535F;
    font: 63 10pt "Montserrat Medium";
	spacing: 8px;
}
QCheckBox:!enabled {
    color: #B5BFC6;
}
QCheckBox::indicator:unchecked {
	image: url(:/icons/Property 1=Default.svg);
}
QCheckBox::indicator:unchecked:hover {
	image: url(:/icons/Property 1=Hover.svg);
}
QCheckBox::indicator:checked {
	image: url(:/icons/Property 1=Checked.svg);
}
QCheckBox::indicator:!enabled {
	image: url(:/icons/Property 1=Not Enabled.svg);
}

/*----------------------------- Table -----------------------------*/
QTableWidget {
    font: 11pt "Montserrat";
    color: #4A535F;
    selection-color: #4A535F;
    background-color: #FFF;
    outline: 0;
}
QHeaderView { 
    font: 63 10pt "Montserrat SemiBold";
    color: #B5BFC6;
    background-color:#FFF;  
    border: 0px;
    padding: 0px;
}
QHeaderView:checked {
    background-color: #4A535F;
}
QTableView::item {
	border-top: 1px solid #EDF0F6;  
	padding-left: 8px;
}
QTableView::item:hover {
    background-color: #F8F9FB;
}      

```