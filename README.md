Cloudtrack
======

What is it?
-----------

**cloudtrack** is a Python package for identification and tracking of convective clouds in different types of gridded datasets, i.e. 3D model output from cloud resolving model simulations or 2D data of satellite observations.

Documentation
-------------
Individual features are indentified as either maxima or minima in a two dimensional time varying field.
The volume/are associated with the identified object can be determined based on a time-varying 2D or 3D field and a threshold value. The in thre tracking step, the identified objects are linked into consistent trajectories representing the cloud over its lifecycle

Installation
------------
Required packages: trackpy scipy numpy iris scikit-learn cartopy pandas pytables 

If you are using anaconda, the following command should make sure all dependencies are met and up to date:
```
conda install -c conda-forge trackpy scipy numpy iris scikit-learn cartopy pandas pytables 
```
You can directly install the package directly from github with pip and either of the two following commands:
```
pip install --upgrade git+ssh://git@github.com/mheikenfeld/cloudtrack.git
pip install --upgrade git+https://github.com/mheikenfeld/cloudtrack.git
```

You can also clone the package with any of the two following commands
```
git clone git@github.com:mheikenfeld/cloudtrack.git 
git clone https://github.com/mheikenfeld/cloudtrack.git
```
and install the package from the locally cloned version:
```
pip install cloudtrack/
```
