
def BuildMatrix(Circuit,mode): 
    extra_unknown_map = {} 

    extra_unknowns = ["V"]

    if mode == "op": 
          extra_unknowns.append("L")

    for component in Circuit.components: 
        if component.name[0] in extra_unknowns: 
             extra_unknown_map[component.name] = len(Circuit.node_map) + len(extra_unknown_map) 

    n = len(Circuit.node_map)+len(extra_unknown_map)
    matrix_a = [[0 for _ in range(n)] for _ in range(n)]
    matrix_b = [0]*n

    for component in Circuit.components: 
         matrix = component.stamp(matrix_a,matrix_b,Circuit.node_map,extra_unknown_map,mode)
    

    aug_matrix = matrix_a

    for i in range(n): 
         aug_matrix[i].append(matrix_b[i])

    return aug_matrix
            