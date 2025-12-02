import tkinter as tk

def show_frame(frame):
    frame.tkraise()

main_window = tk.Tk()
main_window.title("Titan Campus Algorithmic Assistant")
main_window.geometry('1280x720')

main_window.rowconfigure(0, weight=1)
main_window.columnconfigure(1, weight=1)

# styling for navigation bar buttons
button_style = {
    "bg": "#00274c",
    "fg": "white",
    "font": ("Arial", 10, "bold"),
    "relief": "flat",
    "wraplength": 120 
}


nav_frame = tk.Frame(main_window, bg="#00274c")
nav_frame.grid(row=0, column=0, sticky = 'nsew')

campus_nav_btn = tk.Button(
    nav_frame,
    text = "CAMPUS NAVIGATION",
    command = lambda: show_frame(campus_nav_page),
    **button_style
)
campus_nav_btn.pack(fill='x', pady=10, padx=5)

study_planner_btn = tk.Button(
    nav_frame, 
    text="STUDY PLANNER", 
    command=lambda: show_frame(study_planner_page),
    **button_style
)
study_planner_btn.pack(fill='x', pady=10, padx=5)

notes_search_btn = tk.Button(
    nav_frame, 
    text="NOTES SEARCH", 
    command=lambda: show_frame(notes_search_engine_page),
    **button_style
)
notes_search_btn.pack(fill='x', pady=10, padx=5)

algo_info_btn = tk.Button(
    nav_frame, 
    text="ALGORITHM INFO", 
    command=lambda: show_frame(algo_info_page),
    **button_style
)
algo_info_btn.pack(fill='x', pady=10, padx=5)


page_container = tk.Frame(main_window)
page_container.grid(row = 0, column = 1, sticky = 'nsew')

page_container.rowconfigure(0, weight = 1)
page_container.rowconfigure(0, weight = 1)


campus_nav_page = tk.Frame(page_container)
study_planner_page = tk.Frame(page_container)
notes_search_engine_page = tk.Frame(page_container)
algo_info_page = tk.Frame(page_container)

for frame in (campus_nav_page, study_planner_page, notes_search_engine_page, algo_info_page):
    frame.grid(row=0, column=0, sticky='nsew')

# CAMPUS NAV PAGE
campus_nav_label = tk.Label(campus_nav_page, text = "CAMPUS NAV PAGE")
campus_nav_label.pack()

# STUDY PLANNER PAGE
study_planner_label = tk.Label(study_planner_page, text = "STUDY PLANNER PAGE")
study_planner_label.pack()

# NOTES SEARCH ENGINE PAGE
notes_search_label = tk.Label(notes_search_engine_page, text = "NOTES SEARCH PAGE")
notes_search_label.pack()


# ALGO INFO PAGE
algo_info_label = tk.Label(algo_info_page, text = "ALGO INFO PAGE")
algo_info_label.pack()

main_window.mainloop()