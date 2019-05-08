gitignore
---------

Add this to ``.gitignore``

    .DS_Store
    .vscode

If the directory is already on Github

    git rm -r --cached .vscode
    git commit -m 'Remove the now ignored directory ".vscode"'
    git push origin master

Documentation with sphinx
-------------------------

The documentation for this tutorial is created with sphinx. To create rapidly a starting framework do this:

    mkdir docs
    cd docs
    sphinx-quickstart

To compile the documention to HTML do this::

    cd docs
    make html

Symbolic links
--------------

The ``pygamelib`` file is kept in the top GitHub directory. Each subfolder has a symbolic link to it.

    ln -s ../pygamelib.py pygamelib.py

    ls -la
    lrwxr-xr-x   1 raphael  staff    15 May  3 21:41 pygamelib.py -> ../pygamelib.py