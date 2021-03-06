'''
    Shared module of crip.

    https://github.com/z0gSh1u/crip
'''

__all__ = [
    'rotate', 'verticalFlip', 'horizontalFlip', 'stackFlip', 'resize', 'gaussianSmooth', 'stackImages', 'splitImages',
    'binning', 'transpose', 'permute'
]

import numpy as np
import cv2

from .utils import ConvertListNDArray, cripAssert, inArray, is2D, is2or3D, is3D, isInt, isType
from ._typing import *


@ConvertListNDArray
def rotate(img: TwoOrThreeD, deg: int) -> TwoOrThreeD:
    '''
        Rotate the image or each image in a volume by deg [DEG] (multiple of 90) clockwise.
    '''
    deg = int(deg % 360)
    cripAssert(deg % 90 == 0, 'deg should be multiple of 90.')

    k = deg // 90
    axes = (1, 2) if is3D(img) else (0, 1)

    return np.rot90(img, -k, axes)


def verticalFlip(img: TwoOrThreeD, copy=False) -> TwoOrThreeD:
    '''
        Vertical flip one image, or each image in a volume.

        Set `copy = True` to get a copy of array, otherwise a view only.
    '''
    cripAssert(is2or3D(img), 'img should be 2D or 3D.')

    if copy:
        return np.array(img[..., ::-1, :], copy=True)
    else:
        return img[..., ::-1, :]


def horizontalFlip(img: TwoOrThreeD, copy=False) -> TwoOrThreeD:
    '''
        Horizontal flip one image, or each image in a volume.
        
        Set `copy = True` to get a copy of array, otherwise a view only.
    '''
    cripAssert(is2or3D(img), 'img should be 2D or 3D.')

    if copy:
        return np.array(img[..., ::-1], copy=True)
    else:
        return img[..., ::-1]


def stackFlip(img: ThreeD, copy=False) -> ThreeD:
    '''
        Flip a stack w.r.t. z-axis, i.e., reverse slices.

        Set `copy = True` to get a copy of array, otherwise a view only.
    '''
    cripAssert(is3D(img), 'img should be 3D.')

    if copy:
        return np.array(np.flip(img, axis=0), copy=True)
    else:
        return np.flip(img, axis=0)


def resize(img: TwoOrThreeD,
           dsize: Tuple[int] = None,
           scale: Tuple[Or[float, int]] = None,
           interp: str = 'bicubic') -> TwoOrThreeD:
    '''
        Resize the image or each image in a volume to `dsize = (H, W)` (if dsize is not None) or scale 
        by `scale = (facH, facW)` using `interp` (bicubic, linear, nearest available).
    '''
    cripAssert(inArray(interp, ['bicubic', 'linear', 'nearest']), 'Invalid interp method.')

    if dsize is None:
        cripAssert(scale is not None, 'dsize and scale cannot be None at the same time.')
        cripAssert(len(scale) == 2, 'scale should have length 2.')
        fH, fW = scale
    else:
        cripAssert(scale is None, 'scale should not be set when dsize is set.')
        # OpenCV dsize is in (W, H) form, so we reverse it.
        dsize = dsize[::-1]
        fH = fW = None

    interp_ = {'bicubic': cv2.INTER_CUBIC, 'linear': cv2.INTER_LINEAR, 'nearest': cv2.INTER_NEAREST}

    if is3D(img):
        c, _, _ = img.shape
        res = [cv2.resize(img[i, ...], dsize, None, fW, fH, interpolation=interp_[interp]) for i in range(c)]
        return np.array(res)
    else:
        return cv2.resize(img, dsize, None, fW, fH, interpolation=interp_[interp])


def gaussianSmooth(img: TwoOrThreeD, sigma: Or[float, int, Tuple[Or[float, int]]], ksize: int = None):
    '''
        Perform Gaussian smooth with kernel size = ksize and Gaussian \sigma = sigma (int or tuple (x, y)).
        
        Leave `ksize = None` to auto determine to include the majority of Gaussian energy.
    '''
    if ksize is not None:
        cripAssert(isInt(ksize), 'ksize should be int.')

    if not isType(sigma, Tuple):
        sigma = (sigma, sigma)

    if is3D(img):
        c, _, _ = img.shape
        res = [cv2.GaussianBlur(img[i, ...], ksize, sigmaX=sigma[0], sigmaY=sigma[1]) for i in range(c)]
        return np.array(res)
    else:
        return cv2.GaussianBlur(img, ksize, sigmaX=sigma[0], sigmaY=sigma[1])


@ConvertListNDArray
def stackImages(imgList: ListNDArray, dtype=None) -> NDArray:
    '''
        Stack seperate image into one numpy array. I.e., views * (h, w) -> (views, h, w).

        Convert dtype with `dtype != None`.
    '''
    if dtype is not None:
        imgList = imgList.astype(dtype)

    return imgList


def splitImages(imgs: ThreeD, dtype=None) -> List[NDArray]:
    '''
        Split stacked image into seperate numpy arrays. I.e., (views, h, w) -> views * (h, w).

        Convert dtype with `dtype != None`.
    '''
    cripAssert(is3D(imgs), 'imgs should be 3D.')

    if dtype is not None:
        imgs = imgs.astype(dtype)

    return list(imgs)


@ConvertListNDArray
def binning(img: TwoOrThreeD, rate: int = 1, axis='y') -> TwoOrThreeD:
    '''
        Perform binning on certain `axis` with `rate`.
    '''
    cripAssert(isInt(rate) and rate > 0, 'rate should be positive int.')
    cripAssert(inArray(axis, ['x', 'y', 'z']), 'Invalid axis.')

    if is2D(img):
        cripAssert(axis != 'z', 'img is 2D, while axis is z.')

    if axis == 'x':
        return img[..., ::rate]
    if axis == 'y':
        return img[..., ::rate, :]
    if axis == 'z':
        return img[::rate, ...]


@ConvertListNDArray
def transpose(vol: TwoOrThreeD, order: tuple) -> TwoOrThreeD:
    '''
        Transpose vol with axes swapping `order`.
    '''
    if is2D(vol):
        cripAssert(len(order) == 2, 'order should have length 2 for 2D input.')
    if is3D(vol):
        cripAssert(len(order) == 3, 'order should have length 3 for 3D input.')

    return vol.transpose(order)


@ConvertListNDArray
def permute(vol: ThreeD, from_: str, to: str) -> ThreeD:
    '''
        Permute axes (transpose) from `from_` to `to`, reslicing the reconstructed volume.

        Valid directions are: 'sagittal', 'coronal', 'transverse'.
    '''
    dirs = ['sagittal', 'coronal', 'transverse']

    cripAssert(from_ in dirs, f'Invalid direction string: {from_}')
    cripAssert(to in dirs, f'Invalid direction string: {to}')

    dirFrom = dirs.index(from_)
    dirTo = dirs.index(to)

    orders = [
        # to sag       cor         tra      # from
        [(0, 1, 2), (2, 0, 1), (2, 0, 1)],  # sag
        [(1, 2, 0), (0, 1, 2), (0, 2, 1)],  # cor
        [(2, 0, 1), (0, 2, 1), (0, 1, 2)],  # tra
    ]
    order = orders[dirFrom][dirTo]

    return transpose(vol, order)