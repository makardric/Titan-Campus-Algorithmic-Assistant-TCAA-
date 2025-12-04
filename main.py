import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QSize, Qt, QCoreApplication
from ui import Ui_MainWindow
from collections import deque


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 

        # hardcoded for example sake as well as testing
        self.adj_list = {
            "LIBRARY": {"GYM": 10, "DORM": 5, "SCIENCE HALL": 20},
            "GYM": {"LIBRARY": 10, "CAFETERIA": 8},
            "DORM": {"LIBRARY": 5, "CAFETERIA": 15},
            "CAFETERIA": {"GYM": 8, "DORM": 15},
            "SCIENCE HALL": {"LIBRARY": 20}
        }

        # add adj_list to the comboboxes
        for building in self.adj_list.keys():
            self.start_building_combo.addItem(building)
            self.end_building_combo.addItem(building)

        # display current adj_list to the text box
        adj_list_string = ""
        for building, connection in self.adj_list.items():
            adj_list_string += (f"{building} : {connection}\n")
        self.adjacency_list_display.setText(adj_list_string)
        
        
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

    # bfs algorithm
    def bfs_shortest_paths(self, graph, start):
        dist = {v: float('inf') for v in graph}
        parent = {v: None for v in graph}
        visited = set()
        q = deque([start])
        visited.add(start)
        dist[start] = 0
        order = []

        while q:
            u = q.popleft()
            order.append(u)
            for v in graph[u]:
                if v not in visited:
                    visited.add(v)
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    q.append(v)
        return parent, order
    
    # helper function for bfs
    def reconstruct_path(self, parent, start, target):
        rev_path = []
        cur = target
        while cur is not None:
            rev_path.append(cur)
            if cur == start:
                break
            cur = parent.get(cur,None)
        if not rev_path or rev_path[-1] != start:
            return []
        return list(reversed(rev_path))

    def dfs_path(self, graph, start, target):
        visited = set()
        parent = {}
        order = []
        found = False
        has_cycle = False

        def dfs(u, prev_node):
            nonlocal found, has_cycle
            
            visited.add(u)
            order.append(u)

            if u == target:
                found = True

            for v in graph.get(u, {}):

                if v in visited and v != prev_node:
                    has_cycle = True

                if v not in visited:
                    parent[v] = u
                    dfs(v, u)

        if start in graph:
            dfs(start, None)

        return parent, order, has_cycle

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
    
    # function to insert edge
    def insert_edge(self):
        node1 = self.building_name_input.text().upper()
        node2 = self.neighbor_name_input.text().upper()

        # check if user is inputting the same name for both buildings
        if node1 == node2:
            QMessageBox.warning(self, "Warning!", "Building cannot connect to itself")
            return
        
        distance = self.distance_input.value()

        # check if building exists in the adjacency list
        if node1 not in self.adj_list:               # if not add a new entry into the dictionary 
            self.adj_list[node1] = {}
            self.update_combo_boxes(node1)

        self.adj_list[node1][node2] = distance
        
        if node2 not in self.adj_list:
            self.adj_list[node2] = {}
            self.update_combo_boxes(node2)
        
        self.adj_list[node2][node1] = distance

        self.building_name_input.setText("")
        self.neighbor_name_input.setText("")
        self.distance_input.setValue(0)
        formatted_string = ""
        for building, connection in self.adj_list.items():
            formatted_string += (f"{building} : {connection}\n")
        self.adjacency_list_display.setText(formatted_string)
        print(self.adj_list)
        
    # function to update combo boxes with the node inputted by user
    def update_combo_boxes(self, new_node):
        if self.start_building_combo.findText(new_node) == -1:
            self.start_building_combo.addItem(new_node)
            self.end_building_combo.addItem(new_node)

    # function to handle running the selected algorithm
    def handle_run_algorithm(self):
        start_node = self.start_building_combo.currentText()
        end_node = self.end_building_combo.currentText()
        algo = self.algorithm_combo.currentText()
        
        print(f"Running {algo} from {start_node} to {end_node}")
        if algo == "BFS":
            parent, order = self.bfs_shortest_paths(self.adj_list, start_node)
            path = self.reconstruct_path(parent, start_node, end_node)

            if path:
                path_str = " -> ".join(path)
                hops = len(path) - 1
                result_text = (f"Algorithm: BFS \
                                \nPath: {path_str} \
                                \nHops: {hops}")
                print(order)
            else:
                result_text = "No path found"
            self.navigator_output_display.setText(result_text)

        elif algo == "DFS":
            parent, order, has_cycle = self.dfs_path(self.adj_list, start_node, end_node)
            path = self.reconstruct_path(parent, start_node, end_node)

            if path:
                path_str = " -> ".join(path)

                # get total distance
                total_dist = 0
                for i in range(len(path) - 1):
                    u = path[i]
                    v = path[i+1]
                    total_dist += self.adj_list[u][v]
                
                hops = len(path) - 1
                result_text = (f"Algorithm: DFS\
                                \nPath: {path_str}\
                                \nHops: {hops}\
                                \nCycle: {has_cycle}\
                                \nDistance: {total_dist}")
            else:
                result_text = "No path found"
            self.navigator_output_display.setText(result_text)
        elif algo == "Dijkstra":
            pass
        elif algo == "Prim's":
            pass

if __name__ == "__main__":
    # lines to help scaling on different monitors
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())