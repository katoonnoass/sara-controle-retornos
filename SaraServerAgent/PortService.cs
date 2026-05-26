using System;
using System.Diagnostics;
using System.Net.NetworkInformation;
using System.Net.Sockets;

namespace SaraServerAgent
{
    public class PortService
    {
        public bool IsPortOpen(int port)
        {
            try
            {
                using var tcpClient = new TcpClient();
                var result = tcpClient.BeginConnect("127.0.0.1", port, null, null);
                bool success = result.AsyncWaitHandle.WaitOne(TimeSpan.FromSeconds(2));
                if (success)
                {
                    tcpClient.EndConnect(result);
                    return true;
                }
                return false;
            }
            catch
            {
                return false;
            }
        }

        public int? GetProcessIdUsingPort(int port)
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

        public bool IsProcessSaraRelated(int pid, string? projectPath)
        {
            try
            {
                var proc = Process.GetProcessById(pid);
                if (proc == null) return false;

                // Check by module name
                try
                {
                    string? mainModule = proc.MainModule?.FileName;
                    if (mainModule != null)
                    {
                        string name = System.IO.Path.GetFileName(mainModule).ToLowerInvariant();
                        if (name is "python.exe" or "python3.exe" or "waitress-serve.exe")
                            return true;
                    }
                }
                catch { }

                // Check by command line
                try
                {
                    using var searcher = new System.Management.ManagementObjectSearcher(
                        $"SELECT CommandLine FROM Win32_Process WHERE ProcessId = {pid}"
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
                catch { }

                // Check by process name
                string procName = proc.ProcessName.ToLowerInvariant();
                if (procName is "python" or "waitress-serve")
                    return true;
            }
            catch { }
            return false;
        }
    }
}
