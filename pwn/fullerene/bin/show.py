# This is useful if you actually want to see the output when you mesh a chunk. 
# It's not really part of the challenge otherwise.


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

beginv = "Begin VBUF\n"

data = open("output.txt","r").read()

org = data

data = data[data.index(beginv) + len(beginv) - 1 :].replace("vec3(","").replace(")","")

begini = "Begin IBUF\n"

vbuf = [[float(a) for a in vec.split(",")] for vec in data[:data.index(begini)].split("\n")[1:-1]]

ibuf = [int(i) for i in data[data.index(begini) + len(begini) - 1:].split("\n")[1:-1]]

#print(vbuf[:10], vbuf[-10:], org[org.index(beginv) : org.index(beginv) + 50], org[org.index(begini) - 20 : org.index(begini) + 50])
#print(ibuf[:10], ibuf[-10:], org[org.index(begini) : org.index(begini) + 50], org[-10:])


# Define the vertices and faces of the mesh
vertices = np.array(vbuf) # Replace with your vertex coordinates

ibuf = list(zip(ibuf[::3], ibuf[1::3], ibuf[2::3]))

faces = np.array(ibuf) # Replace with your face indices

# Create a new figure and set up a 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extract the x, y, and z coordinates from the vertices
x = vertices[:, 0]
y = vertices[:, 1]
z = vertices[:, 2]

print(vertices[:10],"\n", x[:10], "\n", x[-10:],"\n", y[:10],"\n", y[-10:],"\n", z[:10],"\n", z[-10:])

#faces = faces[:100]

# Plot the mesh surface
ax.plot_trisurf(np.array(x), np.array(y), np.array(z), triangles=faces, cmap='viridis') # You can change the colormap as desired

#ax.set_xlim3d(min(x), max(x))
#ax.set_ylim3d(min(y), max(y))
#ax.set_zlim3d(min(z), max(z))

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Mesh Surface')

# Show the plot
plt.show()
