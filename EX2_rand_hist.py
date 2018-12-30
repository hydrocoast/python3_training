import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns

def main():
    # parameters
    nind = 100
    maxint = 100

    # set variables in array
    val = np.random.randint(0, maxint, size=nind)
    horz = np.linspace(1, nind, nind)

    # get particular value
    stdv = np.std(val, ddof=1)
    meanv = np.mean(val)
    sval = np.sort(val, axis=0)
    sind = np.argsort(val, axis=0)[::-1]
    print(sind[0:5])

    # figure hist
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(horz, val, align="center")
    ax.plot(sind[0:5]+1, val[sind[0:5]], 'ro', ms=8)
    ax.plot(np.array([0,nind+1]), np.array([meanv,meanv]), "-", color="#00ff00", lw=2.0)
    ax.set_xlim(0, nind+1)
    ax.set_title(r'$\sigma$'+ '=' + '%3.2f' % stdv, fontsize=18)

    plt.show()

if __name__ == '__main__':
    main()
