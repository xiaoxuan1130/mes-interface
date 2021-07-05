# coding:utf-8
import yaml
import os

class ReadYaml():

    # 读取页面路径
    def readYamlByValue(module, key,value):
        # 获取当前脚本所在文件夹路径
        curPath = os.path.dirname(os.path.realpath(__file__))
        # 获取yaml文件路径
        yamlPath = os.path.join(curPath, "var.yaml")
        # open方法打开直接读出来
        f = open(yamlPath, 'r', encoding='utf-8')
        cfg = f.read()
        d = yaml.safe_load(cfg)  # 用load方法转字典
        return d.get(module).get(key)+"_"+value

    #读取页面路径
    def readYaml(module,key):
        # 获取当前脚本所在文件夹路径
        curPath = os.path.dirname(os.path.realpath(__file__))
        # 获取yaml文件路径
        yamlPath = os.path.join(curPath, "var.yaml")
        # open方法打开直接读出来
        f = open(yamlPath, 'r', encoding='utf-8')
        cfg = f.read()
        d = yaml.safe_load(cfg)  # 用load方法转字典
        return d.get(module).get(key)

    #读取接口地址
    def realVarYaml(key):
        # 获取当前脚本所在文件夹路径
        curPath = os.path.dirname(os.path.realpath(__file__))
        # 获取yaml文件路径
        yamlPath = os.path.join(curPath, "api.yaml")
        # open方法打开直接读出来
        f = open(yamlPath, 'r', encoding='utf-8')
        cfg = f.read()
        d = yaml.safe_load(cfg)  # 用load方法转字典
        return d.get(key)

    def readUrl(path):
        url = ReadYaml.realVarYaml("mes-url")
        path = ReadYaml.realVarYaml(path)
        return url+path

        # 读取页面路径
        def readYaml(module, key):
            # 获取当前脚本所在文件夹路径
            curPath = os.path.dirname(os.path.realpath(__file__))
            # 获取yaml文件路径
            yamlPath = os.path.join(curPath, "var.yaml")
            # open方法打开直接读出来
            f = open(yamlPath, 'r', encoding='utf-8')
            cfg = f.read()
            d = yaml.safe_load(cfg)  # 用load方法转字典
            return d.get(module).get(key)

