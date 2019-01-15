# coding=utf-8
# author:ss

import datetime
import os
import re

file_static = "statistics.txt"
static_file = os.path.join('..\\', 'reports', file_static)


def get_specified_date(days=5):
    """
    获取包含当天在内几天数据
    :param days:
    :return:
    """
    # 获取当前时间
    today = datetime.datetime.now()
    date_list = []
    # 计算偏移量
    for i in range(days-1, -1, -1):
        offset = datetime.timedelta(days=i)
        re_date = (today-offset).strftime('%Y-%m-%d')
        date_list.append(re_date)
    print date_list
    return date_list


def find_files(data_list):
    report_dir = os.path.join('..\\', 'reports')
    files = os.listdir(report_dir)
    files_dicts = {}
    for f in files:
        if len(f.split("_")) == 1:
            continue
        day = f.split("_")[1]
        if day in data_list:
            # print f
            files_dicts[day] = f
    print files_dicts
    f_dicts = files_dicts.copy()
    # 判断统计文件是否存在
    if os.path.exists(static_file):
        with open(static_file, "a+") as f:
            files = f.readlines()
            line = files[-1].split()
            day = line[0]
            file_name = line[1]
            delete_date = []
            if day in date_list:
                if file_name == files_dicts[day]:
                    
                    last_index = date_list.index(day)
                    delete_date = date_list[:last_index]
            for d in delete_date:
                files_dicts.pop(d)
    print files_dicts
    return files_dicts, f_dicts


def gene_statics(file_dicts):
    file_num = len(file_dicts)
    if file_num < 2:
        f, = file_dicts.values()
        print f
    else:
        files = sorted(file_dicts.items(), key=lambda item: item[0])
        print files
        wars = []
        dangers = []
        sucs = []
        for day, report_name in files:
            filename = os.path.join('..\\', 'reports', report_name)
            war = "0"
            danger = "0"
            suc = "0"
            f = open(filename, "rb")
            while True:
                line = f.readline()
                # 读取报告的失败、错误、成功用例数
                if line:
                    if 'btn btn-warning"' in line:
                        war = line.split()[-2]
                        wars.append(int(war))
                    # elif 'btn btn-danger"' in line:
                        line = f.readline()
                        danger = line.split()[-2]
                        dangers.append(int(danger))
                    # elif 'btn btn-success' in line:
                        line = f.readline()
                        suc = line.split()[-2]
                        sucs.append(int(suc))
                        break
                else:
                    break

            f.close()
            # 判断统计文件是否存在
            if os.path.exists(static_file):
                with open(static_file, "a+") as f:
                    f.readline()
                    f.seek(f.tell())
                    # f.write(head)
                    f.write(day+"\t"+report_name+"\t\t"+war+"\t\t"+danger+"\t\t"+suc+"\n")
            else:
                with open(static_file, "a+") as f:
                    f.write("日期"+"\t\t\t\t\t\t"+"文件名"+"\t\t\t\t\t"+"错误"+"\t\t"+"失败"+"\t\t"+"成功"+"\n")
                    f.write(day + "\t" + report_name + "\t\t" + war + "\t\t" + danger + "\t\t" + suc + "\n")

        print wars, dangers, sucs


def gene_report(date_list, file_dicts):
    wars = []
    dangers = []
    sucs = []
    with open(static_file, "r") as f:
        record = f.readlines()
        for rec in record[1:]:
            fields = rec.split()
            war = fields[2]
            wars.append(war)
            danger = fields[3]
            dangers.append(danger)
            suc = fields[4]
            sucs.append(suc)
    print sucs
    files = sorted(file_dicts.items(), key=lambda item: item[0])
    # 生成最近5天比对数据
    last_day, report_name = files[-1]
    filename = os.path.join('..\\', 'reports', report_name)
    lines = []
    f = open(filename, "rb")
    while True:
        line = f.readline()
        if line:
            x_line = "[' 第一次','第二次','第三次','第四次','第五次']"
            if "'第五次'" in line:
                line = line.replace(x_line, str(date_list))
            elif r'//成功' in line:
                line = re.sub("\[\d+\]", str(sucs), line)
            elif r'//失败' in line:
                line = re.sub("\[\d+\]", str(dangers), line)
            elif r'//错误' in line:
                line = re.sub("\[\d+\]", str(wars), line)
            lines.append(line)
        else:
            break
    f.close()
    fp = open(r"..\reports\report-comp.html", "w")
    fp.writelines(lines)
    fp.close()


if __name__ == '__main__':
    date_list = get_specified_date()
    dic, f_dicts = find_files(date_list)
    gene_statics(dic)
    gene_report(date_list, f_dicts)
