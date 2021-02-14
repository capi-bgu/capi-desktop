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

ipcRenderer.on("cpu", (event, cpu) => {
  ui_store.cpu = cpu;
});

ipcRenderer.on("disk", (event, disk) => {
  ui_store.disk = disk;
});

ipcRenderer.on("route", (event, dest) => {
  router.push({ name: dest });
});

ipcRenderer.on("request-label", () => {
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
    use_camera: true,
    use_keyboard: true,
    use_mouse: true,
    use_meta: true,
    num_sessions: 3600,
    session_duration: 1,
    label_frequency: 60,
    db_path: ""
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
    ipcRenderer.send("to-backend", {
      type: "run-core",
      ...ui_store.settings
    });
    ui_store.running = true;
  },
  stop: () => {
    ipcRenderer.send("to-backend", {
      type: "stop-core"
    });
    ui_store.running = false;
  },
  label: label => {
    ipcRenderer.send("to-backend", {
      type: "label",
      label
    });
    ui_store.mood = label.categorical;
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
