# from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget,Q
#
# app = QApplication([])
# window = QMainWindow()
#
# # Create the central widget and layout
# central_widget = QWidget(window)
# layout = QVBoxLayout(central_widget)
#
# # Create the QTreeWidget
# tree = QTreeWidget(central_widget)
#
# # Adding some top-level items to the tree
# for i in range(3):
#     top_item = QTreeWidgetItem(tree)
#     top_item.setText(0, f"Top Level Item {i}")
#
#     # Adding some child items to each top-level item
#     for j in range(3):
#         child_item = QTreeWidgetItem(top_item)
#         child_item.setText(0, f"Child Item {j}")
#         top_item.addChild(child_item)
#
#
# def on_item_clicked(item, column):
#     top_item = item.parent()
#     if top_item:
#         print(f"Top-level item text: {top_item.text(0)}")
#
#
# tree.itemClicked.connect(on_item_clicked)
#
# # Add the QTreeWidget to the layout
# layout.addWidget(tree)
#
# # Set the central widget and show the window
# window.setCentralWidget(central_widget)
# window.show()
#
# app.exec_()
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget
#
# class StudentTestStatisticsDashboard(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Student Test Statistics Dashboard")
#
#         # Create widgets
#         self.name_label = QLabel("Name:")
#         self.name_edit = QLineEdit()
#         self.score_label = QLabel("Score:")
#         self.score_edit = QLineEdit()
#
#         # Create layout and add widgets
#         layout = QVBoxLayout()
#         layout.addWidget(self.name_label)
#         layout.addWidget(self.name_edit)
#         layout.addWidget(self.score_label)
#         layout.addWidget(self.score_edit)
#
#         # Create central widget and set layout
#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     dashboard = StudentTestStatisticsDashboard()
#     dashboard.show()
#     sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton

class StudentTestResultStatisticsDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Test Result Statistics Dashboard")

        # Create widgets
        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        self.test1_score_label = QLabel("Test 1 Score:")
        self.test1_score_edit = QLineEdit()
        self.test2_score_label = QLabel("Test 2 Score:")
        self.test2_score_edit = QLineEdit()
        self.difference_label = QLabel("Difference:")
        self.difference_display = QLineEdit()
        self.difference_display.setReadOnly(True)
        self.calculate_difference_button = QPushButton("Calculate Difference")

        # Connect button to calculation function
        self.calculate_difference_button.clicked.connect(self.calculate_difference)

        # Create layout for labels and line edits
        inputs_layout = QVBoxLayout()
        inputs_layout.addWidget(self.name_label)
        inputs_layout.addWidget(self.name_edit)
        inputs_layout.addWidget(self.test1_score_label)
        inputs_layout.addWidget(self.test1_score_edit)
        inputs_layout.addWidget(self.test2_score_label)
        inputs_layout.addWidget(self.test2_score_edit)

        # Create layout for button and difference display
        outputs_layout = QVBoxLayout()
        outputs_layout.addWidget(self.difference_label)
        outputs_layout.addWidget(self.difference_display)
        outputs_layout.addWidget(self.calculate_difference_button)

        # Create main layout and add sub-layouts
        main_layout = QHBoxLayout()
        main_layout.addLayout(inputs_layout)
        main_layout.addLayout(outputs_layout)

        # Create central widget and set layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def calculate_difference(self):
        # Get scores from line edits and calculate difference
        test1_score = int(self.test1_score_edit.text())
        test2_score = int(self.test2_score_edit.text())
        difference = test2_score - test1_score

        # Display difference in line edit
        self.difference_display.setText(str(difference))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = StudentTestResultStatisticsDashboard()
    dashboard.show()
    sys.exit(app.exec_())