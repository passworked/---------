import pandas as pd
import numpy as np

# 读取Excel文件
xls = pd.ExcelFile('data.xlsx')

# 读取A矩阵
A_df = pd.read_excel(xls, sheet_name=0, header=None)
A = A_df.to_numpy()

# 读取测量值
measurements_df = pd.read_excel(xls, sheet_name=1, header=None)
measurementsList = measurements_df.iloc[0,:].tolist()

# 读取方差值
Q_num_df = pd.read_excel(xls, sheet_name=2, header=None)
Q_num = Q_num_df.iloc[0,:].tolist()

# 读取sigma0的值
sigma0_df = pd.read_excel(xls, sheet_name=3, header=None)
sigma0 = float(sigma0_df.iloc[0,0])

# 这里计算n和t的值
n = A.shape[1] # 总观测数为A矩阵的列数
t = A.shape[0] # 必要观测数为A矩阵的行数
r = n - t
# 接下来是使用这些变量的计算部分
# 初始化一些必要的矩阵和变量，根据具体情况调整
L = np.array([[float(measurement)] for measurement in measurementsList])
Q = np.diag([float(q)/sigma0 for q in Q_num])
N_aa = A @ Q @ A.T
W = np.zeros((r,1))#初始化闭合差矩阵
for line in range(r):
    constant_value = float(input("输入有可能存在的常数值,没有写0(如果有负号记得带上符号)"))
    closure_error = 0
    for row in range(n):
        closure_error += A[line][row]*measurementsList[row]
    closure_error += constant_value
    W[line][0] = closure_error
K = -np.linalg.inv(N_aa) @ W
V = Q @ A.T @ K#计算最后的平差值
L_adjustment = np.add(L,V)
#检验工作
Check_value = A @ V + W
#单位权中误差的估值
P = np.linalg.inv(Q)
sigma0_hat = np.sqrt((V.T @ P @ V)/r)
Q_hat_hat = Q - Q @ A.T @ np.linalg.inv(N_aa) @ A @ Q
print(f'A:{A}')
print(f'L:{L}')
print(f'W:{W}')
print(f'Q:{Q}')
print(f'N_aa:{N_aa}')
print(f'K:{K}')
print(f'V:{V}')
print(f'sigma0_hat:{sigma0_hat}')
print(f'Q_hat_hat:{Q_hat_hat}')
print(f'L_adjustment:{L_adjustment}')
print(f'Check_value:{Check_value}')
exit = input('按任意键退出')
writer = pd.ExcelWriter('output_data.xlsx', engine='xlsxwriter')

# 将每个输出变量转换为DataFrame，然后写入Excel的不同工作表中
pd.DataFrame(A).to_excel(writer, sheet_name='A', index=False, header=False)
pd.DataFrame(L).to_excel(writer, sheet_name='L', index=False, header=False)
pd.DataFrame(W).to_excel(writer, sheet_name='W', index=False, header=False)
pd.DataFrame(Q).to_excel(writer, sheet_name='Q', index=False, header=False)
pd.DataFrame(N_aa).to_excel(writer, sheet_name='N_aa', index=False, header=False)
pd.DataFrame(K).to_excel(writer, sheet_name='K', index=False, header=False)
pd.DataFrame(V).to_excel(writer, sheet_name='V', index=False, header=False)
pd.DataFrame(sigma0_hat).to_excel(writer, sheet_name='sigma0_hat', index=False, header=False)
pd.DataFrame(Q_hat_hat).to_excel(writer, sheet_name='Q_hat_hat', index=False, header=False)
pd.DataFrame(L_adjustment).to_excel(writer, sheet_name='L_adjustment', index=False, header=False)
pd.DataFrame(Check_value).to_excel(writer, sheet_name='Check_value', index=False, header=False)

# 保存和关闭写入器
writer.close()
# 以下计算可以根据实际情况进行调整和补充
# 注意：原代码中的用户输入部分现已被替换为从Excel读取数据

# 继续进行原代码中的计算流程...

 