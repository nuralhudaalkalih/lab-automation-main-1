import tkinter as tk

class DashboardWindow:
    def __init__(self, root, user, sample_controller,
                 open_sample, open_result, open_manage_users,
                 open_reports, on_logout):

        self.root = root
        self.user = user
        self.sample_controller = sample_controller

        frame = tk.Frame(root, bg="#A8A8AD")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="HOME", font=("Arial", 45, "bold"),
                 bg="#A8A8AD").grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(frame,
                 text=f"Welcome {user['username']} ({user['role']})",
                 font=("Arial", 25),
                 bg="#A8A8AD").grid(row=1, column=0, columnspan=2, pady=10)

        # ── SUMMARY ──
        counts = self.sample_controller.count_samples_by_status()

        tk.Label(frame, font=("Arial", 15),
                 text=f"Pending: {counts.get('Pending',0)}").grid(row=2, column=0, pady=10)

        tk.Label(frame, font=("Arial", 15),
                 text=f"Processing: {counts.get('Processing',0)}").grid(row=2, column=1, pady=10)

        tk.Label(frame, font=("Arial", 15),
                 text=f"Completed: {counts.get('Completed',0)}").grid(row=3, column=0, columnspan=2, pady=10)

        # ── BUTTONS ──
        tk.Button(frame, text="Sample Form", width=20, font=("Arial", 18),
                  command=open_sample).grid(row=4, column=0, pady=10,padx=10)

        tk.Button(frame, text="Result Form", width=20, font=("Arial", 18),
                  command=open_result).grid(row=4, column=1, pady=10,padx=10)

        tk.Button(frame, text="Reports", width=20, font=("Arial", 18),
                  command=open_reports).grid(row=5, column=0, pady=10,padx=10)

        if user["role"] == "Admin":
            tk.Button(frame, text="Manage Users", width=20, font=("Arial", 18),
                      command=open_manage_users).grid(row=5, column=1,padx=10)

        tk.Button(frame, text="Logout", width=25, font=("Arial", 14),
                  command=on_logout).grid(row=6, column=0, columnspan=2, pady=20)