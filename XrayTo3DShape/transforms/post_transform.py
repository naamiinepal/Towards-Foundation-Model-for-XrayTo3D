"""Data transformation for post-processing model prediction."""
from monai.transforms.compose import Compose
from monai.transforms.post.array import Activations, AsDiscrete

post_transform = Compose([Activations(sigmoid=True), AsDiscrete(threshold=0.5)])
post_transform_onehot = Compose([AsDiscrete(argmax=True)])
