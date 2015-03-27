# Jython Vert.x API Implementation Module

This project builds a Vert.x module which implements Python Vert.x API support using Jython.

All Vert.x language support is implemented in the form of modules which are (potentially) loaded on demand by Vert.x when needed.

## Addendum

### What modifications did I make

1. Replaced jython package jar file at ```extralibs``` with 2.7 Beta 4 version
2. Updated vertx/gradle version on ```gradle.properties``` to 2.1.5

 ```
modowner=org.vertx
modname=lang-python
version=2.1.2-jython-py27
gradleVersion=2.2.1
vertxVersion=2.1.5
toolsVersion=2.0.3-final
testFrameworkVersion=2.0.3-final
junitVersion=4.10
jythonVersion=2.7-b4
 ```

### How to get the artifact

1. Run following command

 ```
$ ./gradlew assemble
 ```

2. Zip up the files of interest

 ```
$ cd build/mods
$ zip -r org.vertx~lang-python~2.1.2-jython-py27.zip org.vertx~lang-python~2.1.2-jython-py27
 ```

3. Unzip the artifact under ```build/mods```
