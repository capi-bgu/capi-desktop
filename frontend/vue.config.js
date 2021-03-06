module.exports = {
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
      builderOptions: {
        appId: "bgu.capi.desktop",
        productName: "Capi",
        files: ["**/*", "public/icons/*"],
        icon: "./public/icons/circle.ico"
      }
    }
  }
};
