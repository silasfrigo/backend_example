from typing import Generic, TypeVar
from pydantic.generics import GenericModel


T = TypeVar('T')


class Result(GenericModel, Generic[T]):
    data: T
