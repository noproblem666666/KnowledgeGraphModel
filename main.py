# This is a sample Python script.
import pymysql

from LLMapi import LLMapi
from MysqlToNeo4j import MysqlToNeo4j
from py2neo import Graph, Node, Relationship
from MysqlSearch import MysqlSearch
from Neo4jSearch import Neo4jSearch


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def match_node(input):
    # Todo：提升知识结点识别，设计知识结点比重函数，数据库存储相关参数
    result_name = MysqlSearch().search_node_name()
    result_match = []
    for name in result_name:
        if name in input and name not in result_match:
            result_match.append(name)
    print("开始寻找以下结点信息：")
    print(result_match)
    return result_match


if __name__ == '__main__':
    # Todo：比较知识图谱与RAG的文本召回
    # Todo：返回其他相关结点，帮助快速理清知识脉络
    # Todo：把文本按照实体、关系、事件结构化，从不同角度搜索，挖掘文本，结点扩散度
    graph = Graph("http://localhost:7474", auth=("neo4j", "lzg19981202"), name="neo4j")
    print("请输入查询的结点")
    has_nodes = []
    has_rel = []
    while True:
        user_input = input(": ")
        # result_match = match_node(user_input)
        result_match = [user_input]
        result_information = Neo4jSearch().search_node_information(result_match, graph)
        print(user_input + ": ")
        print(dict(result_information[0]["node"]).get("description", ""))
        after_nodes = []
        has_nodes.append(result_information[0]["node"])
        for rel in result_information[0]["relationships"]:
            if rel.start_node == result_information[0]["node"]:
                connected_node = rel.end_node
            else:
                connected_node = rel.start_node
            if connected_node in has_nodes:
                continue
            description = dict(connected_node).get("description", "")
            print(rel)
            if description:
                after_nodes.append(connected_node)
            else:
                has_nodes.append(connected_node)
            if rel not in has_rel:
                has_rel.append(rel)
        for rel in result_information[0]["relationships1"]:
            if rel.start_node == result_information[0]["node"]:
                connected_node = rel.end_node
            else:
                connected_node = rel.start_node
            if connected_node in has_nodes:
                continue
            description = dict(connected_node).get("description", "")
            print(rel)
            if description:
                after_nodes.append(connected_node)
            else:
                has_nodes.append(connected_node)
            if rel not in has_rel:
                has_rel.append(rel)
        for after_node in after_nodes:
            print("可以继续遍历以下结点：")
            print(dict(after_node)["name"])
        user_input = input(":是否总结以上主题(y/n)")
        if user_input == "y":
            content = ""
            for node in has_nodes:
                if dict(node).get("description", ""):
                    content += "\n " + dict(node).get("name", "") + ": " + dict(node).get("description", "")
            content += "\n 以上信息具有以下的关系"
            for rel in has_rel:
                content += "\n" + rel.start_node["name"] + " " + type(rel).__name__ + " " + rel.end_node["name"]
            # print(content)
            r = LLMapi()
            r.sum_stream(content)
