import json
import subprocess
import shlex
import os
import shutil
from tqdm import tqdm
import re
import operator


# 将每一条数据写入test.go
def create_test(input_string):
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
    #print("拼接后的字符串已写入 test.go 文件。")

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
    #print("包名已替换为 'main'。")


# 删除所有文件以便下一个数据开始处理
def clear():
    # 检查并删除 test.go 文件
    if os.path.isfile('test.go'):
        os.remove('test.go')
        #print("已删除 test.go 文件")

    # 检查并删除 pkgs.txt 文件
    if os.path.isfile('pkgs.txt'):
        os.remove('pkgs.txt')
        #print("已删除 pkgs.txt 文件。")

    # 检查并删除 myprogram.exe 文件
    if os.path.isfile('myprogram.exe'):
        os.remove('myprogram.exe')
        #print("已删除 myprogram.exe 文件。")

    # 检查并删除 result.txt 文件
    if os.path.isfile('result.txt'):
        os.remove('result.txt')
        #print("已删除 result.txt 文件。")
    
    # 检查并删除 somedata 目录
    if os.path.isdir('somedata'):
        shutil.rmtree('somedata')
        #print("已删除 somedata 目录。")

def cal():
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
    #print("Percentage Sum:", percentage_sum)

    return percentage_sum


def main():
    print("\n\n===================================================START FUZZING===================================================\n\n")
    
    # 初始化空的字典，用于按覆盖率从大到小存储数据
    data_map = {}

    # 清理旧文件
    clear()
    if os.path.isfile('hello.go'):
        os.remove('hello.go')


    # 创建 hello.go 文件并写入指定代码
    hello_code = "package main\n\nfunc main(){}"
    with open('hello.go', 'w') as file:
        file.write(hello_code)


    # 输出成功消息
    #print("创建 hello.go 文件并写入指定代码。")
    
    # 读取origin_data.json文件
    with open("origin_data.json", "r") as file:
        data = file.readlines()

    # 遍历每一条数据，并作为参数调用脚本
    for line in tqdm(data):
        # 写入test.go
        line = line.strip()  # 去除行首行尾的空白字符
       # command = f"exec 2>/dev/null && python script.py '{line}'\n"
       # print(command+"\n")
       # subprocess.run(command, shell=True)
        create_test(line)

        if os.path.isfile('test.go'):
            # 执行 go list 命令并将结果写入 pkgs.txt 文件
            command = "exec 2>/dev/null && go list -f '{{.ImportPath}}' -deps . | paste -sd ',' > pkgs.txt"
            subprocess.run(command, shell=True)

            # 输出成功消息
            #print("执行 go list 命令并将结果写入 pkgs.txt 文件。")

            # 检查 pkgs.txt 文件是否存在
            if os.path.isfile('pkgs.txt'):

                # 检查 hello.go 文件是否存在
                if os.path.isfile('hello.go'):
                    # 执行 go build 命令并指定 -coverpkg 参数
                    coverpkg = "`cat pkgs.txt`"
                    build_command = f"exec 2>/dev/null && go build -o myprogram.exe -coverpkg={coverpkg} ."
                    subprocess.run(build_command, shell=True)

                    # 输出成功消息
                    #print("执行 go build 命令成功。")

                    # 检查 myprogram.exe 文件是否存在
                    if os.path.isfile('myprogram.exe'):
                        # 创建 somedata 目录
                        os.mkdir('somedata')

                        #print("已创建 somedata 目录。")

                        # 执行 myprogram.exe 命令
                        subprocess.run('exec 2>/dev/null && GOCOVERDIR=somedata ./myprogram.exe', shell=True)

                        # 执行 go tool covdata 命令并将结果写入 result.txt 文件
                        subprocess.run('exec 2>/dev/null && go tool covdata percent -i=somedata > result.txt', shell=True)

                        # 检查 result.txt 文件是否存在
                        if os.path.isfile('result.txt'):
                            # 执行 cal.py 脚本
                            #subprocess.run('python cal.py', shell=True)
                            percentage_sum=cal()
                            data_map[line] = percentage_sum  
                        else:
                            print("result.txt 文件不存在。")
                    else:
                        print("myprogram.exe 文件不存在。")
    
                else:
                    print("hello.go 文件不存在。")
            else:
                print("pkgs.txt 文件不存在。")
   
   
        else:
            print("test.go 文件不存在。")
        
        # 若覆盖率没有测试成功，则覆盖率按0计算
        if not os.path.isfile("result.txt"):
            data_map[line]=0
        
        # 清理旧文件
        clear()

        print("\n*****************************************************\n")
    
    # 按值对字典进行排序
    sorted_map = dict(sorted(data_map.items(), key=operator.itemgetter(1), reverse=True))

    # 逐行写入数据到 data.json 文件
    with open("data.json", "w") as file:
        for key in  sorted_map.keys():
            line = key + "\n"
            file.write(line)


    # 检查并删除 hello.go 文件
    if os.path.isfile('hello.go'):
        os.remove('hello.go')
        print("已删除 hello.go 文件。")
    
    print("\n\n====================================================END FUZZING====================================================\n\n")

if __name__ == '__main__':
    main()

