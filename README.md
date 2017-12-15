# Staging repo to test-build RPM packages

See https://drone.fpfis.eu/ec-europa/fpfis-repo

## Creating and building a package

### Rules

- Make sure you start from master.
- If you need new code from master `git merge master` in your branch 

### Process

#### Create a package

- Create a branch with a```test/<package-name>```
- Create SPECS/```<package-name>```.spec
- Create SOURCES/```<package-name>```/.gitkeep

#### Build/test a package on local

- Run ```./build-docker.sh <VERSION> <PACKAGE>``` ( version is either 6/7, and you need docker )

#### Build/test a package on Travis

- Push to get drone build it with ```git push```

#### Publish a package from Drone 

- Merge/create to the release/```<package>```
- Push to get drone publish the package to the RPM repo
