import matplotlib.pyplot as plt

color_list = ['tab:blue', 'tab:green', 'tab:red', 'tab:brown', 'tab:cyan',
              'tab:olive', 'tab:orange', 'tab:purple', 'tab:pink', 'tab:gray']

def measure(couple):
    liste1, liste2 = zip(*couple)
    return list(liste2)

def date(couple):
    liste1, liste2 = zip(*couple)
    return list(liste1)

def ShowMeasures(*stList) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

    i = 0
    for st in stList :
        if( st != []) :
            plt.plot(date(st), measure(st), color=color_list[i%len(color_list)])
        i += 1
    plt.show()

