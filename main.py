import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject, QSize
from ui import Ui_MainWindow


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self) 
        
        # add icon to home button
        buttonIcon = QIcon("resources/titans logo.png")
        self.home_button.setIcon(buttonIcon)
        self.home_button.clicked.connect(self.go_to_home_page)
        self.home_button.setIconSize(QSize(130, 130))

        # set initial page to home page
        self.stackedWidget.setCurrentWidget(self.home_page) 

        # add functionality to side navbar
        self.campus_nav_button.clicked.connect(self.go_to_campus_nav_page)
        self.study_planner_button.clicked.connect(self.go_to_study_planner_page)
        self.notes_search_button.clicked.connect(self.go_to_notes_search_page) 
        self.algo_info_button.clicked.connect(self.go_to_algo_info_page)
        

        # connecting functions to buttons on all pages
        self.add_edge_button.clicked.connect(self.insert_edge)
        self.run_algo_button.clicked.connect(self.handle_run_algorithm)

    
    # functions for sidebar buttons
    def go_to_home_page(self):
        self.stackedWidget.setCurrentWidget(self.home_page)

    def go_to_campus_nav_page(self):
        self.stackedWidget.setCurrentWidget(self.campus_nav) 

    def go_to_study_planner_page(self):
        self.stackedWidget.setCurrentWidget(self.study_planner)

    def go_to_notes_search_page(self):
        self.stackedWidget.setCurrentWidget(self.notes_search)

    def go_to_algo_info_page(self):
        self.stackedWidget.setCurrentWidget(self.algo_info)
    
    def insert_edge(self):
        node1 = self.building_name_input.text()
        node2 = self.neighbor_name_input.text()

        if node1.lower() == node2.lower():
            QMessageBox.warning(self, "Warning!", "Building cannot connect to itself")
            return
        
        distance = self.distance_input.value()

        if node1 not in adj_list:
            adj_list[node1] = {}
            self.update_combo_boxes(node1)

        adj_list[node1][node2] = distance
        
        if node2 not in adj_list:
            adj_list[node2] = {}
            self.update_combo_boxes(node2)
        
        adj_list[node2][node1] = distance

        self.building_name_input.setText("")
        self.neighbor_name_input.setText("")
        self.distance_input.setValue(0)
        formatted_string = ""
        for building, connection in adj_list.items():
            formatted_string += (f"{building} : {connection}\n")
        self.adjacency_list_display.setText(formatted_string)
        print(adj_list)
        

    def update_combo_boxes(self, new_node):
        if self.start_building_combo.findText(new_node) == -1:
            self.start_building_combo.addItem(new_node)
            self.end_building_combo.addItem(new_node)

    def handle_run_algorithm(self):
        start_node = self.start_building_combo.currentText()
        end_node = self.end_building_combo.currentText()
        algo = self.algorithm_combo.currentText()
        
        print(f"Running {algo} from {start_node} to {end_node}")
        
        self.navigator_output_display.setText(f"Algorithm running...\nStart: {start_node}\nEnd: {end_node}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()

    adj_list = {}



    sys.exit(app.exec_())