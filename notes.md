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