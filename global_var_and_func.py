import time
import customtkinter
from math import sin, pi



class g():
  app = None
  serClient = None

  motorAOnDuration = 10.0 #sec
  motorBOnDuration = 10.0 #sec

  dirA = 1.00
  dirB = 1.00

  motorConfig = ["LEFT WHEEL", "RIGHT WHEEL"]
  initConfigA = ""
  initConfigB = ""

  motorAOnStartTime = time.time()
  motorBOnStartTime = time.time()

  motorAIsOn = False
  motorBIsOn = False

  ctrlPwmA = 0
  ctrlPwmB = 0

  pprA = 0
  pprB = 0

  initialThetaA = -90.0
  initialThetaB = -90.0

  thetaA = 0.0
  thetaB = 0.0

  angPosA = 0.0
  angPosB = 0.0

  angVelA = 0.0
  angVelB = 0.0

  i2cAddress = 0

  filtOrderA = 1
  filtOrderB = 1

  filtCutOffFreqA = 5.0
  filtCutOffFreqB = 5.0

  stopVelFreqA = 5000
  stopVelFreqB = 5000

  kpA = 0.0
  kpB = 0.0

  kiA = 0.0
  kiB = 0.0

  kdA = 0.0
  kdB = 0.0

  targetA = 0.0
  targetB = 0.0

  filtAngVelA = 0.0
  filtAngVelB = 0.0

  rawAngVelA = 0.0
  rawAngVelB = 0.0

  maxVelA = 1.0
  maxVelB = 1.0

  ctrlVelA = 0.0
  ctrlVelB = 0.0





def stepSignal1(targetMax, deltaT, duration):
  if (deltaT>(2/10*duration)):
     targetCtrl = targetMax
  else:
     targetCtrl = 0              
  return targetCtrl

def stepSignal2(targetMax, deltaT, duration):
  if (deltaT>(1.5/10*duration)) and (deltaT < (8/10*duration)):
     targetCtrl = targetMax
  else:
     targetCtrl = 0              
  return targetCtrl

# def squareSignal1(targetMax, deltaT, duration):
#   if (deltaT>(1/10*duration)) and (deltaT < (5/10*duration)):
#      targetCtrl = targetMax

#   elif (deltaT>(5/10*duration)) and (deltaT < (9/10*duration)):
#      targetCtrl = -1*targetMax
#   else:
#      targetCtrl = 0              
#   return targetCtrl

def squareSignal1(targetMax, deltaT, duration):
  if (deltaT>=(0/10*duration)) and (deltaT < (2/10*duration)):
     targetCtrl = targetMax/2

  elif (deltaT>=(2/10*duration)) and (deltaT < (4/10*duration)):
     targetCtrl = targetMax

  elif (deltaT>=(4/10*duration)) and (deltaT < (6/10*duration)):
     targetCtrl = targetMax/2

  elif (deltaT>=(6/10*duration)) and (deltaT < (8/10*duration)):
     targetCtrl = targetMax
  
  elif (deltaT>=(8/10*duration)) and (deltaT < (10/10*duration)):
     targetCtrl = targetMax/2
  else:
     targetCtrl = 0              
  return targetCtrl

def squareSignal2(targetMax, deltaT, duration):
  if (deltaT>(1/10*duration)) and (deltaT < (4.5/10*duration)):
     targetCtrl = targetMax

  elif (deltaT>(5.5/10*duration)) and (deltaT < (9/10*duration)):
     targetCtrl = -1*targetMax
  else:
     targetCtrl = 0              
  return targetCtrl

def sineSignal1(targetMax, deltaT, duration):
  targetCtrl = targetMax * sin(2*pi*(deltaT/duration))
  return targetCtrl

def sineSignal2(targetMax, deltaT, duration):
  targetCtrl = targetMax * sin(2*pi*(2*deltaT/duration))
  return targetCtrl

signalTypes = ['step1', 'step2', 'square1', 'square2', 'sine1', 'sine2']

def selectSignal(type, targetMax, deltaT, duration):
  if type == 'step1':
    targetCtrl = stepSignal1(targetMax, deltaT, duration)
  elif type == 'step2':
    targetCtrl = stepSignal2(targetMax, deltaT, duration)
  elif type == 'square1':
    targetCtrl = squareSignal1(targetMax, deltaT, duration)
  elif type == 'square2':
    targetCtrl = squareSignal2(targetMax, deltaT, duration)
  elif type == 'sine1':
    targetCtrl = sineSignal1(targetMax, deltaT, duration)
  elif type == 'sine2':
    targetCtrl = sineSignal2(targetMax, deltaT, duration)
  else:
    targetCtrl = 0.0
  
  return targetCtrl






def setPulseDurationA(text):
  try:
    if text:
      val = abs(float(text))
      if val > 30.0:
        g.motorAOnDuration = 30.0
      else:
        g.motorAOnDuration = val
  except:
    pass

  return g.motorAOnDuration

def setPulseDurationB(text):
  try:
    if text:
      val = abs(float(text))
      if val > 30.0:
        g.motorBOnDuration = 30.0
      else:
        g.motorBOnDuration = val
  except:
    pass

  return g.motorBOnDuration







class SetDataCardFrame(customtkinter.CTkFrame):
  def __init__(self, parentFrame, text, initialValue, set_func, inputBoxWidth=120, placeHolderText='enter'):
    super().__init__(master=parentFrame, width=300, corner_radius=10)

    self.value = initialValue
    self.mainText = text
    self.text = f"{self.mainText} = {self.value}"

    self.placeHolderText = placeHolderText
    self.inputBoxWidth = inputBoxWidth

    self.set_func = set_func

    # set card frame
    self.grid_rowconfigure((0,1), weight=0)
    self.grid_columnconfigure((0,1), weight=0)

    self.setTextLabel = customtkinter.CTkLabel(self, text=self.text, font=customtkinter.CTkFont(size=12, weight="bold"))
    self.setTextLabel.grid(row=0, column=0, columnspan=2, padx=(20,5), pady=10, sticky="w")

    self.setTextEntry = customtkinter.CTkEntry(self, placeholder_text=self.placeHolderText, width=self.inputBoxWidth)
    self.setTextEntry.grid(row=1, column=0, padx=(10,3), pady=5, ipadx=3, ipady=3)

    self.setButton = customtkinter.CTkButton(self, text="SET", corner_radius=5, width=50, 
                                             fg_color='#9BABB8', text_color='black', hover_color='#EEEEEE',
                                             command=self.set_data_func)
    self.setButton.grid(row=1, column=1, padx=(2,10), pady=5, ipadx=3, ipady=3)


  def set_data_func(self):
    self.value = self.set_func(self.setTextEntry.get())
    self.text = f"{self.mainText} = {self.value}"

    self.setTextLabel.configure(text=self.text)
    
    self.setTextEntry.destroy()
    self.setTextEntry = customtkinter.CTkEntry(self, placeholder_text=self.placeHolderText, width=self.inputBoxWidth)
    self.setTextEntry.grid(row=1, column=0, padx=(10,3), pady=5, ipadx=3, ipady=3)







class ChooseDataCardFrame(customtkinter.CTkFrame):
  def __init__(self, parentFrame, text, initialValue, input_values, set_func):
    super().__init__(master=parentFrame, width=300, corner_radius=10)

    self.value = initialValue
    self.mainText = text
    self.text = f"{self.mainText} = {self.value}"

    self.set_func = set_func

    # choose card frame
    self.grid_rowconfigure((0,1), weight=0)
    self.grid_columnconfigure((0,1), weight=0)

    self.setTextLabel = customtkinter.CTkLabel(self, text=self.text, font=customtkinter.CTkFont(size=12, weight="bold"))
    self.setTextLabel.grid(row=0, column=0, columnspan=2, padx=(20,5), pady=10, sticky="w")

    self.combobox = customtkinter.CTkComboBox(self, values=input_values, command=self.set_data_func, width=150)
    self.combobox.grid(row=1, column=0, columnspan=2, padx=(10,50), pady=10, ipady=3)
    self.combobox.set("SELECT")

  def set_data_func(self, choice):
    self.value = self.set_func(choice)
    self.text = f"{self.mainText} = {self.value}"
    self.setTextLabel.configure(text=self.text)
    self.combobox.set("SELECT")