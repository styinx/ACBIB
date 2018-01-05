# Assetto Corsa Basic Information Board (ACBIB)

import app.acbib as acbib


# global settings

ratio = 1
font_huge = 50
font_big = 30
font_medium = 20
font_small = 10


# each element as class

# class Laps:
#     def __init__(self, parent):
#         self.best_label = acbib.Object(parent, "Label", "Best: {}", font_medium)
#         self.current_label = acbib.Object(parent, "Label", "Current: {}", font_medium)


def acMain(ac_version):
    global app
    global lap_count, lap_current, lap_last, lap_best, lap_pbest
    global car_speed, car_gear, car_rpm, car_pos, car_fuel
    global car_tyre_1, car_tyre_2, car_tyre_3, car_tyre_4

    app = acbib.App("ACBIB", "", 550, 100, acbib.Color(0.2, 0.2, 0.2, 0.9))

    lap_count = acbib.Object(app, "Label", font_medium)
    lap_current = acbib.Object(app, "Label", font_medium)
    lap_best = acbib.Object(app, "Label", font_medium, acbib.Color(0, 1, 0, 1))

    car_speed = acbib.Object(app, "Label", font_medium)
    car_gear = acbib.Object(app, "Label", font_huge)
    car_rpm = acbib.Object(app, "Label", font_medium)
    car_pos = acbib.Object(app, "Label", font_medium)
    car_fuel = acbib.Object(app, "Label", font_medium)
    car_tyre_1 = acbib.Object(app, "Label", font_small)
    car_tyre_2 = acbib.Object(app, "Label", font_small)
    car_tyre_3 = acbib.Object(app, "Label", font_small)
    car_tyre_4 = acbib.Object(app, "Label", font_small)

    lap_count.setPosition(0, 0)
    lap_best.setPosition(120, 0)

    car_pos.setPosition(0, 30)
    lap_current.setPosition(120, 30)

    car_fuel.setPosition(0, 60)

    car_gear.setPosition(260, 10)
    car_speed.setPosition(300, 10)
    car_rpm.setPosition(300, 40)

    car_tyre_1.setPosition(400, 0)
    car_tyre_2.setPosition(480, 0)
    car_tyre_3.setPosition(400, 50)
    car_tyre_4.setPosition(480, 50)

    return "ACBIB"


def acUpdate(deltaT):
    global app
    global lap_current, lap_last, lap_best, lap_pbest, lap_count
    global car_speed, car_gear, car_rpm, car_pos, car_fuel
    global car_tyre_1, car_tyre_2, car_tyre_3, car_tyre_4

    app.update()

    lap_count.setText("Lap: {}".format(acbib.ACLAP.getLap(0)))
    lap_current.setText("CLP: {}".format(acbib.ACLAP.getCurrentLap(0)))
    lap_best.setText("BLP: {}".format(acbib.ACLAP.getBestLap(0)))

    car_speed.setText("{:3.0f} km/h".format(acbib.ACCAR.getSpeed(0)))
    car_gear.setText("{}".format(acbib.ACCAR.getGear(0)))
    car_rpm.setText("{:4.0f} rpm".format(acbib.ACCAR.getRPM(0)))
    car_pos.setText("Pos: {}/{}".format(acbib.ACCAR.getPosition(0), acbib.ACCAR.getCarsCount()))
    car_fuel.setText("Fuel: {:3.0f} l".format(acbib.ACCAR.getFuel()))

    car_tyre_1.setText("{:3.1f}°C/{:3.1f}°C\n{:3.1f} psi\n{:3.1f}%".format(acbib.ACCAR.getTyreTemp(0),
                                                                           acbib.ACCAR.getTyreCoreTemp(0),
                                                                           acbib.ACCAR.getTyrePressure(0),
                                                                           acbib.ACCAR.getTyreWear(0)))
    car_tyre_2.setText("{:3.1f}°C/{:3.1f}°C\n{:3.1f} psi\n{:3.1f}%".format(acbib.ACCAR.getTyreTemp(1),
                                                                           acbib.ACCAR.getTyreCoreTemp(1),
                                                                           acbib.ACCAR.getTyrePressure(1),
                                                                           acbib.ACCAR.getTyreWear(1)))
    car_tyre_3.setText("{:3.1f}°C/{:3.1f}°C\n{:3.1f} psi\n{:3.1f}%".format(acbib.ACCAR.getTyreTemp(2),
                                                                           acbib.ACCAR.getTyreCoreTemp(2),
                                                                           acbib.ACCAR.getTyrePressure(2),
                                                                           acbib.ACCAR.getTyreWear(2)))
    car_tyre_4.setText("{:3.1f}°C/{:3.1f}°C\n{:3.1f} psi\n{:3.1f}%".format(acbib.ACCAR.getTyreTemp(3),
                                                                           acbib.ACCAR.getTyreCoreTemp(3),
                                                                           acbib.ACCAR.getTyrePressure(3),
                                                                           acbib.ACCAR.getTyreWear(3)))


def acShutdown():
    l = 1