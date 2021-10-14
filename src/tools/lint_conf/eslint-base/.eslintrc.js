/**
 * Base eslint config
 * Import in react and react native projects
 */
module.export = {
  "extends":["eslint:recommended", "plugin:react/recommended", "google"],
  "rules": {
      "react/no-set-state": "off",
      "require-jsdoc" : 0
  },
  "settings": {
    "react": {
      "createClass": "createReactClass", 
      "pragma": "React",
      "version": "detect"
    }
  }
};