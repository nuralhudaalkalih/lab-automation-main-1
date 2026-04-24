# Laboratory Automation and Sample Management System (LASMS)

A desktop application built with Python, Tkinter, and SQLite for managing laboratory samples, test assignments, and patient results. Developed as a group project for the Database and Python Programming course.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Project Structure](#project-structure)
5. [Class Reference (19 Classes)](#class-reference)
6. [Database Schema](#database-schema)
7. [Installation and Setup](#installation-and-setup)
8. [How to Run](#how-to-run)
9. [Default Login Credentials](#default-login-credentials)
10. [Usage Walkthrough](#usage-walkthrough)
11. [Technologies Used](#technologies-used)
12. [Team and Responsibilities](#team-and-responsibilities)

---

## Project Overview

LASMS is a fully functional laboratory information system that allows lab staff to:

- Register patient samples with auto-generated IDs
- Assign tests from a catalogue of 14 standard lab tests
- Track each sample through a defined status workflow (Pending → Processing → Completed)
- Record and view test results with patient details
- Generate and export lab reports
- Manage user accounts with role-based access control

The system uses a strict three-layer architecture — GUI, Controllers, and Database — ensuring clean separation of concerns and making each part independently testable.

---

## Features

### User Management
- Secure login and logout with session tracking
- Two roles: **Admin** and **Technician**
- Admins can create, update, and delete user accounts
- Role-based access: Admin-only actions are hidden from Technicians

### Sample Management
- Register new patient samples (auto-generates IDs: S001, S002, ...)
- Track sample status through three stages: Pending → Processing → Completed
- Search samples by patient name (partial match supported)
- Filter samples by status
- Dashboard summary showing counts per status

### Test Management
- Pre-loaded catalogue of 14 standard lab tests across blood, urine, viral, and hormone categories
- Admins can add, update, or remove tests from the catalogue
- Technicians select from the catalogue when recording results

### Result Management
- Record measured values against any sample and test combination
- Correct previously entered result values
- View all results for a specific sample with test names

### Reporting
- View complete patient reports combining sample info and all results
- Export individual reports to `.txt` files
- Batch export all completed reports to a folder
- Dashboard summary card with total counts

---

## System Architecture

The system follows a three-layer architecture. Each layer only communicates with the layer directly below it.

```
┌─────────────────────────────────────────┐
│              GUI Layer                  │
│  LoginWindow · DashboardWindow          │
│  SampleForm  · ResultForm               │
│  (Tkinter — handles display only)       │
└────────────────┬────────────────────────┘
                 │ calls
┌────────────────▼────────────────────────┐
│           Controller Layer              │
│  AuthController   · SampleController   │
│  TestController   · ReportController   │
│  (business logic, validation, rules)   │
└────────────────┬────────────────────────┘
                 │ queries
┌────────────────▼────────────────────────┐
│          Database Layer                 │
│  DatabaseManager                        │
│  UserDAO · SampleDAO · TestDAO          │
│  ResultDAO                              │
│  (all SQL — INSERT, SELECT, UPDATE)     │
└────────────────┬────────────────────────┘
                 │ reads/writes
┌────────────────▼────────────────────────┐
│           SQLite Database               │
│              lab.db                     │
│  Users · Samples · Tests · Results     │
└─────────────────────────────────────────┘
```

**Key rule:** The GUI never writes SQL. Controllers never import Tkinter. DAOs never contain business logic. Each layer has one job.

---

## Project Structure

```
LABRATORYAUTOMATION/
│
├── main.py                    # Entry point — creates DB, controllers, launches GUI
│
├── database/
│   ├── DatabaseManager.py     # SQLite connection, creates all tables on startup
│   ├── UserDAO.py             # CRUD for the Users table
│   ├── SampleDAO.py           # CRUD for the Samples table
│   ├── TestDAO.py             # CRUD for the Tests table
│   └── ResultDAO.py           # CRUD for the Results table (with JOINs)
│
├── models/
│   └── Admin.py 
│   └── Technician.py
│   └── User.py
│   └── Sample.py
│   └── Test.py
│   └── Result.py     
│
│
├── controllers/
│   ├── AuthController.py      # Login, logout, user management, session
│   ├── SampleController.py    # Sample registration, status workflow, search
│   ├── TestController.py      # Test catalogue, result recording
│   └── ReportController.py    # Report assembly, dashboard summary, file export
│
├── gui/
│   ├── LoginWindow.py         # Login screen
│   ├── DashboardWindow.py     # Main navigation hub
│   ├── SampleForm.py          # Add/view/search samples
│   └── ResultForm.py          # Assign tests and enter results
│
├── utils/
│   └── .gitkeep               # Placeholder for utility helpers
│
├── .gitignore
├── README.md
└── lab.db                     # Created automatically on first run
```

---

## Class Reference

The project contains **19 classes** across all layers.

### Model Classes — `models/models.py`

| Class | Inherits From | Description |
|---|---|---|
| `User` | — | Base class representing a system user. Holds `user_id`, `username`, `password`, `role`. Provides `check_password()`, `is_admin()`, `is_technician()`. |
| `Admin` | `User` | Subclass with role hardcoded to `"Admin"`. Adds permission methods: `can_manage_users()`, `can_delete_samples()`, `can_add_tests()`. |
| `Technician` | `User` | Subclass with role hardcoded to `"Technician"`. Adds `can_add_samples()`, `can_enter_results()`. |
| `Sample` | — | Represents one patient sample. Holds status and provides `advance_status()`, `is_pending`, `is_processing`, `is_completed` properties. |
| `Test` | — | Represents one test type from the catalogue (e.g. CBC, Urinalysis). |
| `Result` | — | Represents one recorded measurement. Supports both basic and JOIN-enriched construction via `from_row()` and `from_joined_row()`. |

### Database Layer Classes — `database/`

| Class | File | Description |
|---|---|---|
| `DatabaseManager` | `DatabaseManager.py` | Opens the SQLite connection, enables foreign keys, creates all four tables on startup. Shared across all DAOs. |
| `UserDAO` | `UserDAO.py` | All SQL for the `Users` table: `add_user`, `get_by_username`, `get_all_users`, `update_password`, `update_role`, `delete_user`, `username_exists`. |
| `SampleDAO` | `SampleDAO.py` | All SQL for the `Samples` table: `add_sample` (auto-generates ID), `get_by_id`, `get_all_samples`, `get_by_status`, `search_by_patient`, `update_status`, `count_by_status`, `delete_sample`. |
| `TestDAO` | `TestDAO.py` | All SQL for the `Tests` table: `add_test`, `add_default_tests` (seeds 14 tests), `get_all_tests`, `get_test_names`, `get_by_name`, `update_test`, `delete_test`. |
| `ResultDAO` | `ResultDAO.py` | All SQL for the `Results` table, including multi-table JOIN queries: `add_result`, `get_results_by_sample`, `get_all_results`, `get_by_test_name`, `update_result_value`, `delete_result`. |

### Controller Classes — `controllers/`

| Class | File | Description |
|---|---|---|
| `AuthController` | `AuthController.py` | Manages login, logout, and `current_user` session. Provides user registration, password changes, role changes, and `seed_admin()` for first-run setup. |
| `SampleController` | `SampleController.py` | Handles sample registration with validation, status workflow enforcement (Pending→Processing→Completed), search, filtering, dashboard counts, and deletion. |
| `TestController` | `TestController.py` | Manages the test catalogue and result entry. Handles name-to-ID translation so the GUI works with names, not database IDs. |
| `ReportController` | `ReportController.py` | Assembles complete reports from multiple DAOs. Provides dashboard summary, single/batch report retrieval, `.txt` export, and formatted string output for GUI text widgets. |

### GUI Classes — `gui/`

| Class | File | Description |
|---|---|---|
| `LoginWindow` | `LoginWindow.py` | Entry screen. Calls `AuthController.login()` and opens the dashboard on success. |
| `DashboardWindow` | `DashboardWindow.py` | Main hub after login. Shows summary cards from `ReportController.get_dashboard_summary()` and provides navigation. Displays role-appropriate menu options. |
| `SampleForm` | `SampleForm.py` | Form for registering new samples, searching by patient name, viewing the sample list, and advancing status. Calls `SampleController`. |
| `ResultForm` | `ResultForm.py` | Form for selecting a sample, choosing a test from the dropdown (populated by `TestController.get_test_names()`), entering a result value, and viewing existing results. |

---

## Database Schema

All tables are created automatically when the application starts.

```
Users
─────────────────────────────────────────
user_id   INTEGER  PRIMARY KEY AUTOINCREMENT
username  TEXT     NOT NULL UNIQUE
password  TEXT     NOT NULL
role      TEXT     NOT NULL  CHECK(role IN ('Admin','Technician'))


Samples
─────────────────────────────────────────
sample_id    TEXT     PRIMARY KEY          (e.g. "S001", "S042")
patient_name TEXT     NOT NULL
date_added   TEXT     NOT NULL             (stored as "YYYY-MM-DD")
status       TEXT     NOT NULL  DEFAULT 'Pending'
                                CHECK(status IN ('Pending','Processing','Completed'))


Tests
─────────────────────────────────────────
test_id     INTEGER  PRIMARY KEY AUTOINCREMENT
test_name   TEXT     NOT NULL UNIQUE       (e.g. "CBC", "Urinalysis")
description TEXT


Results
─────────────────────────────────────────
result_id    INTEGER  PRIMARY KEY AUTOINCREMENT
sample_id    TEXT     NOT NULL  FOREIGN KEY → Samples(sample_id)  ON DELETE CASCADE
test_id      INTEGER  NOT NULL  FOREIGN KEY → Tests(test_id)      ON DELETE RESTRICT
result_value TEXT
```

**Relationships:**
- One `Sample` can have many `Results` (one per test performed)
- One `Test` can appear in many `Results` (same test type used across patients)
- Deleting a `Sample` automatically deletes all its `Results` (CASCADE)
- Deleting a `Test` is blocked if any `Results` reference it (RESTRICT)

---

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- No external packages required — the project uses only Python's standard library

Verify your Python version:
```bash
python --version
```

### Clone or Download

```bash
git clone <your-repository-url>
cd LABRATORYAUTOMATION
```

Or download the ZIP file and extract it.

### No Installation Needed

Because the project uses only built-in Python libraries (`sqlite3`, `tkinter`), there is no `pip install` step. Simply run the application.

---

## How to Run

Open a terminal in the project root folder (where `main.py` is located) and run:

```bash
python main.py
```

On the **first run**, the application will automatically:
1. Create the `lab.db` database file
2. Create all four tables (Users, Samples, Tests, Results)
3. Create the default Admin account
4. Load the 14 standard lab tests into the catalogue

On every subsequent run, the existing database is used and no data is overwritten.

---

## Default Login Credentials

```
Username : admin
Password : admin123
Role     : Admin
```

Use these credentials to log in for the first time and during the demonstration. The Admin account has full access to all features including user management and sample deletion.

To create Technician accounts after logging in, navigate to **Admin Panel → Manage Users → Add User**.

---

## Usage Walkthrough

The following walkthrough demonstrates the complete sample lifecycle.

### Step 1 — Log in
Launch the app and enter `admin` / `admin123`. The dashboard opens showing summary counts for Pending, Processing, and Completed samples.

### Step 2 — Register a sample
Navigate to **Samples → Add New Sample**. Enter the patient's full name (e.g. `John Doe`) and click Register. The system auto-generates a sample ID (e.g. `S001`) and sets status to `Pending`.

### Step 3 — Assign a test and record a result
Navigate to **Tests → Enter Result**. Select the sample ID from the list, choose a test from the dropdown (e.g. `CBC`), and enter the measured value (e.g. `Hemoglobin=13.5 g/dL, WBC=7000 cells/mcL`). Click Save.

### Step 4 — Advance the sample status
Return to the sample list, select `S001`, and click **Mark Processing**. Click again to **Mark Completed**.

### Step 5 — View the report
Navigate to **Reports → View Report**. Select `S001`. The report displays patient name, date, status, and all recorded test results.

### Step 6 — Export the report
From the report view, click **Export to TXT**. Choose a save location. A formatted `.txt` file is created containing the full patient report.

---

## Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.8+ | Primary programming language |
| `sqlite3` | Built-in | Database engine — no server required |
| `tkinter` | Built-in | Graphical user interface |
| `tkinter.ttk` | Built-in | Modern widgets (Treeview tables, Combobox dropdowns) |
| `datetime` | Built-in | Auto-stamping sample registration dates |
| `os` | Built-in | File path handling for report export |

---

## Team and Responsibilities

| Responsibility | Description |
|---|---|
| Database Layer | `DatabaseManager`, `UserDAO`, `SampleDAO`, `TestDAO`, `ResultDAO`, and all model classes in `models.py` |
| Controller Layer | `AuthController`, `SampleController`, `TestController`, `ReportController` |
| GUI Layer | `LoginWindow`, `DashboardWindow`, `SampleForm`, `ResultForm` |

### Architecture contract between layers

The three layers communicate through a strict interface agreement:

- **GUI → Controllers only.** No GUI file imports from `database/` directly.
- **Controllers → DAOs only.** No controller writes raw SQL.
- **DAOs → DatabaseManager only.** All DAOs share one connection created in `main.py`.
- **Models are shared.** Controllers convert raw database rows into model objects before returning them to the GUI.

This contract means each team member can build and test their layer independently, and integration only requires matching method signatures — not rewriting logic.

---

## Pre-loaded Test Catalogue

The following tests are automatically available on first run:

| Category | Tests |
|---|---|
| Blood | CBC, Blood Glucose, Cholesterol, Hemoglobin |
| Urine | Urinalysis, Urine Protein, Urine Glucose |
| Viral / Swab | COVID-19 PCR, Rapid Antigen, Influenza A/B |
| Hormone | TSH, T3, T4, Insulin |

Admins can add additional tests at any time through the application.
