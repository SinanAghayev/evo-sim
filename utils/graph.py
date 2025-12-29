import matplotlib.pyplot as plt


def plot_graph(x, y, title, x_label, y_label):
    plt.figure()
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.show()
