import numpy as np
#计算改正数条件方程
#把角度转换成弧度再放进来
# n=6
# t=3
n = int(input('这里输入总观测数:'))
t = int(input('这里输入必要观测数:'))
r = n - t #多余观测个数
# A=[[1,0,0,1,1,1],
#    [0,1,1,0,-1,-1],
#    [1,1,0,0,0,0]]
# A =np.array(A)
# measurementsList = [14.301,17.074,-20.220,-11.159,12.821,-15.961]
sigma0 = 5
Q_num=[2.2,3.1,2.8,3.7,2.7,2.1]
A = np.zeros((r,n))#初始化系数矩阵
print(f'A:{A}')
#把建立的函数模型的系数给输入到A中
for line in range(r):
    lines = input("这里输入A矩阵的每一行以空格为界限,输入完一行之后回车:").split(' ')
    lines =[float(x) for x in lines]
    for row in range(n):
        A[line][row] = lines[row]
print(f'A:{A}')
#求w矩阵，通过闭合差来求
measurementsList = input('这里输入所有测量值,序号从小到大,以空格为界限').split(' ')#测量值表
measurementsList = [float(x) for x in measurementsList]
closure_error = 0
constant_value = 0
W = np.zeros((r,1))#初始化闭合差矩阵
for line in range(r):
    constant_value = float(input("输入有可能存在的常数值,没有写0(如果有负号记得带上符号)"))
    closure_error = 0
    for row in range(n):
        closure_error += A[line][row]*measurementsList[row]
    closure_error += constant_value
    W[line][0] = closure_error
print(f'W:{W}')
sigma0 = float(input('这里输入sigma0的值,一般取1:'))
Q_num =input('这里输入每一项的方差值').split(' ')
L = np.zeros((n,1))
for line in range(n):
    L[line][0] = float(measurementsList[line])
print(f'L:{L}')
Q_num =[float(x)/sigma0 for x in Q_num]
Q = np.diag(Q_num)#初始化协因数阵
print(f'Q:{Q}')
N_aa = np.zeros((r,r))
N_aa = A @ Q @ A.T
print(f'N_aa:{N_aa}')
K = -np.linalg.inv(N_aa) @ W
print(f'K:{K}')
V = Q @ A.T @ K#计算最后的平差值
print(f'V:{V}')
L_adjustment = np.add(L,V)
print(f'L_adjustment:{L_adjustment}')
#检验工作
Check_value = A @ V + W
print(f'Check_value:{Check_value}')
#单位权中误差的估值
P = np.linalg.inv(Q)
sigma0_hat = np.sqrt((V.T @ P @ V)/r)
print(f'sigma0_hat:{sigma0_hat}')
Q_hhat_hhat = Q - Q @ A.T @ np.linalg.inv(N_aa) @ A @ Q
print(f'Q_hhat_hhat:{Q_hhat_hhat}')
exit = input('按任意键退出')