import paths
import paths
from core.cardModel import *

def load():
    card = CardModel(paths.PICKLE_CONFIG)
    # print(card.front)
    # print(card.back)

def save():
    f_sections = [DropBox(s) for s in ["top", "center", "bottom"]]
    # f_sections[1].appendDragItem("DropLabel", text="Word")
    # f_sections[1].appendDragItem("DropLabel", text="Word")
    b_sections = [DropBox(s) for s in ["top", "center", "bottom"]]
    contents = dict(front=f_sections, back=b_sections)
    cfg = PConfig(paths.PICKLE_CONFIG)
    cfg.save(contents)

if __name__ == '__main__':
    _SAVE = 1
    if _SAVE:
        save()
    else:
        load()