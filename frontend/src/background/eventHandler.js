import { ipcMain, Notification, dialog } from "electron";

const net = require("net");

const port = 9867;
const host = "127.0.0.1";

let connectAttempts = 5;

const initEventHandlers = window => {
  initTCP(window);

  ipcMain.on("win-close", () => {
    window.close();
  });

  ipcMain.on("win-maximize", () => {
    if (window.isMaximized()) window.unmaximize();
    else window.maximize();
  });

  ipcMain.on("win-minimize", () => {
    window.minimize();
  });

  ipcMain.on("notification", (event, content) => {
    showNotification(window, content);
  });
};

const initTCP = window => {
  const client = new net.Socket();
  tryConnect(client, window);
  client.on("error", err => {
    if (err.code === "ECONNREFUSED") {
      window.setEnabled(false);
      if (connectAttempts > 0) {
        setTimeout(() => tryConnect(client, window), 1000);
        connectAttempts--;
      } else failConnect(window);
    }
  });

  client.on("data", chunk => {
    const decoder = new TextDecoder("utf8");
    const chunkText = decoder.decode(chunk);
    let msg = JSON.parse(chunkText);
    window.webContents.send(msg.type, msg);
    console.log(`received message : ${chunkText}`);
    handleMessage(window, msg);
  });

  client.on("end", () => {
    console.log("disconnected from backend");
  });

  return client;
};

const tryConnect = (client, window) => {
  client.connect({ port, host }, () => {
    window.setEnabled(true);
    window.webContents.send("ready");
    ipcMain.on("to-backend", (event, msg) => {
      client.write(JSON.stringify(msg));
      console.log(`sending to backend: ${JSON.stringify(msg)}`);
    });

    ipcMain.on("win-close", () => {
      client.write(JSON.stringify({ type: "close-connection" }));
    });
  });
};

const failConnect = window => {
  dialog.showErrorBox(
    "Failed to connect to collection service",
    `There seems to be a problem connecting to the collection service on port ${port}. Try to close and rerun the application, if this does not help contact an administrator.`
  );
  window.destroy();
};

const handleMessage = (window, msg) => {
  switch (msg.type) {
    case "request-label":
      bringWindowToFront(window);
      showNotification(window, {
        title: "Submit Label",
        subtitle: "Please Tell Us How You Feel",
        body:
          "Choose the the emotion labels that best describe how you feel and click submit.",
        silent: true
      });
      break;
  }
};

const bringWindowToFront = window => {
  window.setAlwaysOnTop(true);
  window.focus();
  window.setAlwaysOnTop(false);
};

const showNotification = (window, content) => {
  const notification = new Notification(content);
  notification.onclick = window => bringWindowToFront(window);
  notification.show();
};

export { initEventHandlers };
