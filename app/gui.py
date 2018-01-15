import ac


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
# All visualized object inherit this class
'''


class Object:
    def __init__(self, parent):
        self.ac_obj = 0
        self._parent = parent
        self._child = None
        self._callback = None
        self._pos = (0, 0)
        self._size = (0, 0)
        self._visible = True
        self._text = ""
        self._font_size = 10
        self._font_ratio = 0.5
        self._font_color = Color(1, 1, 1, 1)
        self._background_texture = 0
        self._background_color = Color(0, 0, 0, 0)
        self._border = False
        self._border_color = Color(0, 0, 0, 0)

        if self._parent is not None:
            self._parent.child = self
            self.pos = self._parent.pos
            self.size = self._parent.size

        if self.ac_obj is not None:
            ac.setPosition(self.ac_obj, self._pos[0], self._pos[1])

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        _x, _y = pos
        if isinstance(_x, int) and isinstance(_y, int):
            if self._parent is not None:
                if not (self._parent.pos[0] <= _x <= self._parent.pos[0] + self._parent.size[0]):
                    _x = self._parent.pos[0]
                if not (self._parent.pos[1] <= _y <= self._parent.pos[1] + self._parent.size[1]):
                    _y = self._parent.pos[1]
            self._pos = (_x, _y)

            if self.ac_obj != 0:
                ac.setPosition(self.ac_obj, _x, _y)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        _w, _h = size
        if isinstance(_w, int) and isinstance(_h, int):
            if self._parent is not None:
                if not (self._pos[0] + _w <= self._parent.size[0] and self._pos[1] + _h <= self._parent.size[1]):
                    _w = self._parent.size[0]
                    _h = self._parent.size[1]
                self._size = (_w, _h)
                self._font_size = min(self.getFontSizeFromText(), _h)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        if isinstance(visible, bool):
            self._visible = visible
            ac.setVisible(visible)

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        if isinstance(font_size, int):
            self._font_size = min(int(font_size), self._size[1])
            ac.setFontSize(self.ac_obj, self._font_size)

    @property
    def font_ratio(self):
        return self._font_ratio

    @font_ratio.setter
    def font_ratio(self, font_ratio):
        if isinstance(font_ratio, int):
            self._font_ratio = min(int(font_ratio), self._size[1])
            ac.setFontSize(self.ac_obj, self._font_size)

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, font_color):
        if isinstance(font_color, Color):
            self._font_color = font_color

        if self.ac_obj is not None:
            ac.setFontColor(self.ac_obj, self.font_color.r, self.font_color.g, self.font_color.b, self.font_color.a)

    def setFontColor(self, font_color):
        self.font_color = font_color

    @property
    def background_texture(self):
        return self._background_texture

    @background_texture.setter
    def background_texture(self, tex):
        if isinstance(tex, str):
            self._background_texture = ac.newTexture(tex)
        else:
            self._background_texture = tex

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        if isinstance(background_color, Color):
            self._background_color = background_color

    @property
    def border(self):
        return self._border

    @border.setter
    def border(self, border):
        if isinstance(border, bool):
            self._border = border

    @property
    def border_color(self):
        return self._border_color

    @border_color.setter
    def border_color(self, border_color):
        if isinstance(border_color, Color):
            self._border_color = border_color

    def setRenderCallback(self, callback):
        self._callback = callback
        ac.addRenderCallback(self.ac_obj, callback)

    def setText(self, text):
        self._text = text
        if self.ac_obj is not None:
            ac.setText(self.ac_obj, text)

    def setTextAlignment(self, alignment="center"):
        if self.ac_obj is not None:
            if alignment == "center" or alignment == "c":
                self.pos = (self.pos[0] + self.size[0] / 2, self.pos[1])
            if alignment == "right" or alignment == "r":
                self.pos = (self.pos[0] + self.size[0], self.pos[1])
            ac.setFontAlignment(self.ac_obj, alignment)

    '''
    # Calculates and returns the text width either of the given text or the saved
    # text in the object
    '''
    def getTextWidth(self, text):
        if text != "":
            return len(text) * (self._font_size * self._font_ratio)
        else:
            return len(self._text) * (self._font_size * self._font_ratio)

    '''
    # Calculates and returns the ideal font size depending on the maximum width of the object
    '''
    def getFontSizeFromText(self):
        return self._size[0] / max(1, len(self._text)) * (1 + self._font_ratio)

    '''
    # Update method
    # updates the object, manages size, position, text, ...
    '''
    def update(self):
        i = 0

    def show(self):
        if self.ac_obj is not None:
            ac.setVisible(self.ac_obj, True)

    def hide(self):
        if self.ac_obj is not None:
            ac.setVisible(self.ac_obj, False)

    '''
    # Render method
    # should only be called from the render update function
    '''
    def render(self):
        if self._visible:
            GL.rect(self._pos[0], self._pos[1], self._size[0], self._size[1])

        if self._child is not None:
            self._child.render()


'''
# Wrapper class for the main app
'''


class App(Object):
    def __init__(self, app_name, app_title, w, h, bg=Color(0, 0, 0, 0.8)):
        super().__init__(None)
        self._app_name = app_name
        self._app_title = app_title
        self._w = w
        self._h = h
        self._bg = bg
        self._size = (w, h)

        self.app = ac.newApp(app_name)
        self.ac_obj = self.app
        ac.setTitle(self.app, app_title)
        ac.setSize(self.app, w, h)
        ac.setIconPosition(self.app, 100000, 0)
        ac.setTitlePosition(self.app, 100000, 0)
        ac.drawBorder(self.app, 0)
        ac.drawBackground(self.app, (bg.a > 0))
        ac.setBackgroundColor(self.app, bg.r, bg.g, bg.b)
        ac.setBackgroundOpacity(self.app, bg.a)

    def render(self):
        ac.setBackgroundColor(self.app, self._bg.r, self._bg.g, self._bg.b)
        ac.setBackgroundOpacity(self.app, self._bg.a)


'''
# A layout container to arrange objects in a linear order (horizontal or vertical)
'''


class Box(Object):
    def __init__(self, parent, orientation=0):
        super().__init__(parent)

        self._orientation = orientation
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)
        self.update()

    def update(self):
        for obj in self.objects:
            if self._orientation == 0 or self._orientation == "h" or self._orientation == "horizontal":
                obj.size = (self._size[0] / len(self.objects), self._size[1])
            elif self._orientation == 1 or self._orientation == "v" or self._orientation == "vertical":
                obj.size = (self._size[0], self._size[1] / len(self.objects))
            obj.update()


class Grid(Object):
    def __init__(self, parent, cols, rows):
        super().__init__(parent)

        self._objects = [[0] * cols] * rows
        self._cols = max(1, cols)
        self._rows = max(1, rows)
        self._cell_width = self._size[0] / self._cols
        self._cell_height = self._size[1] / self._rows

    def add(self, obj, x, y, w=1, h=1, alignment="c"):
        if isinstance(obj, Object):
            if 1 <= x <= self._cols and 1 <= y <= self._rows:
                #self._objects[x][y] = obj
                obj.pos = ((x-1) * self._cell_width, (y-1) * self._cell_height)
                obj.size = (self._cell_width * w, self._cell_height * h)
                obj.setTextAlignment(alignment)
                ac.setPosition(obj.ac_obj, obj.pos[0], obj.pos[1])

    def update(self):
        self._cell_width = self._size[0] / self._cols
        self._cell_height = self._size[1] / self._rows


class Label(Object):
    def __init__(self, parent, app_win, text=""):
        super().__init__(parent)

        self.ac_obj = ac.addLabel(app_win.app, text)
        self._text = text


class Button(Object):
    def __init__(self, parent, app_win, text=""):
        super().__init__(parent)

        self.ac_obj = ac.addButton(app_win.app, text)
        self._text = text
        self._callback = None

    def onClick(self, callback):
        self._callback = callback
        ac.addOnClickedListener(self.ac_obj, callback)


class ProgressBar(Object):
    def __init__(self, parent, orientation=0, progress_range=(0, 100), progress=0):
        super().__init__(parent)

        self._orientation = orientation
        self._progress_range = progress_range
        self._progress = progress
        self._label_shown = True
        self._value_label = str(progress)
        self._border = True
        self._border_color = Color(1, 1, 1, 1)
        self._progress_color = Color(0, 0.5, 0.8, 1)

    @property
    def progress_range(self):
        return self._progress_range

    @progress_range.setter
    def progress_range(self, p_range):
        p_min, p_max = p_range
        if isinstance(p_min, int) and isinstance(p_max, int):
            self._progress_range = (p_min, p_max)

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, progress):
        if self._progress_range[0] <= progress <= self._progress_range[1]:
            self._progress = progress

    def render(self):
        Object.render(self)

        GL.rect(self._pos[0], self._pos[1], self._progress, self._size[1], self._background_color, True)
        GL.rect(self._pos[0], self._pos[1], self._size[0], self._size[1], self._border_color, False)
