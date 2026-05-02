import tkinter as tk
from tkinter import messagebox

class RegisterWindow:
    def __init__(self, root, auth_controller, on_done):
        self.auth = auth_controller
        self.on_done = on_done

        frame = tk.Frame(root, bg="#A8A8AD")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="REGISTER", font=("Arial", 30),
                 bg="#A8A8AD").grid(row=0, column=0, columnspan=2, pady=20)

        # Username
        tk.Label(frame, text="Username:", bg="#A8A8AD",font=("Arial",20)).grid(row=1, column=0,pady=10)
        self.username = tk.Entry(frame,font=("Arial",20))
        self.username.grid(row=1, column=1,pady=10)

        # Password
        tk.Label(frame, text="Password:", bg="#A8A8AD",font=("Arial",20)).grid(row=2, column=0,pady=10)
        self.password = tk.Entry(frame, show="*",font=("Arial",20))
        self.password.grid(row=2, column=1,pady=10)

        # Role
        tk.Label(frame, text="Role:", bg="#A8A8AD",font=("Arial",20)).grid(row=3, column=0,pady=10)

        self.role = tk.StringVar(value="Technician")

        tk.Radiobutton(frame, text="Admin",font=("Arial",12),
                       variable=self.role, value="Admin",
                       bg="#A8A8AD").grid(row=3, column=1,pady=10 ,sticky="w")

        tk.Radiobutton(frame, text="Technician",font=("Arial",12),
                       variable=self.role, value="Technician",
                       bg="#A8A8AD").grid(row=3, column=1,pady=10)

        # Button
        tk.Button(frame, text="Create Account",font=("Arial",10),width=20,
                  command=self.register).grid(row=4, column=0, columnspan=2, pady=15)

    def register(self):
        success = self.auth.register(
            self.username.get(),
            self.password.get(),
            self.role.get()
        )

        if success:
            messagebox.showinfo("Success", "Account created")
            self.on_done()   
        else:
            messagebox.showerror("Error", "Username exists")