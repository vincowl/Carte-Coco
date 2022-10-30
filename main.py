# coding: utf8
from MapGenerator import MapGenerator
from weeblyPublisher import WeeblyPublisher


def main():
    myMapGenerator = MapGenerator()
    myMapGenerator.readXLS()
    myMapGenerator.readVilles()
    myMapGenerator.mergeData()
    #myMapGenerator.printData()
    myMapGenerator.printMap()
    myWeeblyPublisher = WeeblyPublisher()
    myWeeblyPublisher.process()

if __name__ == "__main__":
    # execute only if run as a script
    main()
    print("--- Done : please copy/paste content of weeblyCode.txt ---")
