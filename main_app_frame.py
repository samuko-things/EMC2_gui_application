import customtkinter

# customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
# customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

from motorA_setup.motorA_enc_setup_frame import MotorAEncSetupFrame
from motorB_setup.motorB_enc_setup_frame import MotorBEncSetupFrame
from motorA_setup.motorA_vel_filter_frame import MotorAVelFilterFrame
from motorB_setup.motorB_vel_filter_frame import MotorBVelFilterFrame
from motorA_setup.motorA_pid_setup_frame import MotorAPidSetupFrame
from motorB_setup.motorB_pid_setup_frame import MotorBPidSetupFrame
from motor_driver_params_setup_frame import DriverParamsSetupFrame




class MainApp(customtkinter.CTkFrame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    # create sidebar frame with widgets
    self.sidebarFrame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
    self.sidebarFrame.grid(row=0, column=0, padx=5, pady=0, sticky="nsw")

    self.menuLabel = customtkinter.CTkLabel(self.sidebarFrame, text="MENU", font=customtkinter.CTkFont(size=20, weight="bold"), width=150)
    self.menuLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

    self.motorAEncSetupMenuButton = customtkinter.CTkButton(self.sidebarFrame, text="MotorA Enc Setup", corner_radius=5,
                                                        font=customtkinter.CTkFont(size=14, weight="bold"),
                                                        fg_color='transparent', text_color='grey', hover_color='#EEEEEE',
                                                        command= lambda: self.indicate(self.motorAEncSetupMenuButton, self.motorAEncSetupPage))
    self.motorAEncSetupMenuButton.grid(row=1, column=0, padx=10, pady=(40,5), ipadx=10, ipady=10)

    self.motorAVelFilterMenuButton = customtkinter.CTkButton(self.sidebarFrame, text="MotorA Vel Filter", corner_radius=5,
                                                        font=customtkinter.CTkFont(size=14, weight="bold"),
                                                        fg_color='transparent', text_color='grey', hover_color='#EEEEEE',
                                                        command= lambda: self.indicate(self.motorAVelFilterMenuButton, self.motorAVelFilterPage))
    self.motorAVelFilterMenuButton.grid(row=2, column=0, padx=10, pady=5, ipadx=10, ipady=10)

    self.motorAPidSetupMenuButton = customtkinter.CTkButton(self.sidebarFrame, text="MotorA PID Setup", corner_radius=5,
                                                        font=customtkinter.CTkFont(size=14, weight="bold"),
                                                        fg_color='transparent', text_color='grey', hover_color='#EEEEEE',
                                                        command= lambda: self.indicate(self.motorAPidSetupMenuButton, self.motorAPidSetupPage))
    self.motorAPidSetupMenuButton.grid(row=3, column=0, padx=10, pady=5, ipadx=10, ipady=10)

    self.motorBEncSetupMenuButton = customtkinter.CTkButton(self.sidebarFrame, text="MotorB Enc Setup", corner_radius=5,
                                                        font=customtkinter.CTkFont(size=14, weight="bold"),
                                                        fg_color='transparent', text_color='grey', hover_color='#EEEEEE',
                                                        command= lambda: self.indicate(self.motorBEncSetupMenuButton, self.motorBEncSetupPage))
    self.motorBEncSetupMenuButton.grid(row=4, column=0, padx=10, pady=(40,5), ipadx=10, ipady=10)

    self.motorBVelFilterMenuButton = customtkinter.CTkButton(self.sidebarFrame, text="MotorB Vel Filter", corner_radius=5,
                                                        font=customtkinter.CTkFont(size=14, weight="bold"),
                                                        fg_color='transparent', text_color='grey', hover_color='#EEEEEE',
                                                        command= lambda: self.indicate(self.motorBVelFilterMenuButton, self.motorBVelFilterPage))
    self.motorBVelFilterMenuButton.grid(row=5, column=0, padx=10, pady=5, ipadx=10, ipady=10)

    self.motorBPidSetupMenuButton = customtkinter.CTkButton(self.sidebarFrame, text="MotorB PID Setup", corner_radius=5,
                                                        font=customtkinter.CTkFont(size=14, weight="bold"),
                                                        fg_color='transparent', text_color='grey', hover_color='#EEEEEE',
                                                        command= lambda: self.indicate(self.motorBPidSetupMenuButton, self.motorBPidSetupPage))
    self.motorBPidSetupMenuButton.grid(row=6, column=0, padx=10, pady=5, ipadx=10, ipady=10)

    self.driverParamsSetupMenuButton = customtkinter.CTkButton(self.sidebarFrame, text="Driver Param Setup", corner_radius=5,
                                                        font=customtkinter.CTkFont(size=14, weight="bold"),
                                                        fg_color='transparent', text_color='grey', hover_color='#EEEEEE',
                                                        command= lambda: self.indicate(self.driverParamsSetupMenuButton, self.driverParamsSetupPage))
    self.driverParamsSetupMenuButton.grid(row=7, column=0, padx=10, pady=(40,10), ipadx=10, ipady=10)


    self.mainFrame = customtkinter.CTkFrame(self)
    self.mainFrame.grid(row=0, column=1, padx=(5,0), pady=0, ipadx=0, ipady=0, sticky="nw")


    #####################################################################################
    self.motorAEncSetupFrame = MotorAEncSetupFrame(self.mainFrame)
    self.motorAEncSetupFrame.pack()
    self.motorAEncSetupMenuButton.configure(fg_color='transparent', text_color='black')
    #####################################################################################


  def hide_indicators(self):
    self.motorAEncSetupMenuButton.configure(fg_color='transparent', text_color='grey')
    self.motorBEncSetupMenuButton.configure(fg_color='transparent', text_color='grey')
    self.motorAVelFilterMenuButton.configure(fg_color='transparent', text_color='grey')
    self.motorBVelFilterMenuButton.configure(fg_color='transparent', text_color='grey')
    self.motorAPidSetupMenuButton.configure(fg_color='transparent', text_color='grey')
    self.motorBPidSetupMenuButton.configure(fg_color='transparent', text_color='grey')
    self.driverParamsSetupMenuButton.configure(fg_color='transparent', text_color='grey')
  
  def indicate(self, button, page):
    self.hide_indicators()
    button.configure(fg_color='transparent', text_color='black')
    self.delete_pages()
    page()

  def delete_pages(self):
    for frame in self.mainFrame.winfo_children():
      frame.destroy()


  def motorAEncSetupPage(self):
    self.motorAEncSetupFrame = MotorAEncSetupFrame(self.mainFrame)
    self.motorAEncSetupFrame.pack()
  
  def motorBEncSetupPage(self):
    self.motorBEncSetupFrame = MotorBEncSetupFrame(self.mainFrame)
    self.motorBEncSetupFrame.pack()

  def motorAVelFilterPage(self):
    self.motorAVelFilterFrame = MotorAVelFilterFrame(self.mainFrame)
    self.motorAVelFilterFrame.pack()
  
  def motorBVelFilterPage(self):
    self.motorBVelFilterFrame = MotorBVelFilterFrame(self.mainFrame)
    self.motorBVelFilterFrame.pack()

  def motorAPidSetupPage(self):
    self.motorAPidSetupFrame = MotorAPidSetupFrame(self.mainFrame)
    self.motorAPidSetupFrame.pack()
  
  def motorBPidSetupPage(self):
    self.motorBPidSetupFrame = MotorBPidSetupFrame(self.mainFrame)
    self.motorBPidSetupFrame.pack()
  
  def driverParamsSetupPage(self):
    self.driverParamsSetupFrame = DriverParamsSetupFrame(self.mainFrame)
    self.driverParamsSetupFrame.pack()
