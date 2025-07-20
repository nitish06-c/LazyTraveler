from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QCheckBox, QPushButton, QHBoxLayout, QGroupBox,
    QTreeWidget, QTreeWidgetItem
)
from PySide6.QtCore import QThread, Signal, QObject
from services.chatgpt_service import get_itinerary
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LazyTraveler")

        central_widget = QWidget()
        main_layout = QVBoxLayout()
        title = QLabel("Hop aboard the LazyTraveler")
        main_layout.addWidget(title)
        
        self.destination_input =  QLineEdit()
        self.destination_input.setPlaceholderText("Enter your destination")
        main_layout.addWidget(self.destination_input)

        styles_group = QGroupBox("Select Travel Style")
        styles_layout = QHBoxLayout()
        self.adventurous = QCheckBox("Adventurous")
        self.relaxed = QCheckBox("Relaxed")
        self.luxury = QCheckBox("Luxury")
        self.budget = QCheckBox("Budget")
        styles_layout.addWidget(self.adventurous)
        styles_layout.addWidget(self.relaxed)
        styles_layout.addWidget(self.luxury)
        styles_layout.addWidget(self.budget)
        styles_group.setLayout(styles_layout)
        main_layout.addWidget(styles_group)

        self.number_of_days_input = QLineEdit()
        self.number_of_days_input.setPlaceholderText("How many days are you traveling?")
        main_layout.addWidget(self.number_of_days_input)

        self.generate_button = QPushButton("Generate Itinerary")
        main_layout.addWidget(self.generate_button)
        
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(["Itinerary"])
        main_layout.addWidget(self.results_tree)

        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect button
        self.generate_button.clicked.connect(self.on_generate)

    def on_generate(self):
        destination = self.destination_input.text()
        days = int(self.number_of_days_input.text())
        styles = []
        if self.adventurous.isChecked():
            styles.append("Adventurous")
        if self.relaxed.isChecked():
            styles.append("Relaxed")
        if self.luxury.isChecked():
            styles.append("Luxury")
        if self.budget.isChecked():
            styles.append("Budget")
        
        print("Destination:", destination)
        print("Travel Styles:", styles)
        
        # Get itinerary from ChatGPT
        try:
            itinerary = get_itinerary(destination, styles, days)
        except Exception as e:
            print(f"Error getting itinerary: {e}")

        
        self.results_tree.clear()
        for day, items in itinerary.items():
            day_item = QTreeWidgetItem([day])
            for act in items:
                QTreeWidgetItem(day_item, [act])
            self.results_tree.addTopLevelItem(day_item)