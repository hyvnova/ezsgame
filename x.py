from typing import TypedDict, Type

# Define a TypedDict with keys as Type and values as instances
class TypedInstanceDict(TypedDict):
    key1: Type[str]
    key2: Type[int]
    key3: Type[float]

# Create an instance of the TypedDict with some sample data
typed_dict: TypedInstanceDict = {
    'key1': str,
    'key2': int,
    'key3': float
}

# Accessing values with type hints
value1 = typed_dict['key1']
value2: Type[int] = typed_dict['key2']
value3: Type[float] = typed_dict['key3']

print(value1)  # <class 'str'>
print(value2)  # <class 'int'>
print(value3)  # <class 'float'>
