import redis
from random import choice
import settings


class RedisClient:
    def __init__(self, host=settings.redis_host, port=settings.redis_port, password=settings.redis_password):
        """
        初始化
        :param host: redis地址
        :param port: redis端口
        :param password: redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=50):
        """
        添加代理, 设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not self.db.zscore('proxies', proxy):    # 返回有序集合proxies中元素proxy的分数
            # 向名为proxies的有序集合中添加元素proxy, 分数为score
            self.db.zadd('proxies', {proxy: score})

    def random(self):
        """
        随机获取有效代理, 首先尝试获取最高分数代理, 如果最高分数不存在, 则按排名获取, 否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore('proxies', 50, 50)    # 返回分数为50的代理列表
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange('proxies', 0, 5)    # 返回分数排名的前六个代理的列表
            if len(result):
                return choice(result)
            else:
                raise IndexError

    def decrease(self, proxy):
        """
        代理值减五分, 分数小于0, 则代理删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore('proxies', proxy)
        if score and score > 0:
            print('代理', proxy, '当前分数', score, '减10')
            return self.db.zincrby('proxies', -10, proxy)    # 将代理proxy的分数减五
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem('proxies', proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not (self.db.zscore('proxies', proxy) is None)

    def max(self, proxy):
        """
        将代理设置为50分
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用, 设置为', 50)
        return self.db.zadd('proxies', {proxy: 50})

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard('proxies')

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore('proxies', 0, 50)
