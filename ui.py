import PySimpleGUI as sg
import os

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib

matplotlib.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="none", expand=1)
    return figure_canvas_agg

def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    
def img_update(fig_agg,window,imgs) :
    img_num = ...
    fig = matplotlib.figure.Figure(figsize=(10, 5), dpi=75)
    fig.add_subplot(111).imshow(...)
    fig.axes[0].get_xaxis().set_visible(False)
    fig.axes[0].get_yaxis().set_visible(False)
    if fig_agg is not None :
        delete_fig_agg(fig_agg)
    draw_figure(window["-imgs-"],fig)
    return fig_agg
    
layout = [
                [
                    sg.Text('Prompt:'),
                    sg.In(default_text='hello world',size = (16,1),enable_events = True,key = "-prompt-"),
                    sg.Button("Get",key="-Get-",tooltip=True),
                    sg.Text('Select:'),
                    sg.In(default_text='0',size = (16,1),enable_events = True,key = "-select_idx-"),
                    sg.Button("Select",key="-Select-",tooltip=True)
                ],
                [sg.Canvas(key="-imgs-",size = (120,40))],
            ]

window = sg.Window(title="Hi", layout=layout, background_color="#ffffff", font='Courier 12',finalize=True, element_justification='center')

# 加载初始图片
fig_agg = img_update(fig_agg = None,window = window,imgs = ...)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED :
        break
    if event == "-select_idx-" :
        idx = values["-select_idx-"]
        
    if event == "-Get-" :
        if idx != "" :
            # 再优化
            window.perform_long_operation(lambda:..., "-refine_complete-")
        else:
            # 优化
            window.perform_long_operation(lambda:..., "-refine_complete-")
        
    if event == "-refine_complete-" :
        fig_agg = img_update(fig_agg = fig_agg,window = window,imgs = ...)

window.close()