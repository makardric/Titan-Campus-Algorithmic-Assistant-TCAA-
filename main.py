import sys, heapq, PyPDF2, docx, os, time, re
from collections import deque
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView, QFileDialog
from PyQt5.QtCore import QSize, Qt, QCoreApplication
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



# campus nav page 

        # hardcoded adjacency list for example's sake as well as testing
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
        
# study planner page 

        # hardcoded tasks for example's sake and testing
        self.study_tasks = [
            ("STUDY FOR MATH", 4, 10),
            ("HISTORY HOMEWORK", 3, 7),
            ("PHYSICS LAB", 2, 4)
        ]

        # add the hardcoded tasks to table
        for name, time, value in self.study_tasks:
            self.add_task_to_table(name, time, value)

        # connect functions to buttons/input
        self.add_task_button.clicked.connect(self.add_task)
        self.task_list_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.run_scheduler_button.clicked.connect(self.generate_schedule)

# notes search engine page
        self.text_files = {}
        self.add_file_button.clicked.connect(self.insert_file)
        self.file_list_combo.currentIndexChanged.connect(self.update_file_display)
        self.search_button.clicked.connect(self.run_search)

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

# campus nav functions
         
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

    # function for dfs
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

    # function for dijkstra
    def dijkstra(self, graph, start, target):
        dist = {v: float('inf') for v in graph}
        dist[start] = 0

        parent = {v: None for v in graph}

        pq = [(0, start)]

        visited = set()

        while pq:
            current_dist, u = heapq.heappop(pq)

            if u == target:
                break

            if u in visited:
                continue
            visited.add(u)

            for v, weight in graph.get(u, {}).items():
                distance = current_dist + weight
                if distance < dist[v]:
                    dist[v] = distance
                    parent[v] = u
                    heapq.heappush(pq, (distance, v))
        
        return dist, parent

    # function for prim's
    def prim(self, graph, start):
        mst_edges = []
        visited = set()
        total_cost = 0

        min_heap = [(0, start, start)]

        while min_heap:
            weight, u, v = heapq.heappop(min_heap)

            if v in visited:
                continue
                
            visited.add(v)
            total_cost += weight

            if u!= v:
                mst_edges.append((u, v, weight))

            for neighbor, edge_weight in graph.get(v, {}).items():
                if neighbor not in visited:
                    heapq.heappush(min_heap, (edge_weight, v, neighbor))
        
        return mst_edges, total_cost
    
    # function to insert edge for campus nav
    def insert_edge(self):
        node1 = self.building_name_input.text().upper()
        node2 = self.neighbor_name_input.text().upper()

        # check if user is inputting nothing
        if node1 == "" or node2 == "":
            QMessageBox.warning(self,"Warning!", "Please input valid buildings")
            return
        # check if user is inputting the same name for both buildings
        if node1 == node2:
            QMessageBox.warning(self, "Warning!", "Building cannot connect to itself")
            return
        
        distance = self.distance_input.value()

        # check if building exists in the adjacency list
        if node1 not in self.adj_list:              
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

    # function to handle running the selected algorithm for campus nav
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
                                \nTotal Distance: {total_dist}")
            else:
                result_text = "No path found"
            self.navigator_output_display.setText(result_text)

        elif algo == "Dijkstra":
            distances, parent = self.dijkstra(self.adj_list, start_node, end_node)
            path = self.reconstruct_path(parent, start_node, end_node)

            if path:
                path_str = " -> ".join(path)
                total_dist = distances[end_node]
                hops = len(path) - 1
                result_text = (f"Algorithm: Dijkstra\
                               \nPath: {path_str}\
                               \nHops: {hops}\
                               \nTotal Distance: {total_dist}")
            else:
                result_text = "No path found"
            self.navigator_output_display.setText(result_text)

        elif algo == "Prim's":
            edges, total_cost = self.prim(self.adj_list, start_node)

            if edges:
                edges_str = "" 
                for u, v, w in edges:
                    edges_str += f"{u} -- {w} -- > {v}\n"
                
                result_text = (f"Algorithm: Prim's (MST)\
                               \nTotal Cost: {total_cost}\
                               \nEdges in MST:\n{edges_str}")
            
            else:
                result_text = "No edges found"
            self.navigator_output_display.setText(result_text)


# study planner functions

    def add_task(self):
        task_name = self.task_name_input.text().upper()
        task_time = self.task_time_input.value()
        task_value = self.task_value_input.value()

        if not task_name:
            QMessageBox.warning(self, "Warning", "Please enter a task name.")
            return

        task_tuple = (task_name, task_time, task_value)
        
        self.study_tasks.append(task_tuple)

        self.add_task_to_table(task_name, task_time, task_value)

        self.task_name_input.setText("")
        self.task_time_input.setValue(0)
        self.task_value_input.setValue(0)

    def add_task_to_table(self, name, time, value):
        row_position = self.task_list_table.rowCount()

        self.task_list_table.insertRow(row_position)

        name_item = QTableWidgetItem(name)
        time_item = QTableWidgetItem(str(time) + " hour(s)")
        value_item = QTableWidgetItem(str(value))

        self.task_list_table.setItem(row_position, 0, name_item)
        self.task_list_table.setItem(row_position, 1, time_item)
        self.task_list_table.setItem(row_position, 2, value_item)

    # function runs both greedy and dp (knapsack)
    def generate_schedule(self):
        capacity = self.total_time_input.value()
        tasks = self.study_tasks
        n = len(tasks)

        if n == 0:
            self.totals_label.setText("No tasks added!")
            return
        
        # greedy algorithm
        greedy_list = []
        for name, time, value in tasks:
            if time > 0:
                ratio = value/time
                greedy_list.append((ratio, name, time, value))

        # sort the list by the ratios greatest to least
        greedy_list.sort(key=lambda x: x[0], reverse=True)

        greedy_time = 0
        greedy_value = 0
        greedy_selected = []

        for _, name, time, value in greedy_list:
            if greedy_time + time <= capacity:
                greedy_selected.append(name)
                greedy_time += time
                greedy_value += value

        # dp algorithm
        dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

        for i in range(1, n + 1):
            name, time, value = tasks[i-1]
            for w in range(capacity + 1):
                if time <= w:
                    dp[i][w] = max(dp[i-1][w], dp[i-1][w - time] + value)
                else:
                    dp[i][w] = dp[i-1][w]

        dp_value = dp[n][capacity]
        dp_selected = []
        dp_time = 0
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                name, time, value = tasks[i-1]
                dp_selected.append(name)
                dp_time += time
                w -= time
        dp_selected.reverse()      


        greedy_str = ", ".join(greedy_selected) if greedy_selected else "None"
        dp_str = ", ".join(dp_selected) if dp_selected else "None"

        result_text = (f"Greedy Vs. DP\
                       \nGreedy Algorithm:\
                       \nSchedule: {greedy_str}\
                       \nTotal Value: {greedy_value}\
                       \nTime Used: {greedy_time}/{capacity}\
                       \n\nDP Algorithm\
                       \nSchedule: {dp_str}\
                       \nTotal Value: {dp_value}\
                       \nTime Used: {dp_time}/{capacity}"
                       )

        if greedy_value < dp_value:
            diff = dp_value - greedy_value
            result_text += (f"\nGreedy failed. DP found +{diff} value.")
        else:
            result_text += (f"\nGreedy found the optimal schedule.")

        self.totals_label.setText(result_text)


# note search engine page functions
    # function to insert a file
    def insert_file(self):
        file_path,_ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt *.pdf *.docx)")

        if not file_path:
            return
        
        filename = os.path.basename(file_path)
        file_text = ""

        try:
            if filename.lower().endswith('.pdf'):
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        file_text += page.extract_text() + " "
        
            elif file_path.lower().endswith('.docx'):
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    file_text += para.text + "\n"
            else:
                with open(file_path, "r", encoding = "utf-8") as f:
                    file_text += f.read()

            file_text = file_text.replace("\n", ' ')
            file_text = re.sub(r'\s+', ' ', file_text)
            
            if filename not in self.text_files:
                self.file_list_combo.addItem(filename)
            
            self.text_files[filename] = file_text

            self.file_list_combo.setCurrentText(filename)

            self.file_text_display.setText(file_text)

        except:
            QMessageBox.critical(self, "Error", "Could not read file")

    # updates the file text display when user changes the file in combo box
    def update_file_display(self):
            current_filename = self.file_list_combo.currentText()
            
            if current_filename in self.text_files:
                content = self.text_files[current_filename]
                self.file_text_display.setText(content)

    def naive_search(self, lines, keyword):
        matches = []
        m = len(keyword)
        
        for line_num, line in enumerate(lines, start=1):
            text = line.lower()
            n = len(text)
            
            for i in range(n - m + 1):
                match_found = True
                for j in range(m):
                    if text[i + j] != keyword[j]:
                        match_found = False
                        break 
                if match_found:
                    matches.append((line_num, line.strip()))
                    break
        return matches

# function for rabin_karp search
    def rabin_karp(self, lines, keyword):
        matches = []
        m = len(keyword)
        d = 256 # alphabet size
        q = 101 # prime number
        
        h = 1
        for i in range(m-1):
            h = (h * d) % q
        
        p = 0
        for i in range(m):
            p = (d * p + ord(keyword[i])) % q

        for line_num, line in enumerate(lines, start=1):
            text = line.lower()
            n = len(text)
            if m > n: continue

            t = 0
            for i in range(m):
                t = (d * t + ord(text[i])) % q
            
            for i in range(n - m + 1):
                if p == t:
                    if text[i:i+m] == keyword:
                        matches.append((line_num, line.strip()))
                        break
                
                if i < n - m:
                    t = (d*(t - ord(text[i])*h) + ord(text[i+m])) % q
                    if t < 0: t = t + q

        return matches
        
    def kmp_search(self, lines, keyword):
        matches = []
        m = len(keyword)
        
        # build lps table
        lps = [0] * m
        length = 0
        i = 1
        while i < m:
            if keyword[i] == keyword[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        # search lines
        for line_num, line in enumerate(lines, start=1):
            text = line.lower()
            n = len(text)
            i = 0 
            j = 0 
            
            while i < n:
                if keyword[j] == text[i]:
                    i += 1
                    j += 1
                if j == m:
                    matches.append((line_num, line.strip()))
                    break 
                elif i < n and keyword[j] != text[i]:
                    if j != 0:
                        j = lps[j-1]
                    else:
                        i += 1
        return matches
    
    def run_search(self):
        current_filename = self.file_list_combo.currentText()
        keyword = self.search_bar.text().lower()
        algo_to_run = self.search_algorithm_combo.currentText()


        
        if current_filename not in self.text_files:
            QMessageBox.warning(self, "Warning", "No file selected!")
            return
        
        if keyword == "":
            QMessageBox.warning(self, "Warning", "No keyword provided!")
            return


        # cleans up the text to make sure they aren't grouped together by paragraphs
        text = self.text_files[current_filename] 
        lines = text.split('\n')
        clean_text = text.replace('\n', ' ')
        # separates by punctuation
        lines = re.split(r'(?<=[.!?])\s+', clean_text)
        lines = [line.strip() for line in lines if line.strip()]
        result_text = ""

        # checks if it is one of the three algorithms in combo box
        if algo_to_run != "ALL (Comparison)":
            # start timer
            start_time = time.perf_counter()
            matches = []

            if algo_to_run == "Naive":   
                matches = self.naive_search(lines, keyword)
            elif algo_to_run == "Rabin-Karp":
                matches = self.rabin_karp(lines, keyword)
            elif algo_to_run == "KMP":
                matches = self.kmp_search(lines, keyword)

            end_time = time.perf_counter()
            elapsed = (end_time - start_time) * 1000
            
            result_text = (f"Algorithm: {algo_to_run}\
                           \nTime: {elapsed:.4f} ms\
                           \nMatches Found: {len(matches)}")
            
            if not matches:
                result_text += "\nNo matches found."
            else:
                for line_num, line_text in matches:
                    result_text += (f"\nLine {line_num}: {line_text}")

        if algo_to_run == "ALL (Comparison)":
            naive_start_time = time.perf_counter()
            naive_matches =self.naive_search(lines, keyword)
            end_time = time.perf_counter()
            naive_elapsed = (end_time - naive_start_time) * 1000

            rabin_start_time = time.perf_counter()
            rabin_matches = self.rabin_karp(lines, keyword)
            end_time = time.perf_counter()
            rabin_elapsed = (end_time - rabin_start_time) * 1000

            kmp_start_time = time.perf_counter()
            kmp_matches = self.kmp_search(lines, keyword)
            end_time = time.perf_counter()
            kmp_elapsed = (end_time - kmp_start_time) * 1000

            result_text = (f"Comparison of Naive, Rabin-Karp, and KMP:\
                            \nNaive time taken: {naive_elapsed:.4f} ms\
                            \nNaive matches found: {len(naive_matches)}\
                            \nRabin-Karp time taken: {rabin_elapsed:.4f} ms\
                            \nRabin-Karp matches found: {len(rabin_matches)}\
                            \nKMP time taken: {kmp_elapsed:.4f} ms\
                            \nKMP matches found: {len(kmp_matches)}"
                            )
        self.note_display_browser.setText(result_text)
if __name__ == "__main__":
    # lines to help scaling on different monitors
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())