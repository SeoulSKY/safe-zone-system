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

### Starting Server
1. Ensure Docker and Docker Compose are installed. 
    * See [Environment](#Environment) for setup instructions.
2. Nagivate to the root directory of the project (where the docker-compose.yml file is located).
3. Execute the following command to build and start all docker containers.
    ```
    docker-compose up --build
    ```

### Starting Expo
1. Ensure NodeJS 16 and Android Studio is installed. 
    * See [Environment](#Environment) for setup instructions.
      * Note: Development should occur on an Android or IOS device, thus an emulator should be setup.

2. [Start server](#Starting-Server)
3. Navigate to `<project root>/src/tools/api`.
4. Execute the following command to generate JS API module:
    ```
    ./gen_api.sh
    ```
5. Navigate to `<project root>/src/projects/react-native`.
6. Install dependencies:
    ```
    npm install
    ```
7. Execute the following command to start Expo:
    ```
    npm start
    ```
8. Start the Android emulator in Android Studio.
9. In the running Expo instance press `a` to compile and install the react-native project onto the Android emulator.
    * This will automatically refresh if any changes are made to the source code.

### Useful commands
#### React Native Project
* Run linting
  ```
  npm run lint
  ```
* Run tests:
  ```
  npm test
  ```
* Run tests with auto rerun on file changes:
  ```
  npm run test-watch 
  ```
  or 
  ```
  npm test -- --watch
  ```

#### Web Project
* Run linting
  ```
  npm run lint
  ```
* Run tests:
  ```
  npm test
  ```
* Run tests with auto rerun on file changes:
  ```
  npm test -- --watch
  ```