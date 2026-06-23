"""
inventory_window.py — Backend for 2.ui (Inventory)

Widget map (from 2.ui):
  textEdit      → search input
  pushButton    → "+ Add Part" button
  pushButton_2  → Edit (template row — we replace with dynamic table)
  pushButton_3  → Delete (template row)
  pushButton_4  → nav: Sales History
  pushButton_5  → nav: New Sale
  pushButton_6  → nav: Inventory (self)
  pushButton_7  → nav: Dashboard
  frame         → table container (we build a QTableWidget inside)
  label_2..7    → column headers (ID, Name, Category, Manufacturer, Qty, Price)
"""

from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QWidget, QHeaderView, QMessageBox, QAbstractItemView
)
from PyQt5.QtCore import Qt, QTimer
import os, database
from dialogs import AddEditPartDialog


UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "2.ui")


class InventoryWindow(QMainWindow):
    def __init__(self, nav_callback):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.nav_callback = nav_callback
        self._build_table()
        self._connect_signals()
        self.refresh()

    # ── Table setup ─────────────────────────────────────────────────
    def _build_table(self):
        """Replace the static frame content with a real QTableWidget."""
        self.table = QTableWidget(self.frame)
        self.table.setGeometry(0, 65, self.frame.width(), self.frame.height() - 65)
        self.table.setColumnCount(7)   # ID | Name | Category | Manufacturer | Qty | Price | Actions
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Category", "Manufacturer", "Qty", "Price (Rs.)", "Actions"]
        )
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget { border: none; font: 9pt 'MS Shell Dlg 2'; }
            QHeaderView::section { background-color: #E0E0E0; font: bold 9pt 'MS Shell Dlg 2'; padding: 4px; }
            QTableWidget::item:selected { background-color: #D0E8FF; color: black; }
        """)
        self.table.show()

        # Hide the template edit/delete buttons from the .ui file
        self.pushButton_2.hide()
        self.pushButton_3.hide()

    # ── Signal connections ───────────────────────────────────────────
    def _connect_signals(self):
        # Nav
        self.pushButton_7.clicked.connect(lambda: self.nav_callback("dashboard"))
        self.pushButton_6.clicked.connect(lambda: self.nav_callback("inventory"))
        self.pushButton_5.clicked.connect(lambda: self.nav_callback("new_sale"))
        self.pushButton_4.clicked.connect(lambda: self.nav_callback("sales_history"))

        # Add part
        self.pushButton.clicked.connect(self._open_add_dialog)

        # Live search
        self.textEdit.textChanged.connect(self._on_search)

    # ── Search ───────────────────────────────────────────────────────
    def _on_search(self):
        query = self.textEdit.toPlainText().strip()
        if query:
            parts = database.search_parts(query)
        else:
            parts = database.get_all_parts()
        self._populate_table(parts)

    # ── Data ─────────────────────────────────────────────────────────
    def refresh(self):
        parts = database.get_all_parts()
        self._populate_table(parts)

    def _populate_table(self, parts):
        self.table.setRowCount(0)
        for row_idx, part in enumerate(parts):
            self.table.insertRow(row_idx)
            low = part["quantity"] <= part["low_stock_threshold"]

            for col, value in enumerate([
                str(part["id"]), part["name"], part["category"],
                part["manufacturer"], str(part["quantity"]),
                f"Rs. {part['price']:,.2f}"
            ]):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                if low and col == 4:          # highlight low qty in red
                    item.setForeground(Qt.red)
                self.table.setItem(row_idx, col, item)

            # Action buttons cell
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(2, 2, 2, 2)
            btn_layout.setSpacing(4)

            edit_btn = QPushButton("Edit")
            edit_btn.setStyleSheet("color: rgb(71,151,255); font: 7pt 'MS Shell Dlg 2';")
            edit_btn.clicked.connect(lambda _, pid=part["id"]: self._open_edit_dialog(pid))

            del_btn = QPushButton("Delete")
            del_btn.setStyleSheet("color: rgb(184,12,0); font: 7pt 'MS Shell Dlg 2';")
            del_btn.clicked.connect(lambda _, pid=part["id"]: self._delete_part(pid))

            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(del_btn)
            self.table.setCellWidget(row_idx, 6, btn_widget)

        self.table.resizeRowsToContents()

    # ── Dialogs / actions ────────────────────────────────────────────
    def _open_add_dialog(self):
        dlg = AddEditPartDialog(self)
        if dlg.exec_():
            self.refresh()

    def _open_edit_dialog(self, part_id):
        part = database.get_part_by_id(part_id)
        if not part:
            return
        dlg = AddEditPartDialog(self, part_data=part)
        if dlg.exec_():
            self.refresh()

    def _delete_part(self, part_id):
        part = database.get_part_by_id(part_id)
        if not part:
            return
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete '{part['name']}'?\nThis cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                database.delete_part(part_id)
                self.refresh()
            except ValueError as e:
                # Expected, user-facing case: part has sales history
                QMessageBox.warning(self, "Cannot Delete Part", str(e))
            except Exception as e:
                # Anything unexpected still gets shown instead of crashing
                QMessageBox.critical(self, "Database Error", str(e))
