# Release Process

Make sure that you:

* updated the changelog (/docs/README.md)
* checked the README for pypi (/docs/README_pypi.md)

## Pull-Request into master

* Push changes to Github
* Create PR into master
* Github will run workflows (tox in our case)
* Merge PR when all is well (merge commit, not squash or fast forward)

A commit in master is a release. Pull the new commit and tag it:

```shell
git checkout master
git tag vX.Y.Z
```

Then push the tag back to Github:

```shell
git push origin vX.Y.Z
```

Tagging is important because the version of the package we are going to build
is derived from this tag.

## Build

From the root of the project folder, run

```
python3 -m build --wheel
```

This generates a wheel distribution in /dist.

## Test-pypi

Upload to test.pypi.org by (make sure the '*' selects only your package):

```
twine upload -r testpypi dist/*
```

Note: Your `~/.pypirc` has to specify a `[testpypi]` section providing your
username and password.

## pypi

If everything worked as expected, run

```
twine upload dist/*
```

Note: Your `~/.pypirc` has to specify a `[pypi]` section providing your
username and password.

## Test Install

Activate an environment that does not have a (development-) installation of
this package. Run

```
pip install ppf.datamatrix
```

This should download and install the version you've just released.

## GitHub

Finally, go to github, find the new tag, click the ellipsis, click
"create release". Enter the tag name as title and copy the commit message
into the description.
