from zhipuai import ZhipuAI
from openai import OpenAI
from Prompt import Prompt


class LLMapi:
    def __init__(self):
        self.client = OpenAI(api_key="sk-178d8772e9f14d4e886c131cb6720355", base_url="https://api.deepseek.com")
        self.question = [
            {"role": "user", "content": "作为一个计算机组成原理领域的教学老师，请你为学生解答各种问题"},
            {"role": "assistant", "content": "当然，作为计算机组成原理领域的教学老师，请您提供我需要解答的各种问题"},
            {"role": "user",
             "content": "请尽量使用接下来我提供的信息来回答之后的问题"},
            {"role": "assistant", "content": "好的，我会尽量使用您提供的信息来回答接下来的问题"}
        ]

    def buildPrompt(self, informations, question):
        prompts = []
        prompts.extend(self.question)
        for information in informations:
            prompt_self = {"role": "user"}
            description = information["node"].get("description", "")
            prompt_self["content"] = information["node"]["name"]
            if description:
                prompt_self["content"] += "：有关它的以下信息，" + description
                prompts.append(prompt_self)
                prompt_assistant = {"role": "assistant", "content": "好的，我会尽量使用您提供的信息来回答接下来的问题"}
                prompts.append(prompt_assistant)
        prompts.append({"role": "user", "content": question})
        print("通过获得到的结点信息，拼接成的提示词：")
        for item in prompts:
            print(item)
        return prompts

    def sendMessage(self, prompts):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=prompts,
        )
        print(response.choices[0].message)

    def stream(self, prompts):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=prompts,
            stream=True,
        )
        for chunk in response:
            print(chunk.choices[0].delta.content, end='')

    def direct_stream(self, question):
        self.question.append({"role": "user", "content": question})
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=self.question,
            stream=True,
        )
        for chunk in response:
            print(chunk.choices[0].delta.content, end='')

    def sum_stream(self, content):
        content += "\n 请帮我总结以上信息，输出一段主题性的总结文本"
        self.question.append({"role": "user", "content": content})
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=self.question,
            stream=True,
        )
        for chunk in response:
            print(chunk.choices[0].delta.content, end='')

    def extract_entity(self, prompt, content):

        prompt.append({"role": "user", "content": content})

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=prompt,
            stream=False
        )
        return response.choices[0].message.content


# Todo：数据增强，模型微调
# Todo：可以用beg模型来将问句与实体数据库、关系数据库中的词进行近义查询，搜索查找到的实体

if __name__ == '__main__':
    r = LLMapi()
    p = Prompt()
    response = r.extract_entity(p.entity_extraction_prompt, "为什么redis中的事务不支持回滚")
    print(type(response))
    print(response)
