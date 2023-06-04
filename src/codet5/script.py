import sys
import json
import re

# 获取命令行参数
input_string = sys.argv[1]

# 解析字符串为字典
data = json.loads(input_string)

# 提取代码1和代码2
code1 = data['input'].strip()
code2 = data['output'].strip()


# 将换行符改为 Linux 环境下的换行符
#code1 = code1.replace('\n', '\\n')
#code2 = code2.replace('\n', '\\n')

# 拼接代码1和代码2
result = code1+code2

# 将结果写入文件
with open('test.go', 'w') as f:
    f.write(result)

# 输出成功消息
print("拼接后的字符串已写入 test.go 文件。")



# 定义要替换的包名
new_package_name = 'main'

# 读取 test.go 文件内容
with open('test.go', 'r') as file:
    content = file.read()

# 使用正则表达式匹配并替换包名
pattern = r'package\s+\w+'
content = re.sub(pattern, f'package {new_package_name}', content)

# 将替换后的内容写入 test.go 文件
with open('test.go', 'w') as file:
    file.write(content)

# 输出成功消息
print("包名已替换为 'main'。")


