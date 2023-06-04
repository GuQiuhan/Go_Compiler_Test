import re

# 读取 result.txt 文件
with open('result.txt', 'r') as file:
    lines = file.readlines()

# 计算百分比总和
percentage_sum = 0.0
for line in lines:
    match = re.search(r'coverage:\s*([\d.]+)%', line)
    if match:
        percentage = float(match.group(1))
        percentage_sum += percentage

# 输出百分比总和
print("Percentage Sum:", percentage_sum)

