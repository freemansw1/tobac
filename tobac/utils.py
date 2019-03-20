import logging

def column_mask_from2D(mask_2D,cube,z_coord='model_level_number'):
    '''     function to turn 2D watershedding mask into a 3D mask of selected columns
    Input:
    cube:              iris.cube.Cube 
                       data cube
    mask_2D:           iris.cube.Cube 
                       2D cube containing mask (int id for tacked volumes 0 everywhere else)
    z_coord:           str
                       name of the vertical coordinate in the cube
    Output:
    mask_2D:           iris.cube.Cube 
                       3D cube containing columns of 2D mask (int id for tacked volumes 0 everywhere else)
    '''
    from copy import deepcopy
    mask_3D=deepcopy(cube)
    mask_3D.rename('segmentation_mask')
    dim=mask_3D.coord_dims(z_coord)[0]
    for i in range(len(mask_3D.coord(z_coord).points)):
        slc = [slice(None)] * len(mask_3D.shape)
        slc[dim] = slice(i,i+1)    
        mask_out=mask_3D[slc]
        mask_3D.data[slc]=mask_2D.core_data()
    return mask_3D


def mask_cube_cell(variable_cube,mask,cell,track):
    ''' Mask cube for tracked volume of an individual cell   
    Input:
    variable_cube:     iris.cube.Cube 
                       unmasked data cube
    mask:              iris.cube.Cube 
                       cube containing mask (int id for tacked volumes 0 everywhere else)
    cell:          int
                       interger id of cell to create masked cube for
    Output:
    variable_cube_out: iris.cube.Cube 
                       Masked cube with data for respective cell
    '''
    from copy import deepcopy
    variable_cube_out=deepcopy(variable_cube)
    feature_ids=track.loc[track['cell']==cell,'feature'].values
    variable_cube_out=mask_cube_features(variable_cube,mask,feature_ids)
    return variable_cube_out


def mask_cube_untracked(variable_cube,mask):
    ''' Mask cube for untracked volume 
    Input:
    variable_cube:     iris.cube.Cube 
                       unmasked data cube
    mask:              iris.cube.Cube 
                       cube containing mask (int id for tacked volumes 0 everywhere else)
    Output:
    variable_cube_out: iris.cube.Cube 
                       Masked cube for untracked volume
    '''
    import numpy as np 
    from copy import deepcopy
    variable_cube_out=deepcopy(variable_cube)
    mask_i=mask.data!=0
    variable_cube_out.data=np.ma.array(variable_cube_out.data,mask=mask_i)    
    return variable_cube_out

def mask_cube(cube_in,mask):
    ''' Mask cube where mask is larger than zero
    Input:
    cube_in:     iris.cube.Cube 
                       unmasked data cube
    mask:              numpy.ndarray or dask.array 
                       mask to use for masking, >0 where cube is supposed to be masked
    Output:
    cube_out:          iris.cube.Cube 
                       Masked cube
    '''
    from numpy import ones_like,ma
    from copy import deepcopy
    mask_array=ones_like(cube_in.data,dtype=bool)
    mask_array[mask>0]=False
    mask_array[mask==0]=True
    cube_out=deepcopy(cube_in)
    cube_out.data=ma.array(cube_in.data,mask=mask_array)
    return cube_out

def mask_cell(Mask,cell,track,masked=False):
    ''' create mask for specific cell
    Input:
    variable_cube:     iris.cube.Cube 
                       unmasked data cube
    mask:              iris.cube.Cube 
                       cube containing mask (int id for tacked volumes 0 everywhere else)
    Output:
    variable_cube_out: numpy.ndarray 
                       Masked cube for untracked volume
    '''
    feature_ids=track.loc[track['cell']==cell,'feature'].values
    Mask_i=mask_features(Mask,feature_ids,masked=masked)
    return Mask_i   

def mask_cell_surface(Mask,cell,track,masked=False,z_coord='model_level_number'):
    ''' Mask cube for untracked volume 
    Input:
    variable_cube:     iris.cube.Cube 
                       unmasked data cube
    mask:              iris.cube.Cube 
                       cube containing mask (int id for tacked volumes 0 everywhere else)
    Output:
    variable_cube_out: iris.cube.Cube 
                       Masked cube for untracked volume
    '''
    feature_ids=track.loc[track['cell']==cell,'feature'].values
    Mask_i_surface=mask_features_surface(Mask,feature_ids,masked=masked,z_coord=z_coord)
    return Mask_i_surface

def mask_cell_columns(Mask,cell,track,masked=False,z_coord='model_level_number'):
    ''' Mask cube for untracked volume 
    Input:
    variable_cube:     iris.cube.Cube 
                       unmasked data cube
    mask:              iris.cube.Cube 
                       cube containing mask (int id for tacked volumes 0 everywhere else)
    Output:
    variable_cube_out: iris.cube.Cube 
                       Masked cube for untracked volume
    '''
    feature_ids=track.loc[track['cell']==cell].loc['feature']
    Mask_i=mask_features_columns(Mask,feature_ids,masked=masked,z_coord=z_coord)
    return Mask_i

def mask_cube_features(variable_cube,mask,feature_ids):
    ''' Mask cube for tracked volume of an individual cell   
    Input:
    variable_cube:     iris.cube.Cube 
                       unmasked data cube
    mask:              iris.cube.Cube 
                       cube containing mask (int id for tacked volumes 0 everywhere else)
    cell:          int
                       interger id of cell to create masked cube for
    Output:
    variable_cube_out: iris.cube.Cube 
                       Masked cube with data for respective cell
    '''
    import numpy as np 
    from copy import deepcopy
    variable_cube_out=deepcopy(variable_cube)
    mask_i=~np.isin(mask.data,feature_ids)
    variable_cube_out.data=np.ma.array(variable_cube_out.data,mask=mask_i)    
    return variable_cube_out



def mask_features(Mask,feature_ids,masked=False):
    ''' create mask for specific cell
    Input:
    variable_cube:     iris.cube.Cube 
                       unmasked data cube
    mask:              iris.cube.Cube 
                       cube containing mask (int id for tacked volumes 0 everywhere else)
    Output:
    variable_cube_out: numpy.ndarray 
                       Masked cube for untracked volume
    '''
    import numpy as np 
    from copy import deepcopy
    Mask_i=deepcopy(Mask)
    Mask_i.data[~np.isin(Mask_i.data,feature_ids)]=0
    if masked:
        Mask_i.data=np.ma.array(Mask_i.data,mask=Mask_i.data)
    return Mask_i   

def mask_features_surface(Mask,feature_ids,masked=False,z_coord='model_level_number'):
    ''' Mask cube for untracked volume 
    Input:
    variable_cube:     iris.cube.Cube 
                       unmasked data cube
    mask:              iris.cube.Cube 
                       cube containing mask (int id for tacked volumes 0 everywhere else)
    Output:
    variable_cube_out: iris.cube.Cube 
                       Masked cube for untracked volume
    '''
    from iris.analysis import MAX
    import numpy as np 
    from copy import deepcopy
    Mask_i=deepcopy(Mask)
    Mask_i.data[~np.isin(Mask_i.data,feature_ids)]=0
    for coord in  Mask_i.coords():
        if coord.ndim>1 and Mask_i.coord_dims(z_coord)[0] in Mask_i.coord_dims(coord):
            Mask_i.remove_coord(coord.name())
    Mask_i_surface=Mask_i.collapsed(z_coord,MAX)
    if masked:
        Mask_i_surface.data=np.ma.array(Mask_i_surface.data,mask=Mask_i_surface.data)
    return Mask_i_surface    

def mask_features_columns(Mask,feature_ids,masked=False,z_coord='model_level_number'):
    ''' Mask cube for untracked volume 
    Input:
    variable_cube:     iris.cube.Cube 
                       unmasked data cube
    mask:              iris.cube.Cube 
                       cube containing mask (int id for tacked volumes 0 everywhere else)
    Output:
    variable_cube_out: iris.cube.Cube 
                       Masked cube for untracked volume
    '''
    from iris.analysis import MAX
    import numpy as np 
    from copy import deepcopy
    Mask_i=deepcopy(Mask)
    Mask_i.data[~np.isin(Mask_i.data,feature_ids)]=0
    for coord in  Mask_i.coords():
        if coord.ndim>1 and Mask_i.coord_dims(z_coord)[0] in Mask_i.coord_dims(coord):
            Mask_i.remove_coord(coord.name())
    Mask_i_surface=Mask_i.collapsed(z_coord,MAX)
    for cube_slice in Mask_i.slices(['time','x','y']):
            cube_slice.data=Mask_i_surface.core_data()
    if masked:
        Mask_i.data=np.ma.array(Mask_i.data,mask=Mask_i.data)
    return Mask_i


#def constraint_cell(track,mask_cell,width=None,x=None,):
#     from iris import Constraint
#     import numpy as np
#    
#     time_coord=mask_cell.coord('time')
#     time_units=time_coord.units
#    
#     def time_condition(cell):
#         return time_units.num2date(track.head(n=1)['time']) <= cell <= time_units.num2date(track.tail(n=1)['time'])
#
#     constraint_time=Constraint(time=time_condition)
##     mask_cell_i=mask_cell.extract(constraint_time)
#     mask_cell_surface_i=mask_cell_surface.extract(constraint_time)
#    
#     x_dim=mask_cell_surface_i.coord_dims('projection_x_coordinate')[0]
#     y_dim=mask_cell_surface_i.coord_dims('projection_y_coordinate')[0]
#     x_coord=mask_cell_surface_i.coord('projection_x_coordinate')
#     y_coord=mask_cell_surface_i.coord('projection_y_coordinate')
#    
#     if (mask_cell_surface_i.core_data()>0).any():
#         box_mask_i=get_bounding_box(mask_cell_surface_i.core_data(),buffer=1)
#
#         box_mask=[[x_coord.points[box_mask_i[x_dim][0]],x_coord.points[box_mask_i[x_dim][1]]],
#                  [y_coord.points[box_mask_i[y_dim][0]],y_coord.points[box_mask_i[y_dim][1]]]]
#     else:
#         box_mask=[[np.nan,np.nan],[np.nan,np.nan]]
#
#         x_min=box_mask[0][0]
#         x_max=box_mask[0][1]
#         y_min=box_mask[1][0]
#         y_max=box_mask[1][1]
#     constraint_x=Constraint(projection_x_coordinate=lambda cell: int(x_min) < cell < int(x_max))
#     constraint_y=Constraint(projection_y_coordinate=lambda cell: int(y_min) < cell < int(y_max))
#
#     constraint=constraint_time & constraint_x & constraint_y
#     return constraint
    
def add_coordinates(t,variable_cube):
    import numpy as np
    ''' Function adding coordinates from the tracking cube to the trajectories: time, longitude&latitude, x&y dimensions
    Input:
    t:             pandas DataFrame
                   trajectories/features
    variable_cube: iris.cube.Cube 
                   Cube containing the dimensions 'time','longitude','latitude','x_projection_coordinate','y_projection_coordinate', usually cube that the tracking is performed on
    Output:
    t:             pandas DataFrame 
                   trajectories with added coordinated
    '''
    from scipy.interpolate import interp2d, interp1d

    logging.debug('start adding coordinates from cube')

    # pull time as datetime object and timestr from input data and add it to DataFrame:    
    t['time']=None
    t['timestr']=None
    
    
    logging.debug('adding time coordinate')

    time_in=variable_cube.coord('time')
    time_in_datetime=time_in.units.num2date(time_in.points)
    
    for i, row in t.iterrows():
        t.loc[i,'time']=time_in_datetime[int(row['frame'])]
        t.loc[i,'timestr']=time_in_datetime[int(row['frame'])].strftime('%Y-%m-%d %H:%M:%S')


    # Get list of all coordinates in input cube except for time (already treated):
    coord_names=[coord.name() for coord in  variable_cube.coords()]
    coord_names.remove('time')
    
    logging.debug('time coordinate added')

    # chose right dimension for horizontal axis based on time dimension:    
    ndim_time=variable_cube.coord_dims('time')[0]
    if ndim_time==0:
        hdim_1=1
        hdim_2=2
    elif ndim_time==1:
        hdim_1=0
        hdim_2=2
    elif ndim_time==2:
        hdim_1=0
        hdim_2=1
    
    # create vectors to use to interpolate from pixels to coordinates
    dimvec_1=np.arange(variable_cube.shape[hdim_1])
    dimvec_2=np.arange(variable_cube.shape[hdim_2])

    # loop over coordinates in input data:
    for coord in coord_names:
        logging.debug('adding coord: '+ coord)
        # interpolate 2D coordinates:
        if variable_cube.coord(coord).ndim==1:

            if variable_cube.coord_dims(coord)==(hdim_1,):
                t[coord]=np.nan            
                f=interp1d(dimvec_1,variable_cube.coord(coord).points,fill_value="extrapolate")
                for i, row in t.iterrows():
                    t.loc[i,coord]=float(f(row['hdim_1']))

            if variable_cube.coord_dims(coord)==(hdim_2,):
                t[coord]=np.nan            
                f=interp1d(dimvec_2,variable_cube.coord(coord).points,fill_value="extrapolate")
                for i, row in t.iterrows():
                    t.loc[i,coord]=float(f(row['hdim_2']))

        # interpolate 2D coordinates:
        elif variable_cube.coord(coord).ndim==2:

            t[coord]=np.nan            
            if variable_cube.coord_dims(coord)==(hdim_1,hdim_2):
                f=interp2d(dimvec_2,dimvec_1,variable_cube.coord(coord).points)
                for i, row in t.iterrows():
                    t.loc[i,coord]=float(f(row['hdim_2'],row['hdim_1']))
            if variable_cube.coord_dims(coord)==(hdim_2,hdim_1):
                f=interp2d(dimvec_1,dimvec_2,variable_cube.coord(coord).points)
                for i, row in t.iterrows():
                    t.loc[i,coord]=float(f(row['hdim_1'],row['hdim_2']))
        
        # interpolate 3D coordinates:            
        # mainly workaround for wrf latitude and longitude (to be fixed in future)
        
        elif variable_cube.coord(coord).ndim==3:

            t[coord]=np.nan
            if variable_cube.coord_dims(coord)==(ndim_time,hdim_1,hdim_2):
                f=interp2d(dimvec_2,dimvec_1,variable_cube[0,:,:].coord(coord).points)
                for i, row in t.iterrows():
                    t.loc[i,coord]=float(f(row['hdim_2'],row['hdim_1']))
            
            if variable_cube.coord_dims(coord)==(ndim_time,hdim_2,hdim_1):
                f=interp2d(dimvec_1,dimvec_2,variable_cube[0,:,:].coord(coord).points)
                for i, row in t.iterrows():
                    t.loc[i,coord]=float(f(row['hdim_1'],row['hdim_2']))
        
            if variable_cube.coord_dims(coord)==(hdim_1,ndim_time,hdim_2):
                f=interp2d(dimvec_2,dimvec_1,variable_cube[:,0,:].coord(coord).points)
                for i, row in t.iterrows():
                    t.loc[i,coord]=float(f(row['hdim_2'],row['hdim_1']))
                    
            if variable_cube.coord_dims(coord)==(hdim_1,hdim_2,ndim_time):
                f=interp2d(dimvec_2,dimvec_1,variable_cube[:,:,0].coord(coord).points)
                for i, row in t.iterrows():
                    t.loc[i,coord]=float(f(row['hdim_2'],row['hdim_1']))
                    
                    
            if variable_cube.coord_dims(coord)==(hdim_2,ndim_time,hdim_1):
                f=interp2d(dimvec_1,dimvec_2,variable_cube[:,0,:].coord(coord).points)
                for i, row in t.iterrows():
                    t.loc[i,coord]=float(f(row['hdim_1'],row['hdim_2']))
                    
            if variable_cube.coord_dims(coord)==(hdim_2,hdim_1,ndim_time):
                f=interp2d(dimvec_1,dimvec_2,variable_cube[:,:,0].coord(coord).points)
                for i, row in t.iterrows():
                    t.loc[i,coord]=float(f(row['hdim_1'],row['hdim_2']))
        logging.debug('added coord: '+ coord)

    return t

def get_bounding_box(x,buffer=1):
    from numpy import delete,arange,diff,nonzero,array
    """ Calculates the bounding box of a ndarray
    https://stackoverflow.com/questions/31400769/bounding-box-of-numpy-array
    """
    mask = x == 0

    bbox = []
    all_axis = arange(x.ndim)
    #loop over dimensions
    for kdim in all_axis:
        nk_dim = delete(all_axis, kdim)
        mask_i = mask.all(axis=tuple(nk_dim))
        dmask_i = diff(mask_i)
        idx_i = nonzero(dmask_i)[0]
        # for case where there is no value in idx_i
        if len(idx_i) == 0:
            idx_i=array([0,x.shape[kdim]-1])
        # for case where there is only one value in idx_i
        elif len(idx_i) == 1:
            idx_i=array([idx_i,idx_i])
        # make sure there is two values in idx_i
        elif len(idx_i) > 2:
            idx_i=array([idx_i[0],idx_i[-1]])
        # caluclate min and max values for idx_i and append them to list
        idx_min=max(0,idx_i[0]+1-buffer)
        idx_max=min(x.shape[kdim]-1,idx_i[1]+1+buffer)
        bbox.append([idx_min, idx_max])
    return bbox

def get_spacings(field_in,grid_spacing=None,time_spacing=None):
    import numpy as np
    from copy import deepcopy
    # set horizontal grid spacing of input data
    # If cartesian x and y corrdinates are present, use these to determine dxy (vertical grid spacing used to transfer pixel distances to real distances):
    coord_names=[coord.name() for coord in  field_in.coords()]
    
    if (('projection_x_coordinate' in coord_names and 'projection_y_coordinate' in coord_names) and  (grid_spacing is None)):
        x_coord=deepcopy(field_in.coord('projection_x_coordinate'))
        x_coord.convert_units('metre')
        dx=np.diff(field_in.coord('projection_y_coordinate')[0:2].points)[0]
        y_coord=deepcopy(field_in.coord('projection_y_coordinate'))
        y_coord.convert_units('metre')
        dy=np.diff(field_in.coord('projection_y_coordinate')[0:2].points)[0]
        dxy=0.5*(dx+dy)
    elif grid_spacing is not None:
        dxy=grid_spacing
    else:
        ValueError('no information about grid spacing, need either input cube with projection_x_coord and projection_y_coord or keyword argument grid_spacing')
    
    # set horizontal grid spacing of input data
    if (time_spacing is None):    
        # get time resolution of input data from first to steps of input cube:
        time_coord=field_in.coord('time')
        dt=(time_coord.units.num2date(time_coord.points[1])-time_coord.units.num2date(time_coord.points[0])).seconds
    elif (time_spacing is not None):
        # use value of time_spacing for dt:
        dt=time_spacing
    return dxy,dt