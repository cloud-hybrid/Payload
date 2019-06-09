class VPSWindow(Frame):
  threading.Thread(target = Display().header()).start()
  threading.Thread(target = Display().copyright()).start()
  def __init__(self):
    super().__init__()

    self.master.title("Vault Development")
    self.pack(fill = BOTH, expand = True)

    self.columnconfigure(1, weight = 1)
    self.columnconfigure(2, pad = 1)
    
    self.user_label = Label(self, text = "VPS Username")
    self.user_label.grid(row = 0, column = 0, pady = 5, padx = 5)
    self.user_entry = Entry(self, justify = "center")
    self.user_entry.grid(row = 1, column = 0, pady = 5, padx = 5)

    self.password_label = Label(self, text = "VPS Password")
    self.password_label.grid(row = 0, column = 1, pady = 5, padx = 5)
    self.password_entry = Entry(self, show = "*", justify = "center")
    self.password_entry.grid(row = 1, column = 1, pady = 5, padx = 5)
    self.password_entry.insert(0, "Knowledge")
    self.password_button = Button(self, text = "Show", command = self.showPassword)
    self.password_button.grid(row = 1, column = 3, pady = 5, padx = 5)

    self.server_menu_label = Label(self, text = "VPS Injection")
    self.server_menu_label.grid(row = 0, column = 4, pady = 5, padx = 5)
    self.server_menu_selection = StringVar(self)
    self.server_menu_selection.set("Minimal")
    self.server_menu = OptionMenu(self, self.server_menu_selection, "Minimal", "Basic", "LAMP", "Wordpress")
    self.server_menu.grid(row = 1, column = 4, pady = 5, padx = 5)

    self.SQL_label = Label(self, text = "SQL Password")
    self.SQL_label.grid(row = 2, column = 0, pady = 5, padx = 5)
    self.SQL_entry = Entry(self, show = "*", justify = "center")
    self.SQL_entry.grid(row = 3, column = 0, pady = 5, padx = 5)

    self.CPU_label = Label(self, text = "vCPU(s)")
    self.CPU_label.grid(row = 2, column = 1, pady = 5, padx = 5)
    self.CPU_entry = Entry(self, justify = "center")
    self.CPU_entry.grid(row = 3, column = 1, pady = 5, padx = 5)
    self.CPU_entry.insert(0, 1)

    self.RAM = Label(self, text = "vRAM")
    self.RAM.grid(row = 2, column = 4, pady = 5, padx = 5)
    self.RAM_entry = Entry(self, justify = "center")
    self.RAM_entry.grid(row = 3, column = 4, pady = 5, padx = 5)
    self.RAM_entry.insert(0, 512)

    self.domain_label = Label(self, text = "FQDN")
    self.domain_label.grid(row = 4, column = 0, pady = 5, padx = 5)
    self.domain_entry = Entry(self, justify = "center")
    self.domain_entry.insert(0, "N/A")
    self.domain_entry.grid(row = 5, column = 0, pady = 5, padx = 5)

    self.SSL = IntVar()
    self.SSL.set(0)
    self.check_SSL = Checkbutton(self, text = "SSL", variable = self.SSL, onvalue = 1, offvalue = 0)
    self.check_SSL.grid(row = 5, column = 1, pady = 5, padx = 5)  

    self.email_label = Label(self, text = "eMail")
    self.email_label.grid(row = 4, column = 4, pady = 5, padx = 5)
    self.email_entry = Entry(self, justify = "center")
    self.email_entry.grid(row = 5, column = 4, pady = 5, padx = 5)

    self.activate = Button(self, text = "Execute", command = self.thread)
    self.activate.grid(row = 25, column = 10, pady = 5, padx = 5)

    self.close = Button(self, text = "Close", command = self.master.destroy)
    self.close.grid(row = 25, column = 11, pady = 5, padx = 5)
    
    self.help_button = Button(self, text = "Help")
    self.help_button.grid(row = 25, column = 0, pady = 5, padx = 5)


  def showPassword(self):
    text = self.password_entry.get()

    self.password_entry = Entry(self, justify = "center")
    self.password_entry.insert(0, f"{text}")
    self.password_entry.grid(row = 1, column = 1, columnspan = 1, padx = 5)

  def thread(self):
    threading.Thread(target = self.execute).start()

  def execute(self):
    input.sql_Password = self.SQL_entry.get()

    connection = Connection("root", str(input.sql_Password), "192.168.1.75", "V_PAYLOAD")
    result = connection.queryAll()
    subnet = connection.incrementIP()
    VPS_IP = connection.network + str(subnet)

    input.v_User = self.user_entry.get()
    input.v_Password = self.password_entry.get()
    input.v_IP = VPS_IP
    input.v_Type = self.server_menu_selection.get()
    input.v_CPU = self.CPU_entry.get()
    input.v_RAM = self.RAM_entry.get()

    input.Domain = self.domain_entry.get()
    input.SSL = self.SSL.get()

    input.eMail[2] = self.email_entry.get()

    connection.addVPS(input.v_User, input.v_Password, input.v_Type, VPS_IP, input.v_RAM, input.v_CPU, input.Domain, input.SSL, input.eMail[2])
    connection.disconnect()

    threading.Thread(target = main()).start()