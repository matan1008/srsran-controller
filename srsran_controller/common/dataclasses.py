from dataclasses import asdict


def to_dict_without_none(dataclass_object):
    return {k: v for k, v in asdict(dataclass_object).items() if v is not None}
