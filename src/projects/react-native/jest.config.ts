const {getIOSPreset, getAndroidPreset, withWatchPlugins} = require('jest-expo/config');
  
module.exports = withWatchPlugins({
  preset: 'jest-expo',
  projects: [
      // Create a new project for each platform.
      getIOSPreset(),
      getAndroidPreset(),
  ],
  setupFilesAfterEnv: ["@testing-library/jest-native/extend-expect"]
});