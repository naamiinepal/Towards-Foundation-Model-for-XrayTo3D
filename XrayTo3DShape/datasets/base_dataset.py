"""
Define torch Datasets for AP, LAT, Segmentation images
TODO: subclass from monai.data.PersistentDataset for caching
"""
from typing import Callable, Dict, Sequence

import pandas as pd
from monai.transforms.transform import apply_transform
from torch.utils.data import Dataset


class BaseDataset(Dataset):
    """A generic dataset with a length property and required callable data transform for AP, LAT
    and segmentation  when fetching a data sample.

    [{  'ap': 'image1.nii.gz', 'lat':'image3.nii.gz','seg': 'label1.nii.gz'  } ]
    """

    def __init__(self, data: Sequence, transforms: Dict[str, Callable]) -> None:
        super().__init__()
        self.data = data
        self.transforms = transforms

    def __len__(self) -> int:
        return len(self.data)

    def _transform(self, index: int):
        """Fetch single data item from `self.data`"""
        data_i = self.data[index]
        ap_transform, lat_transform, seg_transform = (
            self.transforms["ap"],
            self.transforms["lat"],
            self.transforms["seg"],
        )
        return (
            apply_transform(ap_transform, data_i),
            apply_transform(lat_transform, data_i),
            apply_transform(seg_transform, data_i),
        )

    def __getitem__(self, index):
        return self._transform(index)


class AtlasDeformationDataset(Dataset):
    """TODO: work in progress"""

    def __init__(self, data: Sequence, atlas_path, transforms: Dict[str, Callable]) -> None:
        super().__init__()
        self.atlas_path = atlas_path
        self.data = data
        self.transforms = transforms

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index: int):
        data_i = self.data[index]
        ap_transform, lat_transform, seg_transform, atlas_transform = (
            self.transforms["ap"],
            self.transforms["lat"],
            self.transforms["seg"],
            self.transforms["atlas"],
        )

        return (
            apply_transform(ap_transform, data_i),
            apply_transform(lat_transform, data_i),
            apply_transform(seg_transform, data_i),
            apply_transform(atlas_transform, {"atlas": self.atlas_path}),
        )


class DeformationDataset(Dataset):
    """TODO: work in progress"""

    def __init__(self, data: Sequence, transforms: Dict[str, Callable]) -> None:
        super().__init__()
        self.data = data
        self.transforms = transforms

    def __len__(self) -> int:
        return len(self.data)

    def transform(self, index: int):
        """Apply transformation to fixed and moving images."""
        data_i = self.data[index]
        fixed_transform, moving_transform = (
            self.transforms["fixed"],
            self.transforms["moving"],
        )
        return (
            apply_transform(fixed_transform, data_i),
            apply_transform(moving_transform, data_i),
        )

    def __getitem__(self, index):
        return self.transform(index)


def get_dataset(filepaths: str, transforms: Dict) -> Dataset:
    """Read filepaths csv and return Dataset."""
    paths = pd.read_csv(filepaths, index_col=0).to_numpy()
    paths = [{"ap": ap, "lat": lat, "seg": seg} for ap, lat, seg in paths]
    return BaseDataset(data=paths, transforms=transforms)
