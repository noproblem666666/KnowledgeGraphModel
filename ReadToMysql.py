import pymysql
import json

class ReadToMysql:
    def __init__(self):
        # 要读取的文件位置
        self.entity_filePath = "C:\\Users\\maccree\\Desktop\\大语言模型和知识图谱实验\\尝试分多个机器人抽取\\抽取实体，实体出处以及描述的机器人\\提取出的实体对象与相应的描述.txt"
        self.relation_filePath = "C:\\Users\\maccree\\Desktop\\大语言模型和知识图谱实验\\尝试分多个机器人抽取\\抽取实体关系的机器人\\抽取出的实体关系.txt"
        self.event_filePath = "C:\\Users\\maccree\\Desktop\\大语言模型和知识图谱实验\\尝试分多个机器人抽取\\抽取实体与相关事件的机器人\\抽取出的事件以及相关实体.txt"
        # 连接数据库需要的信息
        self.password = "lzg19981202"
        self.host = "localhost"
        self.user = "root"
        self.db = "knowledge_graph"
        self.entity_table_name = "ent_desc"
        self.relation_table_name = "ent_relation"
        self.event_table_name = "event"
        # 存储读取出的插入数据
        self.entity_data = []
        self.relation_data = []
        self.event_data = []

    def read_entity_txt(self):
        # 每个放入数组中的单条插入数据
        title = ""
        type = "knowledgeEntity"
        name = ""
        description = ""
        with open(self.entity_filePath, 'r', encoding='utf-8') as file:
            for line in file:
                if "标题" in line:
                    title = line.split(":")[-1].strip()
                if "实体名称" in line:
                    name = line.split(":")[-1].strip()
                if "描述" in line:
                    description = line.split(":")[-1].strip()
                if title and name and description:
                    single_data = {"title": title, "name": name, "description": description, "type": type}
                    self.entity_data.append(single_data)
                    name = ""
                    description = ""

    def read_relation_txt(self):
        entity_from = ""
        relation = ""
        entity_to = ""
        with open(self.relation_filePath, 'r', encoding='utf-8') as file:
            for line in file:
                if "-" in line:
                    entity_to = line.split("-")[-1].strip()
                    relation = line.split("-")[-2].strip()
                    entity_from = line.split("-")[-3].strip()
                if entity_to and relation and entity_from:
                    single_data = {"entity_from": entity_from, "relation": relation, "entity_to": entity_to}
                    self.relation_data.append(single_data)
                    entity_to = ""
                    relation = ""
                    entity_from = ""

    def read_event_txt(self):
        # 每个放入数组中的单条插入数据
        event_name = ""
        entity_names = ""
        with open(self.event_filePath, 'r', encoding='utf-8') as file:
            for line in file:
                if "事件" in line:
                    event_name = line.split(":")[-1].strip()
                if "实体" in line:
                    entity_names = line.split(":")[-1].strip()
                if event_name and entity_names:
                    single_data = {"event_name": event_name, "entity_names": entity_names}
                    self.event_data.append(single_data)
                    entity_names = ""
                    event_name = ""

    def entity_insert_db(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        for item in self.entity_data:
            sql = f"INSERT INTO {self.entity_table_name} (entity_name, description, entity_type, title) VALUES ('{item['name']}', '{item['description']}', '{item['type']}','{item['title']}')"
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                print("插入失败")
                db.rollback()
        cursor.close()
        db.close()

    def relation_insert_db(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        for item in self.relation_data:
            sql = f"INSERT INTO {self.relation_table_name} (entity_from, relation, entity_to) VALUES ('{item['entity_from']}', '{item['relation']}', '{item['entity_to']}')"
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                print("插入失败")
                db.rollback()
        cursor.close()
        db.close()

    def event_insert_db(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        for item in self.event_data:
            sql = f"INSERT INTO {self.event_table_name} (event_name, entity_names) VALUES ('{item['event_name']}', '{item['entity_names']}')"
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                print("插入失败")
                db.rollback()
        cursor.close()
        db.close()

    def json_entity_json(self, data):
        # 每个放入数组中的单条插入数据
        title = "计算机组成原理"
        jsons = json.loads(data)
        for item in jsons:
            name = item.get("entity", "").strip()
            type = item.get("type", "").strip()
            description = item.get("description", "").strip()
            single_data = {"title": title, "name": name, "description": description, "type": type}
            self.entity_data.append(single_data)
            print(single_data)


if __name__ == '__main__':
    r = ReadToMysql()
    r.read_event_txt()
    r.event_insert_db()
