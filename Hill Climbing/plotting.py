import matplotlib.pyplot as plt

file = open('data.txt')
time, *data = map(lambda el: el.split() , file.readlines())
time = " ".join(time)

x_axis = []
y_axis = []

for x,y in data:
    x_axis.append(int(x))
    y_axis.append(int(y))

fig, axs = plt.subplots()
axs.bar(x_axis, y_axis)
fig.suptitle('Results\n'+time)

axs.ticklabel_format(style='plain',useOffset=False)
axs.set_yscale('log')
axs.set_ylabel('Frecuencia')
axs.set_xlabel('Min. score')

for x,y in zip(x_axis,y_axis):
    

    label = "{:d}".format(y)

    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0, 2), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center

plt.show()
