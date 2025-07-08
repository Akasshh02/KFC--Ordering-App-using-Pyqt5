import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpinBox, QStackedWidget, QSizePolicy
)
from PyQt5.QtGui import QIcon, QFont,QPixmap
from PyQt5.QtCore import Qt
from PyQt6.QtWidgets import QRadioButton


class HomePage(QWidget):
    def __init__(self, on_category_selected):
        super().__init__()
        self.on_category_selected = on_category_selected

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(12)

        logo_lbl = QLabel()
        pix = QPixmap("homepic.svg.jpg")
        pix = pix.scaledToWidth(180, Qt.SmoothTransformation)
        logo_lbl.setPixmap(pix)
        logo_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_lbl)

        title = QLabel("🍗 Welcome to KFC")
        title.setFont(QFont("Berlin Sans FB", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        categories = [
            "Burgers", "Chicken Buckets",
            "Box Meals", "Snacks", "Value Lunch Specials"
        ]
        for cat in categories:
            btn = QPushButton(cat)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setFixedHeight(48)
            btn.clicked.connect(lambda _, c=cat: self.on_category_selected(c))
            layout.addWidget(btn)

        layout.addStretch()

class MenuPage(QWidget):
    def __init__(self, category, go_home, go_summary):
        super().__init__()
        self.go_summary = go_summary
        self.selected = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(12)

        topbar = QHBoxLayout()
        back = QPushButton("← Home")
        back.setFixedSize(80,32)
        back.clicked.connect(go_home)
        topbar.addWidget(back)
        topbar.addStretch()
        layout.addLayout(topbar)

        title = QLabel(f"🍴 {category} Menu")
        title.setFont(QFont("Berlin Sans FB", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        menu_items = {
            "Burgers": [
                "Gold Edition – Chicken Zinger & Fries - Rs.199",
                "Spicy Zinger Burger", "Zinger Pro Burger",
                "Classic Zinger", "Classic Zinger-with Cheese",
                "Indian Tandoori Zinger Burger", "Paneer Zinger Burger"],

            "Chicken Buckets": [
                "5pc Smoky Red Chicken", "8 pc Hot & Crispy Chicken",
                "Peri Peri 5 Leg Pc", "6 Pc Strips & Pepsi Bottle Combo",
                "Peri Peri 10 Pc Chicken Strips & 2 Dips",
                "Peri Peri 10 Leg Pc & 4 Dips"
            ],
            "Box Meals": [
                "All Chicken Box", "Classic Zinger Box",
                "Tandoori Zinger Box", "Popcorn Rice Box"
            ],
            "Snacks": [
                "2 pc Hot & Crispy Chicken",
                "Saucy Popcorn x CarryMinati",
                "Popcorn", "French Fries", "4pc Hot Wings",
                "Peri Peri 3pc Chicken Strips",
                "Chicken & Fries Bucket", "Classic Chicken Roll",
                "Chicken Longer Burger & 2 Strips Combo"
            ],
            "Value Lunch Specials": [
                "2 Rice Bowlz Lunch Combo",
                "Chicken Roll & Rice Lunch Combo",
                "Chicken Longer & Rice Lunch Combo",
                "Chicken Longer & Roll Lunch Combo",
                "Chicken Roll & Rice Deluxe Lunch Combo"
            ]
        }

        for item in menu_items.get(category, []):
            row = QHBoxLayout()
            lbl = QLabel(item)
            spin = QSpinBox()
            spin.setRange(0,10)
            spin.valueChanged.connect(lambda v, name=item: self.on_qty_change(name, v))
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(spin)
            layout.addLayout(row)

        layout.addStretch()

        nxt = QPushButton("Next ➡️")
        nxt.setFixedHeight(44)
        nxt.clicked.connect(self.go_summary)
        layout.addWidget(nxt)

    def on_qty_change(self, item, qty):
        if qty > 0:
            self.selected[item] = qty
        elif item in self.selected:
            del self.selected[item]

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KFC Mobile App")
        self.setWindowIcon(QIcon("logo.png"))
        self.setGeometry(100,100,500,700)
        self.setFixedSize(500,700)

        self.setStyleSheet("""
            QWidget { background: #fafafa; font-family: Berlin Sans FB; }
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #ff6666, stop:1 #ff3333);
                color: white; border-radius:8px; font-size:16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #ff7f7f, stop:1 #ff4c4c);
            }
            QSpinBox { font-size:14px; min-width:60px; }
        """)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_page = HomePage(self.show_menu)
        self.stack.addWidget(self.home_page)

    def show_menu(self, category):
        self.menu_page = MenuPage(category, self.show_home, self.show_summary)
        if self.stack.count() == 1:
            self.stack.addWidget(self.menu_page)
        else:
            self.stack.insertWidget(1, self.menu_page)
        self.stack.setCurrentIndex(1)

    def show_home(self):
        self.stack.setCurrentIndex(0)

    def show_summary(self):
            summary = SummaryPage(self.menu_page.selected, self.show_home)
            if self.stack.count() < 3:
                self.stack.addWidget(summary)
            else:
                self.stack.insertWidget(2, summary)
            self.stack.setCurrentIndex(2)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QMessageBox

class SummaryPage(QWidget):
    def __init__(self, selected_items, go_home):
        super().__init__()
        self.selected_items = selected_items
        self.go_home = go_home
        self.total_price = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel("🧾 Order Summary")
        title.setFont(QFont("Berlin Sans FB", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        prices = {
            "Gold Edition – Chicken Zinger & Fries": 199,
            "Spicy Zinger Burger": 179,
            "Zinger Pro Burger": 189,
            "Classic Zinger": 169,
            "Classic Zinger-with Cheese": 179,
            "Indian Tandoori Zinger Burger": 189,
            "Paneer Zinger Burger": 159,
            "5pc Smoky Red Chicken": 299,
            "8 pc Hot & Crispy Chicken": 349,
            "Peri Peri 5 Leg Pc": 319,
            "6 Pc Strips & Pepsi Bottle Combo": 289,
            "Peri Peri 10 Pc Chicken Strips & 2 Dips": 379,
            "Peri Peri 10 Leg Pc & 4 Dips": 389,
            "All Chicken Box": 249,
            "Classic Zinger Box": 229,
            "Tandoori Zinger Box": 239,
            "Popcorn Rice Box": 219,
            "2 pc Hot & Crispy Chicken": 149,
            "Saucy Popcorn x CarryMinati": 189,
            "Popcorn": 99,
            "French Fries": 89,
            "4pc Hot Wings": 149,
            "Peri Peri 3pc Chicken Strips": 149,
            "Chicken & Fries Bucket": 189,
            "Classic Chicken Roll": 129,
            "Chicken Longer Burger & 2 Strips Combo": 169,
            "2 Rice Bowlz Lunch Combo": 259,
            "Chicken Roll & Rice Lunch Combo": 229,
            "Chicken Longer & Rice Lunch Combo": 219,
            "Chicken Longer & Roll Lunch Combo": 229,
            "Chicken Roll & Rice Deluxe Lunch Combo": 279
        }

        for item, qty in selected_items.items():
            price = prices.get(item, 100)
            item_total = price * qty
            self.total_price += item_total
            line = QLabel(f"{item} x{qty}  —  ₹{item_total}")
            layout.addWidget(line)

        layout.addSpacing(10)
        layout.addWidget(QLabel(f"🧮 Total: ₹{self.total_price}"))

        self.dine_in = QRadioButton("Dine-in")
        self.takeaway = QRadioButton("Takeaway")
        self.takeaway.setChecked(True)

        layout.addSpacing(10)
        layout.addWidget(QLabel("Choose your option:"))
        layout.addWidget(self.dine_in)
        layout.addWidget(self.takeaway)

        order_btn = QPushButton("Place Order ✅")
        order_btn.setFixedHeight(44)
        order_btn.clicked.connect(self.place_order)
        layout.addWidget(order_btn)

    def place_order(self):
        option = "Dine-in" if self.dine_in.isChecked() else "Takeaway"
        msg = QMessageBox()
        msg.setWindowTitle("Order Placed ✅")
        msg.setText(f"Your ₹{self.total_price} {option} order has been placed.\nPlease pay at the counter.\nEnjoy your meal!")
        msg.exec_()
        self.go_home()

def main():
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()