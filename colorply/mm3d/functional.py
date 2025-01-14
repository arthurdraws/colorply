"""
Read and extract informations from MicMac xml calibration files.
Functional implementation.
"""

import numpy as np
from lxml import etree


def read_orientation(nameIMGxml):
    """
    This function extracts the rotation matrix from the xml file.

    Parameters
    ----------
    nameIMGxml : str
        name of the file generated by MM3D.

    .. note::
        Usually, it is "Orientation-Im[n°i].JPG.xml"

    Returns
    -------
    np.ndarray
        Rotation of the img, of shape 3x3

    """
    # Get the file
    tree = etree.parse(nameIMGxml)

    # Read the lines of the matrix
    for user in tree.xpath("/ExportAPERO/OrientationConique/Externe/ParamRotation/CodageMatr/L1"):
        # print(user.text)
        L1 = user.text.split(" ")
    for user in tree.xpath("/ExportAPERO/OrientationConique/Externe/ParamRotation/CodageMatr/L2"):
        # print(user.text)
        L2 = user.text.split(" ")
    for user in tree.xpath("/ExportAPERO/OrientationConique/Externe/ParamRotation/CodageMatr/L3"):
        # print(user.text)
        L3 = user.text.split(" ")

    matrix_rotation = np.array([L1, L2, L3], float)
    return matrix_rotation


def read_S(nameIMGxml):
    """
    This function extracts the images's center from the xml file.

    .. note::
        Usually, it is "Orientation-Im[n°i].JPG.xml"

    Parameters
    ----------
    nameIMGxml : str
        The name of the file generated by MM3D.

    Returns
    -------
    np.ndarray
        Center of the IMG, of shape 1x3

    """
    tree = etree.parse(nameIMGxml)

    for user in tree.xpath("/ExportAPERO/OrientationConique/Externe/Centre"):
        # print(user.text)
        S = user.text.split(" ")

    center = np.array(S, float)
    return np.transpose(center)


def read_ori(nameIMGxml):
    """
    This function extracts the rotation matrix from the xml file
    and extracts the images's center from the xml file.

    .. note::
        Usually, it is "Orientation-Im[n°i].JPG.xml"

    Parameters
    ----------
    nameIMGxml : str
        The name of the file generated by MM3D.

    Returns
    -------
    tuple
        The rotation of the img, the center of the IMG,
        tuple(np.array(matrix rotation), np.array(coord S))

    """
    tree = etree.parse(nameIMGxml)
    # The lines of the matrix
    for user in tree.xpath("/ExportAPERO/OrientationConique/Externe/ParamRotation/CodageMatr/L1"):
        # print(user.text)
        L1 = user.text.split(" ")
    for user in tree.xpath("/ExportAPERO/OrientationConique/Externe/ParamRotation/CodageMatr/L2"):
        # print(user.text)
        L2 = user.text.split(" ")
    for user in tree.xpath("/ExportAPERO/OrientationConique/Externe/ParamRotation/CodageMatr/L3"):
        # print(user.text)
        L3 = user.text.split(" ")

    matrix_rotation = np.array([L1, L2, L3], float)

    for user in tree.xpath("/ExportAPERO/OrientationConique/Externe/Centre"):
        # print(user.text)
        S = user.text.split(" ")
    center = np.array(S, float)

    return {'R': matrix_rotation, 'S': center}


##

def read_calib_F(calibxml):
    """
    This function extracts the calibration parameters from the xml file.

    .. note::
        Usually, it is similar to "AutoCal_[Focal]_[CameraName].xml"

    Parameters
    ----------
    calibxml : str
        Name of the camera calibration file

    Returns
    -------
    np.ndarray
        Coordinates of the point F (focale, units : pix)

    """
    tree = etree.parse(calibxml)

    for user in tree.xpath("/ExportAPERO/CalibrationInternConique/PP"):
        PP = user.text.split(" ")
    for user in tree.xpath("/ExportAPERO/CalibrationInternConique/F"):
        F = user.text
    PP.append("-" + F)
    return np.transpose(np.array(PP, float))


def read_calib_PPS(calibxml):
    """
    This function extracts the calibration parameters from the xml file.

    .. note::
        Usually, it is similar to "AutoCal_[Focal]_[CameraName].xml"

    Parameters
    ----------
    calibxml : str
        Name of the camera calibration file

    Returns
    -------
    np.ndarray
        Coordinates of the PPS, of shape 1x3

    """
    tree = etree.parse(calibxml)

    for user in tree.xpath("/ExportAPERO/CalibrationInternConique/CalibDistortion/ModRad/CDist"):
        PPS = user.text.split(" ")

    PPS.append("0")

    return np.transpose(np.array(PPS, float))


def read_calib_distorsion(calibxml):
    """
    This function extracts the calibration parameters from the xml file.

    .. note::
        Usually, it is similar to "AutoCal_[Focal]_[CameraName].xml"

    Parameters
    ----------
    calibxml : str
        Name of the camera calibration file

    Returns
    -------
    np.ndarray
        Distorsion coefficients [a, b, c]

    """
    tree = etree.parse(calibxml)

    coeffDist = []
    for user in tree.xpath("/ExportAPERO/CalibrationInternConique/CalibDistortion/ModRad/CoeffDist"):
        coeffDist.append(user.text)

    return {'a': coeffDist[0], 'b': coeffDist[1], 'c': coeffDist[2]}


##

def read_size(calibxml):
    """
    This function extracts the size of an image from the xml file.

    .. note::
        Usually, it is similar to "AutoCal_[Focal]_[CameraName].xml"

    Parameters
    ----------
    calibxml : str
        Name of the camera calibration file

    Returns
    -------
        np.ndarray
        The size of the image resolution

    """
    tree = etree.parse(calibxml)

    for user in tree.xpath("/ExportAPERO/CalibrationInternConique/SzIm"):
        size = user.text.split(" ")

    return np.array(size, int)


def read_calib(calibxml):
    """
    This function extracts the calibration parameters from the xml file.

    .. note::
        Usually, it is similar to "AutoCal_[Focal]_[CameraName].xml"

    Parameters
    ----------
    calibxml : str
        Name of the camera calibration file

    Returns
    -------
    dict
        Returns F, PPS, distorsion coefficients a, b, c, size

    """
    tree = etree.parse(calibxml)

    coeffDist = []
    for user in tree.xpath("/ExportAPERO/CalibrationInternConique/CalibDistortion/ModRad/CoeffDist"):
        coeffDist.append(user.text)
    coeffDist = {'a': float(coeffDist[0]), 'b': float(coeffDist[1]), 'c': float(coeffDist[2])}

    for user in tree.xpath("/ExportAPERO/CalibrationInternConique/CalibDistortion/ModRad/CDist"):
        PPS = user.text.split(" ")
    PPS.append("0")
    PPS = np.array(PPS, float)

    for user in tree.xpath("/ExportAPERO/CalibrationInternConique/PP"):
        PP = user.text.split(" ")
    for user in tree.xpath("/ExportAPERO/CalibrationInternConique/F"):
        F = user.text
    PP.append("-" + F)
    F = np.array(PP, float)

    for user in tree.xpath("/ExportAPERO/CalibrationInternConique/SzIm"):
        size = user.text.split(" ")
    size = np.array(size, int)

    return {'F': F, 'PPS':PPS, 'cdist': coeffDist, 'size': size}
