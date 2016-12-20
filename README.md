# Staging repo to test-build RPM packages

## Creating and building a package

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
