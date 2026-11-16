#!/usr/bin/env python3.13
"""
Automated unit & functional test suite for ExamRegistrationApp
"""
import unittest
from unittest.mock import patch
import os
import json
import tkinter as tk
from exam_registration_app import ExamRegistrationApp

class TestExamRegistrationApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create hidden root
        cls.root = tk.Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def setUp(self):
        # Use a temporary test json file
        ExamRegistrationApp.DATA_FILE = "test_registrations.json"
        if os.path.exists("test_registrations.json"):
            os.remove("test_registrations.json")
        self.app = ExamRegistrationApp(self.root)

    def tearDown(self):
        if os.path.exists("test_registrations.json"):
            os.remove("test_registrations.json")

    def test_initial_team_data_loaded(self):
        """Verify the 3 students specified in the prompt are pre-loaded"""
        self.assertIn("RA2511033010093", self.app.registrations)
        self.assertIn("RA2511033010094", self.app.registrations)
        self.assertIn("RA2511033010095", self.app.registrations)
        self.assertEqual(self.app.registrations["RA2511033010093"]["name"], "ADITYA KUMAR SINGH")
        self.assertEqual(self.app.registrations["RA2511033010094"]["name"], "VARUN VAIDYANATHAN")
        self.assertEqual(self.app.registrations["RA2511033010095"]["name"], "MANGALWEDHEKAR SARTHAK KEDAR")
        self.assertEqual(self.app.records_listbox.size(), 3)

    @patch("tkinter.messagebox.showerror")
    def test_validation_mandatory_fields(self, mock_error):
        """Test validation for mandatory registration number and student name"""
        self.app.clear_form()

        # 1. Missing reg_no
        self.app.entry_name.insert(0, "Test Student")
        self.app.entry_subject.insert(0, "Maths")
        self.app.entry_fee.insert(0, "1000")
        valid, data = self.app.validate_inputs()
        self.assertFalse(valid)
        self.assertTrue(mock_error.called)

        # 2. Missing student name
        mock_error.reset_mock()
        self.app.entry_reg_no.insert(0, "REG123")
        self.app.entry_name.delete(0, tk.END)
        valid, data = self.app.validate_inputs()
        self.assertFalse(valid)
        self.assertTrue(mock_error.called)

        # 3. Missing subject
        mock_error.reset_mock()
        self.app.entry_name.insert(0, "Test Student")
        self.app.entry_subject.delete(0, tk.END)
        valid, data = self.app.validate_inputs()
        self.assertFalse(valid)
        self.assertTrue(mock_error.called)

    @patch("tkinter.messagebox.showerror")
    def test_validation_fee_non_negative(self, mock_error):
        """Test examination fee validation: must be a non-negative number"""
        self.app.clear_form()
        self.app.entry_reg_no.insert(0, "REG999")
        self.app.entry_name.insert(0, "Alice Smith")
        self.app.entry_subject.insert(0, "Physics")

        # Negative fee
        self.app.entry_fee.insert(0, "-250")
        valid, data = self.app.validate_inputs()
        self.assertFalse(valid)
        self.assertTrue(mock_error.called)

        # Non-numeric fee
        mock_error.reset_mock()
        self.app.entry_fee.delete(0, tk.END)
        self.app.entry_fee.insert(0, "abc_invalid")
        valid, data = self.app.validate_inputs()
        self.assertFalse(valid)
        self.assertTrue(mock_error.called)

        # Valid non-negative fee: 0 (free / scholarship)
        mock_error.reset_mock()
        self.app.entry_fee.delete(0, tk.END)
        self.app.entry_fee.insert(0, "0")
        valid, data = self.app.validate_inputs()
        self.assertTrue(valid)
        self.assertEqual(data["fee"], 0.0)

        # Valid positive fee
        self.app.entry_fee.delete(0, tk.END)
        self.app.entry_fee.insert(0, "1500.50")
        valid, data = self.app.validate_inputs()
        self.assertTrue(valid)
        self.assertEqual(data["fee"], 1500.50)

    @patch("tkinter.messagebox.showinfo")
    def test_register_student_success(self, mock_info):
        """Test registering a new student"""
        self.app.clear_form()
        self.app.entry_reg_no.insert(0, "RA2511033010100")
        self.app.entry_name.insert(0, "John Doe")
        self.app.entry_subject.insert(0, "Operating Systems")
        self.app.entry_fee.insert(0, "2000")
        self.app.exam_type_var.set("Mid-Term Examination")
        self.app.is_supplementary_var.set(1)

        self.app.register_student()
        self.assertTrue(mock_info.called)
        self.assertIn("RA2511033010100", self.app.registrations)
        rec = self.app.registrations["RA2511033010100"]
        self.assertEqual(rec["name"], "John Doe")
        self.assertEqual(rec["fee"], 2000.0)
        self.assertEqual(rec["exam_type"], "Mid-Term Examination")
        self.assertTrue(rec["is_supplementary"])
        self.assertEqual(self.app.records_listbox.size(), 4)

    @patch("tkinter.messagebox.showwarning")
    def test_duplicate_registration_prevented(self, mock_warning):
        """Test that registering an existing registration number warns user"""
        self.app.clear_form()
        self.app.entry_reg_no.insert(0, "RA2511033010093")
        self.app.entry_name.insert(0, "Duplicate Test")
        self.app.entry_subject.insert(0, "Test Subject")
        self.app.entry_fee.insert(0, "1000")

        self.app.register_student()
        self.assertTrue(mock_warning.called)

    @patch("tkinter.messagebox.showinfo")
    def test_search_student(self, mock_info):
        """Test searching for an existing student by registration number"""
        self.app.clear_form()
        self.app.entry_reg_no.insert(0, "RA2511033010094")
        self.app.search_student()

        self.assertTrue(mock_info.called)
        self.assertEqual(self.app.entry_name.get(), "VARUN VAIDYANATHAN")
        self.assertEqual(self.app.entry_subject.get(), "Database Systems")
        self.assertEqual(self.app.entry_fee.get(), "1200.00")

    @patch("tkinter.messagebox.showinfo")
    def test_update_student(self, mock_info):
        """Test updating an existing student's examination details"""
        self.app.clear_form()
        self.app.entry_reg_no.insert(0, "RA2511033010093")
        self.app.entry_name.insert(0, "ADITYA KUMAR SINGH")
        self.app.entry_subject.insert(0, "Advanced Machine Learning")
        self.app.entry_fee.insert(0, "2500")
        self.app.exam_type_var.set("Re-Evaluation")
        self.app.is_supplementary_var.set(1)

        self.app.update_student()
        self.assertTrue(mock_info.called)

        updated = self.app.registrations["RA2511033010093"]
        self.assertEqual(updated["subject"], "Advanced Machine Learning")
        self.assertEqual(updated["fee"], 2500.0)
        self.assertEqual(updated["exam_type"], "Re-Evaluation")
        self.assertTrue(updated["is_supplementary"])

    @patch("tkinter.messagebox.askyesno", return_value=True)
    @patch("tkinter.messagebox.showinfo")
    def test_delete_student(self, mock_info, mock_confirm):
        """Test deleting a registration"""
        self.app.clear_form()
        self.app.entry_reg_no.insert(0, "RA2511033010095")
        self.app.delete_student()

        self.assertTrue(mock_confirm.called)
        self.assertTrue(mock_info.called)
        self.assertNotIn("RA2511033010095", self.app.registrations)
        self.assertEqual(self.app.records_listbox.size(), 2)

    def test_listbox_click_populates_form(self):
        """Test clicking an item in the Listbox loads details into the form"""
        # Select first item
        self.app.records_listbox.selection_clear(0, tk.END)
        self.app.records_listbox.selection_set(0)
        self.app.on_listbox_select(None)

        self.assertEqual(self.app.entry_reg_no.get(), "RA2511033010093")
        self.assertEqual(self.app.entry_name.get(), "ADITYA KUMAR SINGH")

if __name__ == "__main__":
    unittest.main()

