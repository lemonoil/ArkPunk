import { app, BrowserWindow } from 'electron'
const electron = require('electron')
const nodeCmd = require('node-cmd');
/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV !== 'development') {
  global.__static = require('path').join(__dirname, '/static').replace(/\\/g, '\\\\')
}

let mainWindow
const Menu = electron.Menu
const winURL = process.env.NODE_ENV === 'development'
  ? `http://localhost:9080`
  : `file://${__dirname}/index.html`

function createWindow () {
  /**
   * Initial window options
   */
  
  mainWindow = new BrowserWindow({
    height: 800,
    useContentSize: true,
    width: 1000,
    transparent: true,
    resizable: false,
    frame: false,
    webPreferences: {
      devTools: false,
      nodeIntegration: true,
      enablemotemodule: true
    }

  })

  mainWindow.loadURL(winURL)
  Menu.setApplicationMenu(null)
  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

const {PythonShell}  = require("python-shell")


var cmd = 'taskkill /f /t /im  python.exe';
var pyshell = new PythonShell('app.py');
pyshell.end(function (err) {
      if (err) console.log('error' + err + ': app.py shutdown');
    }
);

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
    nodeCmd.run(cmd);
    nodeCmd.run(cmd);
    console.log('app Done')
    nodeCmd.run(cmd);
    nodeCmd.run(cmd);
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

/**
 * Auto Updater
 *
 * Uncomment the following code below and install `electron-updater` to
 * support auto updating. Code Signing with a valid certificate is required.
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-electron-builder.html#auto-updating
 */

/*
import { autoUpdater } from 'electron-updater'

autoUpdater.on('update-downloaded', () => {
  autoUpdater.quitAndInstall()
})

app.on('ready', () => {
  if (process.env.NODE_ENV === 'production') autoUpdater.checkForUpdates()
})
 */
