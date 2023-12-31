import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os
import csv




class LabelInput(tk.Frame):
    """ A widget containing a Label and an Input together """

    def __init__(self, parent, label='', input_class=ttk.Entry,
                 input_var=None, input_args=None, label_args=None,
                 **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = input_var
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
            input_args["textvariable"] = input_var

        self.input = self.create_input_widget(input_class, input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)

    def create_input_widget(self, input_class, input_args):
        if input_class == ttk.Combobox:
            values = input_args.pop("values", [])
            return ttk.Combobox(self, values=values, **input_args)
        else:
            return input_class(self, **input_args)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get('1.0', tk.END)
            elif type(self.input) == ttk.Combobox:
                return self.input.get()
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            # happens when numeric fields are empty
            return ''

    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
            self.variable.set(bool(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        elif type(self.input) == ttk.Combobox:
            self.input.set(value)
        else:
            self.input.delete(0, tk.END)
            self.input.insert(0, value)


            
class DataRecordForm(tk.Frame):
    """ The input form for widgets """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset()
        self.inputs = {}

        recordinfo = tk.LabelFrame(self, text="Record Information")
        
        try:
            print("Creating Date widget")
            self.inputs['Date'] = LabelInput(recordinfo, "Date", input_var=tk.StringVar())
            self.inputs['Date'].grid(row=0, column=0)

            print("Creating Time widget")
            self.inputs['Time'] = LabelInput(recordinfo, "Time", input_class=ttk.Combobox,
                                             input_var=tk.StringVar(), input_args={"values": ["8:00", "12:00", "16:00", "20:00"]})
            self.inputs['Time'].grid(row=0, column=1)

            print("Creating Technician widget")
            self.inputs['Technician'] = LabelInput(recordinfo, "Technician", input_var=tk.StringVar())
            self.inputs['Technician'].grid(row=0, column=2)
        except Exception as e:
            print(f"Error in creating widgets: {e}")

        try:
            print("Creating Lab widget")
            self.inputs['Lab'] = LabelInput(recordinfo, "Lab", input_class=ttk.Combobox,
                                            input_var=tk.StringVar(), input_args={"values": ["A", "B", "C", "D"]})
            self.inputs['Lab'].grid(row=1, column=0)

            print("Creating Plot widget")
            self.inputs['Plot'] = LabelInput(recordinfo, "Plot", input_class=ttk.Combobox, input_var=tk.IntVar(),
                                             input_args={"values": list(range(1, 21))})
            self.inputs['Plot'].grid(row=1, column=1)

            print("Creating Seed sample widget")
            self.inputs['Seed sample'] = LabelInput(recordinfo, "Seed sample", input_var=tk.StringVar())
            self.inputs['Seed sample'].grid(row=1, column=2)
        except Exception as e:
            print(f"Error in creating widgets: {e}")

        recordinfo.grid(row=0, column=0, sticky=(tk.W + tk.E))

        environmentinfo = tk.LabelFrame(self, text="Environment Data")
        try:
            print("Creating Humidity widget")
            self.inputs['Humidity'] = LabelInput(environmentinfo, "Humidity (g/m3)", input_class=tk.Spinbox,
                                                 input_var=tk.DoubleVar(), input_args={"from_": 0.5, "to": 52.0, "increment": .01})
            self.inputs['Humidity'].grid(row=0, column=0)

            print("Creating Light widget")
            self.inputs['Light'] = LabelInput(environmentinfo, "Light (klx)", input_class=tk.Spinbox,
                                              input_var=tk.DoubleVar(), input_args={"from_": 0, "to": 100, "increment": 0.1})
            self.inputs['Light'].grid(row=0, column=1)

            print("Creating Temperature widget")
            self.inputs['Temperature'] = LabelInput(environmentinfo, "Temperature (C)", input_class=tk.Spinbox,
                                                     input_var=tk.DoubleVar(), input_args={"from_": -50, "to": 50, "increment": 0.1})
            self.inputs['Temperature'].grid(row=0, column=2)

            print("Creating Equipment Fault widget")
            self.inputs['Equipment Fault'] = LabelInput(environmentinfo, "Equipment Fault",
                                                         input_class=ttk.Checkbutton, input_var=tk.BooleanVar())
            self.inputs['Equipment Fault'].grid(row=1, column=0, columnspan=3)
        except Exception as e:
            print(f"Error in creating widgets: {e}")

        plantinfo = tk.LabelFrame(self, text="Plant Data")

        try:
            print("Creating Plants widget")
            self.inputs['Plants'] = LabelInput(plantinfo, "Plants", input_class=tk.Spinbox,
                                               input_var=tk.IntVar(), input_args={"from_": 0, "to": 20})
            self.inputs['Plants'].grid(row=0, column=0)

            print("Creating Blossoms widget")
            self.inputs['Blossoms'] = LabelInput(plantinfo, "Blossoms", input_class=tk.Spinbox,
                                                 input_var=tk.IntVar(), input_args={"from_": 0, "to": 1000})
            self.inputs['Blossoms'].grid(row=0, column=1)

            print("Creating Fruit widget")
            self.inputs['Fruit'] = LabelInput(plantinfo, "Fruit", input_class=tk.Spinbox,
                                              input_var=tk.IntVar(), input_args={"from_": 0, "to": 1000})
            self.inputs['Fruit'].grid(row=0, column=2)

            print("Creating Min Height widget")
            self.inputs['Min Height'] = LabelInput(plantinfo, "Min Height (C)", input_class=tk.Spinbox,
                                                    input_var=tk.DoubleVar(), input_args={"from_": 0, "to": 1000, "increment": 0.1})
            self.inputs['Min Height'].grid(row=1, column=0)

            print("Creating Max Height widget")
            self.inputs['Max Height'] = LabelInput(plantinfo, "Max Height (cm)", input_class=tk.Spinbox,
                                                    input_var=tk.DoubleVar(), input_args={"from_": 0, "to": 1000, "increment": 0.1})
            self.inputs['Max Height'].grid(row=1, column=1)

            print("Creating Median Height widget")
            self.inputs['Median Height'] = LabelInput(plantinfo, "Median Height (cm)", input_class=tk.Spinbox,
                                                    input_var=tk.DoubleVar(), input_args={"from_": 0, "to": 1000, "increment": 0.1})
            self.inputs['Median Height'].grid(row=1, column=2)
        except Exception as e:
            print(f"Error in creating widgets: {e}")

        self.inputs['Notes'] = LabelInput(self, "Notes", input_class=tk.Text, input_args={"width": 75, "height": 10})
        self.inputs['Notes'].grid(sticky="w", row=3, column=0)

    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def reset(self):
        for widget in self.inputs.values():
            widget.set('')



        
        
class Application(tk.Tk):
    """Application root window"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("ABQ Data Entry Application")
        self.resizable(width=False, height=False)
        
        ttk.Label(
            self,
            text = "ABQ Data Entry Application",
            font = ("TkDefaultFont", 16)
        ).grid(row=0)
        
        self.recordform = DataRecordForm(self)
        self.recordform.grid(row=1, padx=10)
        
        # the Save Button
        self.savebutton = ttk.Button(self, text="Save",
                                     command=self.on_save)
        self.savebutton.grid(sticky=tk.E, row=2, padx=10)
        
        # status Bar
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)
    
    def on_save(self):
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = "abq_data_record_{}.csv".format(datestring)
        newfile = not os.path.exists(filename)
        
        # get the data from DataEntryForm
        data = self.recordform.get()
        
        # now that the data is acquired, we need to open our file and write the data into it.
        with open(filename, 'a') as file:
            csvwriter = csv.DictWriter(file, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)

if __name__ == "__main__":
    app = Application()
    app.mainloop()