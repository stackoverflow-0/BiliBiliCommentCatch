import PySimpleGUI as sg
import os

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib

from comment_viz.comment_time_viz import *

# fig = matplotlib.figure.Figure(figsize=(20, 4), dpi=50)
# ax = fig.add_subplot(111)
# ax = comment_time_viz(ax=ax,level_limit=6)
matplotlib.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="none", expand=1)
    return figure_canvas_agg

def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()

file_column = [
                # [
                #     sg.Text("Path:"),
                #     sg.In(size = (5,1),enable_events = True,key = "-FOLDER-"),
                #     sg.FolderBrowse(button_text='File',size=(5,1)),
                # ],
                # [
                #     sg.Listbox(values=['e0','e1','e2'], enable_events=True, size=(17, 10), key="-FILE LIST-")
                # ]
                
            ]
viz_column = [
                [
                    sg.Text('user level:'),
                    sg.In(default_text='0,1,2,3,4,5,6',size = (16,1),enable_events = True,key = "-LEVEL-"), 
                    sg.VSeparator(),
                    sg.Button("Viz",key="ok",tooltip=True),
                    # sg.Check(text='<'),
                    # sg.Check(text='='),
                    
                    # sg.Check(text='>'),
                ],
                [sg.Canvas(key="-Comment_Time_Viz-",size = (120,40))],
                [sg.Canvas(key="-Comment_Level_Viz-",size = (40,40)),sg.Canvas(key="-Word_Cloud_Viz-",size = (60,40))],
            ]



layout = [[sg.Column(file_column),sg.VSeparator(),sg.Column(viz_column)]]

window = sg.Window(title="BiliBili Comment Viz", layout=layout, background_color="#ffffff", font='Courier 12',finalize=True, element_justification='center')

level_list = ['0','1','2','3','4','5','6']
time_fig = comment_time_viz(level_list=level_list)
time_fig_agg = draw_figure(window["-Comment_Time_Viz-"].TKCanvas, time_fig)

level_fig = comment_level_viz()
level_fig_agg = draw_figure(window["-Comment_Level_Viz-"].TKCanvas, level_fig)

word_cloud_fig = word_cloud()
word_cloud_fig_agg = draw_figure(window["-Word_Cloud_Viz-"].TKCanvas, word_cloud_fig)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED :
            break
    if event == "-FILE LIST-" :
        print(values["-FILE LIST-"])
    if event == "-LEVEL-" :
        if values["-LEVEL-"] != '':
            level_list = values["-LEVEL-"].split(',')
            print(level_list)
    if event == "ok":
        delete_fig_agg(time_fig_agg)
        time_fig = comment_time_viz(level_list=level_list)
        time_fig_agg = draw_figure(window["-Comment_Time_Viz-"].TKCanvas, time_fig)
        delete_fig_agg(level_fig_agg)
        level_fig = comment_level_viz(level_list=level_list)
        level_fig_agg = draw_figure(window["-Comment_Level_Viz-"].TKCanvas, level_fig)
    
    if event == "-FOLDER-" :
        folder = values["-FOLDER-"]
        try:
            filelist = os.listdir(folder)
            print(filelist)
        except:
            filelist = []
            
window.close()