import matplotlib.pyplot as plt

color_list = ['tab:blue','tab:blue','tab:red','tab:green','tab:brow','tab:cyan','tab:olive','tab:orange','tab:purple','tab:pink','tab:gray']

def mesure(couple):
    liste1, liste2 = zip(*couple)
    return list(liste2)

def date(couple1):
    liste1, liste2 = zip(*couple1)
    return list(liste1)

def show_measures(*measures_list) :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

    fig, ax1 = plt.subplots()

    i = 0

    for measures in measures_list :
        i += 1
        color = color_list[i % len(color_list)]
        ax = ax1.twinx()
        ax.set_xlabel('date')
        ax.set_ylabel(str(i), color=color)
        ax.plot(date(measures), mesure(measures), color=color)
        ax.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
    
