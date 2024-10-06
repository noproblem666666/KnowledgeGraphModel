from zhipuai import ZhipuAI

from ReadToMysql import ReadToMysql
from openai import OpenAI

class Prompt:
    def __init__(self):
        self.client = OpenAI(api_key="sk-178d8772e9f14d4e886c131cb6720355", base_url="https://api.deepseek.com")
        self.entity_extraction_prompt_simple1 = [{"role": "user",
                                                  "content": "你是一款擅长从中文文本中抽取出实体以及与其相关文本描述的AI机器人。你的核心能力是从文本中抽取出实体信息并按照json的格式输出，属性是entity,description,分别表示实体名称，实体描述信息,除了json数据不要输出其他任何信息"},
                                                 {"role": "assistant",
                                                  "content": "当然，我会尽可能抽取出文本中的实体信息以及其文本描述信息，只输出json数据，不输出其他任何信息"}]
        self.entity_extraction_prompt_simple = [{"role": "user",
                                                 "content": "你是一款擅长从中文文本中抽取出实体以及与其相关文本描述的AI机器人。你的核心能力是从文本中抽取出实体信息并按照json的格式输出，属性是entity,description,分别表示实体名称，实体描述信息"
                                                            "输出格式为：" +"""[
                                                 {
                                                     "entity": "xxx",
                                                     "description": "xxx"
                                                 },
                                                {
                                                    "entity": "xxx",
                                                    "description": "xxx"
                                                }
                                                ]"""},
                                                {"role": "assistant",
                                                 "content": "当然，我会尽可能抽取出文本中的实体信息以及其文本描述信息，并按照指定的json的格式进行输出"}]
        self.entity_extraction_prompt = [{"role": "user",
                                          "content": "你是一款擅长从中文文本中抽取出实体以及与其相关文本描述的AI机器人。你的核心能力是从文本中抽取出实体信息并按照json的格式输出，属性是entity,description,分别表示实体名称，实体描述信息"},
                                         {"role": "assistant",
                                          "content": "当然，我会尽可能抽取出实体信息以及其相关的类型与描述信息，并按照json的格式进行输出"},
                                         {"role": "user",
                                          "content": "接下来我会给你几个例子作为学习，请尽量按照它们的模式来抽取实体信息"},
                                         {"role": "assistant",
                                          "content": "好的，我会尽量学习它们的例子来规范化实体抽取信息输出"},
                                         {"role": "user",
                                          "content": "我输入的文本内容是：吞吐量表征一台计算机在某一时间间隔内能够处理的信息量。响应时间表征从输入有效到系统产生响应之间的时间度量，用时间单位来度量。利用率在给定的时间间隔内系统被实际使用的时间所占的比率，用百分比表示。处理机字长指处理机运算器中一次能够完成二进制数运算的位数，如32位、64位。总线宽度一般指CPU中运算器与存储器之间进行互连的内部总线二进制位数。存储器容量存储器中所有存储单元的总数目，通常用KB、MB、GB、TB来表示。存储器带宽单位时间内从存储器读出的二进制数信息量，一般用字节数/秒表示。主频/时钟周期CPU的工作节拍受主时钟控制，主时钟不断产生固定频率的时钟，主时钟的频率(f)叫CPU的主频。度量单位是MHz(兆赫兹)、GHz(吉赫兹)。主频的倒数称为CPU时钟周期(T)，T=1/f，度量单位是μs、ns。CPU执行时间表示CPU执行一般程序所占用的CPU时间，可用下式计算：CPU执行时间=CPU时钟周期数×CPU时钟周期CPl表示每条指令周期数，即执行一条指令所需的平均时钟周期数。用下式计算：CPI=执行某段程序所需的CPU时钟周期数÷程序包含的指令条数MIPS(MillionInstructionsPerSecond)的缩写，表示平均每秒执行多少百万条定点指令数，用下式计算：MIPS=指令数÷(程序执行时间×106)FLOPS(Floating-pointOperationsPerSecond)的缩写，表示每秒执行浮点操作的次数，用来衡量机器浮点操作的性能。用下式计算：FLOPS=程序中的浮点操作次数÷程序执行时间(s)" + """这段文本抽取出的信息是：[
                    {
                    "entity": "吞吐量",
                    "description": "一台计算机在某一时间间隔内能够处理的信息量"
                    },
                    {
                    "entity": "响应时间",
                    "description": "从输入有效到系统产生响应之间的时间度量"
                    },
                    {
                    "entity": "利用率",
                    "description": "在给定的时间间隔内系统被实际使用的时间所占的比率"
                    },
                    {
                    "entity": "处理机字长",
                    "description": "处理机运算器中一次能够完成二进制数运算的位数"
                    },
                    {
                    "entity": "总线宽度",
                    "description": "CPU中运算器与存储器之间进行互连的内部总线二进制位数"
                    },
                    {
                    "entity": "存储器容量",
                    "description": "存储器中所有存储单元的总数目"
                    },
                    {
                    "entity": "存储器带宽",
                    "description": "单位时间内从存储器读出的二进制数信息量"
                    },
                    {
                    "entity": "主频/时钟周期",
                    "description": "CPU的工作节拍受主时钟控制"
                    },
                    {
                    "entity": "CPU执行时间",
                    "description": "CPU执行一般程序所占用的CPU时间"
                    },
                    {
                    "entity": "CPI",
                    "description": "每条指令周期数，即执行一条指令所需的平均时钟周期数"
                    },
                    {
                    "entity": "MIPS",
                    "description": "平均每秒执行多少百万条定点指令数"
                    },
                    {
                    "entity": "FLOPS",
                    "description": "每秒执行浮点操作的次数，用来衡量机器浮点操作的性能"
                    }
                    ]"""},
                                         {"role": "assistant",
                                          "content": "好的，我知道从以上文本中可以抽取出那些json格式的信息"},
                                         {"role": "user",
                                          "content": "习惯上所称的“电子计算机”是指现在广泛应用的电子数字计算机，它分为专用计算机和通用计算机两大类。专用和通用是根据计算机的效率、速度、价格、运行的经济性和适应性来划分的。通用计算机分为超级计算机、大型机、服务器、PC机、单片机、多核机六类，其结构复杂性、性能、价格依次递减。计算机的硬件是由有形的电子器件等构成的，它包括运算器、存储器、控制器、适配器、输入输出设备。早期将运算器和控制器合在一起称为CPU(中央处理器)。目前的CPU包含了存储器，因此称为中央处理机。存储程序并按地址顺序执行，这是冯·诺依曼型计算机的工作原理，也是CPU自动工作的关键。计算机的软件是计算机系统结构的重要组成部分，也是计算机不同于一般电子设备的本质所在。计算机软件一般分为系统程序和应用程序两大类。系统程序用来简化程序设计，简化使用方法，提高计算机的使用效率，发挥和扩大计算机的功能和用途，它包括：①各种服务性程序；②语言类程序；③操作系统；④数据库管理系统。应用程序是针对某一应用课题领域开发的软件。计算机系统是一个由硬件、软件组成的多级层次结构，它通常由微程序级、一般机器级、操作系统级、汇编语言级、高级语言级组成，每一级上都能进行程序设计，且得到下面各级的支持。计算机的性能指标主要是CPU性能指标、存储器性能指标和I/O吞吐率。"},
                                         {"role": "assistant", "content": """[
                                        {
                    "entity": "电子计算机",
                    "description": "指现在广泛应用的电子数字计算机，它分为专用计算机和通用计算机两大类"
                    },
                    {
                    "entity": "通用计算机",
                    "description": "分为超级计算机、大型机、服务器、PC机、单片机、多核机六类，其结构复杂性、性能、价格依次递减"
                    },
                    {
                    "entity": "计算机的硬件",
                    "description": "是由有形的电子器件等构成的，它包括运算器、存储器、控制器、适配器、输入输出设备"
                    },
                    {
                    "entity": "CPU",
                    "description": "早期将运算器和控制器合在一起称为CPU(中央处理器)。目前的CPU包含了存储器，因此称为中央处理机"
                    },
                    {
                    "entity": "计算机软件",
                    "description": "计算机的软件是计算机系统结构的重要组成部分，也是计算机不同于一般电子设备的本质所在。计算机软件一般分为系统程序和应用程序两大类"
                    },
                    {
                    "entity": "系统程序",
                    "description": "系统程序用来简化程序设计，简化使用方法，提高计算机的使用效率，发挥和扩大计算机的功能和用途，它包括：①各种服务性程序；②语言类程序；③操作系统；④数据库管理系统。应用程序是针对某一应用课题领域开发的软件"
                    },
                    {
                    "entity": "应用程序",
                    "description": "应用程序是针对某一应用课题领域开发的软件"
                    },
                    {
                    "entity": "计算机系统",
                    "description": "计算机系统是一个由硬件、软件组成的多级层次结构，它通常由微程序级、一般机器级、操作系统级、汇编语言级、高级语言级组成，每一级上都能进行程序设计，且得到下面各级的支持。"
                    },
                    {
                    "entity": "计算机的性能指标",
                    "description": "计算机的性能指标主要是CPU性能指标、存储器性能指标和I/O吞吐率。"
                    }
                    ]"""}
                                         ]

        self.relationship_extraction_prompt_simple = [{"role": "user",
                                                      "content": "你是一款擅长从中文文本中判断实体之间关系的AI机器人。你的核心能力是分析文本中实体之间的关系，并从提供的选项中选择出正确的选项，返回选项的字母即可，不要返回其他任何信息"},
                                                      {"role": "assistant",
                                                       "content": "当然，我会尽可能分析文本中实体之间的关系，并返回正确答案的选项"}]
        self.relationship_extraction_prompt = [{"role": "user",
                                                "content": "你是一款擅长从中文文本中判断两个实体之间关系的AI机器人。你的核心能力是对文本中两个实体间的关系做出判断，并在提供的选项中选择最合适的进行输出"},
                                               {"role": "assistant",
                                                "content": "当然，我会尽可能准确的判断实体在文本之中的关系"},
                                               {"role": "user",
                                                "content": "接下来我会给你几个例子作为学习，请尽量按照它们的模式来判断实体关系"},
                                               {"role": "assistant",
                                                "content": "好的，我会尽量学习它们的例子来规范化实体关系判断"},
                                               {"role": "user",
                                                "content": "习惯上所称的“电子计算机”是指现在广泛应用的电子数字计算机，它分为专用计算机和通用计算机两大类。专用和通用是根据计算机的效率、速度、价格、运行的经济性和适应性来划分的。通用计算机分为超级计算机、大型机、服务器、PC机、单片机、多核机六类，其结构复杂性、性能、价格依次递减。计算机的硬件是由有形的电子器件等构成的，它包括运算器、存储器、控制器、适配器、输入输出设备。早期将运算器和控制器合在一起称为CPU(中央处理器)。目前的CPU包含了存储器，因此称为中央处理机。存储程序并按地址顺序执行，这是冯·诺依曼型计算机的工作原理，也是CPU自动工作的关键。计算机的软件是计算机系统结构的重要组成部分，也是计算机不同于一般电子设备的本质所在。计算机软件一般分为系统程序和应用程序两大类。系统程序用来简化程序设计，简化使用方法，提高计算机的使用效率，发挥和扩大计算机的功能和用途，它包括：①各种服务性程序；②语言类程序；③操作系统；④数据库管理系统。应用程序是针对某一应用课题领域开发的软件。计算机系统是一个由硬件、软件组成的多级层次结构，它通常由微程序级、一般机器级、操作系统级、汇编语言级、高级语言级组成，每一级上都能进行程序设计，且得到下面各级的支持。计算机的性能指标主要是CPU性能指标、存储器性能指标和I/O吞吐率。" + """
                                                请从这段文本中判断：电子计算机与专用计算机的关系。
                                                提供的选项有：
                                                A. 电子计算机属于专用计算机
                                                B. 电子计算机组成专用计算机
                                                C. 电子计算机包括专用计算机
                                                D. 电子计算机与专用计算机无关
                                              
                                                以上选择的答案为：C
                                            
                                            
                    ]"""},
                                               {"role": "assistant",
                                                "content": "好的，我知道从以上文本中可以做出该关系判断"},
                                               {"role": "user",
                                                "content": "电子计算机从总体上来说分为两大类。一类是电子模拟计算机。“模拟”就是相似的意思，例如计算尺是用长度来标示数值；时钟是用指针在表盘上转动来表示时间；电表是用角度来反映电量大小，这些都是模拟计算装置。模拟计算机的特点是数值由连续量来表示，运算过程也是连续的。另一类是电子数字计算机，它是在算盘的基础上发展起来的，是用数字来表示数量的大小。数字计算机的主要特点是按位运算，并且不连续地跳动计算。"
                                                           "请从以上文本中判断电子计算机和电子模拟计算机的关系"
                                                           "A. 电子计算机属于电子模拟计算机"
                                                           "B. 电子计算机包括电子模拟计算机"
                                                           "C. 电子计算机组成电子模拟计算机"
                                                           "D. 电子计算机和电子模拟计算机无关"},
                                               {"role": "assistant", "content": """
                                               B
                                               """}
                                               ]

    def entity_extraction(self, content):
        self.entity_extraction_prompt.append({"role": "user", "content": content})
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=self.entity_extraction_prompt,
        )
        print("开始抽取文本中的实体信息:")
        data = response.choices[0].message.content
        print(data)
        return data

    # 关系抽取选择题
    def relationship_extraction(self, content, entity1, entity2, choices):
        content += f"\n 请判断{entity1}和{entity2}的关系"
        count = 65
        for choice in choices:
            content += "\n" + chr(count) + ". " + choice
            count += 1
        print(content)
        self.relationship_extraction_prompt.append({"role": "user", "content": content})
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=self.relationship_extraction_prompt,
        )
        data = response.choices[0].message.content
        print(data)
        return data


if __name__ == '__main__':
    # Todo：多标题文本转化，微调、关系问答
    # Todo: 对于关系的选择应该有多重，一个关系树
    # Todo：知识图谱新的数据文件更新，量化抽取结果
    # Todo：找一个统一的知识图谱标准
    r = Prompt()
    m = ReadToMysql()
    while True:
        # user_input = input("请输入要抽取实体的内容: ")
        # print("\n")
        # data = r.entity_extraction(user_input)
        # m.json_entity_json(data)
        # print("\n")
        user_input = input("请输入要抽取关系的内容：")
        print("\n")
        user_entity1 = input("请输入要抽取关系的第一个实体")
        print("\n")
        user_entity2 = input("请输入要抽取关系的第一个实体")
        print("\n")
        choices = []
        choices.append(user_entity1 + "属于" + user_entity2)
        choices.append(user_entity1 + "包括" + user_entity2)
        choices.append(user_entity1 + "组成" + user_entity2)
        choices.append(user_entity1 + "无关于" + user_entity2)
        data = r.relationship_extraction(user_input, user_entity1, user_entity2, choices)
