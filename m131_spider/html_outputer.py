__author__ = 'Gallon'
# coding:utf-8

class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)
        for data in self.datas:
            print(data['title'])
            print(data['img_src'])

    def output_html(self):
        # 文件写权限 并更改编码格式utf-8 [重要]
        fout = open('output.html', 'w', encoding="utf-8")

        fout.write("<html>")
        fout.write("<head>")
        # 添加页面头标签的编码格式 [用于浏览器识别？]
        fout.write('<meta http-equiv="content-type" content="text/html;charset=utf-8">')
        fout.write("</head>")

        fout.write("<body>")
        fout.write("<table>")

        for data in self.datas:
            print(data['title'])
            print(data['img_src'])
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['title'])
            fout.write("<td>%s</td>" % data['img_alt'])
            fout.write("<td>%s</td>" % data['img_src'])
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")

        fout.close()
