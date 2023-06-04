import re

def parse_function_declaration(declaration):
    # 提取函数名
    function_name = re.findall(r'func\s+([a-zA-Z_]\w*)\(', declaration)
    if function_name:
        function_name = function_name[0]

    # 提取参数列表
    parameters = re.findall(r'\((.*?)\)', declaration)
    if parameters:
        parameters = parameters[0]
    else:
        return None, None, None

    # 分割参数列表，并提取参数名称和数据类型
    params = re.findall(r'(\w+)\s+(\w+)', parameters)
    if params:
        param_names, param_types = zip(*params)
    else:
        param_names, param_types = [], []

    return function_name, len(param_names), param_types


def get_last_function_info(filename):
    with open(filename, 'r') as file:
        content = file.read()

        # 提取import语句
        import_statements = re.findall(r'^\s*import\s+\((.*?)\)', content, re.MULTILINE | re.DOTALL)
        # 如果需要访问import语句，可以在这里处理import_statements列表

        # 提取函数定义
        function_declarations = re.findall(r'func\s+\w+\(.*?\)[^{]*{', content, re.MULTILINE | re.DOTALL)

        if function_declarations:
            # 获取最后一个函数的声明
            last_function_declaration = function_declarations[-1]
            # 解析函数声明，获取函数名、参数个数和参数类型
            function_name, param_count, param_types = parse_function_declaration(last_function_declaration)

            return function_name, param_count, param_types

    return None, None, None


# 指定Go源文件的路径
filename = 'test.go'

# 调用函数获取最后一个函数的信息
last_function_name, param_count, param_types = get_last_function_info(filename)

if last_function_name:
    print(f"Last function name: {last_function_name}")
    print(f"Parameter count: {param_count}")
    print(f"Parameter types: {', '.join(param_types)}")
else:
    print("No function found in the file.")

