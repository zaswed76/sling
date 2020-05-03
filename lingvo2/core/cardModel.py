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


class DropItem:
    def __init__(self, idO, qwidgetType, text=None, style=None, **kwargs):
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
        self.soundBtn = kwargs.get("soundBtn", False)
        self.idO = idO



    def __repr__(self):
        return "{}-{}".format("DropItem", self.idO)

class DropBox(UserList):
    def __init__(self, name, **kwargs):
        """
        макет куда вставляют
        :param name:
        :param kwargs:
        """
        super().__init__()
        self.name = name

    def appendDragItem(self, idO, item, **args):
        text = args.get("text")
        soundBtn = args.get("soundBtn", False)
        self.append(DropItem(idO, item, text=text, soundBtn=soundBtn))

    def removeDragItem(self, idO, **args):
        for i in self:
            if idO == i.idO:
                self.remove(i)



    def __repr__(self):
        return "{}:{}".format(self.__class__.__name__, self.__dict__)

class Side(UserList):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return self.name

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
        self._sides = {"front": self.front, "back": self.back}
        self.soundBtnDefault = True

    @property
    def sides(self):
        return self._sides

    def insertItem(self, side, i_section, dragItem):
        self._sides[side][i_section].append(dragItem)

    def removeItemToIdO(self, side, i_section, dragItemidO):
        # print(side, i_section, dragItemidO)
        self._sides[side][i_section].removeDragItem(dragItemidO)

    def appendSection(self, side, section):
        self._sides[side].append(section)

    def setSections(self, side, sections_list):
        self._sides[side].extend(sections_list)

    def __repr__(self):
        return str(self._sides)

    def saveContent(self):
        self.contentCfg.save(self._sides)


def save():
    f_sections = [DropBox(s) for s in ["top", "center", "bottom"]]
    f_sections[1].appendDragItem("DropLabel", text="Word")
    f_sections[1].appendDragItem("DropLabel", text="Word")
    b_sections = [DropBox(s) for s in ["top", "center", "bottom"]]
    contents = dict(front=f_sections, back=b_sections)
    cfg = PConfig(paths.PICKLE_CONFIG)
    cfg.save(contents)


def load():
    card = CardModel(paths.PICKLE_CONFIG)
    # print(card.front)
    # print(card.back)


if __name__ == '__main__':
    import paths
    save()


    # load()
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


