"""
Sometimes, it is convenient to have multiple constructors when writing a class

How in python?
Python can not have function overloading!
solution: use @classmethod
"""

"""
what is @classmethod?
Transform a method into a class method.

what is a class method then?
1. A class method received the class as implicit first argument, just like an instance method
receives the instance.
2. To declare a class method, use this idiom:
    class C:
        @classmethod
        def f(cls, arg1, arg2, ...): ...
    where cls is the Class Object.
3. A class method can be called either on the class (such as C.f()) or on an instance(such as
C().f()). The instance is ignored except for its class. 
4. If a class method is called for a derived class, the derived class object is passed as the 
implied first argument. 
"""


class F:
    # this is the true only one constructor
    def __init__(self, timestamp=0, data=None, metadata=None):
        self.timestamp = timestamp
        self.data = list() if data is None else data
        self.metadata = dict() if metadata is None else metadata

    # this classmethod will use the true __init__ to construct object
    @classmethod
    def from_file(cls, path):
        _file = cls.get_file(path)
        timestamp = _file.get_timestamp()
        data = _file.get_data()
        metadata = _file.get_metadata()
        return cls(timestamp, data, metadata)

    @classmethod
    def from_metadata(cls, timestamp, data, metadata):
        return cls(timestamp, data, metadata)

    @staticmethod
    def get_file(path):
        # ...
        pass
