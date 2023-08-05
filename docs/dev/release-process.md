# Release Process

Make sure that you:

- successfully ran tox
- bumped up the version number (__init__.py of package)
- updated the changelog (/docs/README.md)
- checked the README for pypi (/docs/README_pypi.md)

## Build

From the root of the project folder, run

```
python3 -m build .
```

This generates new source- and wheel distributions in /dist.

## Test-pypi

Upload to test.pypi.org by (make sure the '*' selects only your new .tar.gz
and .whl packages):

```
twine upload -r testpypi dist/*
```

## pypi

If everything worked as expected, run

```
twine upload dist/*
```

## Test Install

Activate an environment that does not have a (development-) installation of
ppf.sample. Run

```
pip install ppf.sample
```

This should download and install the version you've just released.


## Merge into master

```
git checkout master
git merge develop --no-ff
```

Commit message is:

```
0.1.2

- what has been changed
- also changed has this
```

Then:

```
git tag v0.1.2
git checkout develop
git rebase master
git push
git push origin v0.1.2
```

## GitHub

Finally, go to github, find the new tag, click the ellipsis, click
"create release". Enter the tag name as title and copy the commit message
into the description.
