import ac
import app.gui as gui
import app.settings as settings


def acMain():
    global app

    app_settings = settings.Settings("config.ini")

    app = gui.APP("", "", app_settings["Display"]["APP_WIDTH"], app_settings["Display"]["APP_HEIGHT"])
    ac.addRenderCallback(app, render)

    grid = gui.Grid(app, 5, 5)
    button1 = gui.Button(None, "text1")
    button2 = gui.Button(None, "text2")

    grid.add(button1, 1, 1)
    grid.add(button2, 1, 1)


def acUpdate(delta):
    i = 0


def render(delta):
    global app

    app.render()


def acShutdown():
    i = 0


