
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QPushButton,
    QHBoxLayout, QVBoxLayout, QWidget, QHeaderView, QMessageBox,
    QAbstractItemView, QLabel, QSpinBox, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os, database
from dialogs import BillDialog


UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "3rd.ui")


class NewSaleWindow(QMainWindow):
    def __init__(self, nav_callback):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.nav_callback = nav_callback
        self.cart = []           
        self._build_parts_table()
        self._build_cart_panel()
        self._connect_signals()
        self._load_parts()


    def _build_parts_table(self):
        self.parts_table = QTableWidget(self.frame)
        self.parts_table.setGeometry(0, 40, self.frame.width(), self.frame.height() - 40)
        self.parts_table.setColumnCount(5)
        self.parts_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price", "In Stock"])
        self.parts_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.parts_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.parts_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.parts_table.verticalHeader().setVisible(False)
        self.parts_table.setAlternatingRowColors(True)
        self.parts_table.setStyleSheet("""
            QTableWidget { border: none; font: 9pt 'MS Shell Dlg 2'; }
            QHeaderView::section { background-color: #E0E0E0; font: bold 9pt; padding: 3px; }
            QTableWidget::item:selected { background-color: #D0E8FF; color: black; }
        """)
        self.parts_table.show()

    def _build_cart_panel(self):
        layout = QVBoxLayout()

        self.cart_scroll = QScrollArea()
        self.cart_scroll.setWidgetResizable(True)
        self.cart_scroll.setStyleSheet("border: none;")
        self.cart_content = QWidget()
        self.cart_layout  = QVBoxLayout(self.cart_content)
        self.cart_layout.setAlignment(Qt.AlignTop)
        self.cart_scroll.setWidget(self.cart_content)
        layout.addWidget(self.cart_scroll)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        layout.addWidget(sep)

        total_row = QHBoxLayout()
        total_label = QLabel("Total:")
        total_label.setFont(QFont("MS Shell Dlg 2", 10, QFont.Bold))
        self.total_value = QLabel("Rs. 0.00")
        self.total_value.setFont(QFont("MS Shell Dlg 2", 10, QFont.Bold))
        self.total_value.setStyleSheet("color: #185CDA;")
        total_row.addWidget(total_label)
        total_row.addStretch()
        total_row.addWidget(self.total_value)
        layout.addLayout(total_row)

        self.checkout_btn = QPushButton("Complete Sale & Print Bill")
        self.checkout_btn.setStyleSheet(
            "background-color: #185CDA; color: white; border-radius: 6px; padding: 7px; font: bold 9pt;")
        self.checkout_btn.clicked.connect(self._complete_sale)
        layout.addWidget(self.checkout_btn)

        old_layout = self.frame_2.layout()
        if old_layout:
            QWidget().setLayout(old_layout)

        container = QWidget(self.frame_2)
        container.setLayout(layout)
        container.setGeometry(0, 45, self.frame_2.width(), self.frame_2.height() - 45)
        container.show()

    def _connect_signals(self):
        self.pushButton.clicked.connect(lambda: self.nav_callback("dashboard"))
        self.pushButton_2.clicked.connect(lambda: self.nav_callback("inventory"))
        self.pushButton_3.clicked.connect(lambda: self.nav_callback("new_sale"))
        self.pushButton_4.clicked.connect(lambda: self.nav_callback("sales_history"))

        self.textEdit.textChanged.connect(self._on_search)
        self.parts_table.doubleClicked.connect(self._add_to_cart)

    def _load_parts(self, query=""):
        if query:
            parts = database.search_parts(query)
        else:
            parts = database.get_all_parts()
        self._populate_parts_table(parts)

    def _populate_parts_table(self, parts):
        self.parts_table.setRowCount(0)
        for i, part in enumerate(parts):
            self.parts_table.insertRow(i)
            for col, val in enumerate([
                str(part["id"]), part["name"], part["category"],
                f"Rs. {part['price']:,.2f}", str(part["quantity"])
            ]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                if col == 4 and part["quantity"] == 0:
                    item.setForeground(Qt.red)
                self.parts_table.setItem(i, col, item)
        self.parts_table.resizeRowsToContents()

    def _on_search(self):
        q = self.textEdit.toPlainText().strip()
        self._load_parts(q)

    def _add_to_cart(self):
        row = self.parts_table.currentRow()
        if row < 0:
            return
        part_id   = int(self.parts_table.item(row, 0).text())
        part_name = self.parts_table.item(row, 1).text()
        price_txt = self.parts_table.item(row, 3).text().replace("Rs.", "").replace(",", "").strip()
        unit_price = float(price_txt)
        stock     = int(self.parts_table.item(row, 4).text())

        if stock == 0:
            QMessageBox.warning(self, "Out of Stock", f"'{part_name}' is out of stock.")
            return

        for item in self.cart:
            if item["part_id"] == part_id:
                if item["quantity"] >= stock:
                    QMessageBox.warning(self, "Stock Limit", f"Only {stock} units available.")
                    return
                item["quantity"] += 1
                self._refresh_cart_ui()
                return

        self.cart.append({
            "part_id": part_id,
            "part_name": part_name,
            "quantity": 1,
            "unit_price": unit_price,
            "max_stock": stock,
        })
        self._refresh_cart_ui()

    def _refresh_cart_ui(self):
       
        for i in reversed(range(self.cart_layout.count())):
            widget = self.cart_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for idx, item in enumerate(self.cart):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(2, 2, 2, 2)

            name_lbl = QLabel(item["part_name"])
            name_lbl.setFont(QFont("MS Shell Dlg 2", 8))
            name_lbl.setWordWrap(True)

            qty_spin = QSpinBox()
            qty_spin.setRange(1, item["max_stock"])
            qty_spin.setValue(item["quantity"])
            qty_spin.setFixedWidth(55)
            qty_spin.valueChanged.connect(
                lambda val, i=idx: self._update_qty(i, val)
            )

            sub_lbl = QLabel(f"Rs.{item['quantity'] * item['unit_price']:,.2f}")
            sub_lbl.setFixedWidth(75)
            sub_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            sub_lbl.setFont(QFont("MS Shell Dlg 2", 8, QFont.Bold))

            remove_btn = QPushButton("✕")
            remove_btn.setFixedSize(22, 22)
            remove_btn.setStyleSheet("color: red; font: bold 10pt; border: none;")
            remove_btn.clicked.connect(lambda _, i=idx: self._remove_from_cart(i))

            row_layout.addWidget(name_lbl, 2)
            row_layout.addWidget(qty_spin)
            row_layout.addWidget(sub_lbl)
            row_layout.addWidget(remove_btn)
            self.cart_layout.addWidget(row_widget)

        total = sum(it["quantity"] * it["unit_price"] for it in self.cart)
        self.total_value.setText(f"Rs. {total:,.2f}")

    def _update_qty(self, idx, val):
        self.cart[idx]["quantity"] = val
        self._refresh_cart_ui()

    def _remove_from_cart(self, idx):
        self.cart.pop(idx)
        self._refresh_cart_ui()

    def _complete_sale(self):
        customer = self.lineEdit.text().strip()
        if not customer:
            QMessageBox.warning(self, "Missing Name", "Please enter the customer's name.")
            return
        if not self.cart:
            QMessageBox.warning(self, "Empty Cart", "Please add at least one item to the cart.")
            return

        try:
            sale_id = database.create_sale(customer, self.cart)
        except Exception as e:
            QMessageBox.critical(self, "Sale Error", str(e))
            return

        dlg = BillDialog(self, sale_id=sale_id)
        dlg.exec_()

        self.cart.clear()
        self.lineEdit.clear()
        self.textEdit.clear()
        self._refresh_cart_ui()
        self._load_parts()
