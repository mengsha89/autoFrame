# coding=utf-8
# author:ss

import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator


def readPDF(pdf_file, password=''):
    fp = open(pdf_file, 'rb')
    # 创建一个与文档相关联的解释器
    parser = PDFParser(fp)
    # PDF文档对象
    doc = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    # 链接解释器和文档对象
    parser.set_document(doc)
    # doc.set_paeser(parser)
    # 初始化文档
    # doc.initialize("")
    # 创建PDF资源管理器
    resource = PDFResourceManager()
    # # 创建一个pdf设备对象
    # device = PDFDevice(resource)
    # 参数分析器
    laparam = LAParams()
    # 创建一个聚合器
    device = PDFPageAggregator(resource, laparams=laparam)
    # 创建PDF页面解释器
    interpreter = PDFPageInterpreter(resource, device)
    # 使用文档对象得到页面集合
    for page in PDFPage.create_pages(doc):
        # 使用页面解释器来读取
        interpreter.process_page(page)
        # 使用聚合器来获取内容
        layout = device.get_result()
        texts = []
        for out in layout:
            if hasattr(out, "get_text"):
                text = out.get_text()
                texts.append(text)
    print texts


def report_content(report_name):
    filename = os.path.join('..\\', 'reports', report_name)
    lines = []
    f = open(filename, "rb")
    while True:
        line = f.readline()
        if line:
            if 'id="chartline"' in line:
                line = line.replace("50%", "400px")
                continue
            elif 'id="chart"' in line:
                line = line.replace("50%", "400px")
                continue
            elif line.strip() == 'var option = {':
                lines.append(line)
                lines.append("\t\t\t\tanimation: false,\n")
                continue
            elif line.strip() == "<pre>":
                lines.append(line)
                while True:
                    line = f.readline()
                    if line.strip() == "</pre>":
                        lines.append(line)
                        break
            lines.append(line)
        else:
            break

    f.close()
    fp = open(r"..\reports\report.html", "w")
    fp.writelines(lines)
    fp.close()


if __name__ == '__main__':
    readPDF("..\utils\out.pdf")