# 爬取豆瓣Top250书单
import urllib.request
from bs4 import BeautifulSoup


# 获取容器html
def get_html(url):
    web = urllib.request.urlopen(url)
    bsObject = BeautifulSoup(web, "html.parser")
    data = bsObject.find("div", id="wrapper")
    return data


# 提取元素value
def get_all(data):
    data = data.find_all("table")
    list = []
    for link in data:
        name = link.find("div", class_="pl2").find("a").get_text().replace(" ", "").replace("\n", "")
        author = link.find("p", class_="pl").get_text().split("/")[0].replace(" ", "")
        score = link.find("span", class_="rating_nums").get_text().replace(" ", "")
        peopleNum = link.find("span", class_="pl").get_text().replace(" ", "").replace("(", "").replace(")", "").replace("\n", "")
        try:
            remark = link.find("span", class_="inq").get_text().replace(" ", "").replace("\n", "")
        except:
            remark = "暂无评价"

        list.append({"name": name, "author": author, "score": score, "peopleNum": peopleNum, "remark": remark})
        # with open("D://book.txt", "a+", encoding="UTF-8") as f:
        #     f.write(name+" "+author+" "+score+" "+peopleNum+" "+remark+"\r\n")
    return list


# 写入html文件
def output_html(data):
    fout = open("output.html", mode="w", encoding="utf-8")
    fout.write("<head>")
    fout.write("<meta charset='utf-8'>")
    fout.write("</head>")
    fout.write("<html>")
    fout.write("<body>")
    fout.write("<table border=1><tr><th>书籍名称</th><th>作者</th><th>评分</th><th>评价人数</th><th>评论</th></tr>")
    for e in data:
        fout.write("<tr>")
        for tdContent in e:
            fout.write("<td>")
            fout.write(e[tdContent])
            fout.write("</td>")
        fout.write("</tr>")
    fout.write("</table>")
    fout.write("</body>")
    fout.write("</html>")


if __name__ == "__main__":
    url = 'https://book.douban.com/top250?start='
    arr = []
    for num in range(10):
        # 豆瓣每页数量25个
        url2 = url + str(num * 25)
        arr.extend(get_all(get_html(url2)))
    output_html(arr)

