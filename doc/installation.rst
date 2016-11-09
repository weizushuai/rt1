Installation
============

There are currently different methods to install `rt1`. The first two are for users who just want to use the package, while the last one is for developers. All follow standard principles.


Using pip
---------

The `rt1` package is provided on `pip <https://pypi.python.org/pypi/rt1>`_. Install is as easy as::

    pip install rt1

The standard python way
-----------------------

**Note that this has not been tested yet, but is supposed to work**

You can also download the source code package from the `project website <https://pypi.python.org/pypi/rt1>`_ or from `pip <https://pypi.python.org/pypi/rt1>`_. Unpack the file you obtained into some directory (it can be a temporary directory) and then run::

    python setup.py install

If might be that you might need administrator rights for this step, as the program tries to install into system library pathes. To install into a user specific directory you can just do

    python setup.py install --home=xxxxxxxxxx

From code repository for developing
-----------------------------------

Installation from the most recent code repository is also very easy in a few steps::

    # get the code
    cd /go/to/my/directory/
    git clone git@github.com:pygeo/rt1.git .

    # set the python path
    export PYTHONPATH=`pwd`:$PYTHONPATH
    echo PYTHONPATH



Test installation sucess
------------------------
Independent how you installed `rt1`, you should test that it was sucessfull by the following tests::

    python -c "from rt1 install RT1"

If you don't get an error message, the module import was sucessfull.


