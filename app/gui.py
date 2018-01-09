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
# All visualized object inherit this class
'''


class Object:
    def __init__(self, parent=None):
        self.ac_obj = None
        self.parent = parent
        self.pos = (0, 0)
        self.size = (0, 0)
        self.text = ""
        self.font_size = 0
        self.font_color = Color(1, 1, 1, 1)
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
    def pos(self, x, y):
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
    def size(self, w, h):
        if isinstance(w, int) and isinstance(h, int):
            if self.parent is not None:
                if self.pos[0] + w <= self.parent.size[0] and self.pos[1] + h <= self.parent.size[1]:
                    self.size = (w, h)
                    self.font_size = min(self.font_size, h)
            else:
                self.size = (w, h)
                self.font_size = min(self.font_size, h)

    @property
    def font_size(self):
        return self.font_size

    @font_size.setter
    def font_size(self, font_size):
        if isinstance(font_size, int):
            self.font_size = min(font_size, self.size[1])
            ac.setFontSize(self.ac_obj, self.font_size)

    @property
    def font_color(self):
        return self.font_color

    @font_color.setter
    def font_color(self, font_color):
        if isinstance(font_color, Color):
            self.font_color = font_color

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
        acbib.GL.rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


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
        acbib.GL.rect(self.pos[0], self.pos[1], self.progress, self.size[1], self.background_color, True)
        acbib.GL.rect(self.pos[0], self.pos[1], self.size[0], self.size[1], self.border_color, False)
