#!/usr/bin/env python3
"""
================================================================================
EXAMINATION REGISTRATION MANAGEMENT SYSTEM
Developed using Python's Tkinter Library Only

Project Team Members:
  - RA2511033010093: ADITYA KUMAR SINGH
  - RA2511033010094: VARUN VAIDYANATHAN
  - RA2511033010095: MANGALWEDHEKAR SARTHAK KEDAR

Form Fields:
  • Registration Number (Mandatory)
  • Student Name (Mandatory)
  • Subject
  • Examination Fee (Mandatory, Non-negative number)

Selection Widgets:
  • OptionMenu for Examination Type
  • Checkbutton for Supplementary Examination

Required Operations:
  • Register a student
  • Search using registration number
  • Update examination details
  • Delete a registration
  • Display all registrations in a Listbox
================================================================================
"""

import sys
import os
import json

# Fallback: if default python environment lacks _tkinter, re-exec with a Python interpreter that has Tkinter
try:
    import tkinter as tk
    from tkinter import messagebox, font
except ModuleNotFoundError:
    import shutil
    candidates = [
        "python3.13",
        "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3",
        "/usr/bin/python3"
    ]
    for cand in candidates:
        cand_path = shutil.which(cand) or (cand if os.path.exists(cand) else None)
        if cand_path and cand_path != sys.executable:
            os.execv(cand_path, [cand_path] + sys.argv)
    raise

class ExamRegistrationApp:
    DATA_FILE = "exam_registrations.json"

    # Text Field Styling
    ENTRY_FG = "#1e3a8a"         # Crisp, high-contrast Navy Blue font for entered text
    ENTRY_BG = "#ffffff"         # Clean white background
    ENTRY_CURSOR = "#000000"     # High-visibility dark cursor

    # Examination Type Options for OptionMenu
    EXAM_TYPES = [
        "Regular Semester",
        "Mid-Term Examination",
        "Re-Evaluation",
        "Improvement",
        "Special Examination"
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Examination Registration Management System")
        self.root.geometry("1100;730".replace(";", "x"))
        self.root.minsize(1000, 650)
        self.root.configure(bg="#f1f5f9")

        # In-memory registrations dictionary: {reg_no: dict}
        self.registrations = {}

        # Colors & Styling
        self.theme = {
            "primary": "#1e40af",       # Deep Royal Blue
            "primary_dark": "#1e3a8a",  # Darker Blue
            "accent": "#0284c7",       # Light Blue
            "bg": "#f8fafc",           # Crisp Light Background
            "card_bg": "#ffffff",      # White Card
            "card_border": "#cbd5e1",  # Border
            "text_main": "#0f172a",    # Dark Slate
            "text_muted": "#475569",   # Muted Slate
            "success": "#16a34a",      # Green
            "warning": "#d97706",      # Amber
            "danger": "#dc2626",       # Red
            "secondary": "#64748b"     # Slate Gray
        }

        # Setup custom fonts
        self.setup_fonts()

        # Build Interface
        self.create_widgets()

        # Load initial or saved data
        self.load_data()

        # Populate Listbox initially
        self.display_all_registrations()

    def setup_fonts(self):
        """Configure clean, legible typography."""
        self.font_title = font.Font(family="Helvetica", size=17, weight="bold")
        self.font_subtitle = font.Font(family="Helvetica", size=10, weight="normal")
        self.font_team = font.Font(family="Helvetica", size=9, weight="bold")
        self.font_section = font.Font(family="Helvetica", size=12, weight="bold")
        self.font_label = font.Font(family="Helvetica", size=10, weight="bold")
        self.font_entry = font.Font(family="Helvetica", size=11, weight="bold")
        self.font_mono = font.Font(family="Courier", size=10, weight="normal")
        self.font_button = font.Font(family="Helvetica", size=10, weight="bold")
        self.font_status = font.Font(family="Helvetica", size=9, weight="normal")

    def create_widgets(self):
        """Construct the complete user interface layout."""
        # 1. Top Header Frame
        header_frame = tk.Frame(self.root, bg=self.theme["primary_dark"], pady=12, padx=20)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        title_lbl = tk.Label(
            header_frame,
            text="EXAMINATION REGISTRATION MANAGEMENT SYSTEM",
            font=self.font_title,
            fg="#ffffff",
            bg=self.theme["primary_dark"]
        )
        title_lbl.pack(anchor=tk.CENTER)

        sub_lbl = tk.Label(
            header_frame,
            text="Academic Assessment & Course Registration Portal • Python Tkinter Project",
            font=self.font_subtitle,
            fg="#cbd5e1",
            bg=self.theme["primary_dark"]
        )
        sub_lbl.pack(anchor=tk.CENTER, pady=(2, 6))

        # Project Team Members Banner
        team_frame = tk.Frame(header_frame, bg="#172554", bd=1, relief=tk.SOLID, padx=10, pady=4)
        team_frame.pack(fill=tk.X, pady=(2, 0))

        team_text = (
            "Team Members:  RA2511033010093 - ADITYA KUMAR SINGH  |  "
            "RA2511033010094 - VARUN VAIDYANATHAN  |  "
            "RA2511033010095 - MANGALWEDHEKAR SARTHAK KEDAR"
        )
        team_lbl = tk.Label(
            team_frame,
            text=team_text,
            font=self.font_team,
            fg="#93c5fd",
            bg="#172554"
        )
        team_lbl.pack(anchor=tk.CENTER)

        # 2. Main Content Split (Left = Form & Actions, Right = Search & Listbox)
        content_frame = tk.Frame(self.root, bg="#f1f5f9", padx=16, pady=12)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Configure 2 columns: Left column fixed/proportional, Right column takes remaining space
        content_frame.columnconfigure(0, weight=4, minsize=420)
        content_frame.columnconfigure(1, weight=6, minsize=520)
        content_frame.rowconfigure(0, weight=1)

        # Build Left Panel: Registration Form & Action Buttons
        self.create_form_panel(content_frame)

        # Build Right Panel: Listbox, Search, and Summary View
        self.create_list_panel(content_frame)

        # 3. Bottom Status Bar
        self.create_status_bar()

    def create_form_panel(self, parent):
        """Construct the input form and operation buttons on the left panel."""
        left_container = tk.Frame(parent, bg="#ffffff", bd=1, relief=tk.GROOVE, padx=16, pady=14)
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Panel Section Header
        form_title = tk.Label(
            left_container,
            text="Student Registration Form",
            font=self.font_section,
            fg=self.theme["primary_dark"],
            bg="#ffffff"
        )
        form_title.pack(anchor=tk.W, pady=(0, 2))

        form_desc = tk.Label(
            left_container,
            text="Fill required fields (*) to register or update examination records.",
            font=self.font_subtitle,
            fg=self.theme["text_muted"],
            bg="#ffffff"
        )
        form_desc.pack(anchor=tk.W, pady=(0, 12))

        # Input Fields Container
        fields_frame = tk.Frame(left_container, bg="#ffffff")
        fields_frame.pack(fill=tk.X, expand=False)
        fields_frame.columnconfigure(1, weight=1)

        # --- Field 1: Registration Number ---
        lbl_reg = tk.Label(fields_frame, text="Registration No * :", font=self.font_label, fg=self.theme["text_main"], bg="#ffffff")
        lbl_reg.grid(row=0, column=0, sticky=tk.W, pady=6, padx=(0, 8))

        reg_input_box = tk.Frame(fields_frame, bg="#ffffff")
        reg_input_box.grid(row=0, column=1, sticky="ew", pady=6)
        reg_input_box.columnconfigure(0, weight=1)

        self.entry_reg_no = tk.Entry(
            reg_input_box,
            font=self.font_entry,
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            insertbackground=self.ENTRY_CURSOR,
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            relief=tk.SOLID,
            bd=1
        )
        self.entry_reg_no.grid(row=0, column=0, sticky="ew")

        # --- Field 2: Student Name ---
        lbl_name = tk.Label(fields_frame, text="Student Name * :", font=self.font_label, fg=self.theme["text_main"], bg="#ffffff")
        lbl_name.grid(row=1, column=0, sticky=tk.W, pady=6, padx=(0, 8))
        self.entry_name = tk.Entry(
            fields_frame,
            font=self.font_entry,
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            insertbackground=self.ENTRY_CURSOR,
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            relief=tk.SOLID,
            bd=1
        )
        self.entry_name.grid(row=1, column=1, sticky="ew", pady=6)

        # --- Field 3: Subject ---
        lbl_subj = tk.Label(fields_frame, text="Subject * :", font=self.font_label, fg=self.theme["text_main"], bg="#ffffff")
        lbl_subj.grid(row=2, column=0, sticky=tk.W, pady=6, padx=(0, 8))
        self.entry_subject = tk.Entry(
            fields_frame,
            font=self.font_entry,
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            insertbackground=self.ENTRY_CURSOR,
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            relief=tk.SOLID,
            bd=1
        )
        self.entry_subject.grid(row=2, column=1, sticky="ew", pady=6)

        # --- Field 4: Examination Fee ---
        lbl_fee = tk.Label(fields_frame, text="Examination Fee * (₹) :", font=self.font_label, fg=self.theme["text_main"], bg="#ffffff")
        lbl_fee.grid(row=3, column=0, sticky=tk.W, pady=6, padx=(0, 8))
        self.entry_fee = tk.Entry(
            fields_frame,
            font=self.font_entry,
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            insertbackground=self.ENTRY_CURSOR,
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            relief=tk.SOLID,
            bd=1
        )
        self.entry_fee.grid(row=3, column=1, sticky="ew", pady=6)

        # --- Field 5: OptionMenu for Examination Type ---
        lbl_type = tk.Label(fields_frame, text="Examination Type :", font=self.font_label, fg=self.theme["text_main"], bg="#ffffff")
        lbl_type.grid(row=4, column=0, sticky=tk.W, pady=6, padx=(0, 8))

        self.exam_type_var = tk.StringVar(self.root)
        self.exam_type_var.set(self.EXAM_TYPES[0])  # Default: Regular Semester
        self.option_menu_exam = tk.OptionMenu(
            fields_frame,
            self.exam_type_var,
            *self.EXAM_TYPES
        )
        self.option_menu_exam.config(
            font=self.font_entry,
            bg="#f1f5f9",
            fg=self.theme["text_main"],
            relief=tk.SOLID,
            bd=1,
            highlightthickness=0,
            cursor="hand2"
        )
        self.option_menu_exam["menu"].config(font=self.font_entry, bg="#ffffff", fg=self.theme["text_main"])
        self.option_menu_exam.grid(row=4, column=1, sticky="ew", pady=6)

        # --- Field 6: Checkbutton for Supplementary Examination ---
        lbl_supp = tk.Label(fields_frame, text="Supplementary Exam :", font=self.font_label, fg=self.theme["text_main"], bg="#ffffff")
        lbl_supp.grid(row=5, column=0, sticky=tk.W, pady=6, padx=(0, 8))

        self.is_supplementary_var = tk.IntVar(value=0)
        self.chk_supplementary = tk.Checkbutton(
            fields_frame,
            text="Yes, this is a Supplementary / Arrear Examination",
            variable=self.is_supplementary_var,
            font=self.font_subtitle,
            fg=self.theme["text_main"],
            bg="#ffffff",
            activebackground="#ffffff",
            selectcolor="#ffffff",
            cursor="hand2"
        )
        self.chk_supplementary.grid(row=5, column=1, sticky="w", pady=6)

        # Validation Info note
        note_lbl = tk.Label(
            left_container,
            text="• Validation: Reg No & Name mandatory | Fee must be non-negative (>= 0).",
            font=font.Font(family="Helvetica", size=8, slant="italic"),
            fg="#64748b",
            bg="#ffffff"
        )
        note_lbl.pack(anchor=tk.W, pady=(8, 12))

        # Separator line
        sep = tk.Frame(left_container, height=1, bg="#e2e8f0")
        sep.pack(fill=tk.X, pady=(0, 12))

        # --- Operation Buttons Grid ---
        btn_frame = tk.Frame(left_container, bg="#ffffff")
        btn_frame.pack(fill=tk.BOTH, expand=True)
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        # 1. Register Button
        btn_register = tk.Button(
            btn_frame,
            text="✚ Register Student",
            command=self.register_student,
            font=self.font_button,
            bg=self.theme["success"],
            fg="#15803d",
            activebackground="#15803d",
            activeforeground="#166534",
            highlightbackground="#bbf7d0",
            relief=tk.RAISED,
            padx=10,
            pady=8,
            cursor="hand2"
        )
        btn_register.grid(row=0, column=0, columnspan=2, sticky="ew", pady=4)

        # 2. Update Details Button
        btn_update = tk.Button(
            btn_frame,
            text="✎ Update Details",
            command=self.update_student,
            font=self.font_button,
            bg=self.theme["primary"],
            fg="#1e40af",
            activebackground=self.theme["primary_dark"],
            activeforeground="#1e3a8a",
            highlightbackground="#bfdbfe",
            relief=tk.RAISED,
            padx=10,
            pady=7,
            cursor="hand2"
        )
        btn_update.grid(row=1, column=0, sticky="ew", padx=(0, 4), pady=4)

        # 3. Search Button
        btn_search = tk.Button(
            btn_frame,
            text="🔍 Search (Reg No)",
            command=self.search_student,
            font=self.font_button,
            bg=self.theme["accent"],
            fg="#0369a1",
            activebackground="#0369a1",
            activeforeground="#0284c7",
            highlightbackground="#bae6fd",
            relief=tk.RAISED,
            padx=10,
            pady=7,
            cursor="hand2"
        )
        btn_search.grid(row=1, column=1, sticky="ew", padx=(4, 0), pady=4)

        # 4. Delete Record Button
        btn_delete = tk.Button(
            btn_frame,
            text="🗑 Delete Registration",
            command=self.delete_student,
            font=self.font_button,
            bg=self.theme["danger"],
            fg="#b91c1c",
            activebackground="#b91c1c",
            activeforeground="#991b1b",
            highlightbackground="#fecaca",
            relief=tk.RAISED,
            padx=10,
            pady=7,
            cursor="hand2"
        )
        btn_delete.grid(row=2, column=0, sticky="ew", padx=(0, 4), pady=4)

        # 5. Clear Form Button
        btn_clear = tk.Button(
            btn_frame,
            text="↺ Clear / Reset Form",
            command=self.clear_form,
            font=self.font_button,
            bg=self.theme["secondary"],
            fg="#334155",
            activebackground="#475569",
            activeforeground="#1e293b",
            highlightbackground="#e2e8f0",
            relief=tk.RAISED,
            padx=10,
            pady=7,
            cursor="hand2"
        )
        btn_clear.grid(row=2, column=1, sticky="ew", padx=(4, 0), pady=4)

    def create_list_panel(self, parent):
        """Construct the Listbox, search filter, and listview on the right panel."""
        right_container = tk.Frame(parent, bg="#ffffff", bd=1, relief=tk.GROOVE, padx=16, pady=14)
        right_container.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_container.rowconfigure(2, weight=1)
        right_container.columnconfigure(0, weight=1)

        # Header for List Section
        list_header = tk.Frame(right_container, bg="#ffffff")
        list_header.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        list_header.columnconfigure(0, weight=1)

        lbl_list_title = tk.Label(
            list_header,
            text="Registered Students Directory (Listbox)",
            font=self.font_section,
            fg=self.theme["primary_dark"],
            bg="#ffffff"
        )
        lbl_list_title.pack(anchor=tk.W)

        lbl_list_subtitle = tk.Label(
            list_header,
            text="Click any entry below to auto-load details into the form for viewing or updating.",
            font=self.font_subtitle,
            fg=self.theme["text_muted"],
            bg="#ffffff"
        )
        lbl_list_subtitle.pack(anchor=tk.W)

        # Quick Search Bar & Refresh Bar
        search_bar = tk.Frame(right_container, bg="#f8fafc", bd=1, relief=tk.SOLID, padx=8, pady=6)
        search_bar.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        search_bar.columnconfigure(1, weight=1)

        lbl_quick = tk.Label(search_bar, text="Filter / Find:", font=self.font_label, fg=self.theme["text_main"], bg="#f8fafc")
        lbl_quick.grid(row=0, column=0, padx=(0, 6), sticky=tk.W)

        self.entry_quick_search = tk.Entry(
            search_bar,
            font=self.font_entry,
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            insertbackground=self.ENTRY_CURSOR,
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            relief=tk.SOLID,
            bd=1
        )
        self.entry_quick_search.grid(row=0, column=1, sticky="ew", padx=(0, 6))
        self.entry_quick_search.bind("<KeyRelease>", lambda event: self.filter_listbox())

        btn_quick_find = tk.Button(
            search_bar,
            text="Filter",
            command=self.filter_listbox,
            font=self.font_subtitle,
            bg=self.theme["accent"],
            fg="#0369a1",
            activeforeground="#0284c7",
            highlightbackground="#bae6fd",
            relief=tk.RAISED,
            padx=8,
            cursor="hand2"
        )
        btn_quick_find.grid(row=0, column=2, padx=(0, 4))

        btn_show_all = tk.Button(
            search_bar,
            text="Show All",
            command=self.display_all_registrations,
            font=self.font_subtitle,
            bg=self.theme["secondary"],
            fg="#334155",
            activeforeground="#1e293b",
            highlightbackground="#e2e8f0",
            relief=tk.RAISED,
            padx=8,
            cursor="hand2"
        )
        btn_show_all.grid(row=0, column=3)

        # Listbox Column Headers (Fixed-width alignment header bar)
        header_text = f"{'REG. NUMBER':<18} | {'STUDENT NAME':<24} | {'SUBJECT':<18} | {'EXAM TYPE':<16} | {'SUPP?':<6} | {'FEE (₹)':>10}"
        header_bar = tk.Label(
            right_container,
            text=header_text,
            font=self.font_mono,
            bg="#1e293b",
            fg="#f8fafc",
            anchor=tk.W,
            padx=6,
            pady=4
        )
        header_bar.grid(row=2, column=0, sticky="ew", pady=(0, 2))

        # Listbox with Scrollbars (Vertical & Horizontal)
        listbox_frame = tk.Frame(right_container, bg="#ffffff")
        listbox_frame.grid(row=3, column=0, sticky="nsew")
        right_container.rowconfigure(3, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        listbox_frame.columnconfigure(0, weight=1)

        self.records_listbox = tk.Listbox(
            listbox_frame,
            font=self.font_mono,
            bg="#ffffff",
            fg="#0f172a",
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            activestyle="none",
            bd=1,
            relief=tk.SOLID,
            highlightthickness=0
        )
        self.records_listbox.grid(row=0, column=0, sticky="nsew")

        v_scroll = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.records_listbox.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")

        h_scroll = tk.Scrollbar(listbox_frame, orient=tk.HORIZONTAL, command=self.records_listbox.xview)
        h_scroll.grid(row=1, column=0, sticky="ew")

        self.records_listbox.config(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Bind Listbox selection to automatically populate the form fields
        self.records_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        # Listbox Footer with Quick Stats
        self.stats_label = tk.Label(
            right_container,
            text="Total Registrations: 0 | Total Examination Fees: ₹0.00",
            font=self.font_label,
            fg=self.theme["primary_dark"],
            bg="#f1f5f9",
            bd=1,
            relief=tk.SOLID,
            padx=8,
            pady=6,
            anchor=tk.W
        )
        self.stats_label.grid(row=4, column=0, sticky="ew", pady=(8, 0))

    def create_status_bar(self):
        """Construct the bottom status notification strip."""
        status_frame = tk.Frame(self.root, bg="#e2e8f0", bd=1, relief=tk.SUNKEN, padx=12, pady=4)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_var = tk.StringVar(value="System Ready. Enter details to register students or search existing records.")
        status_lbl = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=self.font_status,
            fg=self.theme["text_muted"],
            bg="#e2e8f0",
            anchor=tk.W
        )
        status_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

        system_info = tk.Label(
            status_frame,
            text="Tkinter Examination System v1.0",
            font=self.font_status,
            fg="#64748b",
            bg="#e2e8f0"
        )
        system_info.pack(side=tk.RIGHT)

    def set_status(self, message):
        """Update message in status bar."""
        self.status_var.set(message)

    # =========================================================================
    # REQUIRED OPERATIONS & VALIDATIONS
    # =========================================================================

    def validate_inputs(self, is_update=False):
        """
        Validate all form fields:
          1. Registration number is mandatory.
          2. Student name is mandatory.
          3. Subject is mandatory.
          4. Examination fee must be a valid non-negative number.
        Returns (is_valid, cleaned_data_dict)
        """
        reg_no = self.entry_reg_no.get().strip()
        name = self.entry_name.get().strip()
        subject = self.entry_subject.get().strip()
        fee_raw = self.entry_fee.get().strip()
        exam_type = self.exam_type_var.get().strip()
        is_supp = (self.is_supplementary_var.get() == 1)

        # 1. Registration Number validation (Mandatory)
        if not reg_no:
            messagebox.showerror(
                "Validation Error",
                "Registration Number is mandatory!\nPlease enter a valid registration number."
            )
            self.entry_reg_no.focus_set()
            return False, None

        # 2. Student Name validation (Mandatory)
        if not name:
            messagebox.showerror(
                "Validation Error",
                "Student Name is mandatory!\nPlease enter the student's full name."
            )
            self.entry_name.focus_set()
            return False, None

        # 3. Subject validation (Mandatory)
        if not subject:
            messagebox.showerror(
                "Validation Error",
                "Subject is mandatory!\nPlease enter the course or subject name."
            )
            self.entry_subject.focus_set()
            return False, None

        # 4. Examination Fee validation (Mandatory, Non-negative number)
        if not fee_raw:
            messagebox.showerror(
                "Validation Error",
                "Examination Fee is mandatory!\nPlease enter the examination fee amount."
            )
            self.entry_fee.focus_set()
            return False, None

        try:
            fee = float(fee_raw)
            if fee < 0:
                raise ValueError("Fee cannot be negative")
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Examination Fee must be a valid non-negative number!\n"
                f"Received invalid value: '{fee_raw}'.\nPlease enter 0 or a positive number (e.g. 1500, 1200.50)."
            )
            self.entry_fee.focus_set()
            return False, None

        cleaned_data = {
            "reg_no": reg_no,
            "name": name,
            "subject": subject,
            "fee": fee,
            "exam_type": exam_type if exam_type else self.EXAM_TYPES[0],
            "is_supplementary": is_supp
        }
        return True, cleaned_data

    def register_student(self):
        """Operation: Register a student with validations."""
        valid, data = self.validate_inputs(is_update=False)
        if not valid:
            return

        reg_no = data["reg_no"]

        # Check for duplicate registration
        if reg_no in self.registrations:
            existing = self.registrations[reg_no]
            messagebox.showwarning(
                "Duplicate Registration",
                f"Registration Number '{reg_no}' is already registered!\n\n"
                f"Existing Student: {existing['name']}\nSubject: {existing['subject']}\n\n"
                "To modify this record, click 'Update Details' instead."
            )
            return

        # Add to records
        self.registrations[reg_no] = data
        self.save_data()
        self.display_all_registrations()
        self.highlight_registration(reg_no)

        msg = f"Student '{data['name']}' ({reg_no}) registered successfully!"
        self.set_status(msg)
        messagebox.showinfo("Registration Successful", msg)

    def search_student(self):
        """Operation: Search using registration number and auto-fill form."""
        reg_no = self.entry_reg_no.get().strip()

        # If entry is empty, check quick search box or prompt user
        if not reg_no:
            quick_reg = self.entry_quick_search.get().strip()
            if quick_reg:
                reg_no = quick_reg

        if not reg_no:
            messagebox.showwarning(
                "Search Required",
                "Please enter a Registration Number in the 'Registration No' field to search."
            )
            self.entry_reg_no.focus_set()
            return

        # Case-insensitive matching fallback
        matched_reg = None
        for key in self.registrations:
            if key.upper() == reg_no.upper():
                matched_reg = key
                break

        if matched_reg:
            rec = self.registrations[matched_reg]
            self.populate_form(rec)
            self.highlight_registration(matched_reg)

            supp_str = "Yes" if rec["is_supplementary"] else "No"
            info = (
                f"Registration Record Found!\n\n"
                f"• Registration No: {rec['reg_no']}\n"
                f"• Student Name: {rec['name']}\n"
                f"• Subject: {rec['subject']}\n"
                f"• Examination Type: {rec['exam_type']}\n"
                f"• Supplementary: {supp_str}\n"
                f"• Examination Fee: ₹{rec['fee']:,.2f}"
            )
            self.set_status(f"Found record for Registration No: {matched_reg}")
            messagebox.showinfo("Search Result", info)
        else:
            self.set_status(f"No student found with Registration No: '{reg_no}'")
            messagebox.showwarning(
                "Record Not Found",
                f"No student registration found matching Registration Number:\n'{reg_no}'\n\n"
                "Please verify the number and try again."
            )

    def update_student(self):
        """Operation: Update examination details for an existing student."""
        valid, data = self.validate_inputs(is_update=True)
        if not valid:
            return

        reg_no = data["reg_no"]

        # Verify existence
        if reg_no not in self.registrations:
            # Check case-insensitive
            match = None
            for key in self.registrations:
                if key.upper() == reg_no.upper():
                    match = key
                    break
            if match:
                reg_no = match
                data["reg_no"] = match
            else:
                messagebox.showerror(
                    "Update Failed",
                    f"No existing record found for Registration Number: '{reg_no}'.\n\n"
                    "Please register the student first before attempting an update."
                )
                return

        # Perform update
        self.registrations[reg_no] = data
        self.save_data()
        self.display_all_registrations()
        self.highlight_registration(reg_no)

        msg = f"Registration details for '{data['name']}' ({reg_no}) have been successfully updated!"
        self.set_status(msg)
        messagebox.showinfo("Update Successful", msg)

    def delete_student(self):
        """Operation: Delete a registration record."""
        reg_no = self.entry_reg_no.get().strip()

        if not reg_no:
            # Check if an item in the Listbox is currently selected
            selected_indices = self.records_listbox.curselection()
            if selected_indices:
                selected_line = self.records_listbox.get(selected_indices[0])
                # The first token is the registration number
                reg_no = selected_line.split("|")[0].strip()

        if not reg_no:
            messagebox.showwarning(
                "Delete Selection Required",
                "Please enter a Registration Number or select a student from the Listbox to delete."
            )
            self.entry_reg_no.focus_set()
            return

        # Verify existence
        if reg_no not in self.registrations:
            match = None
            for key in self.registrations:
                if key.upper() == reg_no.upper():
                    match = key
                    break
            if match:
                reg_no = match
            else:
                messagebox.showwarning(
                    "Record Not Found",
                    f"Cannot delete: No registration found for '{reg_no}'."
                )
                return

        rec = self.registrations[reg_no]
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to permanently delete this registration?\n\n"
            f"• Registration No: {rec['reg_no']}\n"
            f"• Student Name: {rec['name']}\n"
            f"• Subject: {rec['subject']}\n"
            f"• Fee: ₹{rec['fee']:,.2f}\n\n"
            "This action cannot be undone."
        )

        if confirm:
            del self.registrations[reg_no]
            self.save_data()
            self.clear_form()
            self.display_all_registrations()

            msg = f"Registration for '{rec['name']}' ({reg_no}) was deleted successfully."
            self.set_status(msg)
            messagebox.showinfo("Record Deleted", msg)

    def display_all_registrations(self, filter_query=None):
        """Operation: Display all registrations in the Listbox."""
        self.records_listbox.delete(0, tk.END)

        total_fee = 0.0
        count = 0

        # Sort by registration number
        sorted_keys = sorted(self.registrations.keys())

        for reg_no in sorted_keys:
            rec = self.registrations[reg_no]

            # If filtering, check match in reg_no, name, or subject
            if filter_query:
                q = filter_query.lower()
                matches = (
                    q in rec["reg_no"].lower() or
                    q in rec["name"].lower() or
                    q in rec["subject"].lower() or
                    q in rec["exam_type"].lower()
                )
                if not matches:
                    continue

            count += 1
            total_fee += rec["fee"]

            supp_str = "Yes" if rec["is_supplementary"] else "No"
            formatted_entry = (
                f"{rec['reg_no']:<18} | "
                f"{rec['name']:<24} | "
                f"{rec['subject']:<18} | "
                f"{rec['exam_type']:<16} | "
                f"{supp_str:<6} | "
                f"₹{rec['fee']:>9.2f}"
            )
            self.records_listbox.insert(tk.END, formatted_entry)

        # Update stats counter
        self.stats_label.config(
            text=f"Total Registrations: {count} | Total Examination Fees: ₹{total_fee:,.2f}"
        )
        if not filter_query:
            self.set_status(f"Displaying all {count} registered students.")

    def filter_listbox(self):
        """Filter registrations currently displayed in the Listbox."""
        query = self.entry_quick_search.get().strip()
        self.display_all_registrations(filter_query=query)
        self.set_status(f"Filter applied: '{query}' ({self.records_listbox.size()} results found).")

    def highlight_registration(self, reg_no):
        """Find and highlight the registration number in the Listbox."""
        for idx in range(self.records_listbox.size()):
            line = self.records_listbox.get(idx)
            if line.startswith(reg_no):
                self.records_listbox.selection_clear(0, tk.END)
                self.records_listbox.selection_set(idx)
                self.records_listbox.activate(idx)
                self.records_listbox.see(idx)
                break

    def on_listbox_select(self, event):
        """Event handler: Auto-populate form when user clicks on a Listbox row."""
        selected_indices = self.records_listbox.curselection()
        if not selected_indices:
            return

        selected_line = self.records_listbox.get(selected_indices[0])
        # Extract Registration Number from formatted row
        tokens = selected_line.split("|")
        if tokens:
            reg_no = tokens[0].strip()
            if reg_no in self.registrations:
                self.populate_form(self.registrations[reg_no])
                self.set_status(f"Loaded details for {self.registrations[reg_no]['name']} ({reg_no}) into form.")

    def populate_form(self, rec):
        """Populate the form widgets with record data."""
        self.entry_reg_no.delete(0, tk.END)
        self.entry_reg_no.insert(0, rec["reg_no"])

        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, rec["name"])

        self.entry_subject.delete(0, tk.END)
        self.entry_subject.insert(0, rec["subject"])

        self.entry_fee.delete(0, tk.END)
        self.entry_fee.insert(0, f"{rec['fee']:.2f}")

        # Set OptionMenu value
        if rec["exam_type"] in self.EXAM_TYPES:
            self.exam_type_var.set(rec["exam_type"])
        else:
            self.exam_type_var.set(self.EXAM_TYPES[0])

        # Set Checkbutton value
        self.is_supplementary_var.set(1 if rec.get("is_supplementary", False) else 0)

    def clear_form(self):
        """Clear all inputs in the form panel."""
        self.entry_reg_no.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_subject.delete(0, tk.END)
        self.entry_fee.delete(0, tk.END)
        self.exam_type_var.set(self.EXAM_TYPES[0])
        self.is_supplementary_var.set(0)
        self.entry_quick_search.delete(0, tk.END)
        self.records_listbox.selection_clear(0, tk.END)
        self.entry_reg_no.focus_set()
        self.set_status("Form cleared. Ready for new student registration.")

    # =========================================================================
    # PERSISTENCE & SAMPLE DATA
    # =========================================================================

    def load_data(self):
        """Load saved data from JSON file, or populate with student credentials."""
        loaded = False
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and data:
                        self.registrations = data
                        loaded = True
            except Exception as e:
                print(f"Notice: Could not read {self.DATA_FILE}: {e}")

        if not loaded:
            # Seed with team members requested by user
            self.registrations = {
                "RA2511033010093": {
                    "reg_no": "RA2511033010093",
                    "name": "ADITYA KUMAR SINGH",
                    "subject": "Advanced Python",
                    "fee": 1500.0,
                    "exam_type": "Regular Semester",
                    "is_supplementary": False
                },
                "RA2511033010094": {
                    "reg_no": "RA2511033010094",
                    "name": "VARUN VAIDYANATHAN",
                    "subject": "Database Systems",
                    "fee": 1200.0,
                    "exam_type": "Regular Semester",
                    "is_supplementary": False
                },
                "RA2511033010095": {
                    "reg_no": "RA2511033010095",
                    "name": "MANGALWEDHEKAR SARTHAK KEDAR",
                    "subject": "Computer Networks",
                    "fee": 1800.0,
                    "exam_type": "Regular Semester",
                    "is_supplementary": True
                }
            }
            self.save_data()

    def save_data(self):
        """Persist current records to JSON file."""
        try:
            with open(self.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.registrations, f, indent=4)
        except Exception as e:
            print(f"Warning: Failed to save to {self.DATA_FILE}: {e}")


def main():
    root = tk.Tk()
    app = ExamRegistrationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

