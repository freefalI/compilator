transition_table={
    1: {'label': (1, 2, 12), "state": 2, "nezr": 'error', 'error_msg': "Відсутнє оголошення"},
    2: {'label': (100, 102), "state": 3, "nezr": 'error', 'error_msg': "Невірний список змінних"},
    3: (
        {'label': 16, "state": 2, 'error_msg': "massag3"},
        {'label': 15, "state": 1, 'error_msg': "massage4"},
        {'label': 13, "state": 4, "nezr": 'error',
            'error_msg': "Немає відкриваючої фігурної дужки"}
    ),
    4: {'label': 15, "stack": 5, "state": 20, "nezr": 'error', 'error_msg': "Відсутній перенос на новий рядок"},
    5: {'label': 15, "state": 6, "nezr": 'error', 'error_msg': "Відсутній перенос на новий рядок"},
    6: (
        {'label': 14, "zr": 'exit'},
        {"label": "any", "stack": 5, "state": 20}
    ),
    # Підавтомат вираз
    10: (
        {'label': (100, 101), "state": 11, 'error_msg': "massage10"},
        {'label': 30, "stack": 12, "state": 10, "nezr": 'error',
            'error_msg': "Відсутній ідентифікатор або кфт"}
    ),
    11: {'label': (26, 27, 28, 29), "state": 10, "nezr": 'exit'},
    12: {'label': 31, "state": 11, "nezr": 'error', 'error_msg': "Відсутня закриваюча дужка"},
    # Підавтомат Оператор
    20: (
        {'label': 6, "stack": 21, "state": 10, 'error_msg': "massage20"},
        {'label': (100, 102), "state": 25, 'error_msg': "massage201"},
        {'label': 7, "state": 30, 'error_msg': "massage202"},
        {'label': 8, "state": 33, 'error_msg': "massage203"},
        {'label': 3, "state": 36, 'error_msg': "massage204"},
        {'label': 11, "state": 43, "nezr": 'error',
            'error_msg': "Невірний оператор"},
    ),
    21: {'label': (20, 21, 22, 23, 24, 25), "stack": 22, "state": 10, "nezr": 'error', 'error_msg': "Відсутній знак відношення"},
    22: {'label': 10, "state": 23, "nezr": 'error', 'error_msg': "Відсутній оператор then"},
    23: {'label': 11, "state": 24, "nezr": 'error', 'error_msg': "Відсутній оператор goto"},
    24: {'label': 102, "zr": 'exit', "nezr": 'error', 'error_msg': "Відсутній ідентифікатор"},
    25: (
        {'label': 32, "zr": 'exit', 'error_msg': "massage25"},
        {'label': 17, "stack": 26, "state": 10, "nezr": 'error',
            'error_msg': "Відсутнє присвоєння або оператор :"},
    ),
    26: {'label': (20, 21, 22, 23, 24, 25), "stack": 27, "state": 10, "nezr": 'exit', 'error_msg': "massage26"},
    27: {'label': 33, "stack": 28, "state": 10, "nezr": 'error', 'error_msg': "Відсутній оператор ?"},
    28: {'label': 32, "stack": 29, "state": 10, "nezr": 'error', 'error_msg': "Відсутній оператор :"},
    29: {},
    30: {'label': 19, "state": 31, "nezr": 'error', 'error_msg': "Відсутній оператор >>"},
    31: {'label': 100, "state": 32, "nezr": 'error', 'error_msg': "Відсутній ідентифікатор"},
    32: {'label': 19,  "state": 31, "nezr": 'exit', 'error_msg': "massage32"},
    33: {'label': 18, "state": 34, "nezr": 'error', 'error_msg': "Відсутній оператор <<"},
    34: {'label': (100, 101), "state": 35, "nezr": 'error', 'error_msg': "Відсутній ідентифікатор"},
    35: {'label': 18, "state": 34, "nezr": 'exit', 'error_msg': "massage35"},
    36: {'label': 100, "state": 37, "nezr": 'error', 'error_msg': "Відсутній ідентифікатор"},
    37: {'label': 17, "stack": 38, "state": 10, "nezr": 'error', 'error_msg': "Відсутній оператор ="},
    38: {'label': 4, "stack": 39, "state": 10, "nezr": 'error', 'error_msg': "Відсутній оператор by"},
    39: {'label': 9, "stack": 40, "state": 10, "nezr": 'error', 'error_msg': "Відсутній оператор while"},
    40: {'label': (20, 21, 22, 23, 24, 25), "stack": 41, "state": 10, "nezr": 'error', 'error_msg': "Відсутній знак відношення"},
    41: {'label': 5, "stack": 42, "state": 20, "nezr": 'error', 'error_msg': "Відсутній оператор do"},
    42: {},
    43: {'label': 102, "zr": 'exit', "nezr": 'error', 'error_msg': "Відсутній ідентифікатор(мітка)"}
}