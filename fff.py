from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

app = QApplication([])
window = QMainWindow()

# Create the central widget and layout
central_widget = QWidget(window)
layout = QVBoxLayout(central_widget)

# Create the QTreeWidget
tree = QTreeWidget(central_widget)

# Adding some top-level items to the tree
for i in range(3):
    top_item = QTreeWidgetItem(tree)
    top_item.setText(0, f"Top Level Item {i}")

    # Adding some child items to each top-level item
    for j in range(3):
        child_item = QTreeWidgetItem(top_item)
        child_item.setText(0, f"Child Item {j}")
        top_item.addChild(child_item)


def on_item_clicked(item, column):
    top_item = item.parent()
    if top_item:
        print(f"Top-level item text: {top_item.text(0)}")


tree.itemClicked.connect(on_item_clicked)

# Add the QTreeWidget to the layout
layout.addWidget(tree)

# Set the central widget and show the window
window.setCentralWidget(central_widget)
window.show()

app.exec_()
