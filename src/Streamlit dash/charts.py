import matplotlib.pyplot as plt
from matplotlib import rcParams 
def line_chart(x,y, **options):
    fig, ax = plt.subplots(1)
    rcParams["figure.figsize"] = 8, 6
    ax.plot(x,y, linewidth= 2)
    ax.set(**options)
    plt.gcf().autofmt_xdate()
    plt.grid(True, color= 'k', linestyle= ':')
    fig.tight_layout()
    return fig 