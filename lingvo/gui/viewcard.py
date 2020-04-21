import datetime
import random
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paths

from gui.custom import customwidgets

class DropLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)


    def __repr__(self):
        return "DropLabel"

    def setExamles(self, examles):
        self.setText(examles)


class Section(QFrame):
    def __init__(self, parent, name, side, config, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.cfg = config
        self.box = customwidgets.BoxLayout(QBoxLayout.TopToBottom, self)
        self.labels = {}
        self.setObjectName("{}".format(name))


        shadow = QGraphicsDropShadowEffect(blurRadius=12, xOffset=3, yOffset=3)
        self.setGraphicsEffect(shadow)

        sfile = str(paths.CSS / self.cfg["currentStyle"] / "{}_card.css".format(side))
        style = open(sfile, "r").read()
        self.setStyleSheet(style)

    def clear(self):

        for n, i in self.labels.items():
            # Todo тут какойто пипец
            try:
                 self.box.removeWidget(i)
                 self.labels[n].deleteLater()
            except RuntimeError:
                pass



    def getWidgets(self):
        w = []
        for i in range(self.box.count()):
            w.append(self.box.itemAt(i).widget())
        return w
    @property
    def typeTegs(self):
        return {"DropLabel": self.addLabel, "ImageBtn": self.addImageBtn}

    def setContent(self, _contents):
        for n, (w, ct) in enumerate(zip(self.getWidgets(), _contents)):
            __text = ct[0]
            if isinstance(__text, str):
                w.setText(__text)
            elif isinstance(__text, list):
                if __text:

                    w.setExamles(__text[n])
                    print(w, __text)

    def setWidget(self, widget_type, side=None, section=None):
        self.typeTegs[widget_type](side, section)

    def addLabel(self, side=None, section=None):
        name = "lb"+self.__getSuffix()
        self.labels[name] = DropLabel()
        self.labels[name].setObjectName("{}_card".format(section))
        self.box.addWidget(self.labels[name])

    def addImageBtn(self,side=None, section=None):
        print("addImageBtn")

    def __getSuffix(self):
        n = str((datetime.datetime.now().strftime("%y%m%d%H%M%S")) + str(random.randint(0, 99999999999)))
        nl = [x for x in n]
        random.shuffle(nl)
        return "_" + "".join(nl)

class Top(Section):
    def __init__(self, parent, name, side, config, *args, **kwargs):
        super().__init__(parent, name, side, config, *args, **kwargs)




class Center(Section):
    def __init__(self, parent, name, side, config, *args, **kwargs):
        super().__init__(parent, name, side, config, *args, **kwargs)



class Bottom(Section):
    def __init__(self, parent, name, side, config, *args, **kwargs):
        super().__init__(parent, name, side, config, *args, **kwargs)

class CardView(QFrame):
    def __init__(self, main, cfg, object_name, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setObjectName(object_name)
        self.side = self.objectName()
        self.cfg = cfg
        self.sections = {}
        self.box = customwidgets.BoxLayout(QBoxLayout.TopToBottom, self)
        # self._initSections()




    def _initSections(self):
        self.sections["top"] = Top(self, "top", self.side, config=self.cfg)
        self.sections["center"] = Center(self, "center", self.side, config=self.cfg)
        self.sections["bottom"] = Bottom(self, "bottom", self.side, config=self.cfg)
        self.box.addWidget(self.sections["top"], stretch=5)
        self.box.addWidget(self.sections["center"], stretch=5)
        self.box.addWidget(self.sections["bottom"], stretch=5)



class ViewCard(QFrame):
    def __init__(self, main, cfg, object_name, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cardModel = None
        self.contentTeg = dict(translation="translation",
                               Word="base",
                               cyrillicTranscription="cyrillicTranscription",
                               example="example",
                               example2="example2")
        self.currentSide = 0
        self.setObjectName(object_name)
        self.config = cfg
        self.setObjectName(name)
        self.main = main
        self.hbox = customwidgets.BoxLayout(QBoxLayout.LeftToRight, self)
        self.hbox.setContentsMargins(14, 14, 14, 14)
        self.vWorkBox = customwidgets.BoxLayout(QBoxLayout.TopToBottom)
        self.hbox.addLayout(self.vWorkBox)

        self.cardsStack = QStackedWidget()
        self.vWorkBox.addWidget(self.cardsStack)

        self.sides = dict(
            front=CardView(self.main, self.config, "front"),
            back=CardView(self.main, self.config, "back")
        )
        self.sides["back"].setStyleSheet('background: #EFEFEF;')
        self.cardsStack.addWidget(self.sides["front"])
        self.cardsStack.addWidget(self.sides["back"])
        self.cardsStack.setCurrentIndex(0)

    def updateContent(self):
        print("view", self.__cardModel)


    def setCardModel(self, cardModel):
        self.__cardModel = cardModel
        self.updateContent()


    def turnSide(self):
        self.currentSide = not self.currentSide
        self.cardsStack.setCurrentIndex(self.currentSide)

    def setSideIndex(self, i):
        self.cardsStack.setCurrentIndex(i)


    def unpack(self, cont, item_word):
        lst = []
        for _ls in cont:
            tx, tp = _ls
            lst.append([getattr(item_word, self.contentTeg[tx]), tp])
        return lst

    def setItemWord(self, item_word):
        if item_word is None:
            return
        _contents = []
        for name, side in  self.config["card"]["content"].items():

            for section, content in side.items():
                if content:
                    sectionsWidget = self.sides[name].sections[section]

                    contents = [x.split("_") for x in content]

                    sectionsWidget.setContent(self.unpack(contents, item_word))



    def initCard(self):
        """
        добавить нужные виджеты в секции
        """
        for s in self.sides["front"].sections.values():
            s.clear()
        for s in self.sides["back"].sections.values():
            s.clear()
        for name, side in  self.config["card"]["content"].items():

            for section, content in side.items():
                if content:
                    sectionsWidget = self.sides[name].sections[section]

                    contents = [x.split("_") for x in content]
                    for _content, widget_type in contents:
                        sectionsWidget.setWidget(widget_type, name, section)

class CardItem:
    def __init__(self):
        pass






