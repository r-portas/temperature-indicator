#!/usr/bin/env python
"""
    Temp Indicator
    A temperature indicator applet for Ubuntu
    (c) 2015 Roy Portas
"""

import sys
import gtk
import time
import appindicator
import sensors

# Icons files
indicator_icon = "gnome-do-symbolic"

# App settings
app_delay = 1000
indicator_id = "hw-indicator"

# Sensor labels
cpu_label = "ISA adapter"
gpu_label = ""
other_label = "Virtual device"

class HWMonitor:
    
    def menu_setup(self):
        """Set up the GTK menu"""
        self.menu = gtk.Menu()
    
    def __init__(self):
        """Initialises the app indicator"""
        self.ind = appindicator.Indicator(indicator_id,
                                           indicator_icon,
                                           appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        
        # Sensor storage variables
        self.cpu = []
        self.gpu = []
        self.other = []
        
        
        self.menu_setup()
        self.ind.set_menu(self.menu)
        
        # Set the required amount of indicator slots
        sensors.init()
        self.read_sensors()
        size = len(self.cpu) + len(self.gpu) + len(self.other) + 3
        self.sensors_items = []
        for x in range(size):
            self.sensors_items.append(gtk.MenuItem(""))
            self.sensors_items[-1].show()
            self.menu.append(self.sensors_items[-1])
            
        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)        
        
    def main(self):
        """The main program loop"""
        self.get_sensors()
        gtk.timeout_add(app_delay, self.get_sensors)
        gtk.main()
    
    def read_sensors(self):
        """Reads the sensors"""
        try:
            for chip in sensors.iter_detected_chips():
                if chip.adapter_name == cpu_label:
                    self.cpu = []
                    for feature in chip:
                        self.cpu.append("  {}: {}".format(feature.label, feature.get_value()))
        
                #TODO: Add GPU adapter
        
                if chip.adapter_name == other_label:
                    self.other = []
                    for feature in chip:
                        self.other.append("  {}: {}".format(feature.label, feature.get_value()))                    
        except:
            pass        
    
    def get_sensors(self):
        """Gets sensor data and writes it to the indicator"""
        self.read_sensors()
        
        try:
            counter = 0
            self.sensors_items[counter].set_label("CPU")
            counter += 1
            
            for reading in self.cpu:
                self.sensors_items[counter].set_label(reading)
                counter += 1
            
            self.sensors_items[counter].set_label("GPU")
            counter += 1            
            #TODO: Do GPU
            
            self.sensors_items[counter].set_label("Other")
            counter += 1            
            for reading in self.other:
                self.sensors_items[counter].set_label(reading)
                counter += 1
            
        except:
            pass
        
        return True # Return true to keep looping
        
    def quit(self, widget):
        """Quits the program"""
        sensors.cleanup() # Clean up after sensors
        sys.exit(0)
        
if __name__ == "__main__":
    indicator = HWMonitor()
    indicator.get_sensors()
    indicator.main()