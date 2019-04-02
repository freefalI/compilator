import json

class Idn:
    def __init__(self,id,name,type,line=None):
        self.id=id
        self.name=name
        self.type=type
        self.line =line
    def __repr__(self):
        res = '(Idn : id = {:5}; name = {:>10}; type = {:>10}'.format(self.id,self.name,self.type)
        res+='; line = {:>10}'.format(self.line) if self.line else ''
        return res+')'
        # return json.dumps(self, default=lambda o: o.__dict__)


class Constant:
    def __init__(self,id,name,type):
        self.id=id
        self.name=name
        self.type=type
    def __repr__(self):
        return '(Con : id = {:5}; name = {:>10}; type = {:>10})'.format(self.id,self.name,self.type)
        # return json.dumps(self, default=lambda o: o.__dict__)
     
class Lexeme:
    def __init__(self,id,line,name,code=None,fid=None):
        self.id=id
        self.line=line
        self.name=name
        self.code=code
        self.fid=fid
    def __repr__(self):
        res = '(Lex : '
        res +='id = {:5}'.format(self.id) 
        res +='; line = {:5}'.format(self.line) 
        res +='; name = {:>10}'.format(self.name if self.name!='\n' else '¶') 
        res +='; code = {:10}'.format(self.code) if self.code else ''
        res +='; fid = {:>10}'.format(self.fid) if self.fid else ''
        return res+')'
        # return json.dumps(self, default=lambda o: o.__dict__)