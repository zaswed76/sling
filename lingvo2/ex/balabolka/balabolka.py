import subprocess

import paths

balabolkaExe = paths.BALABOLKA

# result = subprocess.run([balabolkaExe, '-l'], stdout=subprocess.PIPE)
# print(result.stdout)

p = r"E:/pyprojects/sling/lingvo2/ex/balabolka/b.wav"

res = subprocess.run([balabolkaExe,  "-t cat -w b.wav"], creationflags=0, close_fds = True)
# print(res)
