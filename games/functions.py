import itertools
import pandas as pd
import random
def check_numbers(numbers):
    """
    Check if all numbers in the list are either the same or all different.
    Returns 1 if true, otherwise returns 0.
    """
    unique_numbers = set(numbers)
    return 1 if len(unique_numbers) == 1 or len(unique_numbers) == len(numbers) else 0


# Generating tuples with values 0, 1, 2 for x1, x2, x3, x4
tuples = list(itertools.product([0, 1, 2], repeat=4))
all_tuples = pd.DataFrame(tuples, columns=['x1', 'x2', 'x3', 'x4'])


def get_sets():
    while True:
        random_selection = random.sample(range(81), 9)
        combinations_set = list(itertools.combinations(set(random_selection), 3))

        result = [all_tuples.loc[row,].apply(check_numbers).sum() == 4 for row in combinations_set]

        if sum(result) == 1:
            answer = pd.DataFrame(combinations_set).loc[result].values.tolist()
            return random_selection, answer


##################################################################
def generate_complex_encoding_map():
    charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    encoding_map = {}
    # 线性同余生成器参数
    a = 1664525
    c = 1013904223
    m = 2 ** 32
    seed = [123456789]  # 使用列表封装seed以在闭包内修改

    # 生成伪随机数
    def pseudo_random():
        seed[0] = (a * seed[0] + c) % m
        return seed[0] / m

    for i in range(0, 65):
        # 生成伪随机索引
        index = int(pseudo_random() * len(charset))
        # 确保映射是唯一的
        while charset[index] in encoding_map.values():
            index = int(pseudo_random() * len(charset))
        encoding_map[i] = charset[index]

    return encoding_map

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def product(x, y):
    return x * y

def div(x, y):
    if y != 0:
        return x / y
    else:
        return 0

# 创建一个运算符到函数的映射
operator_functions = {
    'add': add,
    'sub': sub,
    'product': product,
    'div': div
}

###########################################################################################
# 可以被整除的SET
all_pairs = {
    'div': [(j, i, int(j / i)) for i in range(2, 100) for j in range(i + 1, 100) if j % i == 0],
    'product': [(i, j, j * i) for i in range(2, 100) for j in range(i + 1, 100) if i * j < 100],
    'add': [(i, j, j + i) for i in range(2, 100) for j in range(i + 1, 100) if i + j < 100],
    'sub': [(i, j, i - j) for i in range(2, 100) for j in range(2, 100) if i - j > 0]
    }

operator = ['div', 'product', 'add', 'sub']

def distribute_choices():
    ran_operator = random.choice(operator)
    a, b, c = random.choice(all_pairs[ran_operator])
    random_numbers = random.sample([x for x in range(2, 100) if x not in (a, b, c)], 7)

    # 隨機抽掉兩個數字
    chosen = random.choice(['a', 'b', 'c'])

    if chosen == 'a':
        random_numbers.append(b)
        random_numbers.append(c)
        b, c = '', ''
    elif chosen == 'b':
        random_numbers.append(a)
        random_numbers.append(c)
        a, c = '', ''
    else:
        random_numbers.append(a)
        random_numbers.append(b)
        a, b = '', ''

    # 隨機打亂數字
    random.shuffle(random_numbers)

    return(a, b, c, chosen, ran_operator, random_numbers)