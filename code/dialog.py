from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QFileDialog, QWidget
from PyQt6.QtCore import QDate, QDir, Qt
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QMessageBox, QWidget, QApplication
from PyQt6 import uic
from PyQt6.QtCore import Qt

class Dialog(QDialog):
    ui = ''
    def __init__(self,user_id):
        super().__init__()
        self.ui = None
        self.user_id = user_id

    def browseFile(self,btn):
        filepath = QFileDialog.getOpenFileName(self, 'Select image song')
        btn.setText(filepath[0])
        return filepath
    
    def returnInputValue(self):
        Name = self.ui.Name.text().strip()
        Available = self.ui.Available.text().strip()
        Cost = self.ui.Cost.text().strip()
        img = self.ui.Browse_image.text()
        json = self.ui.Browse_json.text()
        #trả về dạng dict để gọi hàm addsong sau này
        #key là tên thuộc tính
        return (self.user_id,Name,Available,Cost,img,json)
    
class AddDialog(Dialog):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.ui = uic.loadUi(r"ui\add_dialog.ui", self)
        self.ui.Browse_image.clicked.connect(lambda: self.browseFile(self.ui.Browse_image))
        self.ui.Browse_json.clicked.connect(lambda: self.browseFile(self.ui.Browse_json))

class EditDialog(Dialog):
    def __init__(self, object , user_id):
        super().__init__(user_id)
        self.ui = uic.loadUi(r"ui\edit_dialog.ui", self)
        self.ui.Browse_image.clicked.connect(lambda: self.browseFile(self.ui.Browse_image))
        self.ui.Browse_json.clicked.connect(lambda: self.browseFile(self.ui.Browse_json))
        self.ui.Name.setText(str(object.name))
        self.ui.Available.setText(str(object.available))
        self.ui.Cost.setText(str(object.cost))