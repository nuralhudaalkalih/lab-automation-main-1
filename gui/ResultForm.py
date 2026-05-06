import tkinter as tk
from tkinter import ttk, messagebox

class ResultForm:
    def __init__(self, root, report_controller, sample_controller, test_controller, on_home):
        self.report = report_controller
        self.sample = sample_controller
        self.test = test_controller
        self.on_home = on_home

        # add default tests
        self.test.add_default_tests()

        frame = tk.Frame(root, bg="#A8A8AD")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            frame,
            text="RESULT FORM",
            font=("Arial", 40),
            bg="#A8A8AD"
        ).grid(row=0, column=0, columnspan=2)

        # ── Sample ID ──
        tk.Label(
            frame,
            text="Sample ID:",
            bg="#A8A8AD",
            font=("Arial", 20)
        ).grid(row=1, column=0, pady=10)

        self.sample_combo = ttk.Combobox(
            frame,
            font=("Arial", 20),
            state="readonly"
        )
        self.sample_combo.grid(row=1, column=1, pady=10)

        # fill combo with all sample IDs
        samples = self.sample.get_all_samples()
        self.sample_combo["values"] = [sample.sample_id for sample in samples]

        # ── Test ──
        tk.Label(
            frame,
            text="Test:",
            bg="#A8A8AD",
            font=("Arial", 20)
        ).grid(row=2, column=0, pady=10)

        self.test_combo = ttk.Combobox(
            frame,
            font=("Arial", 20),
            state="readonly"
        )
        self.test_combo.grid(row=2, column=1, pady=10)
        self.test_combo["values"] = self.test.get_test_names()

        # ── Result ──
        tk.Label(
            frame,
            text="Result:",
            bg="#A8A8AD",
            font=("Arial", 20)
        ).grid(row=3, column=0, pady=10)

        self.result_entry = tk.Entry(frame, font=("Arial", 20))
        self.result_entry.grid(row=3, column=1, pady=10)

        # ── Buttons ──
        tk.Button(
            frame,
            text="Save",
            font=("Arial", 10),
            width=25,
            command=self.save
        ).grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(
            frame,
            text="Home",
            font=("Arial", 10),
            width=20,
            command=self.on_home
        ).grid(row=5, column=0, columnspan=2, pady=10)

    def save(self):
        sample_id = self.sample_combo.get()
        test_name = self.test_combo.get()
        value = self.result_entry.get()

        if not sample_id or not test_name or not value:
            messagebox.showerror("Error", "Fill all")
            return

        test_obj = self.test.get_test_by_name(test_name)

        self.report.add_result(sample_id, test_obj.test_id, value)

        self.sample.update_sample_status(sample_id, "Processing")

        messagebox.showinfo("Success", "Saved")

        self.result_entry.delete(0, tk.END)