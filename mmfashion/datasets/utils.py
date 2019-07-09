from __future__ import division
import shutil
import time
import logging

import torch
import torch.nn as nn
from torch.autograd import Variable

from .In_shop import InShopDataset

def to_tensor(data):
    """Convert objects of various python types to :obj:`torch.Tensor`.
    Supported types are: :class:`numpy.ndarray`, :class:`torch.Tensor`,
    :class:`Sequence`, :class:`int` and :class:`float`.
    """
    if isinstance(data, torch.Tensor):
        return data
    elif isinstance(data, np.ndarray):
        return torch.from_numpy(data)
    elif isinstance(data, Sequence) and not mmcv.is_str(data):
        return torch.tensor(data)
    elif isinstance(data, int):
        return torch.LongTensor([data])
    elif isinstance(data, float):
        return torch.FloatTensor([data])
    else:
        raise TypeError('type {} cannot be converted to tensor.'.format(
            type(data)))


def get_basic_data(data):
    imgs = Variable(data['img']).cuda()
    target = Variable(data['label']).cuda()
    landmark = Variable(data['landmark']).cuda()

    return imgs, target, landmark

def get_data(cfg, data):
    if cfg.find_three:
       anchor_data, pos_data, neg_data = data
       anchor, anchor_lbl, anchor_lm = get_basic_data(anchor_data)
       pos, pos_lbl, pos_lm = get_basic_data(pos_data)
       neg, neg_lbl, neg_lm = get_basic_data(neg_data)
       return anchor, anchor_lm, pos, pos_lm, neg, neg_lm
       
    else:
       return get_basic_data(data)
    
def get_dataset(data_cfg):
    if data_cfg['type'] == 'In-shop':
       dataset = InShopDataset(data_cfg.img_path, data_cfg.img_file,
                              data_cfg.label_file, data_cfg.bbox_file,
                              data_cfg.landmark_file, data_cfg.img_scale,
                              data_cfg.find_three)

    else:
       raise TypeError('type {} does not exist.'.fomat(data_cfg['type']))

    return dataset 
