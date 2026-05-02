import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, root, auth_controller, on_success, open_register):
        self.auth = auth_controller
        self.on_success = on_success
        self.open_register = open_register

        frame = tk.Frame(root, bg="#A8A8AD")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="LOGIN", font=("Arial", 35),
                 bg="#A8A8AD").grid(row=0, column=0, columnspan=2, pady=20)

        # Username
        tk.Label(frame, text="Username:", bg="#A8A8AD",font=("Arial", 20)).grid(row=1, column=0,pady=10)
        self.username = tk.Entry(frame,font=("Arial", 20))
        self.username.grid(row=1, column=1)

        # Password
        tk.Label(frame, text="Password:", bg="#A8A8AD",font=("Arial", 20)).grid(row=2, column=0,pady=10)
        self.password = tk.Entry(frame, show="*",font=("Arial", 20))
        self.password.grid(row=2, column=1)

        # Buttons
        tk.Button(frame, text="Login", width=20,font=("Arial", 15),
                  command=self.login).grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(frame, text="Create Account",font=("Arial", 15),
                  fg="blue", bg="#A8A8AD", borderwidth=0,
                  command=self.open_register).grid(row=4, column=0, columnspan=2)

    def login(self):
        user = self.auth.login(self.username.get(), self.password.get())

        if user:
            self.on_success(user)
        else:
            messagebox.showerror("Error", "Invalid login")