# Movie manager

This is a homework assignment that I completed during my free time over the Easter holidays. The requirements were to build an app that continuously fetches data from a remote source and provides a frontend for users to view, filter, and search the data.

The solution was designed as a standard headless service with a simple API and a frontend that works with the API, written in JavaScript. For more information about the decision-making process, what was accomplished, and what was left undone, please refer to the `project_solution` file in the `docs` folder.


## How to run
**You need docker and docker compose present.**.

1. Assuming you have them, run:
```
make build
```
2. After the build is complete (the MongoDB image is being downloaded, so it might take some time and disk space), run:
```
make up
```
3. When finished
```
make down
```

By default, the frontend should be accessible at [localhost:8080/](localhost:8080/). In case of a port conflict,
 ```
 APP_PORT=your_port make up
 ```

## How to run test

As the service, in practice, only requests data from the database, I have chosen integration tests in favor of unit tests (there is no logic involved, and I don't like writing tests just to have tests).

The integration tests verify that the service is able to fetch data and provide the correct results at each API endpoint (ordering, filtering, searching, and detail).

The frontend was tested manually, as implementing Selenium tests would be overkill for this homework assignment.

To run tests (assuming you have already built the images):

```
make test
```

## Closing notes

The app should be fully functional within the requirements and tested. Some parts would need more care, but for homework, it would be overkill.
