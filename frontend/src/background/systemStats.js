import pidusage from "pidusage";
import { promises as fs } from "fs";

const formatBytes = bytes => {
  const marker = 1024; // Change to 1000 if required
  const decimal = 3; // Change as required
  const kiloBytes = marker; // One Kilobyte is 1024 bytes
  const megaBytes = marker * marker; // One MB is 1024 KB
  const gigaBytes = marker * marker * marker; // One GB is 1024 MB

  // return bytes if less than a KB
  if (bytes < kiloBytes) return bytes + " Bytes";
  // return KB if less than a MB
  else if (bytes < megaBytes)
    return (bytes / kiloBytes).toFixed(decimal) + " KB";
  // return MB if less than a GB
  else if (bytes < gigaBytes)
    return (bytes / megaBytes).toFixed(decimal) + " MB";
  // return GB if less than a TB
  else return (bytes / gigaBytes).toFixed(decimal) + " GB";
};

const updateStats = (window, process_ids, db_path) => {
  setTimeout(() => {
    compute(process_ids, db_path, stats => {
      window.webContents.send("cpu", stats.cpu.toFixed(2));
      window.webContents.send("ram", formatBytes(stats.memory));
      window.webContents.send("disk", formatBytes(stats.disk));
      updateStats(window, process_ids, db_path);
    });
  }, 1000);
};

const compute = (process_ids, db_path, callback) => {
  pidusage(process_ids, (err, stats) => {
    stats = Object.values(stats);
    const sum_stats = sum_process_stats(stats);
    sum_stats.disk = 0;
    fs.stat(db_path)
      .then(fileStats => {
        sum_stats.disk = fileStats.size;
      })
      .then(() => callback(sum_stats))
      .catch(() => {
        callback(sum_stats);
      });
  });
};

const sum_process_stats = stats => {
  return stats.reduce(
    (total, elem) => {
      total.cpu += elem.cpu;
      total.memory += elem.memory;
      return total;
    },
    { cpu: 0, memory: 0 }
  );
};

export { updateStats };
