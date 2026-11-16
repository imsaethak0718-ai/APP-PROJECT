# Examination Registration Management System

Built with **Python Tkinter Only** (No external third-party dependencies required).

---

## 👥 Project Team Members

| Registration Number | Student Name |
| :--- | :--- |
| **RA2511033010093** | **ADITYA KUMAR SINGH** |
| **RA2511033010094** | **VARUN VAIDYANATHAN** |
| **RA2511033010095** | **MANGALWEDHEKAR SARTHAK KEDAR** |

---

## 📋 Project Overview & Specifications

This desktop application manages academic examination registrations with input validation, data persistence, and interactive GUI controls.

### 1. Form Fields
- **Registration Number**: Text input for the unique student registration ID (*Mandatory*).
- **Student Name**: Text input for the full student name (*Mandatory*).
- **Subject**: Text input for the subject/course name (*Mandatory*).
- **Examination Fee**: Numeric input for fee amount (*Mandatory, non-negative number $\ge 0$*).

### 2. Selection Widgets
- **`OptionMenu`**: Allows selection of the Examination Type:
  - *Regular Semester*
  - *Mid-Term Examination*
  - *Re-Evaluation*
  - *Improvement*
  - *Special Examination*
- **`Checkbutton`**: Toggle for supplementary / arrear examinations (`Supplementary Exam: Yes/No`).

### 3. Required Operations
1. **Register a Student (`✚ Register Student`)**:
   - Validates mandatory fields and non-negative examination fee.
   - Prevents duplicate registration numbers.
   - Adds the new record, updates the `Listbox`, and saves to JSON.
2. **Search using Registration Number (`🔍 Search (Reg No)`)**:
   - Searches records by registration number.
   - Auto-populates all form inputs with the matched record details.
   - Highlights the entry in the `Listbox`.
3. **Update Examination Details (`✎ Update Details`)**:
   - Validates inputs and updates an existing student's subject, fee, exam type, or supplementary status.
   - Instantly updates the `Listbox` view.
4. **Delete a Registration (`🗑 Delete Registration`)**:
   - Asks for confirmation before removing the selected student.
   - Refreshes the `Listbox` and resets the form.
5. **Display All Registrations in a `Listbox`**:
   - Formatted mono-spaced table view displaying Reg No, Student Name, Subject, Exam Type, Supplementary status, and Fee.
   - Includes horizontal and vertical scrollbars.
   - **Interactive Auto-Load**: Clicking on any entry in the `Listbox` automatically loads that student's details into the input form.
   - Real-time **Filter / Search Bar** to filter displayed rows.
   - Live **Statistics counter**: Shows total registrations count and total fees collected.

### 4. Validation Rules
- **Registration Number**: Mandatory (cannot be blank or whitespace only).
- **Student Name**: Mandatory (cannot be blank or whitespace only).
- **Examination Fee**: Mandatory and must be a valid non-negative number (`fee >= 0`). Rejects strings, negative numbers, or invalid formats with descriptive error dialogs.

---

## 🚀 How to Run the Application

Run the application using Python 3:

```bash
# Option 1: Run main.py
python3 main.py

# Option 2: Run exam_registration_app.py directly
python3 exam_registration_app.py

# Option 3: Direct execution (macOS/Linux)
./exam_registration_app.py
```

---

## 🧪 Running Automated Unit Tests

A comprehensive unit and functional test suite (`test_app.py`) is included to verify all operations and validations:

```bash
python3.13 test_app.py
```

All 9 tests verify:
- Pre-population of initial team member registrations
- Mandatory field validations (Reg No, Name, Subject)
- Non-negative numeric fee validation
- Registering new students
- Duplicate prevention
- Searching by registration number
- Updating student details
- Deleting registrations with confirmation
- Listbox click-to-load interaction

