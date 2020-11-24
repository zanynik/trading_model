# Trading Model
Requires matplotlib.pyplot and networkx libraries

# Network Instances
By default the demofile.txt contains a basic network instance on which the trading problem is solved. To change the network, change the demofile according to follwing instructions.

To add an edge to the network, see the following example:


Example : Seller having node number 1 and good valuation 0 is connected to a buyer with node number 3 and valuation 10. The above connection is written as follows in the demofile.txt :
1 0 3 10
Therefore the sequence to follow is : 
s - seller node, val_s - seller valuation,  b - buyer node, val_b - buyer valuation

# Run
To solve the trading problem in the network defined in demofile.txt, run the following:

python main.py

