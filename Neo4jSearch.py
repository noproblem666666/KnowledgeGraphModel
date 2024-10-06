from py2neo import Graph, Node, Relationship
import pymysql


class Neo4jSearch:
    def __init__(self):
        self.uri = "bolt://localhost:7687"
        self.entity_data = []
        self.relation_data = []
        self.event_data = []
        # 连接数据库需要的信息
        self.password = "lzg19981202"
        self.host = "localhost"
        self.user = "root"
        self.db = "knowledge_graph"
        self.entity_table_name = "ent_desc"
        self.relation_table_name = "ent_relation"
        self.event_table_name = "event"

    def search_node_information(self, names, graph):
        result_information = []
        for name in names:
            information = {}
            node = graph.nodes.match(name=name).first()
            # 获取节点的所有属性
            properties = dict(node)
            # 查找与该节点相连的其他节点
            relationships = graph.match((node, None), r_type=None)
            relationships1 = graph.match((None, node), r_type=None)
            connected_nodes = []
            for rel in relationships:
                # 获取关系的另一端的节点
                connected_node = rel.end_node if rel.start_node == node else rel.start_node
                connected_nodes.append(connected_node)
            information["node"] = node
            information["connected nodes"] = connected_nodes
            information["relationships"] = relationships
            information["relationships1"] = relationships1
            result_information.append(information)
        return result_information
