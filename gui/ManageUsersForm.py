import tkinter as tk
from tkinter import ttk, messagebox

class ManageUsersForm:
    def __init__(self, root, auth_controller, on_home):
        self.auth = auth_controller
        self.on_home = on_home

        frame = tk.Frame(root, bg="#A8A8AD")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="MANAGE USERS", font=("Arial", 40),
                 bg="#A8A8AD").grid(row=0, column=0, columnspan=2, pady=20)

        # ── ADD USER ──
        tk.Label(frame, text="Username", bg="#A8A8AD",font=("Arial",18)).grid(row=1, column=0,pady=5)
        self.username_entry = tk.Entry(frame,font=("Arial",18))
        self.username_entry.grid(row=1, column=1,pady=5)

        tk.Label(frame, text="Password", bg="#A8A8AD",font=("Arial",18)).grid(row=2, column=0,pady=5)
        self.password_entry = tk.Entry(frame, show="*",font=("Arial",18))
        self.password_entry.grid(row=2, column=1,pady=5)

        tk.Label(frame, text="Role", bg="#A8A8AD",font=("Arial",18)).grid(row=3, column=0,pady=5)
        self.role_combo = ttk.Combobox(frame,font=("Arial",16), values=["Admin", "Technician"])
        self.role_combo.grid(row=3, column=1,pady=5)
        self.role_combo.current(1)

        tk.Button(frame, text="Add User", width=20,
                  command=self.add_user).grid(row=4, column=0, columnspan=2, pady=10)

        # ── TABLE ──
        self.tree = ttk.Treeview(frame,
                                 columns=("username","role"),
                                 show="headings")

        self.tree.heading("username",text="Username")
        self.tree.heading("role", text="Role")

        self.tree.grid(row=5, column=0, columnspan=2)

        # ── BUTTONS ──
        tk.Button(frame, text="Refresh", width=20,
                  command=self.load).grid(row=6, column=0, pady=10)

        tk.Button(frame, text="Delete", width=20,
                  command=self.delete).grid(row=6, column=1, pady=10)

        tk.Button(frame, text="Home", width=20,
                  command=self.on_home).grid(row=7, column=0, columnspan=2, pady=10)

        self.load()

    # ── ADD USER ──
    def add_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combo.get()

        if not username or not password:
            messagebox.showerror("Error", "Fill all fields")
            return

        success = self.auth.register(username, password, role)

        if not success:
            messagebox.showerror("Error", "Username already exists")
            return

        messagebox.showinfo("Success", "User added")

        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        self.load()

    # ── LOAD USERS ──
    def load(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        users = self.auth.get_all_users()

        for u in users:
            self.tree.insert("", "end",
                             values=(u["username"], u["role"]))

    # ── DELETE USER ──
    def delete(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Error", "Select user")
            return

        username = self.tree.item(selected[0])["values"][0]

        self.auth.delete_user(username)

        messagebox.showinfo("Success", "Deleted")

        self.load()