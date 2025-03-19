from typing import Optional, Type, Any, Tuple
from copy import deepcopy

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


def partial_model(model: Type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new
    return create_model(
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.__fields__.items()
        }
    )


def make_optional_model(model: Type[BaseModel], name_suffix="Update") -> Type[BaseModel]:
    """Creates a new model where all fields are optional."""
    return create_model(
        f"{model.__name__}{name_suffix}",
        **{field: (Optional[typ], None) for field, typ in model.__annotations__.items()},
        __base__=model
    )