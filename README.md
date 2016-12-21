# Staging repo to test-build RPM packages

## Creating and building a package

### Rules

- ALWAYS start a new package from master ```git checkout master && git checkout -b package```
- ALWAYS merge your package back to master when you're done with it ```git commit && git checkout master && git merge --no-commit package```
- ALWAYS merge master to your package before working on it ```git checkout package && git merge --no-commit master```
- ALWAYS use a descriptive commit message :

```
php56e 5.5.29-3

 - Did this
 - Did that
```

### Process

- Create a branch with a ```<package-name>```
- Create SPECS/```<package-name>```.spec
- Create SOURCES/```<package-name>```/.gitkeep
- Push to get travis build it

## Uploading a package

Still TODO (deploy section of travis script + http server setup)

## Building the mock docker image

```
docker build -t fpfis/mock conf/
```

See https://travis-ci.org/ec-europa/fpfis-repo-dev/builds
