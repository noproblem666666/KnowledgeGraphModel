from py2neo import Graph, Node, Relationship
import pymysql


class MysqlSearch:
    def __init__(self):
        self.uri = "bolt://localhost:7687"
        self.entity_data = []
        self.relation_data = []
        self.event_data = []
        # 连接数据库需要的信息
        self.password = "###"
        self.host = "localhost"
        self.user = "root"
        self.db = "knowledge_graph"
        self.entity_table_name = "ent_desc"
        self.relation_table_name = "ent_relation"
        self.event_table_name = "event"

    def search_node_name(self):
        result_name = []
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT entity_name FROM {self.entity_table_name}")
            # 获取查询结果
            result = cursor.fetchall()
            # 将结果存储到数组中
            for row in result:
                result_name.append(row[0])

            cursor.execute(f"SELECT entity_from FROM {self.relation_table_name}")
            # 获取查询结果
            result = cursor.fetchall()
            # 将结果存储到数组中
            for row in result:
                result_name.append(row[0])

            cursor.execute(f"SELECT event_name FROM {self.event_table_name}")
            # 获取查询结果
            result = cursor.fetchall()
            # 将结果存储到数组中
            for row in result:
                result_name.append(row[0])
        finally:
            cursor.close()
            db.close()
        # print(result_name)
        return result_name

