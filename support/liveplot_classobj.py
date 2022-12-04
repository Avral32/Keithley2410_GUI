from matplotlib import pyplot
import matplotlib.animation as animation
from random import randrange
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import sys
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import ttk

x_data, y_data = [], []

class Win(tk.Tk):
    
    def __init__(self):
        
        super().__init__()
        
        self.title('I-V liveplot')
        self.geometry('600x530')
        
        #self.rowconfigure(0, weight =0)
        #self.columnconfigure(0, weight =0)
        
        self.fig = plt.figure(figsize=(4, 3.5), dpi=100)
        self.ax = self.fig.add_subplot(1,1,1)
        self.line, = self.ax.plot([0], [0])
        self.ax.set_xlabel('Voltage / V', fontsize = 12)
        self.ax.set_ylabel('Current / A', fontsize = 12)
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.canvas.get_tk_widget().pack(side= tk.BOTTOM)
        
        
        self.is_paused = tk.BooleanVar()  # variable to hold the pause/resume state
        start_butt = ttk.Button(self, text="Pause", command=lambda: self.is_paused.set(True)).pack(side="right")
        stop_butt = ttk.Button(self, text="Resume", command=lambda: self.is_paused.set(False)).pack(side="right")
        
        self.start = tk.BooleanVar(value = False)
        start_butt = ttk.Button(self, text="Start", command= lambda: self.start.set(True)).pack(side='right')
             
        
        for widget in self.winfo_children():
            widget.pack(padx =5, pady =1)
        
        voltage_range_label = tk.Label(self, text = "Voltage range")
        voltage_range_label.pack(side = "left", padx = 10)
        self.voltage_range = tk.IntVar()
        self.voltage_range.set(100)
        voltage_range_spinbox = ttk.Spinbox(self, from_=-3e2, to = 5e2, textvariable = self.voltage_range, width =40)
        voltage_range_spinbox.pack(side="right", padx = 20)
    
        
    def update(self, k=1, step = 2):
    
        if self.start.get() and not self.is_paused.get():
            
            x_data.append([i for i in range(0,k,1)][-1])
            y = [i for i in range(0,k,step)][-1]
            y_data.append(np.sin(y/5))
            self.line.set_data(x_data, y_data)
            self.fig.gca().relim()
            self.fig.gca().autoscale_view()
            self.canvas.draw()
            self.canvas.flush_events()
            k += step
             
        if k <= self.voltage_range.get():
            
            self.after(100, self.update, k)
    
if __name__ == "__main__":
    
    app = Win()
    #ani = animation.FuncAnimation(app.fig, app.update, interval=100, blit=False)
    app.after(100, app.update)
        
    app.mainloop()