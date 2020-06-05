import numpy as np
from scipy.optimize import linprog
import pandas as pd
import time
from math import floor, log
import time
import csv
# generate the ph_table from logic m
def generate_p_matrix(m, p_matrix):
    acc_prod = list(map(lambda x: int(x), [np.prod(m[i+1:]) for i in range(len(m))]))
    l = np.sum(m)-1
    p = [() for _ in range(np.prod(m))]
    level = []

    for i in range(len(p)):
        total = i
        level = []
        for j in range(len(m)):
            current = int(total/acc_prod[j])
            total %= acc_prod[j]
            level.append(current)
        curr_p = []
        for i in range(len(level)):
            temp = [0 for _ in range(m[i])]
            temp[m[i]-1-level[i]] = 1
            curr_p+=temp
        p_matrix.append(curr_p)
        #print(p_matrix)
        
# generate the initial set of basis for the cone for delta

def generate_basis_matrix(m, p_matrix, lhs):
    basis_matrix = []
    acc_prod = list(map(lambda x: int(x), [np.prod(m[i+1:]) for i in range(len(m))]))
    for i in range(len(m)):

        basis = m[i] - 1
        while basis:

            temp = basis
            count=0
            while temp:
                count+=1
                temp>>=1

            for j in range(count):
                if (basis & (1<<j)):
                    p1 = basis*acc_prod[i]
                    p2 = (basis^(1<<j))*acc_prod[i]
                    print(p1,p2)
                    basis_matrix.append(p_matrix[p1]-p_matrix[p2])
                    lhs.add((p1,p2))

            basis -=1

    return  np.array(basis_matrix) 

def generate_relations(relations, extra_matrix, p_matrix, permutations):
    p = p_matrix
    
    l_h = []
    
    for i,j in relations:
        current = (p_matrix[i] - p_matrix[j]).reshape((1,-1))
        l_h.append(current)
        
    basis_matrix = np.concatenate(l_h,axis =0)
    basis_matrix = np.concatenate([basis_matrix, extra_matrix],axis = 0)
    A_eq = basis_matrix.T
    b_ub = np.array([0 for _ in range(len(basis_matrix))])    
    c = np.array([0 for _ in range(len(basis_matrix))])
    A_ub = - np.identity(len(basis_matrix))
    
    ret = set()
    # print(basis_matrix)
    for i,j in permutations:
        #print(i,j)
        if linprog(c = c,A_ub=A_ub,A_eq=A_eq,b_ub = b_ub,b_eq=p[i]-p[j]).success:
            ret.add((i,j))
    return ret

def get_permutations(n):
    ret = []
    for i in range(n):
        for j in range(n):
            if i!=j:
                ret.append((i,j))
    return ret


def test_in_relations(relations, extra_matrix, p_matrix, candidate):
    p = p_matrix
    l_h = []
    
    for i,j in relations:
        current = (p_matrix[i] - p_matrix[j]).reshape((1,-1))
        l_h.append(current)
    
    
    basis_matrix = np.concatenate(l_h,axis =0)
    basis_matrix = np.concatenate([basis_matrix, extra_matrix],axis = 0)
    A_eq = basis_matrix.T
    b_ub = np.array([0 for _ in range(len(basis_matrix))])    
    c = np.array([0 for _ in range(len(basis_matrix))])
    A_ub = - np.identity(len(basis_matrix))
    
    i, j = candidate[0], candidate[1]
    
    if linprog(c = c,A_ub=A_ub,A_eq=A_eq,b_ub = b_ub,b_eq=p[i]-p[j]).success:
        return True
    else:
        return False
    

def generate_predecessors(relations, extra_matrix, p_matrix, permutations):
    zero_logic = generate_relations(relations, extra_matrix, p_matrix, permutations)
    ret = dict()
    for i, j in zero_logic:
        if i in ret:
            ret[i].add(j)
        else:
            ret[i] = set([j])
    return ret

def generate_logics(basic_relations, extra_matrix, p_matrix, permutations):
    ret = dict()
    basic_set = set()
    for i, j in permutations:
        if test_in_relations(basic_relations,extra_matrix,p_matrix,(i,j)):
            basic_set.add((i,j))
    
    for i, j in permutations:
        if ((i, j) not in basic_set) and ((j,i) not in basic_set) :
            temp_set = set()
            relations = basic_relations.union(set([(i,j)]))
            #print(relations)
            for k,l in permutations:
                if (k,l)!=(i,j) and (not (k,l) in basic_set) and \
                test_in_relations(relations,extra_matrix,p_matrix,(k,l)):
                    if (i,j) in ret:
                        ret[(i,j)].add((k,l))
                    else:
                        ret[(i,j)] = set([(k,l)])
    return ret


def trie_dfs(original_basis, newly_added, p_matrix, extra_matrix, candidates, path, ret, permutations, predecessors, logics, file_name):
    
    if not candidates:
        temp_rel = generate_relations(original_basis.union(newly_added), extra_matrix, p_matrix, permutations)
        if len(temp_rel) > int(len(permutations)/2):
            return
        
        with open(file_name,'a') as file:
            file.write(str(path)+'\n')

        ret.add(tuple(path))
    
    temp_settled = set(path)
    
    for i in candidates:
        
        if not predecessors[i].issubset(temp_settled):
            continue
        
        j  = path[-1]
        
        # if inverse in the set then we just continue, else we can add i safely
        if test_in_relations(original_basis.union(newly_added), extra_matrix, p_matrix, (j, i)):
            continue
        else:
            newly_added.add((i,j))
            path.append(i)
            candidates.remove(i)
            temp_predecessors = dict()
            for key in predecessors:
                temp_predecessors[key] = predecessors[key].copy()
            if (i, j) in logics:
                for k,l in logics[(i,j)]:
                    temp_predecessors[k].add(l)
            trie_dfs(original_basis, newly_added, p_matrix, extra_matrix, candidates, path, ret, permutations,temp_predecessors,logics,file_name)
            newly_added.remove((i,j))
            path.pop()
            candidates.add(i)   
            
def indexlist(index,pattern):
    res = []
    for i in range(len(pattern)-1,-1,-1):
        res.append(index%pattern[i])
        index= floor(index/pattern[i])
    res = res[::-1]
    return res


# pattern = [4,2,2]
# index = 4

# indexlist(index, pattern)

# sample = [[X_0, X_1, X_2,X_3],[Y_0,Y_1],[Z_0,Z_1]]
def evalutionord(pattern, sample):
    count  = 1
    for i in range(len(pattern)):
        count*=pattern[i]
    ord = []
    for i in range(count):
        ilist = indexlist(i, pattern)
        x, y, z = sample[0][ilist[0]], sample[1][ilist[1]], sample[2][ilist[2]]
        ord.append(x+y+z)
    return np.argsort(ord)


def random_sample(pattern):
    sample = []
    for i in range(len(pattern)):
        temp = []
        count = floor(log(pattern[i],2))
        points = np.random.uniform(size = count+1)
        first = points[0]
        points[0] = -1
        points = sorted(points)
        points[0] = first
        for j in range(pattern[i]):
            p = j
            pos = 0
            current = points[0]
            while p:
                #print(p, pos)
                v = p%2
                if v:
                    current += points[pos+1]
                pos+=1
                p = floor(p/2)
            temp.append(current)
        sample.append(list(map(lambda x: log(x),temp)))
    return sample


def random_ordering(pattern, time_limit = 1000, size_limpoit = 1000):
    ret = []
    d = {}
    count = time_limit
    for i in range(count):
        sample = random_sample(pattern)
        ord = tuple(evalutionord(pattern,sample))
        ret.append(ord)
        if ord not in d:
            d[ord] = sample
    return ret, d

def extraRelationGenerator(p_matrix, ptotalordering):
    ret = []
    for i in range(1,len(ptotalordering)):
        ret.append(p_matrix[ptotalordering[i]] - p_matrix[ptotalordering[i-1]])
    return np.vstack(ret)

def run5(logic, restrictedOrdering):
    #count = 0
    ret = set([])
    file_name = '{} {}.dat'.format(logic,restrictedOrdering)
    # set parameters
    m =  list(map(lambda x: int(x), logic.split('_')))
    n = np.prod(m)

    # generate p_matrix
    p_matrix = []
    generate_p_matrix(m,p_matrix)
    p_matrix = np.array(p_matrix)

    # get original basis
    original_basis = set([])
    basis_matrix = generate_basis_matrix(m, p_matrix, original_basis)

    # get basis matrix not that useful
    # also delta 1 < delta 2
    extra_matrix = extraRelationGenerator(p_matrix,restrictedOrdering)
    #extra_matrix = np.vstack([extra_matrix, np.array([[0,1,-1,0,0,0,0,0,0,0],[-1,1,1,-1,0,0,0,0,0,0]])])
    tt = [[-1, 0, 0, 1, 1, 0, 0, -1, 0, 0], [-1, 0, 1, 0, 0, 1, 0, -1, 0, 0], [-1, 0, 1, 0, 1, 0, -1, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 1, -1, 0, 0], [-1, 1, 0, 0, 1, -1, 0, 0, 0, 0], [-1, 1, 1, -1, 0, 0, 0, 0, 0, 0], [0, -1, 0, 1, 0, 1, 0, -1, 0, 0], [0, 0, -1, 1, 0, 0, 1, -1, 0, 0], [0, 0, 0, 0, -1, 1, 1, -1, 0, 0]]
    tt = np.array(tt)
    extra_matrix = np.vstack([extra_matrix, tt])
    basis_matrix = np.concatenate([basis_matrix,extra_matrix],axis = 0)
    # permutations
    permutations  = get_permutations(n)

    # get permutations we will loop in algoritm
    candidates = set(range(1,n))

    # predecessors
    predecessors = generate_predecessors(original_basis, extra_matrix, p_matrix, permutations)

    print('predecessors done')
    # first_order_logics
    logics = generate_logics(original_basis, extra_matrix, p_matrix, permutations)
    print('logics done')

    start = time.time()
    path= [0]
    trie_dfs(original_basis, set([]), p_matrix, extra_matrix, candidates, path, ret,permutations,predecessors,logics,file_name)
    #time.time() - start

    #with open(file_name,'a') as file:
    #    file.write(str(time.time()-start)+'\n')

