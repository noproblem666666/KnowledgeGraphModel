import json
import re
import pymysql

from LLMapi import LLMapi
from Prompt import Prompt


class ExtractEntity:
    def __init__(self):
        self.password = "lzg19981202"
        self.host = "localhost"
        self.user = "root"
        self.db = "knowledge_graph"
        self.paragraphs_table_name = "paragraphs"
        self.entity_table_name = "entity"

    def search_paragraphs(self):
        results = []
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.paragraphs_table_name} where id > 44")
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

    def insert_entity(self, results):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        cursor = db.cursor()

        try:
            for item in results:
                sql = f"INSERT INTO {self.entity_table_name} (entity_name, description, title, paragraphs_id, position, file_name) VALUES ('{item['entity']}', '{item['description']}', '{item['title']}','{item['paragraphs_id']}','{item['position']}','{item['file_name']}')"
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
    e = ExtractEntity()
    p = Prompt()

    result = e.search_paragraphs()
    count = 0
    memory = []
    for row in result:
        l = LLMapi()
        e = ExtractEntity()
        # Todo:每次都要重新申请一个提示词函数，否则在函数中的提示词修改是永久性的，之后每次发送提示词都会携带之前拼接的信息
        p = Prompt()
        # if count > 10:
        #     break
        # count = count + 1
        results = []
        try:
            print(row[3])
            llm_return = l.extract_entity(p.entity_extraction_prompt_simple, row[3])
            print(llm_return)
            lines = llm_return.split('\n')
            lines = lines[1:-1]
            result = '\n'.join(lines)
            if llm_return.endswith('\n') and len(lines) > 0:
                result += '\n'
            # print(result)
            temp = json.loads(result)
            jsons = [dict(item) for item in temp]
            # print(jsons)
            for item in jsons:
                if item["entity"] + "--" + item["description"] in memory:
                    continue
                result = {}
                result["paragraphs_id"] = row[0]
                result["file_name"] = row[1]
                result["title"] = row[2]
                result["position"] = row[4]
                result["entity"] = item["entity"]
                result["description"] = item["description"]
                results.append(result)
                memory.append(item["entity"] + "--" + item["description"])
            print(results)
            e.insert_entity(results)
        except Exception as e:
            print(e)

        # pre = r.entity_extraction(row[3])
        # count = count + 1
