import requests, re, sqlite3


class Anime1:
    def __init__(self, name):
        self.set = MyDB(name)
        self.name = name


    def save(self, list1):
        table = 'Anime1'
        columns = ['title', 'episode', 'year', 'season', 'sub', 'link']
        columns_type = ['text', 'text', 'Int', 'text', 'text', 'text']
        primary_key = F'PRIMARY KEY ({columns[0]})'
        self.set.cDB(table, columns, columns_type, primary_key)
        values_list = []
        for each in list1:
            each['title'] = F"'{each['title']}'"
            each['episode'] = F"'{each['episode']}'"
            each['season'] = F"'{each['season']}'"
            each['sub'] = F"'{each['sub']}'"
            each['link'] = F"'{each['link']}'"
            values_list.append(list(each.values()))
        self.set.wDB(table, columns, values_list)
        print('Done')


    def run(self):
        worker = GetData()
        data_list = worker.runing()
        self.save(data_list)


class GetData:
    def __init__(self):
        self.split = '</tr>'
        self.url = 'https://anime1.me/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}


    def re_html(self, html):
        p = r'<tbody class="row-hover">(.+)</tbody>'
        text_list = re.findall(p, html)[0].split(self.split)
        return text_list


    def re_text(self, text_list):
        data_list = []
        addr = 'https://anime1.me'
        p1 = r'<td class=(.+?)</td>'
        for each in text_list:
            dic1 = {}
            temp1 = re.findall(p1, each)
            if temp1 == []:
                continue
            dic1['title'] = temp1[0][:-4].split('>')[-1]
            dic1['episode'] = temp1[1].split('>')[-1]
            dic1['year'] = temp1[2].split('>')[-1]
            dic1['season'] = temp1[3].split('>')[-1]
            dic1['sub'] = temp1[4].split('>')[-1]
            dic1['link'] = addr + temp1[0][:-4].split('>')[-2].split('"')[-2]
            data_list.append(dic1)
        return data_list


    def runing(self):
        html = requests.get(self.url, headers=self.headers).text
        text_list = self.re_html(html)
        list1 = self.re_text(text_list)
        return list1


class MyDB:
    def __init__(self, name):
        self.name = name


    def cDB(self, table='example', columns=['ex_column'], colomns_type=['text'], primary_key=''):
        # create a database
        conn = sqlite3.connect(self.name)
        man = conn.cursor()
        add_time = "date TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')), "
        columns_new = ""
        for each in columns:
            columns_new += "{} {},".format(each, colomns_type[columns.index(each)])
        command = F"CREATE TABLE IF NOT EXISTS {table}({columns_new} {add_time} {primary_key})"
        man.execute(command)
        conn.commit()
        conn.close()


    def wDB(self, table='example', columns=["ex_column"], values_list=[["'ex_data'"]]):
        # write values into a database
        conn = sqlite3.connect(self.name)
        man = conn.cursor()
        columns_new = ""
        for each in columns:
            columns_new += F"{each},"
        for each in values_list:
            values_new = ""
            for i in each:
                values_new += F"{i},"
            command1 = F"INSERT OR REPLACE INTO {table}({columns_new[:-1]}) VALUES({values_new[:-1]})"
            # command2 = F"UPDATE {table} SET 'episode' = {list(values)[1]} WHERE {list(columns)[0]} = {list(values)[0]}"
            try:
                man.execute(command1)
            except sqlite3.IntegrityError as reason:
                # man.execute(command2)
                print(reason)
        conn.commit()
        conn.close()


    def rDB(self, table='example'):
        # read data from database
        conn = sqlite3.connect(self.name)
        man = conn.cursor()
        command = F"SELECT * FROM {table}"
        try:
            for each in man.execute(command):
                print(F'{each}')
        except sqlite3.OperationalError as reason:
            print(reason)
        conn.close()


    def dDB(self, table='example'):
        # delete a table in database
        conn = sqlite3.connect(self.name)
        man = conn.cursor()
        command = F"DROP TABLE '{table}'"
        try:
            man.execute(command)
            conn.commit()
            print('Delete successfully')
        except sqlite3.OperationalError as reason:
            print(reason)
        conn.close()


if __name__ == '__main__':
    anime = Anime1('anime1.db')
    anime.run()