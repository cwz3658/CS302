import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation

#fig, ax = plt.subplots()
#fig.set_tight_layout(True)

fig=plt.figure()


#ax.plot(x, x, 'b', linewidth=2)
#
def update(k):
    ims=[]
    for i in range(k):
        im=plt.imshow(np.random.rand(3, 20)<i/10)
        ims.append([im])
    return ims

#if __name__ == '__main__':
anima=ArtistAnimation(fig, update(10),interval=200,repeat=True)

plt.show()
# 





