# Parser-for-Operator-Precedence-Grammar
It's a parser written in Python for operator-precedence grammar

中文：
在文件中的grammar.txt和sentence.txt中分别输入文法和句子
 
如grammar.txt所示，产生式请按照以下的格式输入：
1)	“→”可以用其他任何字符替换，但是一定不能缺；
2)	务必用“|”来作为分隔符；
3)	不同非终结符的产生式一定要换行输入
 

如sentence.txt所示，句子请按照以下的格式输入：
1)	句子末尾的“#“可加可不加，均能成功；
2)	句子中加入空格符、换行符等空白字符不会影响对语法的判定

本程序是python程序，可在PyCharm IDE中运行

English:
Enter the grammars and sentences in grammar.txt and sentence.txt, respectively.

As grammar.txt shows, the production rules are supposed to be entered in the following format:
1) “→” can be replaced by any other character, but must not be missing
2) Be sure to use “|” as a seperator
3) The production rules of different non-terminal symbol must be entered in different lines

As sentence.txt shows, the sentences are supposed to be entered in the following format:
1) The "#" is optional
2) The space characters, line breaks and other blank characters won't affect the analysis

This program is written by Python, which can run in PyCharm.
