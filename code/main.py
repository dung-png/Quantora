from PyQt6.QtWidgets import QApplication,QMainWindow,QLineEdit,QMessageBox,QPushButton,QGridLayout
from PyQt6 import uic
import sys
from database import User_DATA,Product_DATA
from dialog import AddDialog,EditDialog
from column import ProductContainer

DTB = User_DATA()
class LoginWindow(QMainWindow):
    ui = r"ui\login_.ui"
    def __init__(self):
        super().__init__()
        uic.loadUi(self.ui,self)
        self.btn_Password.clicked.connect(self.passwordechomode)
        self.login_btn.clicked.connect(self.Homepage)
        self.Signup.clicked.connect(self.signup_)
        self.keepmelogin = self.Checkbox.isChecked()
    
    def Homepage(self):
        global HOMEPG
        email = self.Email.text().strip()
        password = self.Password.text().strip()
        phonenumber = self.PhoneNumber.text().strip()
        user_tuple = (email,password,phonenumber,self.keepmelogin)
        if email and password:
            resolve = DTB.signin(user_tuple)
            if resolve:
                self.close()
                if HOMEPG is None:
                    HOMEPG = MainWindow(resolve)
                    HOMEPG.show()
                else:
                    HOMEPG.show()
            else:
                msg_box.setText("Invalid email or password or phonenumber")
                msg_box.exec()
        else:
            msg_box.setText("Please enter both email and password")
            msg_box.exec()

    def signup_(self):
        self.close()
        Signup.show()

    def passwordechomode(self):
        if not self.btn_Password.isChecked() and self.Password.echoMode() == QLineEdit.EchoMode.Password:
            self.Password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.Password.setEchoMode(QLineEdit.EchoMode.Password)

class SignupWindow(QMainWindow):
    ui = r"ui\signup_.ui"
    def __init__(self):
        super().__init__()
        uic.loadUi(self.ui,self)
        self.btn_Password.clicked.connect(self.passwordechomode)
        self.signup_btn.clicked.connect(self.Homepage)
        self.Login.clicked.connect(self.login_)

    def passwordechomode(self):
        if not self.btn_Password.isChecked() and self.Password.echoMode() == QLineEdit.EchoMode.Password:
            self.Password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.Password.setEchoMode(QLineEdit.EchoMode.Password)

    def Homepage(self):
        global HOMEPG
        Business = self.Business.text().strip()
        Username = self.Username.text().strip()
        Email = self.Email.text().strip()
        Password = self.Password.text().strip()
        Confirm_Password = self.Confirm_Password.text().strip()
        PhoneNumber = self.PhoneNumber.text().strip()
        countrycode = self.countrycode.currentText()
        user_tuple = (Business,Username,Email,Password,PhoneNumber,countrycode)
        if Email and Password and Confirm_Password:
            resolve = DTB.signup(user_tuple)
            if resolve == 1:
                msg_box.setText("The password must contain between 8 and 20 characters")
                msg_box.exec()
            elif resolve == 2:
                msg_box.setText("Please enter a valid email address")
                msg_box.exec()
            elif resolve == 3:
                msg_box.setText("Phone number is either too short, too long, or already registered")
                msg_box.exec()
            elif resolve == 4:
                msg_box.setText("Business name must be between 3 and 20 characters and must be unique")
                msg_box.exec()
            elif resolve == 5:
                msg_box.setText("Username must be between 3 and 20 characters and must be unique")
                msg_box.exec()
            elif resolve == 6:
                msg_box.setText("This email is already registered. Please use another one")
                msg_box.exec()
            else:
                self.close()
                if HOMEPG is None:
                    HOMEPG = MainWindow(resolve)
                    HOMEPG.show()
                else:
                    HOMEPG.show()

    def login_(self):
        self.close()
        Login.show()

class MainWindow(QMainWindow):
    ui = r"ui\home.ui"
    def __init__(self,user):
        super().__init__()
        uic.loadUi(self.ui,self)
        global PRODUCT_DTB, grlayout, UI
        UI = self
        PRODUCT_DTB = Product_DATA(user.id, self.SORT.currentText())
        self.user = user
        self.btn_profile.setText(str(self.user.business_name)[0].capitalize())
        self.profile_text.setText(str(self.user.business_name).strip())
        leng = len(str(self.user.business_name))
        if leng <= 10:
            size = 28
        elif leng <= 15:
            size = 21
        else:
            size = 17
        self.profile_text.setStyleSheet(f"font-size: {size}px;")
        self.exit.clicked.connect(self.Exit)
        self.logout.clicked.connect(self.Logout)
        self.Home.clicked.connect(self.home)
        self.Products.clicked.connect(self.products_page)
        self.grid_layout = QGridLayout(self.scrollAreaWidgetContents_2)
        grlayout = self.grid_layout
        grlayout.setVerticalSpacing(10)
        grlayout.setHorizontalSpacing(10)
        grlayout.setContentsMargins(10, 10, 10, 10)
        self.layout = Products_layout()
        self.setupProductpage()
        self.Add.clicked.connect(lambda: ProductsCRUD.Add(self,self.user.id,self.layout))
        self.Edit.clicked.connect(lambda: ProductsCRUD.Edit(self,self.user.id,self.layout))
        self.Remove.clicked.connect(lambda: ProductsCRUD.Remove(self,self.layout))
        self.Search.clicked.connect(lambda: self.layout.Search())
        self.SORT.currentTextChanged.connect(lambda : ProductsCRUD._sort_(self,self.layout,self.SORT.currentText()))

    def Logout(self):
        global HOMEPG
        # Ghi đè file config.ini thành file trắng (xóa hết nội dung)
        with open(r"database\config.ini", "w") as f:
            f.write("")  # hoặc dùng: pass
        self.close()
        HOMEPG = None
        Login.show()
    
    def Exit(self):
        self.close()
        sys.exit()

    def home(self):
        self.stackedWidget.setCurrentIndex(0)

    def products_page(self):
        self.stackedWidget.setCurrentIndex(2)
    
    def products_page_setup(self):
        self.Add.clicked.connect()
        self.Edit.clicked.connect()
        self.Remove.clicked.connect()

    def setupProductpage(self):
        self.layout.display()

class ProductsCRUD():
    def _sort_(self,layout,type):
        sorted_list = PRODUCT_DTB._Sort_(product_object_list,type)
        for item in sorted_list:
            print(item.name)
        layout.updateLayout(sorted_list)

    def Add(self,user_id,layout):
        add_dl = AddDialog(user_id)
        if add_dl.exec(): # CHECK NEU DIALOG DANG RUN  VA BUTTON OK DUOC NHAN
            #LAY DATA INPUT VAO CONVERT SANG DICT
            input = add_dl.returnInputValue()
            if input[5].strip().lower() == "browse".strip().lower():
                input = (input[0],input[4],input[1],input[2],input[3])
                PRODUCT_DTB.Insert_(input)
                layout.updateLayout()
            else:
                pass
    def Edit(self,user_id,layout):
        selected = []
        for product in product_container_object_list:
            if product.selected:
                selected.append(product)
        if len(selected) != 1:
            for product in selected:
                product.selected = False
                product.ui.frame.setStyleSheet("""
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
            msg_box.setText("Please select a single product to edit")
            msg_box.exec()
        elif len(selected) == 1:
            edit_dl = EditDialog(user_id=user_id,object=selected[0].product)
            if edit_dl.exec():
                input = edit_dl.returnInputValue()
                # image_path = ? , name = ? , available = ? , cost = ? WHERE id = ? AND user_id = ?
                PRODUCT_DTB.Edit_((input[4],input[1],input[2],input[3],selected[0].product.id,input[0]))
                selected[0].product.update_((input[4],input[1],input[2],input[3]))
                layout.updateLayout()
        
    def Remove(self,layout):
        for product_container in product_container_object_list:
            if product_container.selected:
                PRODUCT_DTB.Remove_(product_container.product)
                product_container.deleteLater()
        product_container_object_list.clear()
        product_object_list.clear()
        layout.updateLayout()

class Products_layout():
    def __init__(self):
        global product_container_object_list, product_object_list
        product_container_object_list = []
        product_object_list = []

    def display(self):
        global product_container_object_list, product_object_list
        product_container_object_list = []
        product_object_list = []
        for index,product in enumerate(PRODUCT_DTB.product_list):
            row = index % 2       # 0 nếu chẵn, 1 nếu lẻ
            col = index // 2
            product_container = ProductContainer(product)
            product_container_object_list.append(product_container)
            product_object_list.append(product)
            grlayout.addWidget(product_container, row, col)
        UI.scrollAreaWidgetContents_2.setLayout(grlayout)
    
    def clearLayout(self):
        while grlayout.count():
            child = grlayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def updateLayout(self, item_list = None):
        global product_container_object_list, product_object_list
        product_container_object_list = []
        product_object_list = []
        self.clearLayout()
        if item_list is None:
            item_list = PRODUCT_DTB.product_list
        for index,product in enumerate(item_list):
            row = index % 2
            col = index // 2
            product_container = ProductContainer(product)
            product_container_object_list.append(product_container)
            product_object_list.append(product)
            grlayout.addWidget(product_container, row, col)

    def Search(self):
        search_field = UI.searchinput.text().strip()
        if search_field:
            matched_list = PRODUCT_DTB.Search(search_field)
            UI.scrollAreaWidgetContents_2.setLayout(grlayout)
            self.updateLayout(matched_list)
        else:
            self.updateLayout(PRODUCT_DTB.product_list)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    msg_box = QMessageBox()
    msg_box.setWindowTitle("error")
    msg_box.setIcon(QMessageBox.Icon.Warning)
    Login = LoginWindow()
    Signup = SignupWindow()
    keepmelogin = DTB.checkkeeplogin()
    if keepmelogin:
        HOMEPG = MainWindow(keepmelogin)
        HOMEPG.show()
    else:
        HOMEPG = None
        Login.show()
    exit_code = app.exec()
    # Chỉ chạy khi app THOÁT HẲN
    DTB.cursor.close()
    DTB.user_db.close()
    sys.exit(exit_code)