import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import "@/assets/style.css";
import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";

const electron = require("electron");
const { ipcRenderer } = electron;

ipcRenderer.on("ram", (event, ram) => {
  ui_store.ram = ram;
});

ipcRenderer.on("route", (event, dest) => {
  router.push({ name: dest });
});

ipcRenderer.on("label-req", () => {
  if (router.currentRoute.name !== "Label") router.push({ name: "Label" });
});

const ui_store = {
  running: false,
  start_time: Date.now(),
  mood: "Happy",
  cpu: 20,
  ram: "0 Bytes",
  disk: 300,
  settings: {
    num_sessions: 1,
    session_duration: 10,
    label_frequency: 1,
    db_path: "",
    use_camera: true,
    use_keyboard: true,
    use_mouse: true,
    use_meta: true
  }
};

const ui_events = {
  window_close: () => {
    ipcRenderer.send("win-close");
  },
  window_maximize: () => {
    ipcRenderer.send("win-maximize");
  },
  window_minimize: () => {
    ipcRenderer.send("win-minimize");
  },
  start: () => {
    ipcRenderer.send("start");
    ui_store.running = true;
  },
  stop: () => {
    ipcRenderer.send("stop");
    ui_store.running = false;
  }
};

Vue.config.productionTip = false;

new Vue({
  router,
  data() {
    return {
      store: ui_store,
      events: ui_events
    };
  },
  render: h => h(App)
}).$mount("#app");
