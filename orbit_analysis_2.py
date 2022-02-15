from operator import truediv
import numpy as np
import matplotlib.pyplot as plt
import xlrd as xl

loc = ("/Users/henrydeng/Desktop/2021-22/Astrophysics/Unit_1_Project/orbit-data.xlsx")
wb = xl.open_workbook(loc)
sheet = wb.sheet_by_index(2)

#calculating orbital inclination - not used
calculate_tilt = False
num_of_data = 41

X = []
Y = []

if calculate_tilt:
    for x in range (num_of_data):
        x_row = [np.sqrt((sheet.cell_value(x+2, 3) ** 2) + (sheet.cell_value(x+2, 5) ** 2))]
        #account for negative numbers
        if sheet.cell_value(x+2, 3) < 0:
            x_row[0] = -x_row[0]
        X.append(x_row)

    for y in range (num_of_data):
        y_row = [np.sqrt((sheet.cell_value(y+2, 4) ** 2) + (sheet.cell_value(y+2, 5) ** 2))]
        if sheet.cell_value(y+2, 4) < 0:
            y_row[0] = -y_row[0]
        Y.append(y_row)

#read data
else:
    for x in range (num_of_data):
        x_row = [sheet.cell_value(x+2, 3)]
        X.append(x_row)

    for y in range (num_of_data):
        y_row = [sheet.cell_value(y+2, 4)]
        Y.append(y_row)

X = np.array(X)
Y = np.array(Y)

# Formulate and solve the least squares problem ||Ax - b ||^2
A = np.hstack([X**2, X * Y, Y**2, X, Y])
b = np.ones_like(X)
x = np.linalg.lstsq(A, b)[0].squeeze()

# Print the equation of the ellipse in standard form
print('The ellipse is given by {0:.3}x^2 + {1:.3}xy+{2:.3}y^2+{3:.3}x+{4:.3}y = 1'.format(x[0], x[1],x[2],x[3],x[4]))

#calculate eccentricity
D = []
for i in range (num_of_data):
    d_row = [np.sqrt((X[i] ** 2) + (Y[i] ** 2))]
    D.append(d_row)
D = np.array(D)
peri = np.min(D)
apo = np.max(D)
ecc = (apo - peri) / (apo + peri)
print('The eccentricity of the ellipse is ' + str(ecc))

# Plot the data
plt.scatter(X, Y, label='Data Points')

# Plot the least squares ellipse
x_coord = np.linspace(-31,31,600)
y_coord = np.linspace(-31,31,600)
X_coord, Y_coord = np.meshgrid(x_coord, y_coord)
Z_coord = x[0] * X_coord ** 2 + x[1] * X_coord * Y_coord + x[2] * Y_coord**2 + x[3] * X_coord + x[4] * Y_coord
plt.contour(X_coord, Y_coord, Z_coord, levels=[1], colors=('r'), linewidths=2)

plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
