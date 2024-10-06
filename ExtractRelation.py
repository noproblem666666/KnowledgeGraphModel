import json
import re
import pymysql

from LLMapi import LLMapi
from Prompt import Prompt


class ExtractRelation:
    def __init__(self):
        self.password = "lzg19981202"
        self.host = "localhost"
        self.user = "root"
        self.db = "knowledge_graph"
        self.paragraphs_table_name = "paragraphs"
        self.entity_table_name = "entity"
        self.relation_table_name = "relation"
        self.options = ("A. 因果关系 "
                        "B. 从属关系 "
                        "C. 定义关系 "
                        "D. 分类关系 "
                        "E. 属性关系 "
                        "F. 空间关系 "
                        "G. 时间关系 "
                        "H. 没有关系")
        self.options_A = ("A. {实体1}导致了{实体2} "
                          "B. {实体2}导致了{实体1}")
        self.options_B = ("A. {实体1}隶属于{实体2} "
                          "B. {实体2}隶属于{实体1}")
        self.options_C = ("A. {实体1}解释了{实体2} "
                          "B. {实体2}解释了{实体1}")
        self.options_D = ("A. {实体1}是{实体2}的子类 "
                          "B. {实体2}是{实体1}的子类"
                          "C. {实体1}和{实体2}是同类")
        self.options_E = ("A. {实体1}是{实体2}的属性 "
                          "B. {实体2}是{实体1}的属性")
        self.options_F = ("A. {实体1}与{实体2}在空间上相邻 "
                          "B. {实体1}与{实体2}在空间上相隔")
        self.options_G = ("A. {实体1}发生在{实体2}之前 "
                          "B. {实体2}发生在{实体1}之前")
    def search_paragraphs_by_id(self, paragraph_id):
        results = []
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.paragraphs_table_name} where id = {paragraph_id}")
            # 获取查询结果
            result = cursor.fetchall()
            # 将结果存储到数组中
            for row in result:
                results.append(row[0])
        finally:
            cursor.close()
            db.close()
        return result

    def search_entitys_by_id(self, paragraph_id):
        results = []
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.entity_table_name} where paragraphs_id = {paragraph_id}")
            # 获取查询结果
            result = cursor.fetchall()
            # 将结果存储到数组中
            for row in result:
                results.append(row[0])
        finally:
            cursor.close()
            db.close()
        # print(result_name)
        return result

    def insert_relation(self, results):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()

        try:
            for item in results:
                sql = f"INSERT INTO {self.relation_table_name} (entity_name, description, title, paragraphs_id, position, file_name) VALUES ('{item['entity']}', '{item['description']}', '{item['title']}','{item['paragraphs_id']}','{item['file_name']}','{item['paragraphs_id']}')"
                cursor.execute(sql)
                db.commit()
        except:
            print("插入失败")
            db.rollback()
        finally:
            cursor.close()
            db.close()

    def get_json(self, pre):
        i1 = pre.split("[")
        i2 = i1.split("]")
        if not i2:
            print("识别抽取结果失败，以下为抽取信息：")
            print("-------" + pre + "---------")
            return


if __name__ == '__main__':
    count = 0
    paragraph_id = 0
    while paragraph_id < 600:
        paragraph_id = paragraph_id + 1
        e = ExtractRelation()
        l = LLMapi()
        # 存储已经被提取过的实体对
        memory = []
        result_paragraph = e.search_paragraphs_by_id(paragraph_id)
        if len(result_paragraph) == 0 or len(result_paragraph[0][3]) < 50:
            print("当前段落太短，跳过抽取关系")
            continue
        print("段落内容长度："+str(len(result_paragraph[0][3])))
        print(result_paragraph[0][3])
        result_entitys = e.search_entitys_by_id(paragraph_id)
        if len(result_entitys) < 2:
            print("当前段落的实体数量太少，跳过抽取关系")
        for entity_from in result_entitys:
            for entity_to in result_entitys:
                try:
                    if entity_from[1] == entity_to[1]:
                        print("相同的两个实体对，跳过抽取")
                        continue
                    if entity_from[1] not in result_paragraph[0][3] or entity_from[1] not in result_paragraph[0][3]:
                        print("当前实体对没有在段落原文出现，跳过抽取关系")
                        continue
                    if entity_to[1]+"--"+entity_from[1] in memory:
                        print("当前实体对已经抽取过了")
                        continue
                    # 每次都要新申请提示词，避免与之前的冲突
                    p = Prompt()
                    prompt = p.relationship_extraction_prompt_simple
                    content = [result_paragraph[0][3],
                               f"请判断实体1:{entity_from[1]} 和实体2:{entity_to[1]} 在上文之中的关系，并返回正确的选项",
                               e.options]
                    prompt.append({"role": "user", "content": '\n'.join(content)})
                    return_options = l.extract_relation(prompt)
                    print(return_options)
                    option = return_options.split(".")[0]
                    if option == "A":
                        print("A")
                    elif option == "B":
                        print("B")
                    elif option == "C":
                        print("C")
                    elif option == "D":
                        print("D")
                    elif option == "E":
                        print("E")
                    elif option == "F":
                        print("F")
                    elif option == "G":
                        print("G")
                    elif option == "H":
                        continue
                    # 正反双向都要考虑，不需要再反向提取一次关系
                    memory.append(entity_from[1]+"--"+entity_to[1])
                    memory.append(entity_to[1]+"--"+entity_from[1])
                except Exception as e:
                    print(e)



    # for row in result:
    #     l = LLMapi()
    #     if count > 10:
    #         break
    #     count = count + 1
    #     results = []
    #     try:
    #         print(row[3])
    #         llm_return = l.extract_entity(p.relationship_extraction_prompt_simple, row[3])
    #         print(llm_return)
    #         lines = llm_return.split('\n')
    #         lines = lines[1:-1]
    #         result = '\n'.join(lines)
    #         if llm_return.endswith('\n') and len(lines) > 0:
    #             result += '\n'
    #         print(result)
    #         temp = json.loads(result)
    #         jsons = [dict(item) for item in temp]
    #         print(jsons)
    #         for item in jsons:
    #             result = {}
    #             result["from"] = item["from"]
    #             result["to"] = item["to"]
    #             result["relation"] = item["relation"]
    #             results.append(result)
    #         print(results)
    #         # e.insert_entity(results)
    #     except Exception as e:
    #         print(e)

        # pre = r.entity_extraction(row[3])
        # count = count + 1
