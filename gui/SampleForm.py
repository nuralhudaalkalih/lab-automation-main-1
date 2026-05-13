import tkinter as tk
from tkinter import ttk, messagebox, filedialog
class SampleForm:
    def __init__(self, root, sample_controller, on_home):
        self.sample_controller = sample_controller
        self.on_home = on_home

        frame = tk.Frame(root, bg="#A8A8AD")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="SAMPLE FORM", font=("Arial", 40), bg="#A8A8AD").grid(row=0, column=0, columnspan=2)

        # ── ADD SAMPLE ──
        self.patient_entry = tk.Entry(frame, font=("Arial",17))
        self.patient_entry.grid(row=1, column=1)
        tk.Label(frame, text="Patient:", bg="#A8A8AD", font=("Arial",17)).grid(row=1, column=0)
        tk.Button(frame, text="Add Sample",width=20,font=("Arial",10), command=self.add_sample).grid(row=2, column=0, columnspan=2,pady=10)
        # ── SEARCH ──
        tk.Button(frame, text="Search", width=20, font=("Arial",10), command=self.search).grid(row=3, column=0,pady=5)
        self.search_entry = tk.Entry(frame, font=("Arial",12))
        self.search_entry.grid(row=3, column=1, pady=5)

        # ── FILTER ──
        tk.Button(frame, text="Filter", width=20, font=("Arial",10), command=self.filter).grid(row=4, column=0,pady=5)
        self.filter_combo = ttk.Combobox(frame, font=("Arial",11))
        self.filter_combo["values"] = ["All", "Pending", "Processing", "Completed"]
        self.filter_combo.current(0)
        self.filter_combo.grid(row=4, column=1, pady=5)

        # ── TABLE ──
        self.tree = ttk.Treeview(frame, columns=("id","name","status","date"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Patient")
        self.tree.heading("status", text="Status")
        self.tree.heading("date",text="Date")
        self.tree.grid(row=5, column=0, columnspan=2)

        # ── BUTTONS ──
        tk.Button(frame, text="Refresh",width=20,font=("Arial",10), command=self.load_samples).grid(row=6, column=0,pady=10)
        tk.Button(frame, text="Home",width=20,font=("Arial",10), command=self.on_home).grid(row=6, column=1,pady=10)
        tk.Button(frame, text="Processing",width=20,font=("Arial",10), command=self.mark_processing).grid(row=7, column=0,pady=5)
        tk.Button(frame, text="Completed",width=20,font=("Arial",10), command=self.mark_completed).grid(row=7, column=1,pady=5)

        # delete sample
        tk.Button(frame, text="Delete Sample",width=20,font=("Arial",10), command=self.delete_sample).grid(row=8, column=0, columnspan=2,pady=10)

        self.load_samples()

    def add_sample(self):
        name = self.patient_entry.get()
        if not name:
            messagebox.showerror("Error", "Enter name")
            return
        self.sample_controller.add_sample(name)
        
        messagebox.showinfo("Success", "Added")
        self.patient_entry.delete(0, tk.END)
        self.load_samples()

    def load_samples(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        samples = self.sample_controller.get_all_samples()
        for s in samples:
            # Access as object properties
            self.tree.insert("", "end", values=(s.sample_id, s.patient_name, s.status, s.date_added))

    def search(self):
        query = self.search_entry.get()
        for row in self.tree.get_children():
            self.tree.delete(row)
        results = self.sample_controller.search_samples_by_patient(query)
        for s in results:
            self.tree.insert("", "end", values=(s.sample_id, s.patient_name, s.status, s.date_added))

    def filter(self):
        status = self.filter_combo.get()
        for row in self.tree.get_children():
            self.tree.delete(row)

        if status == "All":
            samples = self.sample_controller.get_all_samples()
        else:
            samples = self.sample_controller.get_samples_by_status(status)

        for s in samples:
            self.tree.insert("", "end", values=(s.sample_id, s.patient_name, s.status, s.date_added))

    def get_selected_id(self):
        selected = self.tree.selection()
        if not selected:
            return None
        return self.tree.item(selected[0])["values"][0]

    def mark_processing(self):
        sample_id = self.get_selected_id()
        if not sample_id:
            return
        self.sample_controller.update_sample_status(sample_id, "Processing")
        self.load_samples()

    def mark_completed(self):
        sample_id = self.get_selected_id()
        if not sample_id:
            return
        self.sample_controller.update_sample_status(sample_id, "Completed")
        self.load_samples()

    def delete_sample(self):
        sample_id = self.get_selected_id()
        if not sample_id:
            return
        self.sample_controller.delete_sample(sample_id)
        messagebox.showinfo("Success", "Deleted")
        self.load_samples()