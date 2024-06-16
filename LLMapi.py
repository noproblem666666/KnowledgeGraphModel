from zhipuai import ZhipuAI


class LLMapi:
    def __init__(self):
        self.client = ZhipuAI(api_key="3f077d18d20d1445003549aa7aca7b80.WUFFAtPK1zJP96Ju")
        self.question = [
            {"role": "user", "content": "作为一个计算机组成原理领域的教学老师，请你为学生解答各种问题"},
            {"role": "assistant", "content": "当然，作为计算机组成原理领域的教学老师，请您提供我需要解答的各种问题"},
            {"role": "user",
             "content": "请尽量使用接下来我提供的信息来回答下一个问题：电子数字计算机是在算盘的基础上发展起来的，是用数字来表示数量的大小。数字计算机的主要特点是按位运算，并且不连续地跳动计算。电子数字计算机进一步又可分为专用计算机和通用计算机。"},
            {"role": "assistant", "content": "好的，我会使用以上信息来回答接下来的问题"},
            {"role": "user", "content": "电子计算机的特征是什么"}
        ]

    def sendMessage(self, promts):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": "我会给你一个问句，请帮我从问句中提取出涉及到的实体，并用实体：进行输出"},
                {"role": "assistant", "content": "当然，请提供您的问句，我会按照格式进行输出"},
                {"role": "user", "content": "电子计算机的特征是什么"}
            ],
        )
        print(response.choices[0].message)

    def stream(self):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=self.question,
            stream=True,
        )
        for chunk in response:
            print(chunk.choices[0].delta.content, end='')


if __name__ == '__main__':
    r = LLMapi()
    r.stream()
