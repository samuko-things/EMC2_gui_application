from math import sin, cos, radians, pi
import time
from global_var_and_func import g, setPulseDurationB, SetDataCardFrame, ChooseDataCardFrame
import customtkinter





def setPwmValB(text):
  try:
    if text:
      val = int(text)
      if val > 255:
        g.ctrlPwmB = 255
      elif val < -255:
        g.ctrlPwmB = -255
      else:
        g.ctrlPwmB = val
  except:
    pass

  return g.ctrlPwmB


def setEncBppr(text):
  try:
    if text:
      val = float(text)
      isSuccessful = g.serClient.send("pprB", val)
      val = g.serClient.get("pprB")
      g.pprB = val
  except:
    pass

  return g.pprB


def sendPwmCtrlB():
  if g.motorBIsOn:
    isSuccess = g.serClient.send("pwm", 0, 0)
    if isSuccess:
      g.motorBIsOn = False
      # print('Motor off', isSuccess)
  else:
    isSuccess = g.serClient.send("pwm", 0, g.ctrlPwmB)
    if isSuccess:
      g.motorBIsOn = True
      g.motorBOnStartTime = time.time()
      # print('Motor On', isSuccess)



def resetInitialThetaB():
  if int(g.dirB) == 1:
    g.initialThetaB = g.thetaB - 90
  elif int(g.dirB) == -1:
    g.initialThetaB = g.thetaB + 90



def initDirB():
  try:
    g.dirB = g.serClient.get("rdirB")
    if int(g.dirB) == 1:
      g.initConfigB = g.motorConfig[0]
    elif int(g.dirB) == -1:
      g.initConfigB = g.motorConfig[1]
    resetInitialThetaB()
  except:
    pass

def setDirB(text):
  try:
    if text == g.motorConfig[0]:
      isSuccessful = g.serClient.send("rdirB", 1.00)
      g.dirB = g.serClient.get("rdirB")
    elif text == g.motorConfig[1]:
      isSuccessful = g.serClient.send("rdirB", -1.00)
      g.dirB = g.serClient.get("rdirB")
    
    g.initConfigB = text
    resetInitialThetaB()
  except:
    pass

  return g.initConfigB










class MotorBPosCanvas(customtkinter.CTkFrame):
  def __init__(self, parentFrame):
    super().__init__(parentFrame)
    
    self.myCanvas = customtkinter.CTkCanvas(master=self, width=400, height=360, bg='white')
    self.r = 170 # circle radius
    self.m = (200, 180) #x, y
    self.circle = self.myCanvas.create_oval(32, 12, 368, 348, outline="grey", width=5)
    self.line = self.myCanvas.create_line(self.m[0], self.m[1], 
                                  self.m[0]+self.r*cos(radians(-1*(g.thetaB-g.initialThetaB))), 
                                  self.m[1]+self.r*sin(radians(-1*(g.thetaB-g.initialThetaB))), 
                                  fill='#434242',width=15)
    self.mid_circle = self.myCanvas.create_oval(180, 160, 220, 200, fill="grey", outline="#434242")

    self.myCanvas.grid(row=0, rowspan=5, column=0, columnspan=2, padx=(5,5), pady=10)

    # add display label
    self.angPosDisplayLabel = customtkinter.CTkLabel(self, text="rawPosB (rad): ", font=customtkinter.CTkFont(size=13, weight="bold"), width=250)
    self.angPosDisplayLabel.grid(row=0, column=2, padx=(5,5), pady=5, sticky="w")

    self.angPosDisplayLabelVal = customtkinter.CTkLabel(self, text="0.0", font=customtkinter.CTkFont(size=12, weight="bold"), width=250)
    self.angPosDisplayLabelVal.grid(row=1, column=2, padx=(5,5), pady=5, sticky="nw")

    self.angVelDisplayLabel = customtkinter.CTkLabel(self, text="rawVelB (rad/s): ", font=customtkinter.CTkFont(size=13, weight="bold"), width=250)
    self.angVelDisplayLabel.grid(row=2, column=2, padx=(5,5), pady=5, sticky="w")

    self.angVelDisplayLabelVal = customtkinter.CTkLabel(self, text="0.0", font=customtkinter.CTkFont(size=12, weight="bold"), width=250)
    self.angVelDisplayLabelVal.grid(row=3, column=2, padx=(5,5), pady=5, sticky="nw")

    initDirB()
    self.chooseMotorConfigFrame = ChooseDataCardFrame(self, "CONFIG AS", g.initConfigB,
                                                      input_values=g.motorConfig,
                                                      set_func=setDirB)
    self.chooseMotorConfigFrame.grid(row=4, column=2, padx=5 , pady=10, ipadx=5, ipady=5)

    self.myCanvas.after(1, self.draw_motor_ang_pos)

  def draw_motor_ang_pos(self):
    if g.motorBIsOn and g.motorBOnDuration < time.time()-g.motorBOnStartTime:
        isSuccess = g.serClient.send("pwm", 0, 0)
        if isSuccess:
          g.motorBIsOn = False
          # print('Motor off', isSuccess)
    self.myCanvas.delete(self.line)
    self.myCanvas.delete(self.mid_circle)

    try:
      g.angPosB, g.angVelB = g.serClient.get("dataB")
    except:
      pass
    
    g.thetaB = round(self.absAngDeg(g.angPosB),2)

    if g.dirB == -1:
      self.line = self.myCanvas.create_line(self.m[0], self.m[1], 
                                    self.m[0]+self.r*cos(radians(g.thetaB-g.initialThetaB)), 
                                    self.m[1]+self.r*sin(radians(g.thetaB-g.initialThetaB)),  
                                    fill='#434242',width=10)
    elif g.dirB == 1:
      self.line = self.myCanvas.create_line(self.m[0], self.m[1], 
                                    self.m[0]+self.r*cos(radians(-1*(g.thetaB-g.initialThetaB))), 
                                    self.m[1]+self.r*sin(radians(-1*(g.thetaB-g.initialThetaB))),  
                                    fill='#434242',width=10)
    self.mid_circle = self.myCanvas.create_oval(180, 160, 220, 200, fill="grey", outline="#434242")

    self.angPosDisplayLabelVal.configure(text=f"{g.angPosB}")
    self.angVelDisplayLabelVal.configure(text=f"{g.angVelB}")
    
    self.myCanvas.after(1, self.draw_motor_ang_pos)

  def absAngDeg(self, incAngRad):
    incAngDeg = incAngRad * 180.0 / pi
    return incAngDeg % 360.0


















class MotorBEncSetupFrame(customtkinter.CTkFrame):
  def __init__(self, parent):
    super().__init__(parent)

    self.grid_columnconfigure((0,1,2), weight=0)
    self.grid_rowconfigure((0,1,2,3,4,5,6), weight=0)

    # add heading
    self.heading = customtkinter.CTkLabel(self, text="MOTOR B ENCODER SETUP", font=customtkinter.CTkFont(size=24, weight="bold", underline=False))
    self.heading.grid(row=0, column=0, columnspan=3, padx=10, pady=(5,25))

    # add set card frame
    g.pprB = g.serClient.get("pprB")
    self.setPwmCardFrame = SetDataCardFrame(self, "PPR", g.pprB, placeHolderText="enter PPR", set_func=setEncBppr)
    self.setPwmCardFrame.grid(row=1, column=0, padx=(20,10), pady=10)

    self.setPwmCardFrame = SetDataCardFrame(self, "PWM", g.ctrlPwmB, placeHolderText="enter PWM", set_func=setPwmValB)
    self.setPwmCardFrame.grid(row=1, column=1, padx=10, pady=10)

    self.setDurationCardFrame = SetDataCardFrame(self, "DURATION(sec)", g.motorBOnDuration, placeHolderText="enter DURATION", set_func=setPulseDurationB)
    self.setDurationCardFrame.grid(row=1, column=2, padx=10, pady=10)


    # add buttons
    self.resetHandButton = customtkinter.CTkButton(self, text="RESET HAND", 
                                                   fg_color='#9BABB8', text_color='black', hover_color='#EEEEEE',
                                                   command=resetInitialThetaB)
    self.resetHandButton.grid(row=2, column=0, columnspan=2, padx=20 , pady=(80, 30), ipadx=5, ipady=5)

    self.sendPulsedCmdButton = customtkinter.CTkButton(self, text="SEND PULSED COMMAND", 
                                                       fg_color='#256D85', text_color='white',
                                                       command=sendPwmCtrlB)
    self.sendPulsedCmdButton.grid(row=2, column=2, padx=20, pady=(80, 30), ipadx=5, ipady=5)

    # add canvas
    self.motorBPosCanvas = MotorBPosCanvas(self)
    self.motorBPosCanvas.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
