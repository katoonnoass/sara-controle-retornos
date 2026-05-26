# SARA Server Agent

Windows desktop application (system tray) to control the SARA Flask web server.

## Features

- Start, stop, and restart the SARA web server
- Real-time server log monitoring
- System tray icon with quick controls
- Auto-start with Windows
- Configurable project path, port, and startup mode

## Requirements

- Windows 10 or later (64-bit)
- .NET 8 Runtime (self-contained build includes it)
- Python 3.x installed and in PATH
- PostgreSQL running (for SARA itself)

## How to Build

### Prerequisites

Install the .NET 8 SDK from:
https://dotnet.microsoft.com/download/dotnet/8.0

### Build

```cmd
cd SaraServerAgent
dotnet restore
dotnet build -c Release
```

### Publish (single .exe)

```cmd
cd SaraServerAgent
dotnet publish -c Release -r win-x64 --self-contained true ^
  /p:PublishSingleFile=true ^
  /p:IncludeNativeLibrariesForSelfExtract=true
```

The .exe will be at:
`bin\Release\net8.0-windows\win-x64\publish\SARA Server Agent.exe`

## Configuration

On first run, a `config.json` file is created next to the .exe:

```json
{
  "ProjectPath": "C:\\Users\\joao.silva\\Documents\\SARA",
  "Url": "http://127.0.0.1:5000",
  "Port": 5000,
  "AutoStartWithWindows": false,
  "MinimizeToTrayOnClose": true
}
```

Edit via the Settings window or directly in the file.

## Usage

1. Open the application.
2. Click **Start** to launch the SARA server.
3. The status indicator shows: green (online), yellow (starting), red (stopped/error).
4. Use **Open SARA** to open the system in your browser.
5. Click **Stop** to shut down the server.
6. Close the window to minimize to tray — the agent stays running.

## Troubleshooting

### Python not found

Ensure Python is installed and available in your system PATH.
Alternatively, specify the full path to `python.exe` in the startup arguments via Settings.

### Port already in use

The agent detects if port 5000 is already occupied and warns before starting.
Stop any other process using the port, or change the port in Settings.

### Project folder not found

Check that the project path in Settings points to the correct SARA directory.
The folder must contain `app.py` or `run_producao.ps1`.

### Using run_producao.ps1

If `run_producao.ps1` exists in the project folder, the agent uses it by default.
Otherwise, it falls back to `python app.py`.

## Logs

Log files are saved to:
`logs\agent-YYYY-MM-DD.log`

## Auto-start with Windows

Enable in Settings or manually via Registry:
`HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SARA Server Agent`
