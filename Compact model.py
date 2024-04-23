from pyomo.environ import *
import numpy as np

# Define the model
model = ConcreteModel('Multi-Stage ALM Compact Model')

# Sets
model.I  = Set(initialize=['stocks', 'bonds'])
Nodes  = [f'n{i}' for i in range(15)]
Routes = [f'n{i}' for i in range(7) for _ in range(2)]
model.N  = Set(initialize=Nodes)
model.S  = Set(initialize=Nodes[7:])
model.T  = Set(initialize=Nodes[1:7])
model.M  = Set(initialize=Nodes[:7])

# Parameters
prob = np.array([1/len(model.S)]*len(model.S))
model_R_data = {'stocks': [1.25 if i % 2 == 0 else 1.06 for i in range(14)],
                'bonds': [1.14 if i % 2 == 0 else 1.12 for i in range(14)]}

model.R = Param(model.I, model.N, initialize={
    **{('stocks', f'n{i+1}'): model_R_data['stocks'][i] for i in range(len(model_R_data['stocks']))},
    **{('bonds', f'n{i+1}'): model_R_data['bonds'][i] for i in range(len(model_R_data['bonds']))}
})
model.q  = Param(initialize=1)
model.r  = Param(initialize=1)
model.pr = Param(model.S,initialize={i: prob[j] for i in model.S for j in range(len(prob))},within=Any)
model.W0 = Param(initialize=55000)
model.L  = Param(initialize=80000)

func_a = dict(zip(Nodes[1:], Routes))
def previous_node(node):
    previous_nodes = func_a
    return previous_nodes.get(node)

# Variables
model.x = Var(model.I, model.M, domain=NonNegativeReals)
model.w_plus = Var(model.S, domain=NonNegativeReals)
model.w_minus = Var(model.S, domain=NonNegativeReals)

# Objective function
def obj_rule(model):
    return quicksum(model.pr[s] * (model.q * model.w_plus[s] - model.r * model.w_minus[s]) for s in model.S)
model.obj = Objective(rule=obj_rule, sense=maximize)

# Constraints
def budget_constraint_rule(model):
    return quicksum(model.x[i, 'n0'] for i in model.I) == model.W0
model.budget_constraint = Constraint(rule=budget_constraint_rule)

def return_investment_constraint_rule(model, n):
    if n in model.T:
        return quicksum(model.R[i, n] * model.x[i, previous_node(n)] for i in model.I) == quicksum(model.x[i, n] for i in model.I)
    else:
        return Constraint.Skip
model.return_investment_constraint = Constraint(model.T, rule=return_investment_constraint_rule)

def return_liability_constraint_rule(model, s):
    if s in model.S:
        return quicksum(model.R[i, s] * model.x[i, previous_node(s)] for i in model.I) == model.L + model.w_plus[s] - model.w_minus[s]
    else:
        return Constraint.Skip
model.return_liability_constraint = Constraint(model.S, rule=return_liability_constraint_rule)

# Solve the model
solver = SolverFactory('cplex_direct')
results = solver.solve(model)

# Display results
# results.write()
# model.display()
for i in model.I:
    for m in model.M:
            if value(model.x[i,m]) != 0:
                print(f"x[{i}, {m}] =", round(value(model.x[i, m]),2))
print(round(value(model.obj),2))

