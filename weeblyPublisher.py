# coding: utf8

class WeeblyPublisher:

    def __init__(self):
        self._filename = 'liste_coco.html'
        return
    
    def process(self, outputFileName='weeblyCode.txt'):
        with open(self._filename, 'r', encoding="utf-8") as fidr, open(outputFileName, 'w', encoding="utf-8") as fidw :
            fidw.write('<div style="border:none; overflow:hidden; width:auto; height:690px;" allowTransparency="true">\n')
            for line in fidr:
                if not ("head>" in line or "body>" in line or "DOCTYPE" in line) and ''.join(line.splitlines()[0].split()):
                    fidw.write(line)
            fidw.write('\n</div> \n')