class Enum:
    @classmethod
    def from_value(cls, value):
        if value in cls.__dict__:
            return cls.__dict__[value]
        raise AttributeError("Not found value %s" % value)