как подключить контроллер к представлению
------------------------------------------

**Контроллер** - класс унаследованый от gui.controller.AbcController


имеет два позиционных параметра:

1. main - ссылка на класс main
2. parent - ссылка на класс представления

пример: ::

    self.chooseDictController = ChooseDictStackController(self, self.chooseDict)

контроллер  добавляется в словарь - self.controls,
ключ - objectName предствления

пример: ::

    self.controls["chooseDictStack"] = self.chooseDictController


**Представление**

пример: ::

    class GSettingsDict(AbcGSettingsFrame):
    def __init__(self, main, cfg, textName, obgectName, *args, **kwargs):
        super().__init__(main, cfg, textName, obgectName, *args, **kwargs)
        self.box = QHBoxLayout(self)

        self.main = main
        self.btn = customwidgets.AbcControlBtn("bumcaca", self.main)
        self.box.addWidget(self.btn)

**objectName кнопки  "bumcaca" - это и имя метода в контроллере**


итог:
'''''

1. создаём представление
2. создаём контроллер
3. подключаем

пример: ::

    self.userView = UserView(objectName="userView")
    self.userController = userController(self, self.userView)
    self.controls["userView"] = self.userController

имя метод подключения connect (class main): ::

    def connect(self):
        controll = self.sender()
        slot = controll.objectName()
        object = self.controls[controll.parent().objectName()]
        return getattr(object, slot)()

