# Staging repo to test-build RPM packages

See https://travis-ci.org/ec-europa/fpfis-repo/builds

## Creating and building a package

### Rules

- ALWAYS start a new package from master ```git checkout master && git checkout -b package```
- ALWAYS merge your package back to master when you're done with it ```git commit && git checkout master && git merge package```
- ALWAYS merge master to your package before working on it ```git checkout package && git merge master```
- ALWAYS use a descriptive commit message :

```
php56e 5.5.29-3

 - Did this
 - Did that
```

### Process

#### First time

- Fork the repo 

#### Create a package

- Create a branch with a ```<package-name>```
- Create SPECS/```<package-name>```.spec
- Create SOURCES/```<package-name>```/.gitkeep

#### Build/test a package on local

- Run ```./build-docker.sh <VERSION> <PACKAGE>``` ( version is either 6/7, and you need docker )

#### Build/test a package on Travis

- Push to get travis build it with ```git push```

#### Publish a package from Travis
- Tag your commit with ```<package>_<version>```
- Push to ```ec-europa:fpfis-repo``` when ready with ```git push origin <package>_<version>```


## Building the mock docker image

```
docker build -t fpfis/mock conf/
```
