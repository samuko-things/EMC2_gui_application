from serial_comm_lib import SerialComm
import time

import tkinter
import tkinter.messagebox
import customtkinter

import serial.tools.list_ports

from global_var_and_func import g
from main_app_frame import MainApp





def refreshPortlist():
  try:
    port_list = [port.device for port in serial.tools.list_ports.comports()]
    if len(port_list)==0:
      return ['None']
    return port_list
  except:
    port_list = ['None']

def connectToPort(name):
  try:
    g.serClient = SerialComm(name, 115200, 0.1)
    time.sleep(2)
    isSuccessful = g.serClient.send("mode", 0) # decativate pid mode (activate pwm mode and parameter settings)
    isSuccessful = g.serClient.send("pwm", 0, 0) 
    # print(isSuccessful)
    return True
  except:
    return False




class SelectPortCardFrame(customtkinter.CTkFrame):
  def __init__(self, parentFrame, text, initialValue, input_values, refresh_func=None, connect_func=None, activate_func=None):
    super().__init__(master=parentFrame, width=300, corner_radius=10)

    self.value = initialValue
    self.mainText = text
    self.text = f"{self.mainText} = {self.value}"

    self.refresh_func = refresh_func
    self.connect_func = connect_func
    self.activate_func = activate_func

    # choose card frame
    self.grid_rowconfigure((0,1), weight=0)
    self.grid_columnconfigure((0,1), weight=0)

    self.setTextLabel = customtkinter.CTkLabel(self, text=self.text, font=customtkinter.CTkFont(size=12, weight="bold"))
    self.setTextLabel.grid(row=0, column=0, padx=20, pady=(10,5), sticky="w")

    self.combobox = customtkinter.CTkComboBox(self, values=input_values, command=self.set_data_func, width=150)
    self.combobox.grid(row=1, column=0, padx=20, pady=(5,85), ipady=3)
    self.combobox.set("None")

    self.refreshButton = customtkinter.CTkButton(self, text="REFRESH", command=self.refresh_serial_func)
    self.refreshButton.grid(row=2, column=0, padx=20, pady=5)

    self.connectButton = customtkinter.CTkButton(self, text="CONNECT", command=self.connect_serial_func)
    self.connectButton.grid(row=3, column=0, padx=20, pady=(5,10))


  def set_data_func(self, choice):
    self.value = choice
    self.text = f"{self.mainText} = {self.value}"
    self.setTextLabel.configure(text=self.text)
    self.combobox.set(self.value)
  
  def refresh_serial_func(self):
    port_list = self.refresh_func()
    self.combobox.configure(values=port_list)
    self.combobox.set("None")

    self.value = "None"
    self.text = f"{self.mainText} = {self.value}"
    self.setTextLabel.configure(text=self.text)

  def connect_serial_func(self):
    serIsConnected = connectToPort(self.value)
    if serIsConnected:
      tkinter.messagebox.showinfo("showinfo", f"SUCCESS:\n\nmotor driver module found \non port: {self.value}\n\nclick OK to continue")
      self.activate_func()
    else:
      tkinter.messagebox.showerror("showerror", f"ERROR:\n\nno motor driver module found \non port: {self.value}\n\ntry again or try another port")



class App(customtkinter.CTk):
  def __init__(self):
    super().__init__()

    # configure window
    self.title("Easy Motor Control")
    self.geometry(f"{950}x{780}")


    self.appFrame = customtkinter.CTkFrame(self)
    self.appFrame.pack()

    #####################################################################################
    port_list = refreshPortlist()
    self.selectPortCardFrame = SelectPortCardFrame(self.appFrame, "PORT", "None",
                                                    input_values=port_list,
                                                    refresh_func=refreshPortlist,
                                                    connect_func=connectToPort,
                                                    activate_func=self.startMainApp)
    
    self.selectPortCardFrame.pack()
    #####################################################################################

  
  def startMainApp(self):
    self.delete_pages()
    self.mainAppPage()

  def delete_pages(self):
    for frame in self.appFrame.winfo_children():
      frame.destroy()


  def mainAppPage(self):
    self.appFrame.pack(anchor="nw")
    self.mainAppFrame = MainApp(self.appFrame)
    self.mainAppFrame.pack()





if __name__ == "__main__":
  g.app = App()
  g.app.mainloop()