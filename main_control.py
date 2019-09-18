import sys
import os


help_info = """
-folder 查找目标文件夹，爬取其目录下的所有doc和docx文件，参数后面写上若干个文件夹名(支持正则表达式)
-file 用正则表达式爬取硬盘上所有匹配文件，参数后面写上若干个正则表达式
-both 前两者的结合体，格式为: -both [文件夹名个数] [若干个文件夹名，用空格隔开] [若干个文件名，用空格隔开]
若不带任何参数，则默认爬取硬盘上所有的doc和docx文件

不会爬取该程序所在的盘符，爬取的文件放在该程序所在目录下的doc文件夹中

P.S. 如果参数中包含了中文，则需要把bat文件的编码改为ANSI
"""


def output_log(args):
    with open("log.txt", "a") as f:
        for arg in args:
            f.write(arg + "\n")


def make_dir():
    my_path = os.path.join(os.getcwd(), "doc")
    if not os.path.isdir(my_path):
        os.mkdir(my_path)


if __name__ == '__main__':
    print(sys.argv)
    make_dir()
    args = [s for s in sys.argv]
    output_log(args)

    if len(sys.argv) == 1:
        import copy_all_files
        copy_all_files.main((r"\.doc$", r"\.docx$"))
    else:
        if sys.argv[1] == "-folder" and len(sys.argv) > 2:
            import copy_target_folder
            copy_target_folder.main(sys.argv[2:], (r"\.doc$", r"\.docx$"))
        elif sys.argv[1] == "-file" and len(sys.argv) > 2:
            import copy_all_files
            copy_all_files.main(sys.argv[2:])
        elif sys.argv[1] == "-both" and len(sys.argv) > 4:
            import copy_target_folder
            copy_target_folder.main(sys.argv[3: 3 + int(sys.argv[2])], sys.argv[3 + int(sys.argv[2]):])
        elif sys.argv[1] == "-help":
            print(help_info)
            input()
        else:
            print("参数有误")
