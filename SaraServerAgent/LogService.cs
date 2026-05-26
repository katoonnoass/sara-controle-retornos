using System;
using System.IO;

namespace SaraServerAgent
{
    public class LogService
    {
        private readonly string _logsDir;
        private readonly object _lock = new();

        public event EventHandler<string>? LogAppended;

        public LogService()
        {
            string exeDir = AppDomain.CurrentDomain.BaseDirectory;
            _logsDir = Path.Combine(exeDir, "logs");
            Directory.CreateDirectory(_logsDir);
        }

        private string GetLogFilePath()
        {
            return Path.Combine(_logsDir, $"agent-{DateTime.Now:yyyy-MM-dd}.log");
        }

        public void Append(string message)
        {
            string line = $"{DateTime.Now:HH:mm:ss} [INFO] {message}";
            WriteLine(line);
        }

        public void AppendError(string message)
        {
            string line = $"{DateTime.Now:HH:mm:ss} [ERROR] {message}";
            WriteLine(line);
        }

        public void AppendWarning(string message)
        {
            string line = $"{DateTime.Now:HH:mm:ss} [WARN] {message}";
            WriteLine(line);
        }

        public void AppendServerOutput(string message)
        {
            string line = $"{DateTime.Now:HH:mm:ss} [SERVER] {message}";
            WriteLine(line);
        }

        private void WriteLine(string line)
        {
            lock (_lock)
            {
                try
                {
                    File.AppendAllText(GetLogFilePath(), line + Environment.NewLine);
                }
                catch { }
            }
            LogAppended?.Invoke(this, line);
        }

        public void ClearLogs()
        {
            try
            {
                string logFile = GetLogFilePath();
                if (File.Exists(logFile))
                    File.WriteAllText(logFile, string.Empty);
                Append("Logs cleared.");
            }
            catch { }
        }
    }
}
