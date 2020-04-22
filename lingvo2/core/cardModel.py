import pickle
from collections import UserList
from PyQt5.QtCore import pyqtSignal, QObject

class PConfig:
    def __init__(self, path):
        self.path = path
        self.__data = {}

    def load(self):
        with open(self.path, 'rb') as f:
            self.__data = pickle.load(f)
        return self.__data

    def save(self, data):
        self.__data = data
        with open(self.path, 'wb') as f:
            pickle.dump(self.__data, f)

    @property
    def data(self):
        return self.__data

class DragItemStyle:
    def __init__(self, font, color, color_bg, **kwargs):
        self.color_bg = color_bg
        self.color = color
        self.font = font


class DragItem:
    def __init__(self, qwidgetType, text=None, style=None, **kwargs):
        """
        объект который вставляют

        :param qwidgetType:
        :param text:
        :param style:
        :param kwargs:
        """
        self.qwidgetType = qwidgetType
        self.text = text
        self.style = style

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, self.qwidgetType)

class DropBox(UserList):
    def __init__(self, name, **kwargs):
        """
        макет куда вставляют
        :param name:
        :param kwargs:
        """
        super().__init__()
        self.name = name

    def __repr__(self):
        return "{}:{}".format(self.__class__.__name__, self.name)

class Side(UserList):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return str(self.name)

class CardModel(QObject):
    USideFront = "front"
    USideBack = "back"
    USectionTop = "top"
    USectionCenter = "center"
    USectionBottom = "bottom"

    updateSignal = pyqtSignal()
    def __init__(self, content_path):
        """
        модель карточки имеет две стороны front и back
        :param card_cfg:
        """

        super().__init__()

        self.contentCfg = PConfig(content_path)
        self.content = self.contentCfg.load()

        self.front = self.content["front"]
        self.back = self.content["back"]
        self.sides = {"front": self.front, "back": self.back}


    def insertItem(self, side, i_section, dragItem):
        self.sides[side][i_section].append(dragItem)

    def appendSection(self, side, section):
        self.sides[side].append(section)

    def setSections(self, side, sections_list):
        self.sides[side].extend(sections_list)

    def __repr__(self):
        return str(self.sides)

    def saveContent(self):
        self.contentCfg.save(self.sides)


def save():
    f_sections = [DropBox(s) for s in ["top", "center", "bottom"]]
    b_sections = [DropBox(s) for s in ["top", "center", "bottom"]]
    contents = dict(front=f_sections, back=b_sections)
    cfg = PConfig(paths.PICKLE_CONFIG)
    cfg.save(contents)


def load():
    card = CardModel(paths.PICKLE_CONFIG)
    print(card.front)
    print(card.back)


if __name__ == '__main__':
    import paths
    # save()


    load()
    # card.saveContent()
    # sections = [DropBox(s) for s in ["top", "center", "bottom"]]
    # card.setSections(CardModel.USideFront, sections)
    # card.insertItem(CardModel.USideFront, 1, DragItem("QLabel"))

    # print(card.front)
    # print(card.back)
    # # card.update()

    #
    # for c in contents.values():
    #     print(c)



    # SAVE ---------------------------------------------------------

    # # cfg.load()
    # # print(cfg.data)


