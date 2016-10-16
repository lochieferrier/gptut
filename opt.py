"Very simple problem: minimize x while keeping x greater than 1."
from gpkit import Variable, Model

# Decision variable
x = Variable('x')

# Configuration
n_rotors = Variable('n_rotors',4,'-')
payload_mass = Variable('payload_mass',1,'kg')
structures_mass = Variable()

# Battery
battery_mass = Variable('battery_mass','kg')
battery_energy = Variable('battery_energy','kg')
battery_specificEnergy = Variable('battery_specificEnergy','kg')

# ESC
esc_mass = Variable('esc_mass','kg')
esc_power = Variable('esc_power','W')
esc_specificPower = Variable('esc_specificPower','W/kg')

# Motor
motor_mass = Variable('motor_mass','kg')
motor_power = Variable('motor_power','W')
motor_specificPower = Variable('motor_specificPower','W/kg')

# Propeller
propeller_d = Variable('propeller_d','m')

# Performance variables
t_hover = Variable('t_hover','s')
T_total = Variable('T_total','N')
P_total = Variable('P_total','W')
m_total = Variable('m_total','kg')

# Environment
rho = Variable('rho','kg/m^3')
g = Variable('g','m')

# Constraints
constraints = [m_total >= n_rotors*(esc_mass+motor_mass) + battery_mass,
			   esc_power >= motor_power,
			   t_hover <= battery_energy/P_total]

# Objective (to minimize)
objective = 1/t_hover

# Formulate the Model
m = Model(objective, constraints)

# Solve the Model
sol = m.solve(verbosity=1)

# print selected results
print("Optimal cost:  %s" % sol['cost'])
print("Optimal x val: %s" % sol(x))