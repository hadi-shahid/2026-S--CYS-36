
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics
import os, database
from dialogs import BillDialog


UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "4rth.ui")


class SalesHistoryWindow(QMainWindow):
    def __init__(self, nav_callback):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.nav_callback = nav_callback
        self._hide_duplicate_frames()
        self._build_sales_table()
        self._connect_signals()
        self.refresh()

    def _hide_duplicate_frames(self):
      
        self.frame_2.hide()
        self.frame_4.hide()
        self.label_7.hide()
        self.label_8.hide()

    def _build_sales_table(self):
        self.sales_table = QTableWidget(self.frame_5)
        self.sales_table.setGeometry(0, 0, self.frame_5.width(), self.frame_5.height())
        self.sales_table.setColumnCount(5)

        headers = ["Sale ID", "Customer Name", "Total (Rs.)", "Date", "Details"]
        self.sales_table.setHorizontalHeaderLabels(headers)

        self.sales_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.sales_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        hh = self.sales_table.horizontalHeader()
        hh.setMinimumSectionSize(70)
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)   
        hh.setSectionResizeMode(1, QHeaderView.Stretch)            
        hh.setSectionResizeMode(2, QHeaderView.ResizeToContents)   
        hh.setSectionResizeMode(3, QHeaderView.ResizeToContents)   
        hh.setSectionResizeMode(4, QHeaderView.ResizeToContents)  

        self.sales_table.verticalHeader().setVisible(False)
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.setStyleSheet("""
            QTableWidget {
                border: none;
                font: 9pt 'MS Shell Dlg 2';
            }
            QHeaderView::section {
                background-color: #E0E0E0;
                font: bold 9pt 'MS Shell Dlg 2';
                padding: 4px;
                border: 1px solid #C0C0C0;
            }
            QTableWidget::item:selected {
                background-color: #D0E8FF;
                color: black;
            }
        """)
        self.sales_table.show()

    def _connect_signals(self):
        self.pushButton.clicked.connect(lambda: self.nav_callback("dashboard"))
        self.pushButton_2.clicked.connect(lambda: self.nav_callback("inventory"))
        self.pushButton_3.clicked.connect(lambda: self.nav_callback("new_sale"))
        self.pushButton_4.clicked.connect(lambda: self.nav_callback("sales_history"))
        self.textEdit.textChanged.connect(self._on_search)

    def refresh(self):
        self._update_stats()
        self._populate_sales(database.get_all_sales())

    def _update_stats(self):
        stats = database.get_sales_history_stats()
        self._set_card_value(self.frame,   "sh_sales_val", str(stats["total_sales"]))
        self._set_card_value(self.frame_3, "sh_rev_val",   f"Rs. {stats['total_revenue']:,.2f}")

    def _set_card_value(self, frame, obj_name, text):
        avail_w = frame.width() - 12

        chosen_size = 8
        for pt in range(13, 7, -1):
            fm = QFontMetrics(QFont("MS Shell Dlg 2", pt, QFont.Bold))
            if fm.horizontalAdvance(text) <= avail_w:
                chosen_size = pt
                break

        style = (
            f"font: bold {chosen_size}pt 'MS Shell Dlg 2';"
            " color: #185CDA;"
            " border: none;"
        )

        existing = frame.findChild(QLabel, obj_name)
        if existing:
            existing.setText(text)
            existing.setStyleSheet(style)
            existing.setGeometry(6, 40, avail_w, 36)
            existing.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        else:
            lbl = QLabel(text, frame)
            lbl.setObjectName(obj_name)
            lbl.setStyleSheet(style)
            lbl.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            lbl.setGeometry(6, 40, avail_w, 36)
            lbl.show()

    def _on_search(self):
        q = self.textEdit.toPlainText().strip()
        sales = database.search_sales(q) if q else database.get_all_sales()
        self._populate_sales(sales)

    def _populate_sales(self, sales):
        self.sales_table.setRowCount(0)
        for i, sale in enumerate(sales):
            self.sales_table.insertRow(i)

            for col, val in enumerate([
                str(sale["id"]),
                sale["customer_name"],
                f"Rs. {sale['total_amount']:,.2f}",
                sale["sale_date"][:16],
            ]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                self.sales_table.setItem(i, col, item)

            lbl = QLabel("View Bill")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(
                "color: rgb(71,151,255);"
                " font: 8pt 'MS Shell Dlg 2';"
                " text-decoration: underline;"
                " border: none;"
            )
            lbl.setCursor(Qt.PointingHandCursor)

            lbl.sale_id = sale["id"]
            lbl.mousePressEvent = lambda event, sid=sale["id"]: self._view_bill(sid)
            self.sales_table.setCellWidget(i, 4, lbl)

        self.sales_table.resizeRowsToContents()

    def _view_bill(self, sale_id):
        dlg = BillDialog(self, sale_id=sale_id)
        dlg.exec_()
