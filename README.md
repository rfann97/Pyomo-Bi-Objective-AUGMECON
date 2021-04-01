# Pyomo-Bi-Objective-AUGMECON
Bi Objective Pyomo model using augmented epsilon constraint solution approach

Research Design
The mathematical model from the published work presented in the background reading material, “Making sustainable sourcing decisions: practical evidence from the automotive industry” authored by Ghadimi, Dargi and Heavey (2017) will be re-examined but using an alternative solution approach.
Multiple products, multiple sourcing order allocation model
The model that is proposed has the following assumptions, indices, parameters, and decision variables.
Assumptions include:
	No quantity discount policies are foreseen.
	Fix ordering costs are supplier specific.
	Delivery lead-times are supplier specific.
	There is no item shortage for any suppliers.
	There are no inventories at the beginning and the end of the planning horizon.
	For the entire allocation period, demand is known with certainty and constant.
	Holding costs are dependent on the purchasing price.
Indices:
n	number of suppliers
m	number of products
i	product indices
j	supplier indices
Parameters:
Vij	capacity of j th supplier for i th product
Pij	purchasing price of product i delivered by supplier j
di 	total demand of product i
Tij	on-time delivery rate of product i offered by supplier j
ti	manufacturer’s minimum acceptable on-time delivery rate of product i
ηij	defective rate of product i delivered by supplier j
ηi	manufacturer’s maximum acceptable defective rate of product i
oj	fixed ordering cost for supplier j
oj’	variable ordering cost for supplier j
tcj	transportation cost of supplier j per vehicle
nj	number of vehicles assigned for supplier j
vj	vehicle capacity for supplier j in KG
ψi	weight occupied by each unit of product i in KG
si	space occupied by each unit of product i in m3
S	manufacturer’s total storage capacity in m3
hi	holding cost ratio of product i
spj	sustainability performance value of supplier j
Xij	amount of product i allocated to supplier j
Yj	1,     if an order allocated to supplier j0,     otherwise for all j                        
Objective functions
-	Total purchasing cost (TPC)
The total purchasing costs is defined by the sum of the cost of the products from the suppliers, the fixed ordering costs, the variable ordering costs which is determined by the amount of products to be purchased from each supplier, the inventory and transportation costs. The transportation costs can be calculated by the number of trucks used for transporting the purchased goods, it is also assumed that different product types can be transported in the same vehicle utilising the maximum capacity per vehicle.  
	Min TPC

-	Supplier’s sustainability performance value (SSPV)
The supplier’s sustainability performance value (SSPV) assesses the supplier regarding each sustainability dimension (economic, environmental, and social). By maximising this objective function, it ensures the optimal order allocation from suppliers that are more sustainable. When manufacturers are seeking to co-operate, co-ordinate, and collaborate with suppliers, this objective function pushes the supplier to improve their SSPV to maintain and improve their relationship with the manufacturer by boosting their profitability and competitive advantages.
	Max SSPV

Constraints
Important constraints for SSS&OA have been discussed previously and, in this model, the constraints used are demand, supplier’s production capacity, quality, delivery and manufacturer’s storage capacity which are defined as follows.
-	Demand constraint
This constraint makes sure that the manufacturer’s demand is met.

-	Supplier capacity constraint
This constraint ensures that the total demand for each product i does not exceed the total production capacity of each supplier j.


-	Quality constraint
This constraint aims to ensure that the quality of product is up to the standard of the manufacturer. The constraint is formulated by using the number of defective products in procured items i by each supplier j is less than the manufacturer’s maximum acceptable defective number of product i.  

-	Delivery constraint
This constraint ensures that the suppliers’ on-time delivered items is greater than the manufacturer’s minimum acceptable on-time delivery of purchased items. 

-	Manufacturer storage capacity constraint
This constraint means that there is a limit on the number of products that can be stored in each planning period as the manufacturer has a limited storage capacity S where each procured product i from each supplier j occupies si space. 

-	Binary and non-negativity constraints

The augmented ε-constraint method (AUGMECON)
The AUGMECON method addresses the shortcomings of the ε-constraint method which are: (a) the calculation of the range of the objective functions over the efficient set, (b) the guarantee of efficiency of the obtained solution and (c) the increased solution time for problems with several (more than two) objective functions. It also can be used to guide the DM’s to their most preferred Pareto optimal solution through an iterative procedure. Once again, considering the multi-objective function presented in Equation (9), the AUGMECON model can be shown as follows (Mavrotas, 2009)

By parametrical variation of the RHS of the constrained objective functions (ei) the Pareto-optimal solutions of the model are found, where ri is the range of the i th objective function, ∂ is a small number (usually between 10-3 and 10-6), si is a non-negative slack variable, and diri is the direction of the i th objective function, that is equal to -1 when the i th objective function should be minimised, and equal to +1 when the i th objective function should be maximised. The NISfi and PISfi for each objective function are calculated and then the range of the i th objective function is calculated by:

Next, ri is divided into li equal intervals. Subsequently, li + 1 grip point are achieved by the following equation which are set as the values of εi.

where η is the number of grid points. The model should be solved for each vector of ε, therefore, \prod_{i=2}^{n}{(l_i+1)} optimisation sub-problems should be solved.
In order to help the decision maker selection process for the most preferred Pareto-optimal solutions among all of the solutions, a fuzzy approach can be used as follows (Aghaei, Amjady and Shayanfar, 2011; Du et al., 2014):

where f_i^l shows the value of i th objective function in l th Pareto-optimal solution. \alpha_i^l represents the value of membership function of f_i^l. The overall membership function (overall degree of optimality) for l th Pareto-optimal solution was defined as the total value of sustainable purchasing (TVSP) is calculated by:

The most preferred solution refers to the Pareto solution with the highest value of TVSP.

