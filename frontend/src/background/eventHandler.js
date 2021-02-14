import { ipcMain } from "electron";

const net = require("net");

const port = 9687;
const host = "127.0.0.1";

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
};

const initTCP = window => {
  const client = new net.Socket();
  client.connect({ port, host }, async () => {
    ipcMain.on("to-backend", (event, msg) => {
      client.write(JSON.stringify(msg));
    });

    const close_conn_msg = { type: "close-connection"}

    ipcMain.on("win-close", () => {
      client.write(JSON.stringify(close_conn_msg));
    });
  });

  client.on("data", async chunk => {
    let msg = chunk.toJSON();
    window.webContents.send(msg.type, msg);
  });

  return client;
};

export { initEventHandlers };
