module.exports = {
  purge: { content: ["./public/**/*.html", "./src/**/*.vue"] },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {}
  },
  variants: {
    extend: {
      width: ["hover"],
      margin: ["last", "hover"],
      padding: ["last"]
    }
  },
  plugins: []
};
