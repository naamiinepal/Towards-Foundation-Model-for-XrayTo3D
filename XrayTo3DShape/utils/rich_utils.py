# code from https://github.com/ashleve/lightning-hydra-template/blob/main/src/utils/rich_utils.py

from omegaconf import DictConfig, OmegaConf
import rich
import rich.syntax
import rich.tree
import rich.prompt
from lightning_utilities.core.rank_zero import rank_zero_only

@rank_zero_only
def print_config_tree(cfg):
    style = 'dim'
    tree = rich.tree.Tree('CONFIG',style=style,guide_style=style)
    
    # generate config tree
    for field in cfg:
        branch = tree.add(field,style=style,guide_style=style)

        config_group = cfg[field]
        if isinstance(config_group, DictConfig):
            branch_content = OmegaConf.to_yaml(config_group, resolve=True)
        else:
            branch_content = str(config_group)
        branch.add(rich.syntax.Syntax(branch_content,'yaml'))

    rich.print(tree)


if __name__ == '__main__':
    from XrayTo3DShape import read_config_and_load_components
    config_path = 'configs/360_augmentation/Verse2019-DRR-full.yaml'
    config = read_config_and_load_components(config_path)
    print_config_tree(config)
