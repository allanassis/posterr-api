# ALLAN ASSIS DE ANDRADE

## Setup the project

### Requirements

#### Running with docker 

-   Docker version 20.10.14 (maybe works on others versions, but this one that was used)
-   Docker Compose version 2.5.0 (maybe works on others versions, but this one that was used)
  
#### Running only the service without docker will also nesse these followings

- Python version 3.9.12
- Poetry version 1.1.13
  

### Running:

#### Everything in docker

```console
ROOT_DIRECTORY $ docker-compose build
ROOT_DIRECTORY $ docker-compose up
```

#### Only the databases in docker
You could just kill the container of the service named *posterr-api* and ensure that there is no service using the port **8080**
After that to the following

```console
ROOT_DIRECTORY $ poetry install
ROOT_DIRECTORY $ ENV=local poetry run start
```

### Test the code

Get the id of the container named *posterr-api* with `docker ps`
then run the following

#### Running unit tests
```console
ROOT_DIRECTORY $ docker exec {CONTAINER_ID} poetry run pytest tests/unit

```
#### Running E2E tests
```console
ROOT_DIRECTORY $ docker exec {CONTAINER_ID} poetry run pytest tests/end_to_end
```

#### Running All tests
```console
ROOT_DIRECTORY $ docker exec {CONTAINER_ID} poetry run pytest
```

#### Manual test

There is a file called *posterr.postman_collection.json* in the root directory, this file can help you create a postman collection with example of all the requests that can be made.


## Planning
### Questions about reply-to-post

- The user can reply him self?
- The user can reply the same post any times?
- The UI of the reply is the same if we can reply our selfs?
- How much users do you expect to use this feature?
- How could we break this feature into small features to be delivery separeted?
- There is no notification system, the user who create the post replied should me notificated in any way?
- Should this reply to post be deal as a post like normal, quoted and reposted?
  
### How would i solve
First i assume that this post should has the same behavior of the others posts
We already have all the structure to handle an addition of a new type of post.
One of the reasons i chose mongodb a non schema database to persisti the data is because is easy to extends without the need of migrations that we have to do in normal relational databases.
Should be easy to add this new type of post, just update the enum `PostType` and update the `PostDAO` to handle the query for the second page that should only contains this new type of posts and the original posts as the posts are already cached there is no need to do it.
For the frontend we should see how should be designed this new page and how should look the design of this new type of post.

# Critique

## Tech debits:
- Refactor the code
    - Structure error handling, it is not well defined yet
    - Structure the responses, it is not well defined yet
    - Define the status code correct for each case of response
    - Create a dao base class to handle common data access logic
    - Add strcuture logging, the logger is too simple
    - Add more unit tests and e2e tests to cover all the paths
    - Refactor tests to be more readable and reusable
    - Add a linter
    - Make sure typeguard is been well used in all project
    - Add points of extensability in the code for validation without change the core logic code
    - Add documentation as code or other tool to generate a page with the api documentation, maybe using the openapi definition
- Security
    - Remove error middleware, it is not good practice with security to return any exception to the user, this may lead to exploitation
    - Add rate limit per user for any request to avoid dos or ddos atacks
    - Add auth to databases
    - Add https
    - Add auth
    - Sanityzing body and query strings

- Scaling:
    > For this services handle a big amount of requests like twitter it should be improved
    for this improviments to happen i would do the following modifications.

    - Scale horizontaly the instances of the service by adding more containers
    - Add a loadbalancer  in front of those containers to make a good distribution of the requests and be transparent to the frontend
    - With the horizontal scale of the service the throghput will raise and the databases will not handle
    - Scale the databases
    - We could use mongo sharding with replica sets to have the amount of data/requests distribuited per shard
    - Use redis ring, for the same purpose, reveice de data/requests in a distribuited way without depend on one instance
    - Cache in the border, consider use a CDN (like cloudfront from aws) to have some cache in the border and decrease the latency
    - Use a queue like kafka to handle the input of the data, kafka can handle it better than mongo. We could use kafka connector to send these data to mongodb directly. 
    - For the search feature bonus we could use an elastic search cluster to handle all the text search, since it was optimized for text search
Reliability:
    - Add redundance, we would already have it in data because mongo wold have replica sets, but we could take snapshots every day and keep the recent ones
    - We should add at least two loadbalancers in case one goes down
    - We already have a couple of instances of the service running, so if one fails there are others to handle the requests
    - Circuit breaker, we should also add it for avoid overload the database or others services when they are failling
    - Blue/green and canary deploy
    - SRE:
        - Define SLI, SLAs and SLOs
        - Use CI/CD to have an automate pipeline to test, build and deploy the application. To ensure safety
        - Observability:
            - After structuring the logs in the code we should send them to a log server
            - Metrics, we should collect metrics about service, as it is as http api we probabily should collect metrics about requests latency and status codes
            - Dashboard, the best way to see what is going on is seeing the metrics in a Dashboard
            - Tracing, it is no necessary for now because it is just one microservie, but if we add more would be great to have tracing to see what is going on in each service after a request is middleware
Performance:
    - Decrease the amount of network requests by get data in one query in database instead of go more than one time to get the data
    - Check if all the data beeing transfered in the requests are really needed to avoid huge network data package
    - Depend on the amount of the requests that are being received, consider use a loadbalancer L4, because works on trasport layer so is faster than L7
    - Add cache to the get all methods considering the query strings


