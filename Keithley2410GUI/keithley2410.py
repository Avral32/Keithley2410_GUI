
"""
=====
Basic functionalities of Keith2410 demonstrated in this module by defining a base class "Keith2410".

- In generally, the class covers the most common functionalites of the Keith2410 
  for Setting the source, and sensors for both current and voltage measurements.

- Author@Savutjan Sidik
- Date: 21/11/2022

======
"""

import pyvisa
import time
import warnings


class Keith2410:
    """ 
    The class defines some essential methods for initializing and settings up the device
    """
   
    def __init__(self):
        """ Identify the keithley that is connected to GPIB 
        and choose the front or back panel."""
      
        rm = pyvisa.ResourceManager()
        device_names = rm.list_resources()
        
        self.keith2410 = rm.open_resource(device_names[-1])
        
        try:
            for device in device_names:
                if device == "GPIB0::24::INSTR":
                    self.keith2410 = rm.open_resource(device)
                    print(device, "is initialized!")
                    
        except pyvisa.errors.VisaIOError:
            
            print("Device is not found.")
            return False
             
        #print(self.keith2410.query("*IDN?"))  
        
        self.keith2410.timeout = 4000
        
    def select_panel(self, terminal):

        self.keith2410.write(":route:terminals " + terminal)
        
        
    def set_curr_cmpl(self, current):
        """Set a current compliance to avoid a possible overcurrent."""
        
        self.keith2410.write(":sense:current:protection " + str(current))
    
    
    
    def set_voltage_cmpl(self, voltage):
        """Set a compliance for voltage to be measured."""
    
        self.keith2410.write(":sense:voltage:protection " + str(voltage))

    def set_voltage_range(self, voltage):
        """Set a maximum votlage range that can be supplied."""
    
        self.keith2410.write(":source:voltage:range " + str(voltage))

    def set_curr_nplc(self, nplc):
        """Set the integration time of measurement by NPLC."""
        
        self.keith2410.write(":sense:current:nplcycles " + str(nplc))

    def set_voltage_nplc(self, nplc):
        """Set the integration time of measurement by NPLC."""
        
        self.keith2410.write(":sense:voltage:nplcycles " + str(nplc))
        
    def disp_voltage(self):
        """Display the current voltage setpoint."""
        
        self.keith2410.write(":sense:function 'voltage'")
        self.keith2410.write(":display:digits 7")
        self.keith2410.write(":form:elem voltage")
        self.keith2410.write("output on")
        voltage = float(self.keith2410.query(":read?"))
        return voltage

    def disp_curr(self):
        """Display the current."""
       
        self.keith2410.write(":sense:function 'current'")
        self.keith2410.write(":sense:current:range:auto on")
        #self.keith2410.write(":display:enable on")
        #self.keith2410.write(":display:digits 7")
        self.keith2410.write(":form:elem current")
        self.keith2410.write("output on")
        current = abs(float(self.keith2410.query(":read?")))
        
        return current
          
    def hit_cmpl(self):
        """To check if measured current is hitting the compliance. 
        if current hits the compliance, trip gets "1", and raise an error and system out."""
  
        trip = int(str(self.keith2410.query(":SENSE:CURRENT:PROTECTION:TRIPPED?")))
        
        if trip:
           self.close()
           raise ValueError("You hit the compliance!")
        
    def beep(self, freq=5000, duration=0.02):
        """" Set beeper."""
       
        self.keith2410.write(":system:beeper " + str(freq) + ", " + str(duration))
        time.sleep(duration)
    
    
    def set_voltage_source(self):
        """Setting up source before measuring current and voltage."""
        
        self.keith2410.write(":system:beeper:state off")
        self.keith2410.write(":source:function voltage")
        self.keith2410.write(":source:voltage:mode fixed")
        self.keith2410.write(":source:voltage:range:auto 1")
            
    
    def set_voltage_level(self,volt):
        """Set the voltage level before measuring and important for scanning and point measurements."""
        
        self.keith2410.write(":source:voltage:level " + str(volt))
    
    
    
    def single_point(self, point):
        """ Set a single point for voltage level, and measure 
        the current and voltage at that point. 
        """
        self.keith2410.write(":system:beeper:state off")     # turn off beeper
        self.keith2410.write(":source:function voltage")
        self.keith2410.write(":source:voltage:mode fixed")
        self.keith2410.write(":source:voltage:range:auto 1")
        self.keith2410.write(":source:voltage:level " + str(point))
        
        self.hit_cmpl()
        

    def filter(self, count=20, mode="repeat"):
        self.kei2410.write(":sense:average:count "+str(count))
        self.kei2410.write(":sense:average:tcontrol "+mode) # repeat or moving
        self.kei2410.write(":sense:average:state on")

    def filter_off(self):
        self.kei2410.write(":sense:average:state off")


    def close(self):
        """Close the device afte any measuremts."""
        self.keith2410.write("output off")
        self.keith2410.write("*RST")
        self.keith2410.close()
              
