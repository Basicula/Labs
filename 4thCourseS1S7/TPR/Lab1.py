import numpy as np
from prettytable import PrettyTable
    
def generate(n,m):
    return (np.random.rand(n,m)*10).astype('int')

def show_input(data):    
    table = PrettyTable()
    
    table.field_names = ["X", "Y"]
    
    for i,row in enumerate(data):
        table.add_row(["x"+str(i+1), row])
    
    print(table)
    
def result_table(data):
    table = PrettyTable()
    
    n = len(data)
    
    headers = ["x/x'"]
    for i in range(n):
        headers.append("x"+str(i+1))
    headers.append("Q(x)")
    table.field_names = headers
    
    Q = float("inf")
    for i in range(n):
        row = ["x"+str(i+1)]
        for j in range(n):
            x1 = data[i]
            x2 = data[j]
            m = len(x1)
            cnt = 0
            for k in range(m):
                cnt += x2[k] > x1[k]
            row.append(cnt)
        mx = max(row[1:])
        Q = min(Q,mx)
        row.append(mx)
        table.add_row(row)
    
    print(table)
    print("Q = ",Q)

if __name__ == '__main__':
    N = 7
    M = 20
    
    data = generate(N,M)
    
    show_input(data)
    
    result_table(data)
    