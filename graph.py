import matplotlib.pyplot as plt


def mesure(couple):
    liste1, liste2 = zip(*couple)
    return list(liste2)

def date(couple1):
    liste1, liste2 = zip(*couple1)
    return list(liste1)

def show_measures(height, flow) :
    x_val = []
    y_val = []
    z_val = []                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

    x_val = date(flow)
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('date')
    ax1.set_ylabel('water flow', color=color)
    ax1.plot(x_val,mesure(flow), color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('height', color=color)  # we already handled the x-label with ax1
    ax2.plot(x_val,mesure(height), color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
