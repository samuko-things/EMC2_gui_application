
import time
from global_var_and_func import g, SetDataCardFrame, ChooseDataCardFrame, signalTypes, selectSignal
import customtkinter








def setFilterOrder(text):
  try:
    if text:
      isSuccessful = g.serClient.send("ordA", int(text))
      val = int(g.serClient.get("ordA"))
      g.filtOrderA = val
  except:
    pass

  return g.filtOrderA


def setFilterCutOffFreq(text):
  try:
    if text:
      isSuccessful = g.serClient.send("f0A", float(text))
      val = g.serClient.get("f0A")
      g.filtCutOffFreqA = val
  except:
    pass

  return g.filtCutOffFreqA


def setStopVelFreq(text):
  try:
    if text:
      isSuccessful = g.serClient.send("sfA", float(text))
      val = int(g.serClient.get("sfA"))
      g.stopVelFreqA = val
  except:
    pass

  return g.stopVelFreqA


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













class MotorAGraphCanvas(customtkinter.CTkFrame):
  def __init__(self, parentFrame):
    super().__init__(parentFrame)

    # graph parameters
    self.w = 720
    self.h = 400
    self.xStartOffsetPnt = 40
    self.xStopOffsetPnt = 20
    self.yStopOffsetPnt = 20
    self.xAxisLen = self.w - self.xStartOffsetPnt - self.xStopOffsetPnt
    self.yAxisLen = self.h - (2*self.yStopOffsetPnt)
    self.initStartPnt = (self.xStartOffsetPnt, self.h/2) # x,y


    self.clearPlot = False
    self.doPlot = False
    self.doPlotTime = time.time()
    self.doPlotDuration = g.motorAOnDuration

    self.currTime = 0.0
    self.prevTime = 0.0
    self.t = time.time()

    self.currValA = 0.0
    self.currValB = 0.0
    self.prevValA = 0.0
    self.prevValB = 0.0

    self.plotGraphBuffer = []
    self.plotLineBufferA = []
    self.plotLineBufferB = []

    self.maxXVal = self.doPlotDuration

    self.maxYVal = 2*g.maxVelA

    self.xScale = self.xAxisLen/self.maxXVal
    self.yScale = self.yAxisLen/self.maxYVal

    self.signalType = 'step'


    # add display label
    self.text = f"rawVelA (rad/s) = {0.0}"
    self.rawVelLabel = customtkinter.CTkLabel(self, text=self.text, text_color="blue", font=customtkinter.CTkFont(size=12, weight="bold"))
    self.rawVelLabel.grid(row=0, column=0, padx=(5,5), pady=5, sticky="w")

    self.text = f"filtVelA (rad/s) = {0.0}"
    self.filtVelLabel = customtkinter.CTkLabel(self, text=self.text, text_color="red", font=customtkinter.CTkFont(size=12, weight="bold"))
    self.filtVelLabel.grid(row=0, column=1, padx=(5,5), pady=5, sticky="w")

    # add plot command button
    self.plotButton = customtkinter.CTkButton(self, text="START PLOT", command=self.tryPlot)
    self.plotButton.grid(row=0, column=2, padx=(20,5) , pady=5, ipadx=5, ipady=5)

    # add graghical canvas
    self.myCanvas = customtkinter.CTkCanvas(master=self, width=self.w, height=self.h, bg='white')

    self.drawGraphicalLine(self.maxYVal)

    self.myCanvas.grid(row=1, column=0, columnspan=3, padx=(0,0), pady=5)

    self.myCanvas.after(1, self.plot_graph)



  def drawGraphicalLine(self, maxYVal):
    self.deleteGraphParams(self.plotGraphBuffer)

    xAxisline = self.myCanvas.create_line(self.xStartOffsetPnt, self.h/2,
                                          self.xStartOffsetPnt+self.xAxisLen+self.xStopOffsetPnt, self.h/2,
                                          fill="black",width=2)
    self.plotGraphBuffer.append(xAxisline)
    text = self.myCanvas.create_text(self.xStartOffsetPnt+self.xAxisLen+(self.xStopOffsetPnt/2), (self.h/2)+15,
                                    text="(sec)", fill="green", font=('Helvetica 7 bold'), angle=90.0)
    self.plotGraphBuffer.append(text)
    
    yAxisline = self.myCanvas.create_line(self.xStartOffsetPnt, 0,
                                          self.xStartOffsetPnt, self.h,
                                          fill="black",width=2)
    self.plotGraphBuffer.append(yAxisline)
    text = self.myCanvas.create_text(self.xStartOffsetPnt-15, self.yStopOffsetPnt/2,
                                    text="(rad/s)", fill="green", font=('Helvetica 7 bold'))
    self.plotGraphBuffer.append(text)
    
    text = self.myCanvas.create_text(self.xStartOffsetPnt-15, self.h/2,
                                    text="0.0", fill="black", font=('Helvetica 7 bold'))
    self.plotGraphBuffer.append(text)

    for i in range(1,6):
      yTickVal = i/5*maxYVal*-1
      xAxisline = self.myCanvas.create_line(self.xStartOffsetPnt, (self.h/2)-((self.yScale/2)*yTickVal),
                                                 self.xStartOffsetPnt+self.xAxisLen+self.xStopOffsetPnt, (self.h/2)+(i/5*(self.yScale/2)*self.maxYVal),
                                                 fill="grey",width=0.1, dash=(1,3))
      self.plotGraphBuffer.append(xAxisline)
      text = self.myCanvas.create_text(self.xStartOffsetPnt-15, (self.h/2)-((self.yScale/2)*yTickVal),
                                text=str(round(yTickVal/2, 2)), fill="black", font=('Helvetica 7 bold'))
      self.plotGraphBuffer.append(text)

    for i in range(1,6):
      yTickVal = i/5*maxYVal
      xAxisline = self.myCanvas.create_line(self.xStartOffsetPnt, (self.h/2)-((self.yScale/2)*yTickVal),
                                                 self.xStartOffsetPnt+self.xAxisLen+self.xStopOffsetPnt, (self.h/2)-(i/5*(self.yScale/2)*self.maxYVal),
                                                 fill="grey",width=0.1, dash=(1,3))
      self.plotGraphBuffer.append(xAxisline)
      text = self.myCanvas.create_text(self.xStartOffsetPnt-15, (self.h/2)-((self.yScale/2)*yTickVal),
                                text=str(round(yTickVal/2, 2)), fill="black", font=('Helvetica 7 bold'))
      self.plotGraphBuffer.append(text)
    
    for i in range(1,21):
      xTickVal = i/20*self.maxXVal
      yAxisline = self.myCanvas.create_line(self.xStartOffsetPnt+(self.xScale*xTickVal), 0,
                                               self.xStartOffsetPnt+(self.xScale*xTickVal), self.h,
                                               fill="grey",width=0.1, dash=(1,3))
      self.plotGraphBuffer.append(yAxisline)
      text = self.myCanvas.create_text(self.xStartOffsetPnt+(self.xScale*xTickVal), (self.h/2)+15,
                                text=str(round(xTickVal, 2)), fill="black", font=('Helvetica 7 bold'), angle=90.0)
      self.plotGraphBuffer.append(text)
      


  def setMaxVel(self, text):
    try:
      if self.clearPlot == True or self.doPlot == False:
        if text:
          val = float(text)
          g.maxVelA = abs(val)
          self.maxYVal = 2 * g.maxVelA
          self.yScale = self.yAxisLen/self.maxYVal
          self.drawGraphicalLine(self.maxYVal)
    except:
      pass

    return g.maxVelA


  def getSignalType(self):
    return self.signalType
  

  def setSignalType(self, text):
    if self.clearPlot == True or self.doPlot == False:
      self.signalType = text
    return self.signalType
  

  def tryPlot(self):
    if self.clearPlot:
        self.deletePlot(self.plotLineBufferA, self.plotLineBufferB)
        self.plotButton.configure(text='START PLOT')
        self.clearPlot = False
        time.sleep(0.1)

    elif self.doPlot:
        self.doPlot = False 
        # print('stop plot')
    else:
        self.doPlot = True 
        self.doPlotTime = time.time()
        # print('start plot')
  
  def deleteGraphParams(self, graphParams):
      for param in graphParams:
          self.myCanvas.delete(param)
          # root.update_idletasks()
      self.plotGraphBuffer = []

  def deletePlot(self, linesA, linesB):
      for lineA in linesA:
          self.myCanvas.delete(lineA)
          # root.update_idletasks()
      for lineB in linesB:
          self.myCanvas.delete(lineB)
          # root.update_idletasks()
      self.plotLineBufferA = []
      self.plotLineBufferB = []


  def plot_graph(self):
      
      if self.doPlot and self.doPlotDuration < time.time()-self.doPlotTime:
          if g.motorAIsOn:
            isSuccess = g.serClient.send("pwm", 0, 0)
            if isSuccess:
              g.motorAIsOn = False
              # print('Motor off', isSuccess)
          self.doPlot = False 
          self.clearPlot = True
          self.plotButton.configure(text='CLEAR PLOT')
          self.currValA = 0.0
          self.prevValA = 0.0
          self.currValB = 0.0
          self.prevValB = 0.0
          self.currTime = 0.0
          self.prevTime = 0.0
          self.t = time.time()
          # print('stop plot')
          self.myCanvas.after(1, self.plot_graph)

      elif self.doPlot:
          pwm =selectSignal(type=self.signalType,targetMax=g.ctrlPwmA, duration=self.doPlotDuration, deltaT=time.time()-self.doPlotTime)
          
          if not g.motorAIsOn:
            isSuccess = g.serClient.send("pwm", int(pwm), 0)
            if isSuccess:
              g.motorAIsOn = True
              # print('Motor on', isSuccess)
          isSuccess = g.serClient.send("pwm", int(pwm), 0)

          try:
            g.rawAngVelA, g.filtAngVelA = g.serClient.get("velA")
          except:
            pass

          self.currValA = g.rawAngVelA
          self.currValB = g.filtAngVelA
          self.currTime = time.time()-self.t

          lineA = self.myCanvas.create_line(self.xStartOffsetPnt+(self.prevTime*self.xScale),-self.yScale*self.prevValA+self.h/2,
                                           self.xStartOffsetPnt+(self.currTime*self.xScale), -self.yScale*self.currValA+self.h/2,
                                           fill="blue", width=1.25)
          lineB = self.myCanvas.create_line(self.xStartOffsetPnt+(self.prevTime*self.xScale),-self.yScale*self.prevValB+self.h/2,
                                           self.xStartOffsetPnt+(self.currTime*self.xScale), -self.yScale*self.currValB+self.h/2,
                                           fill="red", width=1.25)
          
          self.text = f"rawVelA (rad/s) = {g.rawAngVelA}"
          self.rawVelLabel.configure(text=self.text)

          self.text = f"filtVelA (rad/s) = {g.filtAngVelA}"
          self.filtVelLabel.configure(text=self.text)

          self.plotButton.configure(text='STOP PLOT')

          self.plotLineBufferA.append(lineA)
          self.plotLineBufferB.append(lineB)
          # root.update_idletasks()

          self.prevValA = self.currValA
          self.prevValB = self.currValB

          self.prevTime = self.currTime
          
          self.myCanvas.after(1, self.plot_graph)

      else:
          if g.motorAIsOn:
            isSuccess = g.serClient.send("pwm", 0, 0)
            if isSuccess:
              self.clearPlot = True
              self.plotButton.configure(text='CLEAR PLOT')
              g.motorAIsOn = False
              # print('Motor off', isSuccess)
          self.currValA = 0.0
          self.prevValA = 0.0
          self.currValB = 0.0
          self.prevValB = 0.0
          self.currTime = 0.0
          self.prevTime = 0.0
          self.t = time.time()
          self.myCanvas.after(1, self.plot_graph)


















class MotorAVelFilterFrame(customtkinter.CTkFrame):
  def __init__(self, parent):
    super().__init__(parent)

    self.grid_columnconfigure((0,1,2), weight=0)
    self.grid_rowconfigure((0,1,2,3,4,5,6), weight=0)

    self.motorAGraphCanvas = MotorAGraphCanvas(self)

    # add heading
    self.heading = customtkinter.CTkLabel(self, text="MOTOR A VELOCITY FILTER SETUP", font=customtkinter.CTkFont(size=24, weight="bold", underline=False))
    self.heading.grid(row=0, column=0, columnspan=3, padx=10, pady=(5,25))

    # add set card frame
    g.filtOrderA = int(g.serClient.get("ordA"))
    self.chooseFiltOrderFrame = ChooseDataCardFrame(self, "FILTER_ORDER", g.filtOrderA,
                                                    input_values=["1", "2"],
                                                    set_func=setFilterOrder)
    self.chooseFiltOrderFrame.grid(row=1, column=0, padx=10, pady=10)

    g.filtCutOffFreqA = g.serClient.get("f0A")
    self.setFiltCutOffFreqFrame = SetDataCardFrame(self, "CUTOFF_FREQ(Hz)", g.filtCutOffFreqA,
                                                   placeHolderText="enter CUTOFF_FREQ",
                                                   set_func=setFilterCutOffFreq)
    self.setFiltCutOffFreqFrame.grid(row=1, column=1, padx=10, pady=10)

    g.stopVelFreqA = int(g.serClient.get("sfA"))
    self.chooseStopVelFreqFrame = ChooseDataCardFrame(self, "VEL_STOP_TIME(us)", g.stopVelFreqA,
                                                      input_values=["500", "1000", "2500", "5000", "7500", "10000", "15000", "20000", "30000", "50000", "75000", "100000"],
                                                      set_func=setStopVelFreq)
    self.chooseStopVelFreqFrame.grid(row=1, column=2, padx=10, pady=10)


    self.motorAGraphCanvas.setSignalType(signalTypes[0])
    self.chooseFiltOrderFrame = ChooseDataCardFrame(self, "SIGNAL_TYPE", self.motorAGraphCanvas.getSignalType(),
                                                    input_values=signalTypes,
                                                    set_func=self.motorAGraphCanvas.setSignalType)
    self.chooseFiltOrderFrame.grid(row=2, column=0, padx=10, pady=10)

    self.setMaxVelFrame = SetDataCardFrame(self, "MAX_VEL(rad/s)", g.maxVelA,
                                                   placeHolderText="enter Max Vel",
                                                   set_func=self.motorAGraphCanvas.setMaxVel)
    self.setMaxVelFrame.grid(row=2, column=1, padx=10, pady=10)

    self.setMaxVelFrame = SetDataCardFrame(self, "CTRL_PWM", g.ctrlPwmA,
                                                   placeHolderText="enter Ctrl PWM",
                                                   set_func=setPwmValA)
    self.setMaxVelFrame.grid(row=2, column=2, padx=10, pady=10)


#     # add canvas
    # self.motorAGraphCanvas = MotorAGraphCanvas(self)
    self.motorAGraphCanvas.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
