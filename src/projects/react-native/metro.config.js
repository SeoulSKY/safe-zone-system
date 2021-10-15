const path = require('path');

const extraNodeModules = {
  'mibs': path.resolve(__dirname + '/../../lib/mibs/ts'),
};

const watchFolders = [
  path.resolve(__dirname + '/../../lib/mibs/ts')
];

module.exports = {
  transformer: {
    getTransformOptions: async () => ({
      transform: {
        experimentalImportSupport: false,
        inlineRequires: false,
      },
    }),
  }, 
  resolver: {
    extraNodeModules: new Proxy(extraNodeModules, {
      get: (target, name) => {
        name in target ? target[name]: 
          path.join(process.cwd(), `node_modules/${name}`)
      }
    }),
  },
  watchFolders,
};