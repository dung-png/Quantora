from PyQt6.QtWidgets import QApplication,QMainWindow,QLineEdit,QMessageBox,QPushButton
from PyQt6 import uic
import sys
from database import User_DATA

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
        print(self.btn_Password.isChecked())
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
        print(self.btn_Password.isChecked())
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
            print(resolve)
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