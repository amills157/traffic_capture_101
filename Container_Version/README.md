The docker command to run the instance is:

`docker run --name test --rm -it --net mynet123 --ip 172.18.0.10 -v $(pwd):/Server server_image:101`

This should be run from inside the cloned repo

This will start a docker container running the server, allowing the host machine to connect to it on IP `172.18.0.10` using the client python script

The server docker image will need to be built first using the command:

`docker build -t server_image:101 .` 

This command should again be run inside the clone repo - Please do not ignore the `.` that is required to build using the included Dockerfile