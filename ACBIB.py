# Assetto Corsa Basic Information Board (ACBIB)

import ac
import math
import app.acbib as acbib

# global settings

APP_WIDTH = 600
APP_HEIGHT = 170

invalid_lap = False
ratio = 1
font_huge = 70
font_big = 40
font_medium = 20
font_small = 15


def acMain(ac_version):
    global app
    global lap_count, lap_current, lap_last, lap_best, lap_delta
    global car_speed, car_gear, car_rpm, car_pos, car_fuel, car_prev, car_next
    global car_tyre_1, car_tyre_2, car_tyre_3, car_tyre_4

    app = acbib.App("ACBIB", "", APP_WIDTH, APP_HEIGHT, acbib.Color(0, 0, 0, 0.8))
    ac.addRenderCallback(app.getApp(), glRender)

    lap_count = acbib.Object(app, "Label", font_medium)
    lap_current = acbib.Object(app, "Label", font_medium)
    lap_last = acbib.Object(app, "Label", font_medium)
    lap_best = acbib.Object(app, "Label", font_medium, acbib.Color(0, 1, 0, 1))
    lap_delta = acbib.Object(app, "Label", font_medium, acbib.Color(0, 1, 0, 1))

    car_speed = acbib.Object(app, "Label", font_medium)
    car_gear = acbib.Object(app, "Label", font_huge)
    car_rpm = acbib.Object(app, "Label", font_medium)
    car_pos = acbib.Object(app, "Label", font_medium)
    car_fuel = acbib.Object(app, "Label", font_medium)
    car_prev = acbib.Object(app, "Label", font_medium, acbib.Color(1, 0, 0, 1))
    car_next = acbib.Object(app, "Label", font_medium, acbib.Color(0, 1, 0, 1))
    car_tyre_1 = acbib.Object(app, "Label", font_small)
    car_tyre_2 = acbib.Object(app, "Label", font_small)
    car_tyre_3 = acbib.Object(app, "Label", font_small)
    car_tyre_4 = acbib.Object(app, "Label", font_small)

    lap_count.setPosition(0, 0)
    car_pos.setPosition(0, 30)
    car_fuel.setPosition(0, 60)

    lap_best.setPosition(120, 0)
    lap_last.setPosition(120, 30)
    lap_current.setPosition(120, 60)

    car_gear.setPosition(265, 0)
    car_speed.setPosition(320, 20)
    car_rpm.setPosition(320, 50)

    car_prev.setPosition(10, 140)
    lap_delta.setPosition(280, 140)
    car_next.setPosition(510, 140)

    car_tyre_1.setPosition(470, 0)
    car_tyre_2.setPosition(530, 0)
    car_tyre_3.setPosition(470, 70)
    car_tyre_4.setPosition(530, 70)

    return "ACBIB"


def acUpdate(deltaT):
    global invalid_lap

    global app
    global lap_current, lap_last, lap_best, lap_count, lap_delta
    global car_speed, car_gear, car_rpm, car_pos, car_fuel, car_prev, car_next
    global car_tyre_1, car_tyre_2, car_tyre_3, car_tyre_4

    app.update()

    if acbib.ACLAP.getCurrentLapTime() <= 1000:
        invalid_lap = False

    if invalid_lap:
        lap_current.setFontColor(acbib.Color(1, 0, 0, 1))
    else:
        lap_current.setFontColor(acbib.Color(1, 1, 1, 1))

    lap_count.setText("Lap:   {}/{}".format(acbib.ACLAP.getLap(0), acbib.ACLAP.getLaps()))
    lap_current.setText("CUR: {}".format(acbib.ACLAP.getCurrentLap(0)))
    lap_last.setText("LST: {}".format(acbib.ACLAP.getLastLap(0)))
    lap_best.setText("BST: {}".format(acbib.ACLAP.getBestLap(0)))

    if acbib.ACLAP.getLapDelta() > 0:
        lap_delta.setText("+{:3.3f}".format(acbib.ACLAP.getLapDelta()))
        lap_delta.setFontColor(acbib.Color(1, 0, 0, 1))
    else:
        lap_delta.setText("{:3.3f}".format(acbib.ACLAP.getLapDelta()))
        lap_delta.setFontColor(acbib.Color(0, 1, 0, 1))

    car_prev.setText("{}".format(acbib.ACCAR.getPrevCarDiffTime(True)))
    car_next.setText("{}".format(acbib.ACCAR.getNextCarDiffTime(True)))

    car_speed.setText("{:3.0f} km/h".format(acbib.ACCAR.getSpeed(0)))
    car_gear.setText("{}".format(acbib.ACCAR.getGear(0)))
    car_rpm.setText("{:4.0f} rpm".format(acbib.ACCAR.getRPM(0)))
    car_pos.setText("Pos:   {}/{}".format(acbib.ACCAR.getPosition(0), acbib.ACRACE.getCarsCount()))
    car_fuel.setText("Fuel: {:3.0f} l".format(acbib.ACCAR.getFuel()))

    car_tyre_1.setText("{:3.1f}°C\n{:3.1f} psi\n{:3.1f}%".format(acbib.ACCAR.getTyreTemp(0, "c"),
                                                                 acbib.ACCAR.getTyrePressure(0),
                                                                 acbib.ACCAR.getTyreWear(0)))
    car_tyre_2.setText("{:3.1f}°C\n{:3.1f} psi\n{:3.1f}%".format(acbib.ACCAR.getTyreTemp(1, "c"),
                                                                 acbib.ACCAR.getTyrePressure(1),
                                                                 acbib.ACCAR.getTyreWear(1)))
    car_tyre_3.setText("{:3.1f}°C\n{:3.1f} psi\n{:3.1f}%".format(acbib.ACCAR.getTyreTemp(2, "c"),
                                                                 acbib.ACCAR.getTyrePressure(2),
                                                                 acbib.ACCAR.getTyreWear(2)))
    car_tyre_4.setText("{:3.1f}°C\n{:3.1f} psi\n{:3.1f}%".format(acbib.ACCAR.getTyreTemp(3, "c"),
                                                                 acbib.ACCAR.getTyrePressure(3),
                                                                 acbib.ACCAR.getTyreWear(3)))
    
    st = ""
    for i in acbib.ACCAR.getCarDamage():
        st = st + str(i) + " "
    ac.console(st)


def glRender(deltaT):
    # delta

    acbib.GL.rect(APP_WIDTH / 2 - 100, 120, 200, 10, acbib.Color(1, 1, 1, 1), False)
    acbib.GL.line(APP_WIDTH / 2, 120, APP_WIDTH / 2, 130, acbib.Color(1, 1, 1, 1))

    delta = acbib.ACLAP.getLapDelta()
    d = 0
    if delta != 0:
        d = max(abs(delta), 10 * math.log10(abs(delta))) * 10

    if delta > 0:
        acbib.GL.rect(APP_WIDTH / 2 - (min(d, 99) + 1), 120, min(d, 99), 9, acbib.Color(0.9, 0, 0, 1))
    elif delta < 0:
        acbib.GL.rect(APP_WIDTH / 2, 120, min(d, 99), 9, acbib.Color(0, 0.9, 0, 1))

    # shifting

    rpm_max = acbib.ACCAR.getRPMMax()
    rpm = acbib.ACCAR.getRPM()
    progress = rpm / rpm_max
    offset = rpm_max * 0.8 / rpm_max
    shift_min = 0.9
    shift_max = 0.95
    cube_len = int(APP_WIDTH / 40)

    # shift steering wheel lights
    if progress > offset:
        for i in range(min(10, int((progress - offset) / (1 - offset) * 10))):
            if i < 2:
                acbib.GL.rect(i * int(APP_WIDTH / 10) + (cube_len / 2), -cube_len, int(APP_WIDTH / 10) - cube_len,
                              cube_len, acbib.Color(0, 0.9, 0, 1))
            elif i < 7:
                acbib.GL.rect(i * int(APP_WIDTH / 10) + (cube_len / 2), -cube_len, int(APP_WIDTH / 10) - cube_len,
                              cube_len, acbib.Color(1, 1, 0, 1))
            else:
                acbib.GL.rect(i * int(APP_WIDTH / 10) + (cube_len / 2), -cube_len, int(APP_WIDTH / 10) - cube_len,
                              cube_len, acbib.Color(0, 0.2, 0.9, 1))

    # shift progress background
    acbib.GL.rect(0, APP_HEIGHT, APP_WIDTH, 6, acbib.Color(0.6, 0.6, 0.6, 1))

    # shift progress indicator
    if acbib.ACCAR.getRPM() < acbib.ACCAR.getRPMMax() * shift_min:
        acbib.GL.rect(0, APP_HEIGHT, progress * APP_WIDTH, 6, acbib.Color(0, 0.9, 0, 1.0))
    elif acbib.ACCAR.getRPMMax() * shift_min <= acbib.ACCAR.getRPM() <= acbib.ACCAR.getRPMMax() * shift_max:
        acbib.GL.rect(0, APP_HEIGHT, progress * APP_WIDTH, 6, acbib.Color(0.9, 0.9, 0, 1.0))
        acbib.GL.rect(-10, 0, 10, APP_HEIGHT + 6, acbib.Color(0.9, 0.9, 0, 1.0))
        acbib.GL.rect(APP_WIDTH, 0, 10, APP_HEIGHT + 6, acbib.Color(0.9, 0.9, 0, 1.0))
    elif acbib.ACCAR.getRPM() > acbib.ACCAR.getRPMMax() * shift_max:
        acbib.GL.rect(0, APP_HEIGHT, progress * APP_WIDTH, 6, acbib.Color(0.9, 0, 0, 1.0))
        
    # track progress
    track_progress = acbib.ACCAR.getLocation()
    
    if track_progress > 0:
        acbib.GL.rect(0, APP_HEIGHT + 6, track_progress * APP_WIDTH, 6, acbib.Color(0, 0.5, 0.9, 1))


def acShutdown():
    l = 1
