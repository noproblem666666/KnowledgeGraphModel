from py2neo import Graph, Node, Relationship
import pymysql


class MysqlToNeo4j:
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
        self.entity_table_name = "entity"
        self.relation_table_name = "relation"

    def search_entity_count(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        try:
            cursor.execute(
                f"SELECT entity_name,count(*) as count FROM {self.entity_table_name} group by entity_name order by count desc")
            # 获取查询结果
            result = cursor.fetchall()
        finally:
            cursor.close()
            db.close()
        return result

    def search_entity_by_name(self, name):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.entity_table_name} where entity_name = \"{name}\"")
            # 获取查询结果
            result = cursor.fetchall()
        finally:
            cursor.close()
            db.close()
        print(result)
        return result

    def search_relation(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.relation_table_name}")
            # 获取查询结果
            result = cursor.fetchall()
        finally:
            cursor.close()
            db.close()
        return result

    def search_mysql(self):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.entity_table_name}")
            # 获取查询结果
            result = cursor.fetchall()
            # 将结果存储到数组中
            for row in result:
                self.entity_data.append(row)

            cursor.execute(f"SELECT * FROM {self.relation_table_name}")
            # 获取查询结果
            result = cursor.fetchall()
            # 将结果存储到数组中
            for row in result:
                self.relation_data.append(row)

        finally:
            cursor.close()
            db.close()
        print(self.entity_data)
        print(self.relation_data)
        print(self.event_data)

    def insert_entity(self, graph, information, type):
        # 新版连接格式不太一样
        for item in information:
            node = Node(type, name=item[1], description=item[2], title=item[3], paragraphs_id=item[4], position=item[5],
                        file_name=item[6])
            try:
                graph.create(node)
                print(f"成功插入一个知识结点{item[1]}")
            except Exception as e:
                print("插入到neo4j时产生错误：", e)

    def insert_relation(self, graph, relations):
        for relation in relations:
            #后面必须跟.first(),否则是一个node链表而不是node类型，即使查找出来只有一个node
            nodes_from = graph.nodes.match(name=relation[1], paragraphs_id=int(relation[5])).first()
            nodes_to = graph.nodes.match(name=relation[3], paragraphs_id=int(relation[5])).first()
            temp = relation[2]
            relation_type1 = temp.split("--")[0]
            relation_type2 = temp.split("--")[1]
            relation_specific = temp.split("--")[2]
            properties = {'simple': relation_type2, 'specific': relation_specific}
            nodes = [nodes_from, str(relation_type1), nodes_to]
            if nodes_from and nodes_to:
                try:
                    rel = Relationship(*nodes, **properties)
                    print(f"成功插入一条关系")
                    graph.merge(rel)
                except Exception as e:
                    print("插入到neo4j时产生错误：", e)
            else:
                print("未找到对应的结点")
            # if len(nodes) == 0:
            #     node = Node("关系指向", name=relation[3], start=relation[1])
            #     try:
            #         graph.create(node)
            #         print(f"成功插入一个关系指向结点{relation[3]}")
            #     except Exception as e:
            #         print("插入到neo4j时产生错误：", e)
            #         nodes = graph.nodes.match(name=relation[3])
            # nodes = graph.nodes.match(name=relation[1])
            # if len(nodes) == 0:
            #     node = Node("关系指向", name=relation[1], end=relation[3])
            #     try:
            #         graph.create(node)
            #         print(f"成功插入一个关系指向结点{relation[1]}")
            #     except Exception as e:
            #         print("插入到neo4j时产生错误：", e)
            #
            # from_node = graph.nodes.match(name=relation[1]).first()
            # to_node = graph.nodes.match(name=relation[3]).first()
            # if from_node and to_node:
            #     try:
            #         rel = Relationship(from_node, relation[2], to_node)
            #         print(f"成功插入一条关系{relation[1]} - {relation[2]} - {relation[3]}")
            #         graph.create(rel)
            #     except Exception as e:
            #         print("插入到neo4j时产生错误：", e)
            # else:
            #     print("One or both nodes not found.")

    def insert_event_relation(self, graph):
        for event in self.event_data:
            entities = event[2].split("：")[-1].split("，")
            event_node = graph.nodes.match(name=event[1].split("：")[-1]).first()
            for entity in entities:
                entity_node = graph.nodes.match(name=entity).first()
                if entity_node and event_node:
                    try:
                        rel = Relationship(entity_node, "相关于", event_node)
                        print(f"成功插入一条关系{entity_node} - 相关于 - {event_node}")
                        graph.create(rel)
                    except Exception as e:
                        print("插入到neo4j时产生错误：", e)

    def search_node(self, name, graph):
        alice = graph.nodes.match(name=name).first()

        # 检查是否找到节点
        if alice:
            print("Node:")
            print(alice)
            # 查找与Alice有关的所有边和节点
            relationships = graph.match(nodes=[alice])
            for rel in relationships:
                print("Relationship:")
                print(rel)
                print("Start node:")
                print(rel.start_node)
                print("End node:")
                print(rel.end_node)


if __name__ == '__main__':
    r = MysqlToNeo4j()
    graph = Graph("http://localhost:7474", auth=("neo4j", "lzg19981202"), name="deepseek20241009")
    relations = r.search_relation()
    r.insert_relation(graph, relations)
    # entity_names = r.search_entity_count()
    # for entity_name in entity_names:
    #     count = entity_name[1]
    #     type = ""
    #     if count >= 10:
    #         type = "一级知识点"
    #     elif count >= 5:
    #         type = "二级知识点"
    #     else:
    #         type = "三级知识点"
    #     information = r.search_entity_by_name(entity_name[0])
    #     r.insert_entity(graph, information, type)

    # while True:
    #     # Todo：把结点查询出的消息放入大模型，让大模型生成相关回答
    #     user_input = input("请输入要查询的相关结点: ")
    #     r.search_node(user_input, graph)
