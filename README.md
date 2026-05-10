# Laboratory Automation and Sample Management System (LASMS)

A desktop application built with **Python**, **Tkinter**, and **SQLite** for managing laboratory samples, test assignments, and patient results. Developed as a group project for a Programming for Data Engineering course.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Project Structure](#project-structure)
5. [Class Reference](#class-reference)
6. [Database Schema](#database-schema)
7. [Prerequisites and Installation](#prerequisites-and-installation)
8. [How to Run](#how-to-run)
9. [Account Creation and Roles](#account-creation-and-roles)
10. [Usage Walkthrough](#usage-walkthrough)
11. [Pre-loaded Test Catalogue](#pre-loaded-test-catalogue)
12. [Technologies Used](#technologies-used)
13. [Key Design Patterns](#key-design-patterns)

---

## Project Overview

LASMS is a fully functional laboratory information system that allows lab staff to:

- Register patient samples with auto-generated IDs (`S001`, `S002`, ...)
- Assign tests from a pre-loaded catalogue of 14 standard lab tests
- Track each sample through a defined status workflow: **Pending → Processing → Completed**
- Record and view test results linked to both patient and test name
- Generate and export lab reports to `.txt` files
- Manage user accounts with role-based access control (**Admin** / **Technician**)

The system enforces a strict three-layer architecture — GUI, Controllers, and Database — ensuring clean separation of concerns. No GUI file writes SQL. No controller imports Tkinter. No DAO contains business logic.

---

## Features

### User Management
- Secure login and logout with session tracking across the whole application
- Two roles: **Admin** and **Technician**
- Self-registration via the Register screen; creating an Admin account requires a secret admin code (`admin123`)
- Admins can also create, view, and delete accounts from the **Manage Users** panel (Admin-only)
- Password validation on registration: minimum 8 characters, at least one uppercase letter, at least one alphanumeric character
- Role-based access: the **Manage Users** button is hidden from Technician accounts entirely

### Sample Management
- Register new patient samples — the system auto-generates the next ID (e.g. `S006`)
- Track status through three stages: `Pending → Processing → Completed`
- Advancing to `Processing` happens automatically when a result is first recorded for a sample
- Mark samples as `Completed` manually from the Sample Form
- Search samples by patient name (partial match supported)
- Filter sample list by status (`All`, `Pending`, `Processing`, `Completed`)
- Dashboard summary showing live counts per status

### Test Management
- A catalogue of 14 standard lab tests is seeded automatically on first use
- Tests span four categories: Blood, Urine, Viral/Swab, and Hormone
- Test names are displayed in a dropdown — technicians never need to know internal test IDs

### Result Management
- Record a measured value for any sample + test combination
- Selecting a sample and test from dropdowns prevents data-entry errors
- Saving a result automatically advances the sample status to `Processing`
- Results are stored with JOIN support so patient name and test name are always accessible together

### Reporting
- Select any sample ID and view all recorded test results in a formatted display
- Export the report to a `.txt` file via a standard file-save dialog
- Reports include test name and measured value for each result recorded

---

## System Architecture

The system follows a strict three-layer architecture. Each layer only communicates with the layer directly below it.

```
┌─────────────────────────────────────────────┐
│                 GUI Layer                   │
│  LoginWindow    · RegisterWindow            │
│  DashboardWindow · SampleForm               │
│  ResultForm     · ReportForm                │
│  ManageUsersForm                            │
│  (Tkinter — handles display and input only) │
└──────────────────┬──────────────────────────┘
                   │  calls methods on
┌──────────────────▼──────────────────────────┐
│             Controller Layer                │
│  AuthController   · SampleController        │
│  TestController   · ReportController        │
│  (business logic, validation, rules)        │
└──────────────────┬──────────────────────────┘
                   │  queries via
┌──────────────────▼──────────────────────────┐
│             Database Layer                  │
│  DatabaseManager                            │
│  UserDAO · SampleDAO · TestDAO · ResultDAO  │
│  (all SQL — INSERT, SELECT, UPDATE, DELETE) │
└──────────────────┬──────────────────────────┘
                   │  reads / writes
┌──────────────────▼──────────────────────────┐
│              SQLite Database                │
│                 lab.db                      │
│   Users · Samples · Tests · Results        │
└─────────────────────────────────────────────┘
```

**Layer contract:**
- The **GUI** never imports from `database/` and never writes SQL
- **Controllers** never import Tkinter; they receive plain values and return model objects
- **DAOs** contain no business logic — only parameterised SQL queries
- **Models** are shared data objects that wrap raw database rows into Python objects with meaningful attributes and methods

---

## Project Structure

```
LabratoryAutomation/
│
├── main.py                      # Entry point — wires DB, controllers, and GUI together
│
├── models/
│   ├── User.py                  # User base class + Admin and Technician subclasses
│   ├── Sample.py                # Sample model with status properties and advance_status()
│   ├── Test.py                  # Test model (test_id, test_name, description)
│   └── Result.py                # Result model; supports plain and JOIN-enriched rows
│
├── database/
│   ├── DatabaseManager.py       # Opens SQLite connection, enables FK constraints, creates tables
│   ├── UserDAO.py               # CRUD for the Users table
│   ├── SampleDAO.py             # CRUD for the Samples table (includes auto-ID generation)
│   ├── TestDAO.py               # CRUD for the Tests table + default test seeding
│   └── ResultDAO.py             # CRUD for Results table; includes multi-table JOIN queries
│
├── controllers/
│   ├── AuthController.py        # Login, registration, password/role changes, user deletion
│   ├── SampleController.py      # Sample registration, status workflow, search, filtering
│   ├── TestController.py        # Test catalogue access and name-to-ID translation
│   └── ReportController.py      # Result recording, retrieval by sample/test, report assembly
│
├── gui/
│   ├── LoginWindow.py           # Login screen with link to registration
│   ├── RegisterWindow.py        # Account creation with role selection and admin code gate
│   ├── DashboardWindow.py       # Main navigation hub with live sample status summary
│   ├── SampleForm.py            # Add samples, search, filter, advance status
│   ├── ResultForm.py            # Select sample + test, enter result value
│   ├── ReportForm.py            # View results by sample, export to .txt
│   └── ManageUsersForm.py       # Admin-only: add and delete user accounts
│
├── lab.db                       # SQLite database — created automatically on first run
└── .gitignore
```

---

## Class Reference

The project contains **19 classes** across all layers.

### Model Classes — `models/`

| Class | Inherits From | Key Members |
|---|---|---|
| `User` | — | `user_id`, `username`, `password`, `role`; `check_password()`, `is_admin()`, `is_technician()`, `from_row()` |
| `Admin` | `User` | Role hardcoded to `"Admin"`; adds `can_manage_users()`, `can_delete_samples()`, `can_add_tests()` |
| `Technician` | `User` | Role hardcoded to `"Technician"`; adds `can_add_samples()`, `can_enter_results()` |
| `Sample` | — | `sample_id`, `patient_name`, `date_added`, `status`; `advance_status()`, `is_pending`, `is_processing`, `is_completed` (properties) |
| `Test` | — | `test_id`, `test_name`, `description`; `from_row()` |
| `Result` | — | `result_id`, `sample_id`, `test_id`, `result_value`, `patient_name`, `test_name`; `from_row()`, `from_joined_row()` |

### Database Layer — `database/`

| Class | File | Responsibilities |
|---|---|---|
| `DatabaseManager` | `DatabaseManager.py` | Opens the `lab.db` connection, enables `PRAGMA foreign_keys = ON`, creates all four tables on startup, exposes shared `conn` and `cursor` |
| `UserDAO` | `UserDAO.py` | `add_user`, `get_by_username`, `get_all_users`, `username_exists`, `update_password`, `update_role`, `delete_user` |
| `SampleDAO` | `SampleDAO.py` | `generate_sample_id`, `add_sample`, `get_by_id`, `get_all_samples`, `get_by_status`, `search_by_patient`, `get_by_date`, `update_status`, `count_by_status`, `delete_sample` |
| `TestDAO` | `TestDAO.py` | `add_test`, `add_default_tests` (seeds 14 tests, idempotent), `get_all_tests`, `get_test_names`, `get_by_name`, `update_test`, `delete_test` |
| `ResultDAO` | `ResultDAO.py` | `add_result`, `get_all_results`, `get_by_sample`, `get_by_test_name`, `get_by_id`, `sample_has_results`; key queries use `JOIN` across Samples and Tests |

### Controller Layer — `controllers/`

| Class | File | Responsibilities |
|---|---|---|
| `AuthController` | `AuthController.py` | Validates login credentials, enforces password rules on registration, manages role and password updates, wraps UserDAO results in `User` model objects |
| `SampleController` | `SampleController.py` | Validates patient name, delegates to SampleDAO, enforces the three valid statuses, wraps rows in `Sample` objects |
| `TestController` | `TestController.py` | Exposes test names for dropdowns, resolves name → test object for result recording, seeds default tests |
| `ReportController` | `ReportController.py` | Records results via ResultDAO, retrieves results by sample or test name, wraps rows in `Result` objects using `from_joined_row()` |

### GUI Layer — `gui/`

| Class | File | What it shows |
|---|---|---|
| `LoginWindow` | `LoginWindow.py` | Username/password form; link to registration; calls `AuthController.login()` |
| `RegisterWindow` | `RegisterWindow.py` | Username, password, role radio buttons, admin code field; calls `AuthController.register()` |
| `DashboardWindow` | `DashboardWindow.py` | Welcome message, live Pending/Processing/Completed counts, navigation buttons; Manage Users button only shown to Admins |
| `SampleForm` | `SampleForm.py` | Add sample, search by name, filter by status, Treeview table, mark Processing/Completed |
| `ResultForm` | `ResultForm.py` | Sample ID dropdown, test dropdown (from catalogue), result value entry, Save button |
| `ReportForm` | `ReportForm.py` | Sample ID dropdown, View Report (populates Text widget), Export to TXT |
| `ManageUsersForm` | `ManageUsersForm.py` | Add user form, Treeview of all users, Delete selected user (Admin-only screen) |

---

## Database Schema

All tables are created automatically by `DatabaseManager` when the application starts. No manual setup is required.

```
Users
─────────────────────────────────────────────────────
user_id   INTEGER  PRIMARY KEY AUTOINCREMENT
username  TEXT     NOT NULL  UNIQUE
password  TEXT     NOT NULL
role      TEXT     NOT NULL  CHECK(role IN ('Admin', 'Technician'))


Samples
─────────────────────────────────────────────────────
sample_id    TEXT     PRIMARY KEY              (e.g. "S001", "S042")
patient_name TEXT     NOT NULL
date_added   TEXT     NOT NULL                 (stored as "YYYY-MM-DD")
status       TEXT     NOT NULL  DEFAULT 'Pending'
                                CHECK(status IN ('Pending','Processing','Completed'))


Tests
─────────────────────────────────────────────────────
test_id     INTEGER  PRIMARY KEY AUTOINCREMENT
test_name   TEXT     NOT NULL  UNIQUE           (e.g. "CBC", "TSH")
description TEXT


Results
─────────────────────────────────────────────────────
result_id    INTEGER  PRIMARY KEY AUTOINCREMENT
sample_id    TEXT     NOT NULL  → Samples(sample_id)  ON DELETE CASCADE
test_id      INTEGER  NOT NULL  → Tests(test_id)      ON DELETE RESTRICT
result_value TEXT
```

**Relationships:**
- One `Sample` → many `Results` (one result per test performed on it)
- One `Test` → many `Results` (same test type used across many patients)
- Deleting a `Sample` automatically deletes all its `Results` (CASCADE)
- Deleting a `Test` is blocked if any `Results` reference it (RESTRICT)

---

## Prerequisites and Installation

### Requirements

- **Python 3.8 or higher**
- No external packages — the project uses only Python's standard library (`tkinter`, `sqlite3`, `datetime`, `os`)

Verify your Python version:

```bash
python --version
```

### Get the code

```bash
git clone <your-repository-url>
cd LabratoryAutomation
```

Or download and unzip the project archive, then open a terminal inside the `LabratoryAutomation/` folder.

---

## How to Run

From the project root (the folder containing `main.py`):

```bash
python main.py
```

**On first run**, the application automatically:
1. Creates `lab.db` in the current directory
2. Creates all four tables (`Users`, `Samples`, `Tests`, `Results`)
3. Seeds the 14 standard lab tests into the `Tests` table

On every subsequent run, the existing database is reused and no data is overwritten.

---

## Account Creation and Roles

There is no default account. You create the first account on the Register screen.

### Creating an Admin account

1. Click **Create Account** on the login screen
2. Enter a username and password
3. Select **Admin** as the role
4. Enter the admin code: `admin123`
5. Click **Create Account**

### Creating a Technician account

Technician accounts can be created in two ways:

**Via the Register screen** (self-service):
1. Click **Create Account** on the login screen
2. Enter credentials and select **Technician** — no admin code required

**Via Manage Users** (Admin-only):
1. Log in as an Admin
2. Navigate to **Manage Users** from the dashboard
3. Fill in the username, password, and select a role, then click **Add User**

### Password requirements

Passwords must:
- Be at least 8 characters long
- Contain at least one uppercase letter
- Contain at least one number or special character

### Role permissions

| Action | Admin | Technician |
|---|:---:|:---:|
| Login / Logout | ✓ | ✓ |
| View Dashboard | ✓ | ✓ |
| Add / Search Samples | ✓ | ✓ |
| Mark Sample Processing / Completed | ✓ | ✓ |
| Record Results | ✓ | ✓ |
| View / Export Reports | ✓ | ✓ |
| Manage Users (add / delete accounts) | ✓ | ✗ |

---

## Usage Walkthrough

### Step 1 — Create an account and log in
Launch the app with `python main.py`. Click **Create Account**, fill in credentials, and select a role. Return to the login screen and sign in. The dashboard appears showing live sample counts.

### Step 2 — Register a patient sample
Click **Sample Form**. Enter the patient's name (e.g. `Jane Smith`) and click **Add Sample**. The system auto-generates a sample ID (e.g. `S001`) with status `Pending`. The new sample appears in the table immediately.

### Step 3 — Record a test result
Click **Home** then **Result Form**. Select the sample ID from the dropdown, choose a test (e.g. `CBC`) from the test catalogue dropdown, and type the measured value (e.g. `Hemoglobin: 13.5 g/dL, WBC: 7200 cells/µL`). Click **Save**. The sample status automatically advances to `Processing`.

### Step 4 — Mark the sample as completed
Return to **Sample Form**, select `S001` in the table, and click **Completed**. The status updates to `Completed` and the dashboard count adjusts.

### Step 5 — View and export the report
Click **Reports** from the dashboard. Select `S001` from the dropdown and click **View Report**. All recorded test results appear in the text area. Click **Export to TXT** to save the report to a file.

### Step 6 (Admin only) — Manage users
Click **Manage Users** from the dashboard. The current user list is shown. Use the form at the top to add a new account, or select a row and click **Delete** to remove a user.

---

## Pre-loaded Test Catalogue

The following 14 tests are seeded automatically on first run and are available in the test dropdown immediately:

| Category | Test Name | Description |
|---|---|---|
| Blood | CBC | Complete Blood Count — Hemoglobin, WBC, Platelets |
| Blood | Blood Glucose | Blood sugar level (fasting or random) |
| Blood | Cholesterol | Total cholesterol, LDL, HDL, Triglycerides |
| Blood | Hemoglobin | Single hemoglobin value measurement |
| Urine | Urinalysis | pH, Protein, Glucose, Nitrites — full urine panel |
| Urine | Urine Protein | Detects abnormal protein levels in urine |
| Urine | Urine Glucose | Checks for glucose presence in urine |
| Viral / Swab | COVID-19 PCR | Nasal swab — PCR method, Positive or Negative |
| Viral / Swab | Rapid Antigen | Nasal swab — rapid antigen test |
| Viral / Swab | Influenza A/B | Tests for Influenza A and B strains |
| Hormone | TSH | Thyroid Stimulating Hormone — mIU/L |
| Hormone | T3 | Triiodothyronine thyroid hormone |
| Hormone | T4 | Thyroxine thyroid hormone |
| Hormone | Insulin | Fasting insulin level |

Seeding is idempotent — calling `add_default_tests()` multiple times will never create duplicates.

---

## Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.8+ | Primary programming language |
| `sqlite3` | Built-in | Embedded database engine — no server required |
| `tkinter` | Built-in | Desktop GUI framework |
| `tkinter.ttk` | Built-in | Modern widgets: `Treeview` tables, `Combobox` dropdowns |
| `datetime` | Built-in | Auto-stamping `date_added` when a sample is registered |
| `os` | Built-in | File path resolution for report export |

---

## Key Design Patterns

### Data Access Object (DAO)
Each DAO class is responsible for exactly one database table. Controllers never write SQL; they call DAO methods and receive raw `sqlite3.Row` objects back.

### Model / from_row factory
Every model class provides a `from_row(row)` classmethod that converts a raw database row into a typed Python object. The `Result` model additionally provides `from_joined_row(row)` for queries that JOIN across tables, populating `patient_name` and `test_name` without a second query.

### Dependency Injection
`DatabaseManager` is created once in `main.py` and passed into every DAO. All DAOs share a single connection to `lab.db`. Controllers receive their DAOs via `__init__`, and GUI classes receive their controllers the same way.

### Parameterised queries
All SQL in the DAO layer uses `?` placeholders rather than f-strings or string concatenation. This prevents SQL injection regardless of what a user types into any input field.

```python
# Safe — sqlite3 fills the placeholder, never interprets user input as SQL
cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))

# Unsafe — never done in this codebase
cursor.execute(f"SELECT * FROM Users WHERE username = '{username}'")
```

### Role-based access enforcement
Role checks happen at two levels. The GUI hides buttons that a role cannot access (e.g. Manage Users is not rendered for Technicians). The controller layer (`open_manage_users` in `main.py`) also guards the action with a role check, so bypassing the UI is not sufficient.