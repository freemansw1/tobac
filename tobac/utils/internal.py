"""Internal tobac utilities
"""


def get_label_props_in_dict(labels):
    """Function to get the label properties into a dictionary format.

    Parameters
    ----------
    labels : 2D array-like
        Output of the `skimage.measure.label` function.

    Returns
    -------
    region_properties_dict: dict
        Output from skimage.measure.regionprops in dictionary
        format, where they key is the label number.
    """

    import skimage.measure

    region_properties_raw = skimage.measure.regionprops(labels)
    region_properties_dict = {
        region_prop.label: region_prop for region_prop in region_properties_raw
    }

    return region_properties_dict


def get_indices_of_labels_from_reg_prop_dict(region_property_dict):
    """Function to get the x and y indices (as well as point count) of
    all labeled regions.

    Parameters
    ----------
    region_property_dict : dict of region_property objects
        This dict should come from the get_label_props_in_dict function.

    Returns
    -------
    curr_loc_indices : dict
        The number of points in the label number (key: label number).

    y_indices : dict
        The y indices in the label number (key: label number).

    x_indices : dict
        The x indices in the label number (key: label number).

    Raises
    ------
    ValueError
        A ValueError is raised if there are no regions in the region
        property dict.
    """

    import numpy as np

    if len(region_property_dict) == 0:
        raise ValueError("No regions!")

    y_indices = dict()
    x_indices = dict()
    curr_loc_indices = dict()

    # loop through all skimage identified regions
    for region_prop_key in region_property_dict:
        region_prop = region_property_dict[region_prop_key]
        index = region_prop.label
        curr_y_ixs, curr_x_ixs = np.transpose(region_prop.coords)

        y_indices[index] = curr_y_ixs
        x_indices[index] = curr_x_ixs
        curr_loc_indices[index] = len(curr_y_ixs)

    return (curr_loc_indices, y_indices, x_indices)