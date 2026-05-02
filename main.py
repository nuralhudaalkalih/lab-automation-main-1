import tkinter as tk

from database.DatabaseManager import DatabaseManager
from controllers.AuthController import AuthController
from controllers.SampleController import SampleController
from controllers.TestController import TestController
from controllers.ReportController import ReportController

from gui.LoginWindow import LoginWindow
from gui.RegisterWindow import RegisterWindow
from gui.DashboardWindow import DashboardWindow
from gui.SampleForm import SampleForm
from gui.ResultForm import ResultForm
from gui.ManageUsersForm import ManageUsersForm
from gui.ReportForm import ReportForm   # 🔥 جديد

# ── DB + CONTROLLERS ──
db = DatabaseManager()

auth = AuthController(db)
sample = SampleController(db)
test = TestController(db)
report = ReportController(db)

# ── ROOT ──
root = tk.Tk()
root.title("Laboratory System")
root.geometry("900x700")
root.configure(bg="#A8A8AD")

# ── GLOBAL USER ──
current_user = None

# ── CLEAR SCREEN ──
def clear():
    for w in root.winfo_children():
        w.destroy()

# ── LOGIN ──
def open_login():
    clear()

    LoginWindow(
        root,
        auth_controller=auth,
        on_success=open_dashboard,
        open_register=open_register
    )

# ── REGISTER ──
def open_register():
    clear()

    RegisterWindow(
        root,
        auth_controller=auth,
        on_done=open_login
    )

# ── DASHBOARD ──
def open_dashboard(user):
    global current_user
    current_user = user

    clear()

    DashboardWindow(
        root,
        user=user,
        sample_controller=sample,
        open_sample=open_sample,
        open_result=open_result,
        open_manage_users=open_manage_users,
        open_reports=open_reports,   
        on_logout=open_login
    )

# ── SAMPLE ──
def open_sample():
    clear()

    SampleForm(
        root,
        sample_controller=sample,
        on_home=lambda: open_dashboard(current_user)
    )

# ── RESULT ──
def open_result():
    clear()

    ResultForm(
        root,
        report_controller=report,
        sample_controller=sample,
        test_controller=test,
        on_home=lambda: open_dashboard(current_user)
    )

# ── REPORTS ── 
def open_reports():
    clear()

    ReportForm(
        root,
        report_controller=report,
        on_home=lambda: open_dashboard(current_user)
    )

# ── MANAGE USERS ──
def open_manage_users():
    if current_user["role"] != "Admin":
        return

    clear()

    ManageUsersForm(
        root,
        auth_controller=auth,
        on_home=lambda: open_dashboard(current_user)
    )

# ── START ──
open_login()
root.mainloop()