'''
    Shared module of crip.

    by z0gSh1u @ https://github.com/z0gSh1u/crip
'''

import numpy as np
import cv2


def rotate(img, deg):
    """
        Rotate img by deg [DEG] (multiple of 90) clockwise.
    """
    deg = int(deg % 360)
    if deg == 0:
        return img
    degToCode = {
        '90': cv2.ROTATE_90_CLOCKWISE,
        '180': cv2.ROTATE_180,
        '270': cv2.ROTATE_90_COUNTERCLOCKWISE,
    }
    return cv2.rotate(img, degToCode[str(deg)])


def resize(projection, dsize=None, fx=None, fy=None, interp='bicubic'):
    """
        Resize the projection to `dsize` (H, W) (if dsize is not None) or scale by ratio `(fx, fy)`
        using `interp` (bicubic, linear, nearest available).
    """
    if dsize is None:
        assert fx is not None or fy is not None
        fx = fx if fx else 1
        fy = fy if fy else 1
    else:
        assert fx is None and fy is None
    interp_ = {'bicubic': cv2.INTER_CUBIC, 'linear': cv2.INTER_LINEAR, 'nearest': cv2.INTER_NEAREST}
    # OpenCV dsize is in (W, H) form, so we reverse it.
    return cv2.resize(projection.astype(np.float32), dsize[::-1], None, fx, fy, interpolation=interp_[interp])


def binning(projection, binning=(1, 1)):
    """
        Perform binning on row and col directions. `binning=(rowBinning, colBinning)`.
    """
    res = np.array(projection[::binning[0], ::binning[1]])
    return res


def gaussianSmooth(projection, ksize, sigma):
    """
        Perform Gaussian smooth with kernel size = ksize and Gaussian \sigma = sigma (int or tuple (x, y)).
    """
    if isinstance(sigma, int):
        sigma = (sigma, sigma)
    return cv2.GaussianBlur(projection.astype(np.float32), ksize, sigmaX=sigma[0], sigmaY=sigma[1])
