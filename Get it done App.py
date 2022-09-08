import PySimpleGUI as sg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Window settings
sg.theme('DarkBlue12')
margins = (100, 60)
button_size_1 = (20,1)
font_1=("Calibri 22")
font_2=("Calibri 15")

# Goals
raw_data = pd.read_table("goalsDB.txt", sep=";", header=0)

def build_string_of_goals(list_of_goals):
    new_list = ""
    for goal in list_of_goals:
        new_list+="- "
        new_list+=goal
        new_list+="\n"
    if len(new_list) >= 2:
        new_list = new_list[:-1]
    return new_list

def build_string_of_goals_numerated(list_of_goals):
    new_list = ""
    i=1
    for goal in list_of_goals:
        new_list = new_list + str(i) + ". "
        new_list+=goal
        new_list+="\n"
        i+=1
    if len(new_list) >= 2:
        new_list = new_list[:-1]
    return new_list

def make_main_window():
    layout = [  [sg.Text("Get it done", size=(13,1), font=font_1)],
                [sg.Button('My goals', size=button_size_1, font=font_2)],
                [sg.Button("Goal analysis", size=button_size_1, font=font_2)],
                [sg.Button("Goal update", size=button_size_1, font=font_2)],
                [sg.Button('Exit', size=button_size_1, font=font_2)]
             ]
    return sg.Window(title="Get it done App", layout=layout, margins=(200,70), finalize=True)

def make_goals_window(goals):
    if len(goals)==0:
        text="Your goals will\nappear here as\nyou add them."
    else:
        text=build_string_of_goals(goals)
    goals_column = [
                     [sg.Text("My goals", size=(15,1), font=font_1)],
                     [sg.Multiline(key="listofgoals", default_text=text, size=(16,8), font="Calibri 16")]
                   ]
    buttons_column = [
                       [sg.Text("Add new goals or delete them by writing them and", size=(40,1), font="Calibri 13")],
                       [sg.Text("then clicking on the corresponding button.", size=(40,1), font="Calibri 13")],
                       [sg.Text("You can add up to 8 but the recommended is 6.", size=(40,1), font="Calibri 13")],
                       [sg.InputText(key="newgoal", font="Calibri 16", size=(16,2), border_width=3)],
                       [sg.Button('Add new goal', size=button_size_1, font=font_2)],
                       [sg.Button('Delete goal', size=button_size_1, font=font_2)],
                       [sg.Button('Clear all goals', size=button_size_1, font=font_2, button_color="#ff3333")],
                       [sg.Button('Back', size=button_size_1, font=font_2)]
                     ]
    layout = [
        [
         sg.Column(goals_column),
         sg.VSeperator(),
         sg.Column(buttons_column),
        ]
             ]
    return sg.Window(title='Get it done App - Goals', layout=layout, margins=margins, finalize=True)

def create_plot(data):
    goals = list(data["GOALS"])
    freq = list(data["TIMES DONE"])
    fig = plt.figure(figsize = (5.7, 4.6))
    fig.patch.set_facecolor('#324E7B')
    my_colors = ["#ef5350","#ec407a","#ab47bc","#5c6bc0","#29b6f6","#26a69a","#9ccc65","#ffca28"] 
    plt.bar(goals, freq, color = my_colors, width = 0.7)
    plt.rc('grid', linestyle="--", color='grey')
    plt.grid(b=True, axis="y")
    plt.yticks(color="white")
    plt.xticks(rotation=25, color="white", fontsize=11)
    plt.ylabel("Frequency", fontsize=15, color="white")
    return plt.gcf()

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def make_todays_goals_window(goals, times_done):
    data = pd.DataFrame(list(zip(goals, times_done)), columns=["GOALS", "TIMES DONE"])
    max_slider = len(data["GOALS"])
    if len(data["GOALS"])==0:
        max_slider = 1
        text = "You haven't added any goal yet."
    elif len(data["GOALS"])<4:
        sorted_goals = [data["GOALS"][i] for i in np.argsort(data["TIMES DONE"].to_numpy())]
        text = build_string_of_goals_numerated(sorted_goals)
    else:
        sorted_goals = [data["GOALS"][i] for i in np.argsort(data["TIMES DONE"].to_numpy())][0:4]
        text = build_string_of_goals_numerated(sorted_goals)
    left_column = [
        [sg.Text("Goals Frequency Graph", size=(25,1), font=font_1)],
        [sg.Canvas(key="goalsfrequency", size=(400,400))],
        [sg.Text("Here's a graph of the amount of times you have", size=(40,1), font="Calibri 13")],
        [sg.Text("registered each goal.", size=(40,1), font="Calibri 13")]
                  ]
    right_column = [
        [sg.Text("Recommended goals for today:", size=(26,1), font="Calibri 15")],
        [sg.Multiline(key="recommendedgoals", default_text=text, size=(18,4), font="Calibri 14")],
        [sg.HSeparator(color="Black")],
        [sg.Slider((1,max_slider),default_value=int(len(data["GOALS"])/2),key="randomslider", orientation="horizontal")],
        [sg.Button('Random set of goals', size=button_size_1, font=font_2)],
        [sg.Multiline(key="randomgoals", default_text=" ", size=(18,4), font="Calibri 14")],
        [sg.HSeparator(color="Black")],
        [sg.Button('Back', size=button_size_1, font=font_2)]
                   ]
    layout = [
        [
         sg.Column(left_column),
         sg.VSeperator(),
         sg.Column(right_column),
        ]
             ]
    window = sg.Window(title="Get it done App - Goal analysis", layout=layout, margins=(50,40), finalize=True)
    draw_figure(window["goalsfrequency"].TKCanvas, create_plot(data))
    return window

def make_goal_update_window(goals):
    if len(goals)==0:
        text="Your goals will\nappear here as\nyou add them."
    else:
        text=build_string_of_goals(goals)
    goals_column = [
                     [sg.Text("Currently doing", size=(15,1), font=font_1)],
                     [sg.Multiline(key="listofgoals", default_text=text, size=(16,8), font="Calibri 16")]
                   ]
    buttons_column = [
                       [sg.Text("What have you done today?", size=(30,1), font="Calibri 17")],
                       [sg.Text("One by one, select and then save the goals you", size=(40,1), font="Calibri 12")],
                       [sg.Text("have done today. Once you do it, the Goal Analysis", size=(41,1), font="Calibri 12")],
                       [sg.Text("section will be automatically updated.", size=(40,1), font="Calibri 12")],
                       [sg.Combo(goals, key="savebutton", size=(30,1), font="Calibri 13", default_value="None selected")],
                       [sg.Button('Save', size=button_size_1, font=font_2, button_color="green")],
                       [sg.Button('Back', size=button_size_1, font=font_2)]
                     ]
    layout = [
        [
         sg.Column(goals_column),
         sg.VSeperator(),
         sg.Column(buttons_column),
        ]
             ]
    return sg.Window(title='Get it done App - Goal update', layout=layout, margins=margins, finalize=True)

    

def main(data):
    # Data
    goals = list(data["GOALS"])
    times_done = list(data["TIMES DONE"])
    
    # Window management
    goal_window = None
    todays_goals_window = None
    goal_update_window = None
    main_window = make_main_window()
    
    # Main loop
    while True:
        
        # Load loop information
        window, event, values = sg.read_all_windows()
        
        # MAIN WINDOW
        if window == main_window:
            
            # Closing window management
            if event in (sg.WIN_CLOSED, "Exit"):
                break
            
            # My goals BUTTON
            if event == "My goals":
                main_window.hide()
                goal_window = make_goals_window(goals)
            
            # Goal analysis BUTTON
            if event == "Goal analysis":
                main_window.hide()
                todays_goals_window = make_todays_goals_window(goals, times_done)
            
            # Goal update BUTTON
            if event == "Goal update":
                main_window.hide()
                goal_update_window = make_goal_update_window(goals)
                
        
        # GOAL WINDOW
        if window == goal_window:
            
            # Closing window management
            if event in (sg.WIN_CLOSED, "Back"):
                goal_window.close()
                goal_window = None
                main_window.un_hide()
            
            # Add new goal BUTTON
            if event == "Add new goal":
                # Get the goal
                new_goal = values["newgoal"]
                # Bug management
                if new_goal=="" or new_goal=="Write the goal here" or new_goal=="Goal already saved!" or new_goal=="Goal not found!":
                    goal_window["newgoal"].update("Write the goal here")
                    continue
                if new_goal in goals:
                    goal_window["newgoal"].update("Goal already saved!")
                    continue
                if len(goals)==8:
                    goal_window["newgoal"].update("The maximum is 8")
                    continue
                # Save and update goals
                goals.append(new_goal)
                times_done.append(0)
                new_list = build_string_of_goals(goals)
                goal_window["listofgoals"].update(new_list)
                goal_window["newgoal"].update("")
            
            # Delete goal BUTTON
            if event == "Delete goal":
                # Get the goal
                new_goal = values["newgoal"]
                # Bug management
                if new_goal not in goals:
                    goal_window["newgoal"].update("Goal not found!")
                    continue
                # Save and update
                del times_done[goals.index(new_goal)]
                goals.remove(new_goal)
                new_list = build_string_of_goals(goals)
                goal_window["listofgoals"].update(new_list)
                goal_window["newgoal"].update("")
                
            # Clear all goals BUTTON
            if event == "Clear all goals":
                goals = []
                times_done = []
                goal_window["listofgoals"].update("The goals have\nbeen cleared.")

        # GOAL ANALYSIS WINDOW
        if window == todays_goals_window:
            
            # Closing window management
            if event in (sg.WIN_CLOSED, "Back"):
                todays_goals_window.close()
                todays_goals_window = None
                main_window.un_hide()
            
            if event == "Random set of goals":
                # Get the info
                num_goals = int(values["randomslider"])
                if len(goals)==0:
                    todays_goals_window["randomgoals"].update("You haven't added any goal yet.")
                    continue
                sample = random.sample(range(0, len(goals)), num_goals)
                goals_random_sample = [goals[i] for i in sample]
                list_random_goals = build_string_of_goals(goals_random_sample)
                todays_goals_window["randomgoals"].update(list_random_goals)
            
        # GOAL UPDATE WINDOW
        if window == goal_update_window:
            
            # Closing window management
            if event in (sg.WIN_CLOSED, "Back"):
                goal_update_window.close()
                goal_update_window = None
                main_window.un_hide()
            
            if event == "Save":
                # Get the info
                selected_goal = values["savebutton"]
                if selected_goal in goals:
                    index = goals.index(selected_goal)
                    times_done[index] += 1
                    goal_update_window["savebutton"].update("Goal saved!")
                


    new_data = pd.DataFrame(list(zip(goals, times_done)), columns=data.columns)
    main_window.close()
    return new_data

if __name__ == '__main__':
    new_data = main(raw_data)
    # Write the data
    new_data.to_csv("goalsDB.txt", sep=";", header=raw_data.columns, index=False)
    
