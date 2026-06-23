
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics
import os, database

UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "1st.ui")


class DashboardWindow(QMainWindow):
    def __init__(self, nav_callback):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.nav_callback = nav_callback
        self._fix_all_frames()
        self._connect_nav()
        self.refresh()

    def _fix_all_frames(self):
       
        VALUE_NAMES = {"parts_val", "stock_val", "inv_val", "rev_val"}
        SKIP_LABELS = {self.label_8, self.label_10, self.label_11}

        all_frames = (
            self.frame, self.frame_2, self.frame_3, self.frame_4,  
            self.frame_5,                                           
            self.frame_6,                                           
        )

        for section in all_frames:
            
            for child in section.children():
                if isinstance(child, QFrame):
                    child.setStyleSheet(
                        "QFrame { border: none; background: transparent; }"
                    )
            
            for lbl in section.findChildren(QLabel):
                if lbl.objectName() not in VALUE_NAMES \
                        and lbl not in SKIP_LABELS \
                        and not lbl.objectName().startswith("dyn_sale_"):
                    lbl.setStyleSheet(
                        "font: bold 11pt 'MS Shell Dlg 2'; border: none;"
                    )

    def _connect_nav(self):
        self.pushButton.clicked.connect(lambda: self.nav_callback("dashboard"))
        self.pushButton_2.clicked.connect(lambda: self.nav_callback("inventory"))
        self.pushButton_3.clicked.connect(lambda: self.nav_callback("new_sale"))
        self.pushButton_4.clicked.connect(lambda: self.nav_callback("sales_history"))

    def refresh(self):
        stats = database.get_dashboard_stats()

        self._set_card_value(self.frame,   "parts_val", str(stats["parts_types"]))
        self._set_card_value(self.frame_2, "stock_val", str(stats["total_stock"]))
        self._set_card_value(self.frame_3, "inv_val",   f"Rs. {stats['inventory_value']:,.2f}")
        self._set_card_value(self.frame_4, "rev_val",   f"Rs. {stats['total_revenue']:,.2f}")

        self.label_8.setGeometry(10, 42, self.frame_5.width() - 20, 45)
        self.label_8.setWordWrap(True)

        low = stats["low_stock"]
        if low:
            alert_parts = "  |  ".join(
                f"{r['name']}  (qty: {r['quantity']})" for r in low[:5]
            )
            self.label_8.setText(alert_parts)
            self.label_8.setStyleSheet(
                "color: rgb(180,0,0); font: 11pt 'MS Shell Dlg 2'; border: none;")
        else:
            self.label_8.setText("All parts are sufficiently stocked.")
            self.label_8.setStyleSheet(
                "color: green; font: 11pt 'MS Shell Dlg 2'; border: none;")

        recent = stats["recent_sales"]
        full_w = self.frame_6.width() - 40

        sep = self.frame_6.findChild(QFrame, "recent_sales_sep")
        if not sep:
            sep = QFrame(self.frame_6)
            sep.setObjectName("recent_sales_sep")
            sep.setFrameShape(QFrame.HLine)
            sep.setFrameShadow(QFrame.Sunken)
            sep.setStyleSheet("border: none; background-color: #B0B0B0;")
            sep.setGeometry(10, 42, self.frame_6.width() - 20, 2)
            sep.show()

        for lbl in [self.label_10, self.label_11]:
            lbl.setGeometry(30, lbl.y(), full_w, 25)
            lbl.setWordWrap(False)
            lbl.setStyleSheet("font: 11pt 'MS Shell Dlg 2'; border: none;")
            lbl.setText("")

        for i, sale in enumerate(recent[:2]):
            [self.label_10, self.label_11][i].setText(
                f"#{sale['id']}   {sale['customer_name']}   —   "
                f"Rs. {sale['total_amount']:,.2f}     {sale['sale_date'][:16]}"
            )

        self._populate_extra_recent_sales(recent[2:])

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

    def _populate_extra_recent_sales(self, extra_sales):
        for child in self.frame_6.findChildren(QLabel):
            if child.objectName().startswith("dyn_sale_"):
                child.deleteLater()

        full_w = self.frame_6.width() - 40
        y_start = 140
        for i, sale in enumerate(extra_sales[:3]):
            lbl = QLabel(
                f"#{sale['id']}   {sale['customer_name']}   —   "
                f"Rs. {sale['total_amount']:,.2f}     {sale['sale_date'][:16]}",
                self.frame_6
            )
            lbl.setObjectName(f"dyn_sale_{i}")
            lbl.setStyleSheet("font: 11pt 'MS Shell Dlg 2'; border: none;")
            lbl.setGeometry(30, y_start + i * 30, full_w, 25)
            lbl.show()
