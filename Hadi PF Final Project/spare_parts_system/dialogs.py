
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QDoubleSpinBox, QSpinBox,
    QPushButton, QMessageBox, QTextEdit, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import database


class AddEditPartDialog(QDialog):

    def __init__(self, parent=None, part_data=None):
        super().__init__(parent)
        self.part_data = part_data
        self.setWindowTitle("Edit Part" if part_data else "Add New Part")
        self.setFixedSize(420, 380)
        self.setStyleSheet("background-color: #EBEBEB;")
        self._build_ui()
        if part_data:
            self._populate(part_data)

    def _build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Edit Part" if self.part_data else "Add New Spare Part")
        title.setFont(QFont("MS Shell Dlg 2", 14, QFont.Bold))
        layout.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        layout.addWidget(sep)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(10)

        self.name_edit       = QLineEdit()
        self.category_edit   = QLineEdit()
        self.mfg_edit        = QLineEdit()
        self.qty_spin        = QSpinBox();       self.qty_spin.setRange(0, 999999)
        self.price_spin      = QDoubleSpinBox(); self.price_spin.setRange(0, 9999999); self.price_spin.setDecimals(2); self.price_spin.setPrefix("Rs. ")
        self.threshold_spin  = QSpinBox();       self.threshold_spin.setRange(1, 999); self.threshold_spin.setValue(5)

        for label, widget in [
            ("Part Name *",         self.name_edit),
            ("Category *",          self.category_edit),
            ("Manufacturer *",      self.mfg_edit),
            ("Quantity *",          self.qty_spin),
            ("Price (Rs.) *",       self.price_spin),
            ("Low Stock Alert at",  self.threshold_spin),
        ]:
            form.addRow(label, widget)

        layout.addLayout(form)
        layout.addSpacing(10)

        btn_row = QHBoxLayout()
        self.save_btn   = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.save_btn.setStyleSheet(
            "background-color: #185CDA; color: white; border-radius: 6px; padding: 6px 18px;")
        self.cancel_btn.setStyleSheet(
            "background-color: #888; color: white; border-radius: 6px; padding: 6px 18px;")
        btn_row.addStretch()
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)
        layout.addLayout(btn_row)

        self.save_btn.clicked.connect(self._save)
        self.cancel_btn.clicked.connect(self.reject)

    def _populate(self, row):
        self.name_edit.setText(row["name"])
        self.category_edit.setText(row["category"])
        self.mfg_edit.setText(row["manufacturer"])
        self.qty_spin.setValue(row["quantity"])
        self.price_spin.setValue(row["price"])
        self.threshold_spin.setValue(row["low_stock_threshold"])

    def _save(self):
        name     = self.name_edit.text().strip()
        category = self.category_edit.text().strip()
        mfg      = self.mfg_edit.text().strip()
        qty      = self.qty_spin.value()
        price    = self.price_spin.value()
        threshold = self.threshold_spin.value()

        if not all([name, category, mfg]):
            QMessageBox.warning(self, "Validation", "Please fill in all required fields.")
            return

        try:
            if self.part_data:
                database.update_part(self.part_data["id"], name, category, mfg, qty, price, threshold)
            else:
                database.add_part(name, category, mfg, qty, price, threshold)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))


class BillDialog(QDialog):

    W = 52   
    def __init__(self, parent=None, sale_id=None):
        super().__init__(parent)
        self.setWindowTitle(f"Bill  —  Sale #{sale_id}")
        self.setFixedSize(530, 560)
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        sale  = database.get_sale_by_id(sale_id)
        items = database.get_sale_items(sale_id)

        W = self.W

        def sep(char="="):
            return char * W

        def centered(text):
            return text.center(W)

        lines = [
            sep("="),
            centered("Vehicle Spare Parts Store"),
            centered("*** CUSTOMER BILL ***"),
            sep("="),
            f"  Sale ID   : {sale['id']}",
            f"  Customer  : {sale['customer_name']}",
            f"  Date      : {sale['sale_date']}",
            sep("-"),
        ]

     
        lines.append(
            f"  {'Item':<20}  {'Qty':>5}  {'Unit Price':>11}  {'Subtotal':>11}"
        )
        lines.append(sep("-"))

        for it in items:
            name     = it['part_name'][:20]
            qty      = it['quantity']
            uprice   = it['unit_price']
            subtotal = it['subtotal']
            lines.append(
                f"  {name:<20}  {qty:>5}  Rs.{uprice:>8,.2f}  Rs.{subtotal:>8,.2f}"
            )

        lines += [
            sep("="),
            f"  TOTAL AMOUNT  :  Rs. {sale['total_amount']:,.2f}",
            sep("="),
            centered("Thank you for your business!"),
        ]

        text = QTextEdit()
        text.setReadOnly(True)
        text.setFont(QFont("Courier New", 9))
        text.setLineWrapMode(QTextEdit.NoWrap)
        text.setPlainText("\n".join(lines))
        text.setStyleSheet("border: 1px solid #ddd; background: white;")
        layout.addWidget(text)

        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(100)
        close_btn.setStyleSheet(
            "background-color: #185CDA; color: white; border-radius: 6px; padding: 6px 20px;")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)
