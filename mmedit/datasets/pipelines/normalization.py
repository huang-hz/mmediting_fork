import mmcv
import numpy as np

from ..registry import PIPELINES


@PIPELINES.register_module
class Normalize(object):
    """Normalize images with the given mean and std value.

    Required keys are the keys in attribute "keys", added or modified keys are
    the keys in attribute "keys" and these keys with postfix '_norm_cfg'.

    Attributes:
        keys (Sequence[str]): The images to be normalized.
        mean (np.ndarray): Mean values of different channels.
        std (np.ndarray): Std values of different channels.
        to_rgb (bool): Whether to convert channels from BGR to RGB.
    """

    def __init__(self, keys, mean, std, to_rgb=False):
        self.keys = keys
        self.mean = np.array(mean, dtype=np.float32)
        self.std = np.array(std, dtype=np.float32)
        self.to_rgb = to_rgb

    def __call__(self, results):
        for key in self.keys:
            results[key] = mmcv.imnormalize(results[key], self.mean, self.std,
                                            self.to_rgb)
        results['img_norm_cfg'] = dict(
            mean=self.mean, std=self.std, to_rgb=self.to_rgb)
        return results

    def __repr__(self):
        repr_str = self.__class__.__name__
        repr_str += '(keys={}, mean={}, std={}, to_rgb={})'.format(
            self.keys, self.mean, self.std, self.to_rgb)

        return repr_str


@PIPELINES.register_module
class RescaleToZeroOne(object):
    """Transform the images into a range between 0 and 1.

    Required keys are the keys in attribute "keys", added or modified keys are
    the keys in attribute "keys".

    Attributes:
        keys (Sequence[str]): The images to be transformed.
    """

    def __init__(self, keys):
        self.keys = keys

    def __call__(self, results):
        for key in self.keys:
            results[key] = results[key].astype(np.float32) / 255.
        return results

    def __repr__(self):
        return self.__class__.__name__ + f'(keys={self.keys})'