from ConfigParser import ConfigParser
import os


class Settings(ConfigParser):
    def __init__(self, filename):
        ConfigParser.__init__(self)

        self.filename = filename
        self.dict = {}
        self.setDefault()

        if os.path.isfile(os.path.abspath(filename)):
            self.read(filename)

        for sec in self.sections():
            for op in self.options(sec):
                self.dict[sec][op] = self.get(sec, op)

    def update(self):
        for sec in self.sections():
            for op in self.options(sec):
                self.set(sec, op, self.dict[sec][op])

        self.write(self.filename)
        
    def setDefault(self):
        self.dict["Display"]["APP_POS_X"] = 0
        self.dict["Display"]["APP_POS_Y"] = 0
        self.dict["Display"]["APP_WIDTH"] = 650
        self.dict["Display"]["APP_HEIGHT"] = 160
        self.dict["Display"]["modules"] = "engine,timers,driver,car"
        self.dict["Display"]["grid"] = "7,3"
        self.dict["Display"]["engine"] = "3,1,3,3"

        self.dict["Preferences"]["BACKGROUND"] = "(0.2,0.2,0.2,0.8)"
        self.dict["Preferences"]["FONT_COLOR"] = "(1,1,1,1)"
        self.dict["Preferences"]["SPEED_UNIT"] = "kmh"
        self.dict["Preferences"]["SIDEKICK_ENABLED"] = "yes"
