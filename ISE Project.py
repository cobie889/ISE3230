import gurobipy as gp
from gurobipy import GRB

m = gp.Model("wellness Baseline")
m.Params.LogToConsole = 0  # use this to disable detailed result output

x = m.addVars(4, lb = 0, name="x")
y = m.addVars(3, lb=0, name="y")
w = m.addVars(3, lb=0, name="w")
t = m.addVars(3, lb=0, name="t")
s = m.addVars(3, lb=0, name="s")
r = m.addVars(4, lb=0, name="r")
# A for Either social activity >7 or studying>7
A = m.addVars(2, vtype =GRB.BINARY, name ="A")
# B[0] for If physical activity > 1.5,
# B[1] for If physical activity > .5
# B[2] for If academics  > 10
# B[3] for If physical activity > 4
B = m.addVars(4, vtype =GRB.BINARY, name ="B")
# C for Either social activity >7 or studying>7
C = m.addVars(2, vtype =GRB.BINARY, name ="C")


# Ask for student type input
print("Enter the number assigned to the type of student you are: ")
print("1) Normal Student")
print("2) Scholar")
print("3) Student Athlete")
print("4) Social Butterfly")

studentType = 0
while studentType != '1' and studentType != '2' and studentType != '3' and studentType != '4':
    studentType = input()

    if studentType == '1':
        m.setObjective(.35*(90*x[0]+10*x[1]-10*x[2]-40*x[3]) + .20*(100*t[0]-5*t[1]-20*t[2]) + .18*(100*y[0] -5*y[1] -20*y[2]) + .09*(95*w[0] + 5*w[1] -20*w[2]) + .11*(80*s[0] + 20*s[1] -20*s[2]) + .07*(80*r[0] + 20*r[1] -15*r[2] -20*r[3]), GRB.MAXIMIZE)
        print("Optimized weekday for the normal student: ")
    elif studentType == '2':
        m.setObjective(.25*(90*x[0]+10*x[1]-10*x[2]-40*x[3]) + .15*(100*t[0]-5*t[1]-20*t[2]) + .4*(80*y[0] +20*y[1] -5*y[2]) + .02*(95*w[0] + 5*w[1] -20*w[2]) + .15*(80*s[0] + 20*s[1] -20*s[2]) + .03*(80*r[0] + 20*r[1] -15*r[2] -20*r[3]), GRB.MAXIMIZE)    
        print("Optimized weekday for the scholar: ")
    elif studentType == '3':
        m.setObjective(.25*(90*x[0]+10*x[1]-10*x[2]-40*x[3]) + .25*(100*t[0]+0*t[1]-10*t[2]) + .05*(100*y[0] -5*y[1] -20*y[2]) + .4*(70*w[0] + 25*w[1] -20*w[2]) + .03*(80*s[0] + 20*s[1] -20*s[2]) + .02*(80*r[0] + 20*r[1] -15*r[2] -20*r[3]), GRB.MAXIMIZE)
        m.addConstr(w[0] == 1)
        m.addConstr(w[1] == 1)
        m.addConstr(w[2] >= 2)
        print("Optimized weekday for the student athlete: ")
    elif studentType == '4':
        m.setObjective(.13*(90*x[0]+10*x[1]-10*x[2]-40*x[3]) + .2*(100*t[0]-5*t[1]-20*t[2]) + .07*(100*y[0] -5*y[1] -20*y[2]) + .09*(95*w[0] + 5*w[1] -20*w[2]) + .11*(80*s[0] + 20*s[1] -20*s[2]) + .4*(40*r[0] + 40*r[1] +20*r[2] -20*r[3]), GRB.MAXIMIZE)
        print("Optimized weekday for the social butterfly: ")
    else:
        print("Input not recognized, try again")
        

m.addConstr(x[0] <= 7)
m.addConstr(x[1] <= 2)
m.addConstr(x[2] <= 3)
m.addConstr(x[3] <= 12)
m.addConstr(t[0] <= 1.5)
m.addConstr(t[1] <= 1)
m.addConstr(t[2] <= 21.5)
m.addConstr(y[0] <= 9)
m.addConstr(y[1] <= 3)
m.addConstr(y[2] <=12)
m.addConstr(w[0] <= 1)
m.addConstr(w[1] <= 1)
m.addConstr(w[2] <= 22)
m.addConstr(s[0] <= 1)
m.addConstr(s[1] <=1)
m.addConstr(s[2] <= 22)
m.addConstr(r[0] <= 2)
m.addConstr(r[1] <= 2)
m.addConstr(r[2] <= 2)
m.addConstr(r[3] <= 18)
m.addConstr(x[0] + x[1] + x[2] + x[3] + t[0] + t[1] +t[2] + y[0] + y[1] + y[2] + w[0] + w[1] + w[2] + s[0] + s[1] + s[2] + r[0] + r[1] + r[2] + r[3] ==24 )


#If physical activity > 1.5, then meal >= 1.5
m.addConstr(t[0] >= 1.5 -100000*(1-B[0]))
m.addConstr(.5 >= w[1] -100000* B[0])

#If physical activity > 1.5, then sleep must be >= 8
m.addConstr(x[1] >= 1-100000*(1-B[0]))
m.addConstr(0.5 >= w[1] -100000* B[0])

#If physical activity > .5, then personal activities must be >= .5
m.addConstr(s[0] >= 0.5 -10000*(1-B[1]))
m.addConstr(0.5 >= w[0] -100000* B[1])

#If academics  > 10, then sleep must be >= 9
m.addConstr(x[1] >= 2 -10000*(1-B[2]))
m.addConstr(1 >= y[1] -10000*B[2])

#If physical activity > 4, then sleep must be >= 9
m.addConstr(x[1] >= 2-100000*(1-B[3]))
m.addConstr(2 >= w[2] -100000* B[3])

#Either social activity >5 or studying>7
m.addConstr(1 <= r[1] + 100000*(1-A[0]))
m.addConstr(7 <= y[0] + 100000*(1-A[1]))
m.addConstr(A[0] + A[1] == 1)

#at least meals > 1.5 or sleep >= 8
m.addConstr(1.5 <= t[0] + 100000*(1-C[0]))
m.addConstr(7 <= x[0] +100000*(1-C[1]))
m.addConstr(C[0] + C[1] >= 1)

m.optimize()

print("obj_func = ", m.objVal)

for v in m.getVars():
    print('value of %s is %g' % (v.varName, v.x))





