# -*- coding: utf-8 -*-
# Created on Sun Jul 14 10:17:54 2019
# @author: Cédric Perion | Arthur Dujardin


"""
Contains reading and writing functions for ply files as well as a conversion function and other useful functions related to ply files
"""



import numpy as np
import plyfile



def read_plyfile(file_name):
    """
    Read and extract the data of a ply file.

    Parameters
    ----------
    file_name : str
        The path to the ply file.

    Raises
    ------
    FileNotFoundError
        If the file is not found, raises an error.

    Returns
    -------
    plydata : plyfile.PlyData
        The data of the cloud points file.
    """
    
    try:
        ply = open(file_name, mode='rb')
    except FileNotFoundError :
        raise FileNotFoundError("ply file not found")
    plydata = plyfile.PlyData.read(ply)
    
    return plydata

def write_plydata(plydata, data_channel, 
                  new_channel_name,  outfile_name = "my_cloud.ply"):
    """
    Create a ply file from plydata.
    Can add an additional channel to the plydata.

    Parameters
    ----------
    plydata : plyfile.PlyData
        The plydata to write in the file.
    data_channel : numpy.ndarray
        Data of the added channel.
    new_channel_name : str
        Name of the new added channel.
    outfile_name : str, optionnal
        Name of the ply file created.
        The default is "my_cloud.ply".

    Returns
    -------
    None
    """

    dtype = plydata.elements[0].data.dtype.descr
    
    # If there is a channel added
    dtype = dtype + [(new_channel_name, 'u1')]
    
    vertex = plydata.elements[0].name    
    data = []
    for i in range(len(data_channel)):
         l = tuple( list(plydata[vertex][i]) + [data_channel[i]])
         data.append(l)
        
    data = np.array(data, dtype)

    el = plyfile.PlyElement.describe(data, 'vertex')
    plyfile.PlyData([el], text=True).write(outfile_name)
    

def plydata_to_array(plydata):
    """
    Convert a plydata to numpy array.

    Parameters
    ----------
    plydata : plyfile.PlyData
        The plydata to convert.

    Returns
    -------
    numpy.ndarray
        The converted data, containing the 3D coordinates of the plydata's points.
    """
    
    data = np.array([plydata.elements[0].data['x'], 
                     plydata.elements[0].data['y'], 
                     plydata.elements[0].data['z']])

    return np.transpose(data)


def add_channel_from_plydata(plydata, coord, channel):
    """
    Add a channel to the numpy data.

    Parameters
    ----------
    plydata : plyfile.PlyData
        Raw data.
    coord : numpy.ndarray
        The coordinates of the 3D points.
    channel : str
        Name of the channel to add.

    Returns
    -------
    data : TYPE
        DESCRIPTION.
    """

    data = np.column_stack((coord, plydata.elements[0].data[channel]))
    return data

# def add_channel_from_data(data, channel_data, channel_name):
#     """
#     Add a channel (usually generated by a projection into other images) 
#     to the numpy data.

#     Parameters
#     ----------
#     data : numpy.ndarray
#         The data which contains the coordinates of every points.
#     channel_data : numpy.ndarray
#         Vector of the channel's values.
#     channel_name : str
#         DESCRIPTION.

#     Returns
#     -------
#     coord : TYPE
#         DESCRIPTION.

#     """
    
#     if len(channel_data) != len(data):
#         print("\nERROR : different size between the channel added and the matrix of coordinates points\n\n")
#     else:
#         coord = np.column_stack((data, channel_data))
#     return coord



def extract_channel_from_plydata(plydata, channel = "all"):
    """
    Extract a channel from a 3D cloud points.

    Parameters
    ----------
    plydata : plyfile.PlyData
        The data to extract the channel.
    channel : str, optional
        The name of the channel to extract. 
        The default is "all".

    Returns
    -------
    data : numpy.ndaray
        The extracted channel data.
    """
    
    data = plydata_to_array(plydata)
    if channel.lower() == "all":
        data = add_channel_from_plydata(plydata, data, "red")
        data = add_channel_from_plydata(plydata, data, "green")
        data = add_channel_from_plydata(plydata, data, "blue")
        
    elif channel.lower() == "red":
        data = add_channel_from_plydata(plydata, data, "red")
        
    elif channel.lower() == "blue":
        data = add_channel_from_plydata(plydata, data, "blue")
        
    elif channel.lower() == "green":
        data = add_channel_from_plydata(plydata, data, "green")

    return data


    