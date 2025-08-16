from PyQt6.QtCore import Qt
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
from database import Product

class ProductContainer(QWidget):
    def __init__(self,product_object : Product):
        super().__init__()
        self.ui = uic.loadUi(r"ui\product_box.ui", self)
        self.product = product_object
        self.display_column()
        self.selected = False

    def display_column(self):
        self.ui.image.setStyleSheet(f"""border: 3px solid black;
background-image: url({self.product.image});
background-position: center;
background-repeat: no-repeat;""")
        self.ui.product_name.setText(self.product.name)
        self.ui.quantity.setText(str(self.product.available))
        self.ui.Cost.setText(str(self.product.cost)+" vnd")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Toggle trạng thái
            self.selected = not self.selected

            # Đổi style để highlight khi được chọn
            if self.selected:
                self.ui.frame.setStyleSheet("""
                    QFrame {
background-color:white;
border:3px solid black;
border-radius:20%;
background-color:rgba(150, 150, 150, 150);
}
QFrame > QLabel{
	border:none;
	background:none;
	font: 87 18pt "Segoe UI Black";
	color:black;
}
                """)
            else:
                self.ui.frame.setStyleSheet("""
QFrame {
background-color:white;
border:3px solid black;
border-radius:20%;
}
QFrame > QLabel{
	border:none;
	background:none;
	font: 87 18pt "Segoe UI Black";
	color:black;
}
""")