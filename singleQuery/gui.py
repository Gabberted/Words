import npyscreen

class myTUI(npyscreen.ActionForm):
	def activate(self):
		self.edit()
		self.parentApp.setNextForm("Hal's")
	def create(self):
		self.hello = self.add(npyscreen.TitleFixedText, name="Say Hello, Hal", value="Hello, Dave")
		self.retort = self.add(npyscreen.Textfield, value="Hal, you are terrible. Read my lips: You suck!")
		self.onAscale = self.add(npyscreen.TitleSlider, out_of=10, name="On a scale of one to ten,"
		                                                                                      "how is Hal's performance?")
		self.favFile = self.add(npyscreen.TitleFilenameCombo, name="What is your favorite file?", label=True)
		self.chooseDate = self.add(npyscreen.DateCombo, name="When you started hating Hal", allowPastDate=True,
		                       allowTodaysDate=True, label=True)
		self.siriOrHal = self.add(npyscreen.TitleSelectOne, values=["Siri", "Cortana", "Hal", "Tay"],
		                      name="Who do you prefer?")
