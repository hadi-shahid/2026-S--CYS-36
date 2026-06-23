
import sys
import os
from PyQt5.QtWidgets import QApplication


import database
database.initialize_database()

from dashboard_window     import DashboardWindow
from inventory_window     import InventoryWindow
from new_sale_window      import NewSaleWindow
from sales_history_window import SalesHistoryWindow


class AppController:

    def __init__(self):
        self.windows = {
            "dashboard":     DashboardWindow(self.navigate),
            "inventory":     InventoryWindow(self.navigate),
            "new_sale":      NewSaleWindow(self.navigate),
            "sales_history": SalesHistoryWindow(self.navigate),
        }
        self.current = None
        self.navigate("dashboard")

    def navigate(self, screen_name: str):
        if self.current:
            self.current.hide()

        window = self.windows.get(screen_name)
        if window is None:
            return

        if hasattr(window, "refresh"):
            window.refresh()

        window.show()
        self.current = window


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Vehicle Spare Parts Store")

    controller = AppController()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
