import ac
import acbib


APP = ac.newApp("appname")


class Color:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a


'''
# Wrapper class for gl primitives
'''


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


'''
# Wrapper class for the main app
'''


class App:
    def __init__(self, app_name, app_title, w, h, bg=Color(0, 0, 0, 0.8)):
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

    def render(self):
        ac.setBackgroundColor(self.app, self.bg.r, self.bg.g, self.bg.b)
        ac.setBackgroundOpacity(self.app, self.bg.a)


'''
# All visualized object inherit this class
'''


class Object:
    def __init__(self, parent=None):
        self.ac_obj = None
        self.parent = parent
        self.pos = (0, 0)
        self.size = (0, 0)
        self.visible = True
        self.text = ""
        self.font_size = 10
        self.font_ratio = .5
        self.font_color = Color(1, 1, 1, 1)
        self.background_texture = None
        self.background_color = Color(0, 0, 0, 0)
        self.border = False
        self.border_color = Color(0, 0, 0, 0)

        if parent is not None:
            self.pos = parent.pos
            self.size = parent.size

    @property
    def pos(self):
        return self.pos

    @pos.setter
    def pos(self, (x, y)):
        if isinstance(x, int) and isinstance(y, int):
            if self.parent is not None:
                if x >= self.parent.pos[0] and y >= self.parent.pos[1]:
                    self.pos = (x, y)
            else:
                self.pos = (x, y)

    @property
    def size(self):
        return self.size

    @size.setter
    def size(self, (w, h)):
        if isinstance(w, int) and isinstance(h, int):
            if self.parent is not None:
                if self.pos[0] + w <= self.parent.size[0] and self.pos[1] + h <= self.parent.size[1]:
                    self.size = (w, h)
                    self.font_size = min(self.getFontSizeFromText(), h)
            else:
                self.size = (w, h)
                self.font_size = min(self.getFontSizeFromText(), h)

    @property
    def visible(self):
        return self.visible

    @visible.setter
    def visible(self, visible):
        if isinstance(visible, bool):
            self.visible = visible
            ac.setVisible(visible)

    @property
    def font_size(self):
        return self.font_size

    @font_size.setter
    def font_size(self, font_size):
        if isinstance(font_size, int):
            self.font_size = min(font_size, self.size[1])
            ac.setFontSize(self.ac_obj, self.font_size)

    @property
    def font_ratio(self):
        return self.font_ratio

    @font_ratio.setter
    def font_ratio(self, font_ratio):
        if isinstance(font_ratio, int):
            self.font_ratio = min(font_ratio, self.size[1])
            ac.setFontSize(self.ac_obj, self.font_size)

    @property
    def font_color(self):
        return self.font_color

    @font_color.setter
    def font_color(self, font_color):
        if isinstance(font_color, Color):
            self.font_color = font_color

    @property
    def background_texture(self):
        return self.background_texture

    @background_texture.setter
    def background_texture(self, tex):
        if isinstance(tex, str):
            self.background_texture = ac.newTexture(tex)
        else:
            self.background_texture = tex

    @property
    def background_color(self):
        return self.background_color

    @background_color.setter
    def background_color(self, background_color):
        if isinstance(background_color, Color):
            self.background_color = background_color

    @property
    def border(self):
        return self.border

    @border.setter
    def border(self, border):
        if isinstance(border, bool):
            self.border = border

    @property
    def border_color(self):
        return self.border_color

    @border_color.setter
    def border_color(self, border_color):
        if isinstance(border_color, Color):
            self.border_color = border_color

    def getTextWidth(self):
        return len(self.text) * (self.font_size * self.font_ratio)

    def getFontSizeFromText(self):
        return self.size[0] / len(self.text) * (1 + self.font_ratio)

    '''
    # Update method
    # updates the object, manages size, position, text, ...
    '''
    def update(self):
        i = 0

    '''
    # Render method
    # should only be called from the render update function
    '''
    def render(self):
        if self.visible:
            GL.rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


'''
# A layout container to arrange objects in a linear order (horizontal or vertical)
'''


class Box(Object):
    def __init__(self, parent, orientation=0):
        Object.__init__(parent)

        self.orientation = orientation
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)
        self.update()

    def update(self):
        for obj in self.objects:
            if self.orientation == 0 or self.orientation == "h" or self.orientation == "horizontal":
                obj.size = (self.size[0] / len(self.objects), self.size[1])
            elif self.orientation == 1 or self.orientation == "v" or self.orientation == "vertical":
                obj.size = (self.size[0], self.size[1] / len(self.objects))
            obj.update()


class Grid(Object):
    def __init__(self, parent, cols, rows):
        Object.__init__(parent)

        self.objects = [[] * cols] * rows
        self.cols = cols
        self.rows = rows
        self.cell_width = self.size[0] / self.cols
        self.cell_height = self.size[1] / self.rows

    def add(self, obj, x, y, w=1, h=1):
        if isinstance(obj, Object):
            self.objects[x][y] = obj
            if obj.size[0] > self.cell_width:
                obj.size[0] = self.cell_width
            if obj.size[1] > self.cell_height:
                obj.size[1] = self.cell_height

    def update(self):
        self.cell_width = self.size[0] / self.cols
        self.cell_height = self.size[1] / self.rows


class Label(Object):
    def __init__(self, parent, text=""):
        Object.__init__(parent)

        self.ac_obj = ac.addLabel(APP, text)
        self.text = text


class Button(Object):
    def __init__(self, parent, text=""):
        Object.__init__(parent)

        ac.addButton(self.ac_obj, text)
        self.text = text
        self.callback = None

    def onClick(self, callback):
        self.callback = callback
        ac.addOnClickedListener(self.ac_obj, callback)


class ProgressBar(Object):
    def __index__(self, parent, progress_range=(0, 100), progress=0):
        Object.__init__(parent)

        self.progress_range = progress_range
        self.progress = progress
        self.label_shown = True
        self.value_label = str(progress)
        self.border = True
        self.border_color = Color(1, 1, 1, 1)
        self.progress_color = Color(0, 0.5, 0.8, 1)

    @property
    def progress_range(self):
        return self.progress_range

    @progress_range.setter
    def progress_range(self, (p_min, p_max)):
        if isinstance(p_min, int) and isinstance(p_max, int):
            self.progress_range = (p_min, p_max)

    @property
    def progress(self):
        return self.progress

    @progress.setter
    def progress(self, progress):
        if self.progress_range[0] <= progress <= self.progress_range[1]:
            self.progress = progress

    def render(self):
        GL.rect(self.pos[0], self.pos[1], self.progress, self.size[1], self.background_color, True)
        GL.rect(self.pos[0], self.pos[1], self.size[0], self.size[1], self.border_color, False)
