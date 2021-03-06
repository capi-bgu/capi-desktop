import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import "@/assets/style.css";
import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";

const electron = require("electron");
const { ipcRenderer } = electron;

ipcRenderer.on("ready", () => {
  ui_store.ready = true;
});

ipcRenderer.on("ram", (event, ram) => {
  ui_store.ram = ram;
});

ipcRenderer.on("cpu", (event, cpu) => {
  ui_store.cpu = cpu;
});

ipcRenderer.on("disk", (event, disk) => {
  ui_store.disk = disk;
});

ipcRenderer.on("request-label", () => {
  if (router.currentRoute.name !== "Label") router.push({ name: "Label" });
  ui_store.scheduledLabel = true;
});

const ui_store = {
  ready: false,
  running: false,
  start_time: Date.now(),
  lastMood: "Happy",
  mood: "none",
  valance: "none",
  arousal: "none",
  dominance: "none",
  cpu: NaN,
  ram: "0 Bytes",
  disk: NaN,
  lastScheduledLabel: Date.now(),
  scheduledLabel: false,
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
  callbacks: {
    onStart: new Map(),
    onStop: new Map()
  },
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
      num_sessions: ui_store.settings.num_sessions,
      session_duration: ui_store.settings.session_duration,
      ask_freq: ui_store.settings.label_frequency,
      use_camera: ui_store.settings.use_camera,
      use_kb: ui_store.settings.use_keyboard,
      use_mouse: ui_store.settings.use_mouse,
      use_metadata: ui_store.settings.use_meta
    });
    ui_store.running = true;
    ui_store.start_time = Date.now();
    ui_events.callbacks.onStart.forEach(callback => callback());
  },
  stop: () => {
    ipcRenderer.send("to-backend", {
      type: "stop-core"
    });
    ui_store.running = false;
    ui_events.callbacks.onStop.forEach(callback => callback());
  },
  label: () => {
    ipcRenderer.send("to-backend", {
      type: "label",
      label: {
        categorical: ui_store.mood,
        VAD: {
          valance: ui_store.valance,
          arousal: ui_store.arousal,
          dominance: ui_store.dominance
        }
      }
    });
    ui_store.lastMood = ui_store.mood;
    if (ui_store.scheduledLabel) ui_store.lastScheduledLabel = Date.now();
    ui_store.scheduledLabel = false;
  },
  notification: content => {
    ipcRenderer.send("notification", content);
  },
  onStart(id, callback) {
    ui_events.callbacks.onStart.set(id, callback);
  },
  onStop(id, callback) {
    ui_events.callbacks.onStop.set(id, callback);
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
