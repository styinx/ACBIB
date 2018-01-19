# Assetto Corsa Basic Information Board (ACBIB)

import ac
import math
try:
    import app.acbib as acbib
    import app.gui as gui
except:
    ac.console("error importing gui")

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
    global lap_count, lap_current, lap_last, lap_best, lap_delta, lap_diff
    global car_speed, car_gear, car_rpm, car_pos, car_fuel, car_prev, car_next
    global car_tyre_1, car_tyre_2, car_tyre_3, car_tyre_4

    try:
        app = gui.App("ACBIB", "", APP_WIDTH, APP_HEIGHT, gui.Color(0, 0, 0, 0.8))
        app.setRenderCallback(glRender)

        grid = gui.Grid(app, 5, 5)
        #ac.console("{}{}".format(self.pos[0], self.pos[1]))

        lap_count = gui.Label(None, app)
        car_pos = gui.Label(None, app)
        car_fuel = gui.Label(None, app)

        lap_best = gui.Label(None, app)
        lap_last = gui.Label(None, app)
        lap_current = gui.Label(None, app)

        car_prev = gui.Label(None, app, "", gui.Color(1, 0, 0, 1))
        lap_diff = gui.DiffBar(None, app, True)
        car_next = gui.Label(None, app, "", gui.Color(0, 1, 0, 1))

        car_speed = gui.Label(None, app)
        car_gear = gui.Label(None, app)
        car_rpm = gui.Label(None, app)

        car_tyre_1 = gui.Label(None, app)
        car_tyre_2 = gui.Label(None, app)
        car_tyre_3 = gui.Label(None, app)
        car_tyre_4 = gui.Label(None, app)

        grid.add(lap_count, 0, 0)
        grid.add(car_pos, 0, 1)
        grid.add(car_fuel, 0, 2)

        grid.add(lap_best, 1, 0)
        grid.add(lap_last, 1, 1)
        grid.add(lap_current, 1, 2)

        grid.add(car_prev, 0, 4)
        grid.add(lap_diff, 2, 3)
        grid.add(car_next, 4, 4)

        grid.add(car_speed, 2, 0)
        grid.add(car_gear, 2, 1)
        grid.add(car_rpm, 2, 2)

        grid.add(car_tyre_1, 3, 0, 1, 2)
        grid.add(car_tyre_2, 4, 0, 1, 2)
        grid.add(car_tyre_3, 3, 2, 1, 2)
        grid.add(car_tyre_4, 4, 2, 1, 2)

    except TypeError:
        ac.console(" ACBIB: Error while initializing.")

    return "ACBIB"


def acUpdate(deltaT):
    global app
    global lap_current, lap_last, lap_best, lap_count, lap_delta, lap_diff
    global car_speed, car_gear, car_rpm, car_pos, car_fuel, car_prev, car_next
    global car_tyre_1, car_tyre_2, car_tyre_3, car_tyre_4

    app.update()

    lap_count.setText("Lap: {}/{}".format(acbib.ACLAP.getLap(0), acbib.ACLAP.getLaps()))
    car_pos.setText("Pos: {}/{}".format(acbib.ACCAR.getPosition(0), acbib.ACSESSION.getCarsCount()))
    car_fuel.setText("Fuel: {:3.0f} l".format(acbib.ACCAR.getFuel()))

    lap_current.setText("CUR: {}".format(acbib.ACLAP.getCurrentLap(0)))
    lap_last.setText("LST: {}".format(acbib.ACLAP.getLastLap(0)))
    lap_best.setText("BST: {}".format(acbib.ACLAP.getBestLap(0)))

    car_prev.setText("{}".format(acbib.ACCAR.getPrevCarDiffTime(True)))
    car_next.setText("{}".format(acbib.ACCAR.getNextCarDiffTime(True)))

    car_speed.setText("{:3.0f} km/h".format(acbib.ACCAR.getSpeed(0)))
    car_gear.setText("{}".format(acbib.ACCAR.getGear(0)))
    car_rpm.setText("{:4.0f} rpm".format(acbib.ACCAR.getRPM(0)))

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


def glRender(deltaT):
    global app
    global lap_diff

    app.render()
    lap_diff.render()


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
                gui.GL.rect(i * int(APP_WIDTH / 10) + (cube_len / 2), -cube_len, int(APP_WIDTH / 10) - cube_len,
                            cube_len, gui.Color(0, 0.9, 0, 1))
            elif i < 7:
                gui.GL.rect(i * int(APP_WIDTH / 10) + (cube_len / 2), -cube_len, int(APP_WIDTH / 10) - cube_len,
                            cube_len, gui.Color(1, 1, 0, 1))
            else:
                gui.GL.rect(i * int(APP_WIDTH / 10) + (cube_len / 2), -cube_len, int(APP_WIDTH / 10) - cube_len,
                            cube_len, gui.Color(0, 0.2, 0.9, 1))

    # shift progress background
    gui.GL.rect(0, APP_HEIGHT, APP_WIDTH, 6, gui.Color(0.6, 0.6, 0.6, 1))

    # shift progress indicator
    if acbib.ACCAR.getRPM() < acbib.ACCAR.getRPMMax() * shift_min:
        gui.GL.rect(0, APP_HEIGHT, progress * APP_WIDTH, 6, gui.Color(0, 0.9, 0, 1.0))
    elif acbib.ACCAR.getRPMMax() * shift_min <= acbib.ACCAR.getRPM() <= acbib.ACCAR.getRPMMax() * shift_max:
        gui.GL.rect(0, APP_HEIGHT, progress * APP_WIDTH, 6, gui.Color(0.9, 0.9, 0, 1.0))
        gui.GL.rect(-10, 0, 10, APP_HEIGHT + 6, gui.Color(0.9, 0.9, 0, 1.0))
        gui.GL.rect(APP_WIDTH, 0, 10, APP_HEIGHT + 6, gui.Color(0.9, 0.9, 0, 1.0))
    elif acbib.ACCAR.getRPM() > acbib.ACCAR.getRPMMax() * shift_max:
        gui.GL.rect(0, APP_HEIGHT, progress * APP_WIDTH, 6, gui.Color(0.9, 0, 0, 1.0))

    # track progress
    track_progress = acbib.ACCAR.getLocation()

    if track_progress > 0:
        gui.GL.rect(0, APP_HEIGHT + 6, track_progress * APP_WIDTH, 6, gui.Color(0, 0.5, 0.9, 1))


def acShutdown():
    l = 1
