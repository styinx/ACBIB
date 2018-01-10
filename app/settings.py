from ConfigParser import ConfigParser


class Settings(ConfigParser):
    def __init__(self, filename):
        ConfigParser.__init__(self)

        self.filename = filename
        self.dict = {}

        self.read(filename)

        for sec in self.sections():
            for op in self.options(sec):
                self.dict[sec][op] = self.get(sec, op)

    def update(self):
        for sec in self.sections():
            for op in self.options(sec):
                self.set(sec, op, self.dict[sec][op])

        self.write(self.filename)


settings = Settings("config.ini")

settings["Display"]["APP_POS_X"] = 0
settings["Display"]["APP_POS_Y"] = 0
settings["Display"]["APP_WIDTH"] = 650
settings["Display"]["APP_HEIGHT"] = 160
settings["Display"]["modules"] = "engine,timers,driver,car"
settings["Display"]["grid"] = "7,3"
settings["Display"]["engine"] = "3,1,3,3"

settings["Preferences"]["BACKGROUND"] = "(0.2,0.2,0.2,0.8)"
settings["Preferences"]["FONT_COLOR"] = "(1,1,1,1)"
settings["Preferences"]["SPEED_UNIT"] = "kmh"
settings["Preferences"]["SIDEKICK_ENABLED"] = "yes"
