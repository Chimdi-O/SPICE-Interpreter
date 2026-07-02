from SIunit import SI_prefix


class Circuit(): 
    def __init__(self):
        self.components = [] 
        self.node_map = {} # node_name -> matrix index 
        self.extra_unknown_map = {}
        self.reversed_node_map = {}
        self.voltage_dict = {} 
        self.current_dict = {} 
        self.power_dict = {} 
       
    def addComponent(self,comp): 
        self.components.append(comp) 

        for i in comp.nodes: 
            if i != "0" and i not in self.node_map: 
                if len(self.node_map) == 0: 
                    self.node_map[i] = 0 
                    self.reversed_node_map[0] = i 
                else: 
                    length = len(self.node_map)
                    self.node_map[i] = length
                    self.reversed_node_map[length] = i 

    def __repr__(self): 
        netlist = [] 
        for component in self.components: 
            netlist.append(repr(component)) 
        
        return "\n".join(netlist)   
    
    def parseResultsMatrix(self,results_matrix,mode): 
        # voltage

        for i in range(len(results_matrix)): 
            node = self.reversed_node_map[i]
            value = round(results_matrix[i][-1],3)
            self.voltage_dict[node] = value 

        # Currents 
        for i in self.components: 
            i.calcCurrent(results_matrix,self.node_map,self.extra_unknown_map,mode)

        # Power
        
    def printValues(self): 

        for node in self.voltage_dict: 
            value = SI_prefix(self.voltage_dict[node])
            print(f"{f"V({node})":<10} :       {value}V")
        
        for component in self.components: 
            value = SI_prefix(component.current)
            print(f"{f"I({component.name})":<10} :       {value}A")