from Utils import parseUnits

class Component(): 
    def __init__(self,name,nodes,str_value): 
        self.name = name 
        self.nodes = nodes 
        self.str_value = str_value
        self.num_value = parseUnits(str_value)
    
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
   

class Capacitor(Component): 
    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode): 
        if mode == "op": 
            pass 
          
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