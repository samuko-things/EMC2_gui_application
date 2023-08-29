
from global_var_and_func import g, SetDataCardFrame

import tkinter
import tkinter.messagebox
import customtkinter



def setI2Caddress(text):
  try:
    if text:
      isSuccessful = g.serClient.send("i2c", float(text))
      val = int(g.serClient.get("i2c"))
      g.i2cAddress = val
  except:
    pass
  

  return g.i2cAddress

def resetAllParams():
  isSuccessful = g.serClient.send("reset")
  return isSuccessful







class DriverParamsSetupFrame(customtkinter.CTkFrame):
  def __init__(self, parent):
    super().__init__(parent, width=500, height=700)

    # add heading
    self.heading = customtkinter.CTkLabel(self, text="OTHER PARAMS SETUP", font=customtkinter.CTkFont(size=24, weight="bold", underline=False))
    self.heading.grid(row=0, column=0, padx=10, pady=(5,25))

    # add set card frame for i2c settings
    g.i2cAddress = int(g.serClient.get("i2c"))
    self.setPwmCardFrame = SetDataCardFrame(self, "I2C_ADDRESS", g.i2cAddress,
                                            placeHolderText="enter I2C_ADDRESS",
                                            inputBoxWidth=200, set_func=setI2Caddress)
    self.setPwmCardFrame.grid(row=1, column=0, pady=20)

    # add reset button
    self.resetButton = customtkinter.CTkButton(self, text="RESET ALL PARAMETERS", font=customtkinter.CTkFont(size=12, weight="bold"),
                                                   fg_color='#9BABB8', text_color='black', hover_color='#EEEEEE',
                                                   command=self.open_reset_dialog_event)
    self.resetButton.grid(row=2, column=0, pady=(50, 20), padx=10, ipadx=10, ipady=10)


  def open_reset_dialog_event(self):
    dialog = customtkinter.CTkInputDialog(text="This will reset all parameters to default.\nEnter 'reset' to continue", title="RESET WARNING!!!")
    val = dialog.get_input()
    if val == "reset":
      isSuccessful = resetAllParams()
      if isSuccessful:
        # print(isSuccessful)
        tkinter.messagebox.showinfo("showinfo", "SUCCESS:\n\nParameters Reset was successful.\n\nRestart gui application\n\nReset controller with the reset button\nor turn off and on the controller")
      else:
        tkinter.messagebox.showerror("showerror", "ERROR:\n\nSomething went wrong\nAttempt to reset was unsuccessful\nTry again")
