# douban_social_graph
Plots the social graph for members in a douban group

## Instructions
You need to install docker to build and run the program.

Rename `creds.yaml.example` to `creds.yaml`, and put in your cookie.

Build and run:
```
docker build -t social-graph .
docker run -it --rm  -v $(pwd)/output:/code/output social-graph <group_id> creds.yaml
```
