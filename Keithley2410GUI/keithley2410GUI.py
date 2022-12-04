"""
=====
Voltage and TIME SCANS with Keithley2410
=====
- In generally, you can measure the current, voltage under a given bias voltage 

- Do scanning voltage FOR a given range (start, stop, and step)
- Do a single-point current-voltage measurment OVER time.

- Author@Savutjan Sidik
- Date: 21/11/2022
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import keithley2410
from drawnow import drawnow
import matplotlib.pyplot as plt
import time
import numpy as np
import pandas as pd
from timeit import default_timer as timer


keith2410 = keithley2410.Keith2410()


class Keith2140(tk.Tk):
    """This is the main tkinter object that holds other three objects, 
    inlcuding Settings, VoltageScan and Timescan."""
    
    def __init__(self):
        
        super().__init__()
        
        self.title('Keithley2410 GUI')
        self.geometry('900x610')
        self.iconbitmap(self, default = "keithley2410.ico")
        
        
        self.rowconfigure(1, weight =1)
        self.columnconfigure(1, weight =1)
        
        
        self.__create_widgets()
        
    def __create_widgets(self):
    
        settings_frame = Settings(self)
        settings_frame.grid(row = 0, column = 0, pady = 10,  padx = 10, columnspan =2)
        
        voltage_scan = VoltageScan(self)
        voltage_scan.grid(row = 1, column = 0, padx =45, pady =10)
        
        
        time_scan = TimeScan(self)
        time_scan.grid(row =1, column =1,  padx =10, pady =10)


global save_status
save_status = False
 
def save_file(data, status):    
    global save_status
    save_status = status 
    
    if save_status:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("csv file", ".csv")],
                                                )
        data.to_csv(file_path, sep = ";", index = False, decimal = ",")

        

class Settings(ttk.Frame):
    
    def __init__(self,container):
        super().__init__(container)
        
        #self.columnconfigure(0,weight =0)
        #self.columnconfigure(0,weight =0)
        
        #self.label = ttk.Label(self, text ="Keithley2410 GUI")
        #self.label.pack(**options)
        self.__create_widgets()
        
        
        
    def __create_widgets(self):
        """LabelFrame that holds widgets for basic Settings.""" 
        
        settings_label_frame = ttk.LabelFrame(self, text = "Settings Information", labelanchor = "nw")
        settings_label_frame.grid(row =0, column = 0, padx =10, pady =10, sticky = "w") #, sticky = "e"
        
        
        
        #butt_init_label = ttk.Label(settings_label_frame, text = "Initialization")
        #butt_init_label.grid(row =0, column = 0)
        butt_init = ttk.Button(settings_label_frame, text = "Initializing", 
                        command = self.init, width = 14)
        butt_init.grid(row =0, column = 1, columnspan = 2, ipadx =1)
        
        panel_label = ttk.Label(settings_label_frame, text = "Panel", width =12)
        panel_label.grid(row = 1,  column =0, padx =15)
        
        self.terminal = tk.StringVar(value = "FRONT")
        panel_combobox = ttk.Combobox(settings_label_frame, values = ["FRONT", "REAR"], width =12, textvariable=self.terminal)
        panel_combobox.grid(row =1, column = 1)
        
        filter_label = ttk.Label(settings_label_frame, text = "Filter")
        filter_label.grid(row = 0,  column =2)
        self.filter_status = tk.StringVar(value = "OFF")
        filter_status = ttk.Combobox(settings_label_frame, values = ["ON", "OFF"], 
                                width =12, textvariable=self.filter_status)
        filter_status.grid(row =0, column = 3)
        
        averaging_mode_label = ttk.Label(settings_label_frame, text = "Mode")
        averaging_mode_label.grid(row = 1,  column =2)
        self.mode_status = tk.StringVar(value = "REPEAT")
        averaging_mode = ttk.Combobox(settings_label_frame, values = ["REPEAT", "MOVING"], 
                                width =12, textvariable=self.mode_status)
        averaging_mode.grid(row =1, column = 3)
        

        self.curr_nplc = tk.StringVar()
        curr_nplc_lable = ttk.Label(settings_label_frame, text = "Current NPLC")
        curr_nplc_lable.grid(row = 0,  column =4)
        #curr_nplc_combobox = ttk.Combobox(self, values = [1, 5, 10])
        curr_nplc = ttk.Combobox(settings_label_frame, state = "readonly", width =12, textvariable=self.curr_nplc)
        curr_nplc["values"] = ("1", "5", "10")
        curr_nplc.current(1)
        curr_nplc.grid( row =0, column = 5)


        self.volt_nplc = tk.StringVar()
        volt_nplc_lable = ttk.Label(settings_label_frame, text = "Voltage NPLC")
        volt_nplc_lable.grid(row = 1,  column =4)
        #curr_nplc_combobox = ttk.Combobox(self, values = [1, 5, 10])
        volt_nplc = ttk.Combobox(settings_label_frame, state = "readonly", width =12, textvariable= self.volt_nplc)
        volt_nplc["values"] = ("1", "5", "10")
        volt_nplc.current(1)
        volt_nplc.grid(row = 1,  column =5)

        
        self.current_compliance = tk.StringVar(value = "105E-6")
        current_compliance_label = ttk.Label(settings_label_frame, text = "Current Cmpl")
        current_compliance_label.grid(row = 2,  column =0)
        current_compliance = ttk.Entry(settings_label_frame, textvariable = self.current_compliance,
                                                width =14)
        current_compliance.grid(row =2, column =1, ipadx =3)
        current_compliance.focus()
        
        self.voltcmpl = tk.IntVar()
        self.voltcmpl.set(300)
        voltage_cmpl_label = ttk.Label(settings_label_frame, text = "Voltage Cmpl")
        voltage_cmpl_label.grid(row = 2, column =2)
        
        voltage_cmpl_spinbox = ttk.Spinbox(settings_label_frame, from_=-1e4, to = 1e14, 
                                         textvariable = self.voltcmpl, width =12)
        voltage_cmpl_spinbox.grid( row =2, column =3, ipadx =5)
        
        
        
        # Apply settings
        
        butt_apply = ttk.Button(settings_label_frame, text = "Apply Settings",
                        command = self.submit, width = 12)
        butt_apply.grid( row =2, column =5, ipadx =8, ipady =5, sticky="e")
        
        

        # setting up widgets and align
        for widget in settings_label_frame.winfo_children():
            widget.grid_configure(padx =10, pady =10, sticky="w")


    def init(self):
        """ Initialize the setup 
        """
        keith2410.__init__()
        print("***** System Initialized!!! ******")


    
    def submit(self):
        """By pressing the ApplSettings button, each setting gets its own value."""
        
        """Import to note that if self.curr_NPLC.get() works fine,
        try to add 'fasr, slow' by assigning values"""
        self.settings(
                      self.terminal.get(),
                      self.current_compliance.get(),
                      self.voltcmpl.get(),
                      self.curr_nplc.get(),
                      self.volt_nplc.get()
                      )  # self.curr_n
                      
        
        
    def settings(self, terminal, current_compliance, voltcmpl, curr_nplc, volt_nplc): # curr_nplc removed
        """Setting up basic measurement parameters."""
        keith2410.select_panel(terminal)
        keith2410.set_curr_cmpl(current_compliance)
        keith2410.set_voltage_range(voltcmpl)  
        keith2410.set_curr_nplc(curr_nplc)
        keith2410.set_voltage_nplc(volt_nplc)
        
        
        
        

class VoltageScan(ttk.Frame):
    
    def __init__(self,container):
        super().__init__(container)
        
        self.columnconfigure(0,weight =2)
        #self.columnconfigure(1,weight =3)
        
        #self.label = ttk.Label(self, text ="Keithley2410 GUI")
        #self.label.pack(**options)
        self.__create_widgets()
        
    def __create_widgets(self):
        
        """LabelFrame that holds widgets for VoltageScan."""
        
        voltage_scan_frame = ttk.LabelFrame(self, text = "Voltage Scan")
        voltage_scan_frame.grid(row =1, column = 0, sticky="e", pady =1, padx = 10)  #, ipadx = 85
        
        start_label = ttk.Label(voltage_scan_frame, text = "Start")
        start_label.grid(row = 0,  column =0)
        
        self.start = tk.IntVar()
        self.start.set(1)
        start_spinbox = ttk.Spinbox(voltage_scan_frame, from_=-3e2, to = 5e2, textvariable = self.start, width =12)
        start_spinbox.grid(row = 0, column = 1)
        
        stop_label = ttk.Label(voltage_scan_frame, text = "Stop")
        stop_label.grid(row = 1,  column =0)
        self.stop = tk.IntVar()
        self.stop.set(10)
        stop_spinbox = ttk.Spinbox(voltage_scan_frame, from_=-3e2, to = 5e2, textvariable = self.stop, width =12)
        stop_spinbox.grid(row = 1, column = 1)


        step_label = ttk.Label(voltage_scan_frame, text = "Step")
        step_label.grid(row = 2,  column =0, padx = 20)
        
        self.step = tk.IntVar()
        self.step.set(1)
        step_spinbox = ttk.Spinbox(voltage_scan_frame, from_=0, to = 1e2, textvariable = self.step, width =12)
        step_spinbox.grid(row = 2, column = 1)
        
        
        delay_label = ttk.Label(voltage_scan_frame, text = "Delay")
        delay_label.grid(row = 3,  column =0)
        
        self.delay = tk.IntVar()
        self.delay.set(1)
        delay_spinbox = ttk.Spinbox(voltage_scan_frame, from_=0, to = 1e2, textvariable = self.delay, width =12)
        delay_spinbox.grid(row = 3, column = 1)
        
        
        
        scan_now_label = ttk.Label(voltage_scan_frame, text = "Voltage Sweep")
        scan_now_label.grid(row = 4, column = 0, sticky="w")
        
        voltage_scan_butt = ttk.Button(voltage_scan_frame, text = "Start", 
                        command = self.start_scan, width =12)  
        voltage_scan_butt.grid(row = 4,  column =1, ipady =1, sticky="w", ipadx = 8) 


        # save checkbox
        #save_label = ttk.Label(voltage_scan_frame, text = "Save Status")
        
        self.save = tk.BooleanVar(value = False) 
        save = ttk.Checkbutton(voltage_scan_frame, text = "Save Data", 
                                   variable = self.save, onvalue = True, offvalue = False)
        save.grid(row =5, column = 0, padx = 15)
        
        for widget in voltage_scan_frame.winfo_children():
            widget.grid_configure(padx =15, pady =12,  sticky="w")
        
          
    def start_scan(self):
        """By pressing the ApplSettings button, each varsetting gets  its own value."""
          
        self.voltage_scan(
                      self.start.get(),
                      self.stop.get(),
                      self.step.get(),
                      self.delay.get()
                      
                      )    
            
        
    def voltage_scan(self, start, stop, step, delay):
        """Setting up scan parameters."""
             
        var = [start, stop, step, delay]
        
        for v in var:
            if type(v) != int:
                print(type(v))
                raise ValueError("Please enter interger numbers as input!")
                
        def make_plot():
            plt.scatter(mvol,mcurr)
            plt.xlabel('Voltage / V', fontsize = 12)
            plt.ylabel('Current / A', fontsize = 12)
            plt.xticks(fontsize=12), plt.yticks(fontsize=12)
            plt.title("I-V Curve", size= 12)
            plt.tight_layout()
        
        keith2410.beep()
        if start < stop:
       
            stop = stop + 1
            
            keith2410.set_voltage_source()
            
            mvol = 0
            mcurr =0
            
            plt.ion()  # enable interactivity
            fig = plt.figure(figsize = (5,3.5), dpi = 100)
            ax = fig.add_subplot(111)
             
            #bias = []
            mvol = []
            mcurr = []
            t = 0
            
            for vol in range(start, stop, step):
                
                
                start_time = timer()
                #bias.append(vol)
                keith2410.set_voltage_level(vol)
                self.after(1000*delay) 
                #keith2410.filter()
                mvol.append(keith2410.disp_voltage())
                
                keith2410.hit_cmpl() 
                mcurr.append(keith2410.disp_curr())
                
                #print("Current: {} {}".format(keith2410.disp_curr(), "[A]"),
                #"Voltage: {} {}".format(keith2410.disp_voltage(), "[V]"))
                
                drawnow(make_plot)
                end_time = timer()
                delta_t = end_time - start_time
                
                t = delta_t + t
                #print(delta_t, t)
                t_init = round(t / (delta_t*((stop+1 - start) // step)),2)
                t_init = t_init*100
                print('\nProcessing {:.0f}%.'\
                .format(t_init), "\n")
            data = np.array([mvol, mcurr])
            data = data.transpose()
            data = pd.DataFrame(data, columns = ["Voltage [V]", "Current [A]"])
            save_file(data, self.save.get())
            print("***** Data *****", "\n")
            print(data)
            
            
        else:
        
            stop = stop - 1
            step =  - step
            
            bias = []
            mvol = []
            mcurr = []
            
            for vol in range(start, stop, step):
                bias.append(vol)
                keith2410.set_voltage_level(vol)
                self.after(1000*delay)
                mvol.append(keith2410.disp_voltage())
                keith2410.hit_cmpl()
                mcurr.append(keith2410.disp_curr())
                print("Current: {} {}".format(keith2410.disp_curr(), "[A]"),
                "Voltage: {} {}".format(keith2410.disp_voltage(), "[V]"))
                drawnow(make_plot)
                
            data = np.array([mvol, mcurr])
            data = data.transpose()
            data = pd.DataFrame(data, columns = ["Voltage [V]", "Current [A]"])
            save_file(data, self.save.get())
            
            
        keith2410.close()       
    
     
        
class TimeScan(ttk.Frame):
    
    def __init__(self,container):
        super().__init__(container)
        
        self.columnconfigure(1,weight =3)
        #self.columnconfigure(1,weight =1)
        
        self.__create_widgets()
        
    def __create_widgets(self):
        """LabelFrame that holds widgets for TimeScan."""
        
        time_scan_frame = ttk.LabelFrame(self, text = "Time Scan")
        time_scan_frame.grid(row =1, column = 1, sticky = "w", padx =1, pady =1)
        
        # Voltage setpoint
        voltage_label = ttk.Label(time_scan_frame, text = "Voltage")
        voltage_label.grid(row = 0,  column =0, padx =10, pady =10, sticky = "w")
        self.voltage = tk.IntVar()
        self.voltage.set(1)
        voltage_spinbox = ttk.Spinbox(time_scan_frame, from_=-3e2, to = 5e2, textvariable = self.voltage, width =12)
        voltage_spinbox.grid(row = 0, column = 1)
        
        # scan duration in minutes
        duration_label = ttk.Label(time_scan_frame, text = "Duration (Min)")
        duration_label.grid(row = 1,  column =0, padx =10, pady =10, sticky = "w")
        self.duration = tk.DoubleVar()
        self.duration.set(0.1)
        duration_spinbox = ttk.Spinbox(time_scan_frame, from_=0, to = 1e5, textvariable = self.duration, width =12)
        duration_spinbox.grid(row = 1, column = 1)
        
        # dime delay bebween the each scan
        delay_time_label = ttk.Label(time_scan_frame, text = "Delay (s)")
        delay_time_label.grid(row = 2,  column =0, padx =10, pady =10, sticky = "w")
        self.delay_time = tk.IntVar()
        self.delay_time.set(1)
        delay_time_spinbox = ttk.Spinbox(time_scan_frame, from_=0, to = 1e5, textvariable = self.delay_time, width =12)
        delay_time_spinbox.grid(row = 2, column = 1)
    


        time_scan_label = ttk.Label(time_scan_frame, text = "Time Sweep")
        time_scan_label.grid(row = 4, column = 0, sticky = "w")
        
        time_scan_butt = ttk.Button(time_scan_frame, text = "Start", 
                        command = self.timeScan_start, width =12)  
        time_scan_butt.grid(row = 4,  column =1, ipady =1, sticky="w", ipadx = 8) 

        self.save = tk.BooleanVar(value = False) 
        save = ttk.Checkbutton(time_scan_frame, text = "Save Data", 
                                   variable = self.save, onvalue = True, offvalue = False)
        #save_label.grid(row =1, column = 5)
        save.grid(row =5, column = 0, padx = 20)

        for widget in time_scan_frame.winfo_children():
            widget.grid_configure(padx =15, pady =15)


    def timeScan_start(self):
        """By pressing the Start scan button, each varsetting gets  its own value."""
          
        self.time_scan(
                      self.voltage.get(),
                      self.duration.get(),
                      self.delay_time.get()
                      )


    start_time = 0
    
    def time_scan(self, voltage, duration, delay_time):
        """ Scan voltage over a given time period in minutes"""
        
        
        def make_plot():
            plt.scatter(time_elapse,current)
            plt.xlabel('Time elapse / s', fontsize = 12)
            plt.ylabel('Current / A', fontsize = 12)
            plt.xticks(fontsize=12), plt.yticks(fontsize=12)
            plt.title("Monitor current over time", size= 12)
            plt.tight_layout()
        
        plt.ion()  # enable interactivity
        fig = plt.figure(figsize = (5,3.5), dpi = 100)
        ax = fig.add_subplot(111)
        
        keith2410.beep() 
        start_time = time.time()
        duration = round(duration * 60) #%% convert to second 
        duration  = round(duration / delay_time)
        
        time_elapse = []
        current =[]
        
        print("\n","***** Measuring ******")
        for t in range(duration):
            #self.after(1000*delay_time - (time.time() - start_time) % delay_time)
            time.sleep(delay_time - (time.time() - start_time) % delay_time)
            #print(delay_time - (time.time() - start_time) % delay_time)
            keith2410.single_point(voltage)
            # total time elapse
            total = round(((time.time()- start_time) / delay_time)*delay_time, 0)
            #print("Time: {} {}".format(total, "[s]"),
            #    "Current: {} {}".format(keith2410.disp_curr(), "[A]"))
            time_elapse.append(total)
            current.append(keith2410.disp_curr())
            drawnow(make_plot)
            
            
            
        data = np.array([time_elapse, current])
        data = data.transpose()
        data = pd.DataFrame(data, columns = ["Time Elapse [Second]", "Current [A]"])
        save_file(data, self.save.get())
        print(data)   
        
        keith2410.close() 



       
       
if __name__ == "__main__":

    k2410 = Keith2140()
    k2410.mainloop()
