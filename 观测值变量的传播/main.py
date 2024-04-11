import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt

# 读取Excel文件
xls = pd.ExcelFile('data.xlsx')

# 从第一张工作表的第一行读取所有变量名
variables_df = pd.read_excel(xls, sheet_name=0, header=None, nrows=1)
variable_names = variables_df.values.flatten().tolist()  # 变量名列表
symbols = sp.symbols(variable_names)  # 声明SymPy符号
symbols_dict = dict(zip(variable_names, symbols))  # 变量名到SymPy符号的映射

# 更新的convert_df_to_sympy函数
def convert_df_to_sympy(df, symbols_dict):
    sympy_matrix = []
    for _, row in df.iterrows():
        sympy_row = [sp.sympify(expr, locals=symbols_dict) for expr in row if pd.notnull(expr)]
        sympy_matrix.append(sympy_row)
    return sp.Matrix(sympy_matrix)

# 读取并转换系数矩阵K1（位于第二张工作表）
K1_df = pd.read_excel(xls, sheet_name=1, header=None)
K1 = convert_df_to_sympy(K1_df, symbols_dict)

# 读取并转换系数矩阵K2（位于第四张工作表）
K2_df = pd.read_excel(xls, sheet_name=3, header=None)
K2 = convert_df_to_sympy(K2_df, symbols_dict)

# 读取并转换方差阵D_LL（位于第三张工作表）
D_LL_df = pd.read_excel(xls, sheet_name=2, header=None)
D_LL = convert_df_to_sympy(D_LL_df, symbols_dict)

# 计算D11\D12\D22
D_K1_K2 = K1 * D_LL * K2.T
D_K1_K1 = K1 * D_LL * K1.T
D_K2_K2 = K2 * D_LL * K2.T
# 将SymPy矩阵转换为Pandas DataFrame，以便写入Excel
result_file = 'D1_2.xlsx'



latex_code_D_K1_K2 = sp.latex(D_K1_K2)
latex_code_D_K1_K1 = sp.latex(D_K1_K1)
latex_code_D_K2_K2 = sp.latex(D_K2_K2)
data = {
    "矩阵名称": ["D_K1_K2", "D_K1_K1", "D_K2_K2"],
    "对应LaTeX代码": [latex_code_D_K1_K2, latex_code_D_K1_K1, latex_code_D_K2_K2]
}

# 使用字典创建DataFrame
df = pd.DataFrame(data)
result_file = '矩阵LaTeX代码.xlsx'

# 将DataFrame写入Excel文件
df.to_excel(result_file, index=False)
print(f'D_K1_K2')
print(latex_code_D_K1_K2)
print(f'D_K1_K1')
print(latex_code_D_K1_K1)
print(f'D_K2_K2')
print(latex_code_D_K2_K2)
print(f'D1_2 has been successfully written to {result_file}')