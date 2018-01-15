import ac
import acsys
import sys
import os
import platform

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + '/../stdlib64'
else:
    sysdir = os.path.dirname(__file__) + '/../stdlib'

sys.path.insert(0, sysdir)
sys.path.insert(0, os.path.dirname(__file__) + '/../third_party')
os.environ['PATH'] = os.environ['PATH'] + ";."


from third_party.sim_info import info


class Color:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a


def formatTime(millis):
    m = int(millis / 60000)
    s = int((millis % 60000) / 1000)
    ms = millis % 1000

    return "{:02d}:{:02d}.{:03d}".format(m, s, ms)


def formatGear(gear):
    if gear == 0:
        return "R"
    elif gear == 1:
        return "N"
    else:
        return str(gear - 1)


class ACPLAYER:
    @staticmethod
    def getPlayerNickname():
        return info.static.playerNick

    @staticmethod
    def getPlayerFirstname():
        return info.static.playerName

    @staticmethod
    def getPlayerLastname():
        return info.static.playerSurname


class ACSESSION:
    @staticmethod
    def getSessionType():
        return info.graphics.session

    @staticmethod
    def getSessionStatus():
        return info.graphics.status

    @staticmethod
    def isTimedRace():
        return info.static.isTimedRace

    @staticmethod
    def getRaceTimeLeft():
        return info.graphics.sessionTimeLeft

    @staticmethod
    def getTrackLength():
        return ac.getTrackLength(0)

    @staticmethod
    def getTrackName():
        return ac.getTrackName(0)

    @staticmethod
    def getCarsCount():
        return ac.getCarsCount()


class ACLAP:
    @staticmethod
    def getCurrentLapTime(car=0):
        return ac.getCarState(car, acsys.CS.LapTime)

    @staticmethod
    def getCurrentLap(car=0):
        time = ac.getCarState(car, acsys.CS.LapTime)
        if time > 0:
            return formatTime(time)
        else:
            return "--:--"

    @staticmethod
    def getLastLapTime(car=0):
        return ac.getCarState(car, acsys.CS.LastLap)

    @staticmethod
    def getLastLap(car=0):
        time = ac.getCarState(car, acsys.CS.LastLap)
        if time > 0:
            return formatTime(time)
        else:
            return "--:--"

    @staticmethod
    def getBestLapTime(car=0):
        return ac.getCarState(car, acsys.CS.BestLap)

    @staticmethod
    def getBestLap(car=0):
        time = ac.getCarState(car, acsys.CS.BestLap)
        if time > 0:
            return formatTime(time)
        else:
            return "--:--"

    @staticmethod
    def getSplit():
        return info.graphics.split

    @staticmethod
    def getSplits(car=0):
        return ac.getLastSplits(car, )

    @staticmethod
    def getLap(car=0):
        return ac.getCarState(car, acsys.CS.LapCount) + 1

    @staticmethod
    def getLapDelta(car=0):
        return ac.getCarState(car, acsys.CS.PerformanceMeter)

    @staticmethod
    def isLapInvalidated(car=0):
        return ac.getCarState(car, acsys.CS.LapInvalidated) or ACCAR.getTyresOut() > 2 or ACCAR.isInPit()

    @staticmethod
    def getLaps():
        if info.graphics.numberOfLaps > 0:
            return info.graphics.numberOfLaps
        else:
            return "-"

    @staticmethod
    def lastSectorTime():
        return info.graphics.lastSectorTime

    @staticmethod
    def getSectors():
        return info.static.sectorCount


class ACCAR:
    @staticmethod
    def getFocusedCar():
        return ac.getFocusedCar()

    @staticmethod
    def getCarDamage(loc="front"):
        if loc == "front":
            return info.physics.carDamage[0]
        elif loc == "rear":
            return info.physics.carDamage[1]
        elif loc == "left":
            return info.physics.carDamage[2]
        elif loc == "right":
            return info.physics.carDamage[3]
        else:
            return info.physics.carDamage[4]

    @staticmethod
    def getPrevCarDiffTime(formatted=False):
        time = 0
        dist = 0
        track_len = ACSESSION.getTrackLength()
        lap = ACLAP.getLap(0)
        pos = ACCAR.getLocation(0)

        for car in range(ACSESSION.getCarsCount()):
            if ACCAR.getPosition(car) == ACCAR.getPosition(0) - 1:
                lap_next = ACLAP.getLap(car)
                pos_next = ACCAR.getLocation(car)

                dist = max(0, (pos_next * track_len + lap_next * track_len) - (pos * track_len + lap * track_len))
                time = max(0.0, dist / max(10.0, ACCAR.getSpeed(0, "ms")))
                break

        if not formatted:
            return time
        else:
            if dist > track_len:
                laps = dist / track_len
                if laps > 1:
                    return "+{:3.1f}".format(laps) + " Laps"
                else:
                    return "+{:3.1f}".format(laps) + " Lap"
            elif time > 60:
                return "+" + formatTime(int(time * 1000))
            else:
                return "+{:3.3f}".format(time)

    @staticmethod
    def getNextCarDiffTime(formatted=False):
        time = 0
        dist = 0
        track_len = ACSESSION.getTrackLength()
        lap = ACLAP.getLap(0)
        pos = ACCAR.getLocation(0)

        for car in range(ACSESSION.getCarsCount()):
            if ACCAR.getPosition(car) == ACCAR.getPosition(0) + 1:
                lap_next = ACLAP.getLap(car)
                pos_next = ACCAR.getLocation(car)

                dist = max(0, (pos * track_len + lap * track_len) - (pos_next * track_len + lap_next * track_len))
                time = max(0.0, dist / max(10.0, ACCAR.getSpeed(car, "ms")))
                break

        if not formatted:
            return time
        else:
            if dist > track_len:
                laps = dist / track_len
                if laps > 1:
                    return "-{:3.1f}".format(laps) + " Laps"
                else:
                    return "-{:3.1f}".format(laps) + " Lap"
            elif time > 60:
                return "-" + formatTime(int(time * 1000))
            else:
                return "-{:3.3f}".format(time)

    @staticmethod
    def getGas():
        return info.physics.gas

    @staticmethod
    def getBrake():
        return info.physics.brake

    @staticmethod
    def hasDRS():
        return info.static.hasDRS

    @staticmethod
    def DRSEnabled():
        return info.physics.drsEnabled

    @staticmethod
    def hasERS():
        return info.static.hasERS

    @staticmethod
    def hasKERS():
        return info.static.hasKERS

    @staticmethod
    def ABS():
        return info.physics.abs

    @staticmethod
    def getSpeed(car=0, unit="kmh"):
        if unit == "kmh":
            return ac.getCarState(car, acsys.CS.SpeedKMH)
        elif unit == "mph":
            return ac.getCarState(car, acsys.CS.SpeedMPH)
        elif unit == "ms":
            return ac.getCarState(car, acsys.CS.SpeedMS)

    @staticmethod
    def getGear(car=0):
        return formatGear(ac.getCarState(car, acsys.CS.Gear))

    @staticmethod
    def getRPM(car=0):
        return ac.getCarState(car, acsys.CS.RPM)

    @staticmethod
    def getRPMMax():
        if info.static.maxRpm:
            return info.static.maxRpm
        else:
            return 8000

    @staticmethod
    def getPosition(car=0):
        return ac.getCarRealTimeLeaderboardPosition(car) + 1

    @staticmethod
    def getLocation(car=0):
        return ac.getCarState(car, acsys.CS.NormalizedSplinePosition)

    @staticmethod
    def isInPit(car=0):
        return ac.isCarInPitline(car) or ac.isCarInPit(car)

    @staticmethod
    def isAIDriven():
        return info.physics.isAIControlled

    @staticmethod
    def getFuel():
        return info.physics.fuel

    @staticmethod
    def getMaxFuel():
        return info.static.maxFuel

    @staticmethod
    def getTyresOut():
        return info.physics.numberOfTyresOut

    @staticmethod
    def getTyreWearValue(tyre=0):
        return info.physics.tyreWear[tyre]

    @staticmethod
    def getTyreWear(tyre=0):
        return (ACCAR.getTyreWearValue(tyre) - 94) * 16.6

    @staticmethod
    def getTyreDirtyLevel(tyre=0):
        return info.physics.tyreDirtyLevel

    @staticmethod
    def getTyreCompund():
        return info.graphics.tyreCompound

    @staticmethod
    def getTyreTemp(tyre=0, loc="m"):
        if loc == "i":
            return info.physics.tyreTempI[tyre]
        elif loc == "m":
            return info.physics.tyreTempM[tyre]
        elif loc == "o":
            return info.physics.tyreTempO[tyre]
        elif loc == "c":
            return info.physics.tyreCoreTemperature[tyre]

    @staticmethod
    def getTyrePressure(tyre=0):
        return info.physics.wheelsPressure[tyre]

    @staticmethod
    def getBrakeTemperature(tyre=0):
        return info.physics.brakeTemp[tyre]


class GL:
    @staticmethod
    def rect(x, y, w, h, color=Color(1, 1, 1, 1), filled=True):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        if filled:
            ac.glQuad(x, y, w, h)
        else:
            ac.glBegin(1)
            ac.glVertex2f(x, y)
            ac.glVertex2f(x + w, y)
            ac.glVertex2f(x + w, y)
            ac.glVertex2f(x + w, y + h)
            ac.glVertex2f(x + w, y + h)
            ac.glVertex2f(x, y + h)
            ac.glVertex2f(x, y + h)
            ac.glVertex2f(x, y)
            ac.glEnd()

    @staticmethod
    def line(x1, y1, x2, y2, color=Color(1, 1, 1, 1)):
        ac.glColor4f(color.r, color.g, color.b, color.a)
        ac.glBegin(1)
        ac.glVertex2f(x1, y1)
        ac.glVertex2f(x2, y2)
        ac.glEnd()


class App:
    def __init__(self, app_name, app_title, w, h, bg=Color(0, 0, 0, 1)):
        self.app_name = app_name
        self.app_title = app_title
        self.w = w
        self.h = h
        self.bg = bg
        self.size = (w, h)

        self.app = ac.newApp(app_name)
        ac.setTitle(self.app, app_title)
        ac.setSize(self.app, w, h)
        ac.setIconPosition(self.app, 100000, 0)
        ac.setTitlePosition(self.app, 100000, 0)
        ac.drawBorder(self.app, 0)
        ac.drawBackground(self.app, (bg.a > 0))
        ac.setBackgroundColor(self.app, bg.r, bg.g, bg.b)
        ac.setBackgroundOpacity(self.app, bg.a)

    def update(self):
        ac.setBackgroundColor(self.app, self.bg.r, self.bg.g, self.bg.b)
        ac.setBackgroundOpacity(self.app, self.bg.a)

    def getApp(self):
        return self.app

    def getAppName(self):
        return self.app_name


class Object:
    pos = (0, 0)
    size = (0, 0)
    obj = 0

    text = ""
    font_size = 0
    font_color = Color(1, 1, 1, 1)

    def __init__(self, parent, type, font_size=10, color=Color(1, 1, 1, 1)):
        self.parent = parent
        self.type = type
        self.font_size = font_size
        self.font_color = color

        if type == "Label":
            self.obj = ac.addLabel(parent.getApp(), self.text)

        if self.obj != 0:
            ac.setFontSize(self.obj, font_size)
            ac.setFontColor(self.obj, color.r, color.g, color.b, color.a)

    def setPosition(self, x, y):
        self.pos = (x, y)
        ac.setPosition(self.obj, x, y)

    def setSize(self, w, h):
        self.size = (w, h)
        ac.setSize(self.obj, w, h)

    def getPosition(self):
        return ac.getPosition(self.obj)

    def setText(self, text):
        if self.text != text:
            self.text = text
            ac.setText(self.obj, text)

    def setTextFormat(self, format, values):
        if self.text != format.format(values):
            self.text = format.format(values)
            ac.setText(self.obj, self.text)

    def setFontColor(self, color):
        self.font_color = color
        ac.setFontColor(self.obj, color.r, color.g, color.b, color.a)
