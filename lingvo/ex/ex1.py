
import config


cfg = config.Config(r"E:\1_SYNS_ORIGINAL\0SYNC\python_projects\sling\lingvo\ex\say\ex.yaml")

print(cfg.data)
cfg["example"] = 333
cfg.save()
print(cfg.data)
