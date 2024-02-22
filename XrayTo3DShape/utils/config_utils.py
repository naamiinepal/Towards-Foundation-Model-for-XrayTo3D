"""utils for working with dicts"""
from collections import ChainMap
import copy

"""
adapted from https://github.com/shagunsodhani/torch-template
These utility functions are used to read a custom hierarchical yaml file.
each major module configuration keys are the top of the hierarchy (say datasets, architectures etc.)
The detailed configuration of these modules may be shared across experiments
and may be stored in a separate yaml file.
These separate yaml are merged into main configuration with a special key '_load'
"""
from pathlib import Path
from typing import Any, Dict, Union, cast

from omegaconf import DictConfig, ListConfig, OmegaConf

ConfigType = Union[DictConfig, ListConfig]


def read_config_and_load_components(filepath, special_key="_load"):
    """read yaml from filepath and load subcomponents"""
    config_dict = OmegaConf.load(filepath)
    assert isinstance(config_dict, DictConfig)
    for key in config_dict:
        config_dict[key] = load_components(
            config_dict[key], Path(filepath).parent, special_key
        )
    return config_dict


def load_components(config: ConfigType, basepath, special_key) -> ConfigType:
    """
    update dict if the key == special_key
    return a updated dict
    """
    if config is not None and special_key in config:
        loaded_config = OmegaConf.load(basepath / config.pop(special_key))
        updated_config = OmegaConf.merge(loaded_config, config)
        return updated_config
    else:
        return config


def to_dict(config: ConfigType) -> Dict[str, Any]:
    """thin wrapper to OmegaConf.to_container"""
    dict_config = cast(Dict[str, Any], OmegaConf.to_container(config))
    return dict_config


def substitute_value_in_nested_dict(key, template_dict, substitute_val):
    """use recursion to find a key in a nested dict and update value"""
    if hasattr(template_dict, "items"):  # dict-like object
        for k, v in template_dict.items():
            if k == key:
                template_dict[k] = substitute_val
            if isinstance(v, dict):
                substitute_value_in_nested_dict(key, v, substitute_val)


def update_multiple_key_values_in_nested_dict(target_dict: dict, source_dict: dict):
    """update nested dict"""
    updated_dict = copy.deepcopy(target_dict)
    for k, v in source_dict.items():
        substitute_value_in_nested_dict(k, updated_dict, v)
    return updated_dict


def merge_dicts(dict1, dict2):
    """simpler naming"""
    return ChainMap(dict1, dict2)

if __name__ == "__main__":
    test_configpath = "configs/test/LIDC-DRR-test.yaml"
    config_dict = read_config_and_load_components(test_configpath)
    print(config_dict)