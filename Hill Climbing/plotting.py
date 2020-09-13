import matplotlib.pyplot as plt

data = {'Naive': 10, 'Hill climbing': 15}
x_axis = ['naive', 'Hill climbing']

names = list(data.keys())
values = list(data.values())

fig, axs = plt.subplots()
axs.bar(names, values)
fig.suptitle('Permormance algorithm')

plt.show()
