using System;
using System.Diagnostics;
using System.IO;
using System.Threading;
using System.Threading.Tasks;

namespace SaraServerAgent
{
    public enum ServerStatus
    {
        Stopped,
        Starting,
        Running,
        Error,
        Restarting
    }

    public class ServerController
    {
        private Process? _process;
        private int _processId;
        private readonly object _lock = new();
        private CancellationTokenSource? _cts;
        private string? _pidFilePath;
        private string? _workingDir;

        public event EventHandler<string>? OutputReceived;
        public event EventHandler<string>? ErrorReceived;
        public event EventHandler<ServerStatus>? StatusChanged;

        public ServerStatus Status { get; private set; } = ServerStatus.Stopped;
        public int ProcessId => _processId;

        public bool IsRunning
        {
            get
            {
                lock (_lock)
                {
                    return _process != null && !_process.HasExited;
                }
            }
        }

        public async Task StartAsync(string command, string arguments, string workingDir)
        {
            if (IsRunning)
            {
                OutputReceived?.Invoke(this, "Server is already running.");
                return;
            }

            if (!Directory.Exists(workingDir))
            {
                ErrorReceived?.Invoke(this, $"Project directory not found: {workingDir}");
                return;
            }

            _workingDir = workingDir;
            SetStatus(ServerStatus.Starting);

            await Task.Run(() =>
            {
                try
                {
                    var psi = new ProcessStartInfo
                    {
                        FileName = command,
                        Arguments = arguments,
                        WorkingDirectory = workingDir,
                        UseShellExecute = false,
                        CreateNoWindow = true,
                        RedirectStandardOutput = false,
                        RedirectStandardError = false,
                    };

                    lock (_lock)
                    {
                        _cts = new CancellationTokenSource();
                        _process = new Process { StartInfo = psi, EnableRaisingEvents = true };

                        _process.Exited += (s, e) =>
                        {
                            DeletePidFile();
                            SetStatus(ServerStatus.Stopped);
                            lock (_lock)
                            {
                                _process?.Dispose();
                                _process = null;
                                _processId = 0;
                                _cts?.Dispose();
                                _cts = null;
                            }
                        };

                        _process.Start();
                        _processId = _process.Id;
                        SavePidFile(_processId);
                    }

                    OutputReceived?.Invoke(this, "Server process started.");
                }
                catch (Exception ex)
                {
                    ErrorReceived?.Invoke(this, $"Failed to start server: {ex.Message}");
                    SetStatus(ServerStatus.Error);
                }
            });
        }

        public async Task StopAsync()
        {
            int targetPid = 0;
            Process? proc;

            lock (_lock)
            {
                proc = _process;
                _cts?.Cancel();
                if (_process != null && !_process.HasExited)
                    targetPid = _processId;
            }

            // Try to stop the tracked process
            if (proc != null && !proc.HasExited)
            {
                try
                {
                    OutputReceived?.Invoke(this, $"Stopping server PID {targetPid}...");
                    proc.CloseMainWindow();
                    if (!proc.WaitForExit(5000))
                    {
                        proc.Kill(entireProcessTree: true);
                        proc.WaitForExit(3000);
                    }
                    OutputReceived?.Invoke(this, $"Server PID {targetPid} stopped.");
                }
                catch (Exception ex)
                {
                    ErrorReceived?.Invoke(this, $"Error stopping PID {targetPid}: {ex.Message}");
                }
            }
            else
            {
                // Process not tracked — try PID file
                targetPid = ReadPidFile();
                if (targetPid > 0)
                {
                    try
                    {
                        var staleProc = Process.GetProcessById(targetPid);
                        if (staleProc != null && !staleProc.HasExited)
                        {
                            // Confirm it looks like our server before killing
                            if (IsProcessSaraRelated(staleProc))
                            {
                                OutputReceived?.Invoke(this, $"Stopping stale SARA process PID {targetPid}...");
                                staleProc.Kill(entireProcessTree: true);
                                staleProc.WaitForExit(3000);
                                OutputReceived?.Invoke(this, $"Stale process PID {targetPid} stopped.");
                            }
                            else
                            {
                                OutputReceived?.Invoke(this, $"PID {targetPid} found but does not appear to be SARA. Not killing.");
                            }
                        }
                    }
                    catch (ArgumentException)
                    {
                        // Process doesn't exist anymore — stale PID file
                        OutputReceived?.Invoke(this, $"PID {targetPid} no longer exists (stale PID file).");
                    }
                    catch (Exception ex)
                    {
                        ErrorReceived?.Invoke(this, $"Error checking stale PID {targetPid}: {ex.Message}");
                    }
                }
                else
                {
                    OutputReceived?.Invoke(this, "No server PID file found. Nothing to stop.");
                }
            }

            DeletePidFile();
            lock (_lock)
            {
                _process?.Dispose();
                _process = null;
                _processId = 0;
                _cts?.Dispose();
                _cts = null;
            }

            SetStatus(ServerStatus.Stopped);
            OutputReceived?.Invoke(this, "Server stopped.");
            await Task.CompletedTask;
        }

        public async Task RestartAsync(string command, string arguments, string workingDir)
        {
            SetStatus(ServerStatus.Restarting);
            OutputReceived?.Invoke(this, "Restarting server...");
            await StopAsync();
            await Task.Delay(2000);
            await StartAsync(command, arguments, workingDir);
        }

        private void SavePidFile(int pid)
        {
            try
            {
                string dir = Path.Combine(_workingDir ?? AppDomain.CurrentDomain.BaseDirectory, "runtime");
                Directory.CreateDirectory(dir);
                _pidFilePath = Path.Combine(dir, "sara-server.pid");
                File.WriteAllText(_pidFilePath, pid.ToString());
            }
            catch { }
        }

        private int ReadPidFile()
        {
            try
            {
                string defaultDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "runtime");
                string? dir1 = _pidFilePath != null ? Path.GetDirectoryName(_pidFilePath) : null;
                string? dir2 = _workingDir != null ? Path.Combine(_workingDir, "runtime") : null;
                string?[] dirsToTry = new string?[] { dir1, dir2, defaultDir };

                foreach (string? dir in dirsToTry)
                {
                    if (dir == null) continue;
                    string path = Path.Combine(dir, "sara-server.pid");
                    if (File.Exists(path))
                    {
                        string content = File.ReadAllText(path).Trim();
                        if (int.TryParse(content, out int pid) && pid > 0)
                            return pid;
                    }
                }
            }
            catch { }
            return 0;
        }

        private void DeletePidFile()
        {
            try
            {
                if (_pidFilePath != null && File.Exists(_pidFilePath))
                    File.Delete(_pidFilePath);
            }
            catch { }
        }

        private bool IsProcessSaraRelated(Process proc)
        {
            try
            {
                string? mainModule = proc.MainModule?.FileName;
                if (mainModule != null)
                {
                    string name = Path.GetFileName(mainModule).ToLowerInvariant();
                    if (name == "python.exe" || name == "python3.exe" || name == "waitress-serve.exe")
                        return true;
                }
            }
            catch { }

            try
            {
                if (_workingDir != null)
                {
                    string cmdLine = proc.StartInfo.Arguments?.ToLowerInvariant() ?? "";
                    if (cmdLine.Contains("app.py") || cmdLine.Contains("run.py") || cmdLine.Contains("run_producao"))
                        return true;
                }
            }
            catch { }

            // Fallback: check by working directory if accessible
            try
            {
                if (_workingDir != null)
                {
                    using var searcher = new System.Management.ManagementObjectSearcher(
                        $"SELECT CommandLine FROM Win32_Process WHERE ProcessId = {proc.Id}"
                    );
                    foreach (var obj in searcher.Get())
                    {
                        string? cmdLine = obj["CommandLine"]?.ToString() ?? "";
                        if (cmdLine.Contains("sara", StringComparison.OrdinalIgnoreCase) ||
                            cmdLine.Contains("app.py", StringComparison.OrdinalIgnoreCase) ||
                            cmdLine.Contains("run.py", StringComparison.OrdinalIgnoreCase))
                            return true;
                    }
                }
            }
            catch { }

            return false;
        }

        private void SetStatus(ServerStatus status)
        {
            Status = status;
            StatusChanged?.Invoke(this, status);
        }

        public int? FindProcessOnPort(int port)
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "netstat",
                    Arguments = "-ano | findstr \":" + port + "\" | findstr \"LISTENING\"",
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true
                };
                using var proc = Process.Start(psi);
                if (proc == null) return null;
                string output = proc.StandardOutput.ReadToEnd();
                proc.WaitForExit(2000);

                foreach (string line in output.Split('\n', StringSplitOptions.RemoveEmptyEntries))
                {
                    string[] parts = line.Trim().Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
                    if (parts.Length > 0)
                    {
                        string last = parts[^1].Trim();
                        if (int.TryParse(last, out int pid) && pid > 0)
                            return pid;
                    }
                }
            }
            catch { }
            return null;
        }
    }
}
