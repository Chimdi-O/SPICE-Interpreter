from Simulation.MatrixMaths import buildMatrix, matrixSolver
from SIunit import SI_prefix


class OperatingPoint(): 
    def __init__(self,circuit): 
        self.circuit = circuit 
        self.results_matrix = [] 

    def run(self): 
        matrix = buildMatrix(self.circuit,"op")
        self.results_matrix = matrixSolver(matrix)
        self.circuit.parseResultsMatrix(self.results_matrix,"op")
        self.circuit.printValues() 


     

    
    