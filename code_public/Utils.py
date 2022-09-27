import matplotlib.pyplot as plt

def save_bar(filename, x, heights, xlabels):
    plt.bar(x, height = heights)
    plt.xticks(x, xlabels)
    plt.savefig(filename)
    plt.close()