class A():
    def __init__(self, **dic):
        #for x in dic:
        #    self.__dict__[x] = dic[x]
        self.__dict__ = dict(**dic)

    def __getattr__(self, key):
        return self.__dict__.get(key)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __str__(self):
        s='{'
        for key in self.__dict__:
            s += "\n    %s : %s,"%(key, self.__dict__[key])
        s+="\n}"
        return s

a=A(a=1,b=2)
print(a)
