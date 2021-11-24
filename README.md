# Safe Zone System

## Developer Setup Instuctions
### Environment
* [NodeJS 16](https://nodejs.org/en/)
* [Android Studio](https://developer.android.com/studio/install)
  * Ensure `$ANDROID_HOME` and `$ANDROID_SDK` environment variables available. These are used by Expo to connect to an android emulator.
  * Create an emulator that has a browser available.
    * Pixel 5, API: 29 
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Git LFS](https://git-lfs.github.com/)

### Starting Server
1. Ensure Docker, Docker Compose and Git LFS are installed. 
    * See [Environment](#Environment-1) for setup instructions.
2. Nagivate to the `<project root>/docker/dev` directory of the project (where the docker-compose.yml file is located).
3. Execute the following command to build and start all docker containers.
    ```
    docker-compose --env-file dev.env up --build
    ```

### Starting Expo
1. Ensure NodeJS 16 and Android Studio is installed. 
    * See [Environment](#Environment-1) for setup instructions.
      * Note: Development should occur on an Android or IOS device, thus an emulator should be setup.

2. [Start server](#Starting-Server)
3. Navigate to `<project root>/src/tools/api`.
4. Execute the following command to generate JS API module:
    ```
    ./gen_api.sh
    ```
5. Navigate to `<project root>/src/lib/mibs/ts
6. Execute the following command to configure yarn
    ```
    yarn install
    ```
7. Navigate to `<project root>/src/projects/react-native`.
8. Install dependencies:
    ```
    yarn install
    ```
9. Execute the following command to start Expo:
    ```
    yarn start
    ```
10. Start the Android emulator in Android Studio.
11. In the running Expo instance press `a` to compile and install the react-native project onto the Android emulator.
    * This will automatically refresh if any changes are made to the source code.

### Useful commands
#### React Native Project
* Run linting
  ```
  yarn run lint
  ```
* Run tests:
  ```
  yarn test
  ```
* Run tests with auto rerun on file changes:
  ```
  yarn run test-watch 
  ```
  or 
  ```
  yarn test -- --watch
  ```

#### Web Project
* Run linting
  ```
  yarn run lint
  ```
* Run tests:
  ```
  yarn test
  ```
* Run tests with auto rerun on file changes:
  ```
  yarn test -- --watch
  ```

#### Keycloak
* The keycloak admin page can be found http://localhost/auth/admin/
* Login to the admin account.
  * Username: admin
  * Password: cmpt371



# Tester Setup Instructions

### Environment
* [Android Studio](https://developer.android.com/studio/install)
  * Ensure `$ANDROID_HOME` and `$ANDROID_SDK` environment variables available. These are used by Expo to connect to an android emulator.
  * Create an emulator that has a browser available.
    * Pixel 5, API: 29 
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)
### Starting Server
1. Ensure Docker, Docker Compose and Git LFS are installed. 
    * See [Environment](#Environment-2) for setup instructions.
2. Nagivate to the `<project root>/docker/test` directory of the project (where the docker-compose.yml file is located).
3. Execute the following command to pull and start all docker containers using the latest code from master.
    ```
    docker-compose -f docker-compose.yml -f local/docker-compose.postgres.yml --env-file local/local-test.env up 
    ```
    * To start different server version you can set the TAG variable with the appropriate docker tag.
      * This will pull the latest ID4 images. 
        ```
        TAG=ID4 docker-compose -f docker-compose.yml -f local/docker-compose.postgres.yml --env-file local/local-test.env up
        ```
      * This will pull the code from ID4 built at 2021-11-22-04-06-27. 
        ```
        TAG=ID4-2021-11-22-04-06-27 docker-compose -f docker-compose.yml -f local/docker-compose.postgres.yml --env-file local/local-test.env up
        ```
      * Container versions can be seen here https://github.com/orgs/UniversityOfSaskatchewanCMPT371/packages?ecosystem=container
        * Select the any of the container and all availabe tags will be shown. 
      * The docker-compose files are setup to allow optionally starting a postgres database in docker. To do this one should use the `local/docker-compose.postgres.yml` override file and `local/local-test.env` environment file.
          ```
          docker-compose -f docker-compose.yml -f local/docker-compose.postgres.yml --env-file local/local-test.env up
          ```
        * Note in the future we plan on using services such as postgres not in docker.

# Mobile App
* APKs and IPA can be downloaded from https://github.com/UniversityOfSaskatchewanCMPT371/term-project-fall-2021-team1/actions
  1. Search for the branch you want to get the latest artifact from. I.e master or ID*
  2. Select the latest passing build for that branch
  3. Download the APK or IPA from the `Artifacts` at the bottom of the page