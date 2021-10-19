from jotdx.reader import Reader

# market 参数 std 为标准市场(就是股票), ext 为扩展市场(期货，黄金等)
# tdxdir 是通达信的数据目录, 根据自己的情况修改

reader = Reader.factory(market='ext', tdxdir='C:/new_jyplug')

# 读取日线数据
# df = reader.daily(symbol='600000')
df = reader.minute(symbol='30#RBL8')
print(1)

if __name__ == '__main__':
    pass