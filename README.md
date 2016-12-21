# Staging repo to test-build RPM packages

See https://travis-ci.org/ec-europa/fpfis-repo-dev/builds

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

- Fork the repo on your own user account
- Clone your own repo
- Add fpfis-repo as "publish" remote with ```git remote add publish git@github.com:ec-europa/fpfis-repo.git```

#### Create a package

- Create a branch with a ```<package-name>```
- Create SPECS/```<package-name>```.spec
- Create SOURCES/```<package-name>```/.gitkeep

#### Build/test a package on local

- Run ```./build-docker.sh <VERSION> <PACKAGE>``` ( version is either 6/7, and you need docker )

#### Build/test a package on Travis

- Push to get travis build it with ```git push``` (you need a Travis account)

#### Publish a package from Travis
- Push to ```ec-europa:fpfis-repo``` publish when ready with ```git push publish```


## Building the mock docker image

```
docker build -t fpfis/mock conf/
```

## TODO

deploy section of travis script + http server setup
