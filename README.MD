# Fixed Width File Data Parser

The purpose of the project is to build a parser that could parse
fixed width files


## Built With

The section covers tools used to enable the project.

1. Python to generate and parse fixed width files
2. Pytest to do testing
3. Docker for building and running the application


## Files and Folders

1. parser.py - Contains logic to generate and parse the fixed width file
2. test_fixedwidth_parsing.py - Contains testing code to run unit tests
3. run.sh - Bash wrapper to run the parser and unit tests
4. spec.js - Json spec file that contains specification for fixed width file configs
5. Dockerfile - Docker application build code
6. requirements.txt - Python libraries and dependecies
   
## Running the application locally via docker

1. Open terminal
2. Navigate to the repo's root directory
3. Build the docker image

```bash 
docker build . -t parser:latest
```

4. Run docker container

```bash  
docker run -it parser:latest 
```

# Contact for questions or support

Nakul Bajaj
bajaj.nakul@gmail.com
