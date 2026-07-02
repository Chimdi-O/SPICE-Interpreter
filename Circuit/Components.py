from SIunit import SI_prefix

class Component(): 
    def __init__(self,name,nodes,str_value,num_value): 
        self.name = name 
        self.nodes = nodes 
        self.str_value = str_value
        self.num_value = num_value
        self.current = 0
        self.power = 0 
    
    def __repr__(self): 
        node_str = " ".join(self.nodes)
        return f"{self.name} {node_str} {self.str_value}"
    
    def stamp_cell(self,row,column,value,matrix): 
        if row != None and column != None: 
             matrix[row][column] += value 

class Resistor(Component): 

    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode): 
        g = 1/self.num_value

        a = node_map.get(self.nodes[0])
        b = node_map.get(self.nodes[1])

        self.stamp_cell(a,a,g,matrix_a)
        self.stamp_cell(a,b,-g,matrix_a)
        self.stamp_cell(b,a,-g,matrix_a)
        self.stamp_cell(b,b,g,matrix_a)
    
    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode): 
            node1_V = 0 
            node2_V = 0 
            
            if self.nodes[0] != "0": 
                node1_V = results_matrix[node_map[self.nodes[0]]][-1]
            
            if self.nodes[1] != "0": 
                node2_V = results_matrix[node_map[self.nodes[1]]][-1]
            
            self.current = (node1_V - node2_V)/self.num_value
            #current = SI_prefix(current)
            #print(f"{f"I({self.name})":<10} :       {current}A")
   
class Capacitor(Component): 
    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode): 
        if mode == "op": 
            pass 
          
        elif mode == "tran": 
            pass
    
    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode):
        if mode == "op": 
            self.current = 0 
            #print(f"{f"I({self.name})":<10} :       {0}A")
        
        elif mode == "tran": 
            pass 
    
        
class Inductor(Component): 
    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode):
        if mode == "op": # in OP inductor is a short which means a voltage source with an inductance of zero1``
            a = node_map.get(self.nodes[0])
            b = node_map.get(self.nodes[1])
            c = extra_unknown_map.get(self.name)

            self.stamp_cell(a,c,1,matrix_a)
            self.stamp_cell(b,c,-1,matrix_a)
            self.stamp_cell(c,a,1,matrix_a)
            self.stamp_cell(c,b,-1,matrix_a)
            matrix_b[c] = self.num_value   
        if mode == "tran": 
            pass 
    
    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode): 
        if mode == "op": 
            index = extra_unknown_map[self.name]
            self.current = results_matrix[index][-1]
            #current = SI_prefix(current)
            #print(f"{f"I({self.name})":<10} :       {current}A")

class VoltageSource(Component): 
    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode):

        a = node_map.get(self.nodes[0])
        b = node_map.get(self.nodes[1])
        c = extra_unknown_map.get(self.name)

        self.stamp_cell(a,c,1,matrix_a)
        self.stamp_cell(b,c,-1,matrix_a)
        self.stamp_cell(c,a,1,matrix_a)
        self.stamp_cell(c,b,-1,matrix_a)
        matrix_b[c] = self.num_value

    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode): 
        index = extra_unknown_map[self.name]
        self.current = results_matrix[index][-1]
        #current = SI_prefix(current)
        #print(f"{f"I({self.name})":<10} :       {current}A")


class CurrentSource(Component): 
    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode):

        a = node_map.get(self.nodes[0])
        b = node_map.get(self.nodes[1])

        self.stamp_cell(a,0,-self.num_value,matrix_b)
        self.stamp_cell(b,0,self.num_value,matrix_b)

    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode):
        self.current = self.num_value
        #current = SI_prefix(self.num_value) 
        #print(f"{f"I({self.name})":<10} :       {current}A")
 
        