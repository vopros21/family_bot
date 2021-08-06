import re
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = {'apple': 10, 'orange': 15, 'lemon': 5, 'lime': 20}
    names = list(data.keys())
    values = list(data.values())

    fig, axs = plt.subplots(1, 1, figsize=(3, 3))
    axs.bar(names, values)
    # axs[1].scatter(names, values)
    # axs[2].plot(names, values)
    fig.suptitle('Categorical Plotting')
    plt.show()
    # plt.savefig('graph.png')

