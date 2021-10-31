module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      ["babel-plugin-module-resolver",
        {
          root: ".",
          alias: {
            "@/common": "./src/common",
            "@/components": "./src/components",
            "@/screens": "./src/screens",
            "@/hooks": "./src/hooks",
            "@/assets": "./assets",
          }
        }
      ],
    ],
  };
};