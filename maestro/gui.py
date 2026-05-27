import json
import logging
import os
import threading
import time
import tkinter as tk
from tkinter import ttk

from maestro.core import Maestro

logging.basicConfig(level=logging.INFO, filename='./logs/maestro.log',format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%d/%m/%Y %H:%M:%S')

class MaestroGui:
    def __init__(self):
        self.screen = tk.Tk()
        self.frame = ttk.Frame(self.screen)
        
        
    def start_gui(self):
        self.screen.title("Maestro")
        self.screen.configure(padx=50, pady=20)
        self.frame.grid()
        
        self.create_commands_inputs()
        self.create_sensitivity_inputs()
        self.create_bottom_section()
        
        self.read_commands_config_file_and_show()
        self.maestro = Maestro()
        self.screen.mainloop()
        
    
    def run_maestro(self):
        self.maestro.running = True
        self.toggle_ui(True)        
        
        self.maestro_thread = threading.Thread(target=self.run_wrapper, daemon=True)
        self.maestro_thread.start()
    
    
    def run_wrapper(self):
        try:
            self.maestro.start_orchestra()
            
        except Exception as e:
            message = f"An error occured trying to run the program: {e}\n"
            logging.error(message)
            print(message)
            
        finally:
            self.screen.after(0, lambda: self.toggle_ui(False))
        
    
    def stop_maestro(self):
        time.sleep(0.5)
        self.maestro.running = False
    
    
    def toggle_ui(self, is_running):
        '''
        Switch the ui widgets state.
        '''
        state = "disabled" if is_running else "enabled"
        inverse_state = "enabled" if is_running else "disabled"
        
        self.running_stats.config(
            text="Running." if is_running else "Not running.",
            foreground="Green" if is_running else "red"
        )
        
        self.start_btn.config(state=state)
        self.update_config_btn.config(state=state)
        self.stop_btn.config(state=inverse_state)
        
        for widget_group in [self.commands_entries, self.sensitivity_scales]:
            for widget in widget_group.values():
                widget.config(state=state)
                
    
    def write_commands_config_file(self):
        '''
        Receives the values of the commands and sensitivity from the tkinter and then saves them in the configuration file.
        '''
        commands_data = {name:widget.get() for name, widget in self.commands_entries.items()}
        
        sensitivity_data = {name:round(widget.get(), 2) for name, widget in self.sensitivity_scales.items()}
        
        config_data = {"commands": commands_data, "sensitivity": sensitivity_data}
        
        if not os.path.exists("./config"):
            os.mkdir("./config")
            
        with open("./config/config.json", "w") as config_file:
            json.dump(config_data, config_file, indent=2)
            print("Config Saved")
            
            
    def read_commands_config_file_and_show(self):
        '''
        Read the settings file and insert the commands and sensitivity values into tkinter.
        '''
        if not os.path.exists("./config/config.json"):
            self.write_commands_config_file()
            
        with open("./config/config.json", "r") as config_file:
            config_data =  json.load(config_file)
            cmd_data = config_data["commands"]
            sens_data = config_data["sensitivity"]
            
            for name, widget in self.commands_entries.items():
                widget.insert(0, cmd_data[name])
            
            for name, widget in self.sensitivity_scales.items():
                widget.set(sens_data[name])


    def create_commands_inputs(self):
        '''
        Creates tkinter entries widgets that receive terminal commands for each gesture present in the mediapipe model.
        '''
        ttk.Label(self.frame, text="Commands:").grid(column=0, row=0, pady=10)
        
        self.commands_entries = {
            "Closed_Fist": None,
            "ILoveYou": None,
            "Thumb_Up": None,
            "Thumb_Down": None,
            "Pointing_Up": None,
            "Victory": None,
        }
        
        iteration = 0
        for name in self.commands_entries:
            self.commands_entries[name] = ttk.Entry(self.frame)
            widget = self.commands_entries[name]
            
            ttk.Label(self.frame, text=f"{name} Command:").grid(column=0, row=iteration + 1)
            widget.grid(column=1, row=iteration + 1)
            iteration += 1


    def create_sensitivity_inputs(self):
        '''
        Creates tkinter scales widgets that receive values from 0.1 to 1 for each confidence parameter that can be changed in mediapipe.
        Values closer to 0 == Higher sensitivity.
        '''
        
        ttk.Label(self.frame, text="Sensitivity:").grid(column=3, row=0, pady=10)
        
        self.sensitivity_scales = {
            "Detection_Sens": None,
            "Presence_Sens": None,
            "Tracking_Sens": None,
            "Gesture_Recognizer_Sens": None,
        }

        iteration = 0
        for name in self.sensitivity_scales:
            self.sensitivity_scales[name] = ttk.Scale(self.frame, from_=1.0, to=0.1, length=200)
            widget = self.sensitivity_scales[name]
            
            ttk.Label(self.frame, text=f"{name}:").grid(column=2, row=iteration + 1)
            widget.grid(column=3, row=iteration + 1)
            iteration += 1


    def create_bottom_section(self):
        ttk.Label(self.frame, text="Note: Some commands may not run correctly, specially interactive ones, e.g., 'nano' or 'btop'.").grid(column=0, columnspan=4, row=7, pady=20)

        self.running_stats = ttk.Label(self.frame, text="Not running.", foreground="red")
        self.start_btn = ttk.Button(self.frame, text="Start", command=self.run_maestro)
        self.stop_btn = ttk.Button(self.frame, text="Stop", command=self.stop_maestro, state="disabled")
        self.update_config_btn = ttk.Button(self.frame, text="Update Config", command=self.write_commands_config_file)
        
        self.start_btn.grid(column=0, row=8)
        self.stop_btn.grid(column=1, row=8)
        self.update_config_btn.grid(column=2, row=8)
        self.running_stats.grid(column=3, row=8)
        
        ttk.Label(self.frame, text="Version: 1.0 - Bernstein").grid(column=3, row=9, pady=10)

