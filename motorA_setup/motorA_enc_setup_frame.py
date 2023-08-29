from math import sin, cos, radians, pi
import time
from global_var_and_func import g, setPulseDurationA, SetDataCardFrame, ChooseDataCardFrame
import customtkinter





def setPwmValA(text):
  try:
    if text:
      val = int(text)
      if val > 255:
        g.ctrlPwmA = 255
      elif val < -255:
        g.ctrlPwmA = -255
      else:
        g.ctrlPwmA = val
  except:
    pass

  return g.ctrlPwmA
  


def setEncAppr(text):
  try:
    if text:
      val = float(text)
      isSuccessful = g.serClient.send("pprA", val)
      val = g.serClient.get("pprA")
      g.pprA = val
  except:
    pass

  return g.pprA


def sendPwmCtrlA():
  if g.motorAIsOn:
    isSuccess = g.serClient.send("pwm", 0, 0)
    if isSuccess:
      g.motorAIsOn = False
      # print('Motor off', isSuccess)
  else:
    isSuccess = g.serClient.send("pwm", g.ctrlPwmA, 0)
    if isSuccess:
      g.motorAIsOn = True
      g.motorAOnStartTime = time.time()
      # print('Motor On', isSuccess)



def resetInitialThetaA():
  if int(g.dirA) == 1:
    g.initialThetaA = g.thetaA - 90
  elif int(g.dirA) == -1:
    g.initialThetaA = g.thetaA + 90



def initDirA():
  try:
    g.dirA = g.serClient.get("rdirA")
    if int(g.dirA) == 1:
      g.initConfigA = g.motorConfig[0]
    elif int(g.dirA) == -1:
      g.initConfigA = g.motorConfig[1]
    resetInitialThetaA()
  except:
    pass

def setDirA(text):
  try:
    if text == g.motorConfig[0]:
      isSuccessful = g.serClient.send("rdirA", 1.00)
      g.dirA = g.serClient.get("rdirA")
    elif text == g.motorConfig[1]:
      isSuccessful = g.serClient.send("rdirA", -1.00)
      g.dirA = g.serClient.get("rdirA")
    
    g.initConfigA = text
    resetInitialThetaA()
  except:
    pass

  return g.initConfigA












class MotorAPosCanvas(customtkinter.CTkFrame):
  def __init__(self, parentFrame):
    super().__init__(parentFrame)
    
    self.myCanvas = customtkinter.CTkCanvas(master=self, width=400, height=360, bg='white')
    self.r = 170 # circle radius
    self.m = (200, 180) #x, y
    self.circle = self.myCanvas.create_oval(32, 12, 368, 348, outline="grey", width=5)
    self.line = self.myCanvas.create_line(self.m[0], self.m[1], 
                                  self.m[0]+self.r*cos(radians(-1*(g.thetaA-g.initialThetaA))), 
                                  self.m[1]+self.r*sin(radians(-1*(g.thetaA-g.initialThetaA))), 
                                  fill='#434242',width=15)
    self.mid_circle = self.myCanvas.create_oval(180, 160, 220, 200, fill="grey", outline="#434242")

    self.myCanvas.grid(row=0, rowspan=5, column=0, columnspan=2, padx=(5,5), pady=10)

    # add display label
    self.angPosDisplayLabel = customtkinter.CTkLabel(self, text="rawPosA (rad): ", font=customtkinter.CTkFont(size=13, weight="bold"), width=250)
    self.angPosDisplayLabel.grid(row=0, column=2, padx=(5,5), pady=5, sticky="w")

    self.angPosDisplayLabelVal = customtkinter.CTkLabel(self, text="0.0", font=customtkinter.CTkFont(size=12, weight="bold"), width=250)
    self.angPosDisplayLabelVal.grid(row=1, column=2, padx=(5,5), pady=5, sticky="nw")

    self.angVelDisplayLabel = customtkinter.CTkLabel(self, text="rawVelA (rad/s): ", font=customtkinter.CTkFont(size=13, weight="bold"), width=250)
    self.angVelDisplayLabel.grid(row=2, column=2, padx=(5,5), pady=5, sticky="w")

    self.angVelDisplayLabelVal = customtkinter.CTkLabel(self, text="0.0", font=customtkinter.CTkFont(size=12, weight="bold"), width=250)
    self.angVelDisplayLabelVal.grid(row=3, column=2, padx=(5,5), pady=5, sticky="nw")

    initDirA()
    self.chooseMotorConfigFrame = ChooseDataCardFrame(self, "CONFIG AS", g.initConfigA,
                                                      input_values=g.motorConfig,
                                                      set_func=setDirA)
    self.chooseMotorConfigFrame.grid(row=4, column=2, padx=5 , pady=10, ipadx=5, ipady=5)

    self.myCanvas.after(1, self.draw_motor_ang_pos)

  def draw_motor_ang_pos(self):
    if g.motorAIsOn and g.motorAOnDuration < time.time()-g.motorAOnStartTime:
        isSuccess = g.serClient.send("pwm", 0, 0)
        if isSuccess:
          g.motorAIsOn = False
          # print('Motor off', isSuccess)
    self.myCanvas.delete(self.line)
    self.myCanvas.delete(self.mid_circle)

    try:
      g.angPosA, g.angVelA = g.serClient.get("dataA")
    except:
      pass

    g.thetaA = round(self.absAngDeg(g.angPosA),2)

    if int(g.dirA) == -1:
      self.line = self.myCanvas.create_line(self.m[0], self.m[1], 
                                    self.m[0]+self.r*cos(radians(g.thetaA-g.initialThetaA)), 
                                    self.m[1]+self.r*sin(radians(g.thetaA-g.initialThetaA)),  
                                    fill='#434242',width=10)
    elif int(g.dirA) == 1:
      self.line = self.myCanvas.create_line(self.m[0], self.m[1], 
                                    self.m[0]+self.r*cos(radians(-1*(g.thetaA-g.initialThetaA))), 
                                    self.m[1]+self.r*sin(radians(-1*(g.thetaA-g.initialThetaA))),  
                                    fill='#434242',width=10)
    self.mid_circle = self.myCanvas.create_oval(180, 160, 220, 200, fill="grey", outline="#434242")

    self.angPosDisplayLabelVal.configure(text=f"{g.angPosA}")
    self.angVelDisplayLabelVal.configure(text=f"{g.angVelA}")

    self.myCanvas.after(1, self.draw_motor_ang_pos)

  def absAngDeg(self, incAngRad):
    incAngDeg = incAngRad * 180.0 / pi
    return incAngDeg % 360.0


















class MotorAEncSetupFrame(customtkinter.CTkFrame):
  def __init__(self, parent):
    super().__init__(parent)

    self.grid_columnconfigure((0,1,2), weight=0)
    self.grid_rowconfigure((0,1,2,3,4,5,6), weight=0)

    # add heading
    self.heading = customtkinter.CTkLabel(self, text="MOTOR A ENCODER SETUP", font=customtkinter.CTkFont(size=24, weight="bold", underline=False))
    self.heading.grid(row=0, column=0, columnspan=3, padx=10, pady=(5,25))

    # add set card frame
    g.pprA = g.serClient.get("pprA")
    self.setPwmCardFrame = SetDataCardFrame(self, "PPR", g.pprA, placeHolderText="enter PPR", set_func=setEncAppr)
    self.setPwmCardFrame.grid(row=1, column=0, padx=(20,10), pady=10)

    self.setPwmCardFrame = SetDataCardFrame(self, "PWM", g.ctrlPwmA, placeHolderText="enter PWM",set_func=setPwmValA)
    self.setPwmCardFrame.grid(row=1, column=1, padx=10, pady=10)

    self.setDurationCardFrame = SetDataCardFrame(self, "DURATION(sec)", g.motorAOnDuration, placeHolderText="enter DURATION", set_func=setPulseDurationA)
    self.setDurationCardFrame.grid(row=1, column=2, padx=10, pady=10)


    # add buttons
    self.resetHandButton = customtkinter.CTkButton(self, text="RESET HAND", 
                                                   fg_color='#9BABB8', text_color='black', hover_color='#EEEEEE',
                                                   command=resetInitialThetaA)
    self.resetHandButton.grid(row=2, column=0, columnspan=2, padx=20 , pady=(80, 30), ipadx=5, ipady=5)

    self.sendPulsedCmdButton = customtkinter.CTkButton(self, text="SEND PULSED COMMAND", 
                                                       fg_color='#256D85', text_color='white',
                                                       command=sendPwmCtrlA)
    self.sendPulsedCmdButton.grid(row=2, column=2, padx=20, pady=(80, 30), ipadx=5, ipady=5)

    # add canvas
    self.motorAPosCanvas = MotorAPosCanvas(self)
    self.motorAPosCanvas.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
