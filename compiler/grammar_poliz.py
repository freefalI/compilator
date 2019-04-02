grammar = {
    # 'program': ('<sp og>', '¶','{','¶', '<sp op1>', '}'),# 14 konflicts
     '<expr1>':('<expr>',),
    '<expr>':(
        ('<expr>','+','<term1>'),
        ('<expr>','-','<term1>'),
        ('<term1>',)
    ),
    '<term1>':('<term>',),
      '<term>':(
        ('<term>','*','<factor>'),
        ('<term>','/','<factor>'),
        ('<factor>',)
    ),
    '<factor>':(
        ('idn',),
        ('constant',),
        ('(','<expr1>',')')
    )
}