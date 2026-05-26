using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Input;

namespace SaraServerAgent
{
    public class MainViewModel : INotifyPropertyChanged
    {
        private readonly ConfigService _configService;
        private readonly ServerController _serverController;
        private readonly HealthCheckService _healthCheck;
        private readonly PortService _portService;
        private readonly LogService _logService;
        private readonly StartupService _startupService;

        private ServerStatus _serverStatus = ServerStatus.Stopped;
        private string _lastCheckTime = "--:--:--";
        private readonly SynchronizationContext? _uiContext;

        public event PropertyChangedEventHandler? PropertyChanged;
        public event EventHandler? LogAppended;

        public AgentConfig Config => _configService.Config;
        public string ServerUrl => Config.Url;
        public string ServerPort => Config.Port.ToString();
        public bool IsAutoStartEnabled => _startupService.IsAutoStartEnabled();

        public ServerStatus ServerStatus
        {
            get => _serverStatus;
            set { _serverStatus = value; OnPropertyChanged(); OnPropertyChanged(nameof(StatusText)); }
        }

        public string StatusText
        {
            get => _serverStatus switch
            {
                ServerStatus.Stopped => "Server: Stopped",
                ServerStatus.Starting => "Server: Starting...",
                ServerStatus.Running => "Server: Online",
                ServerStatus.Error => "Server: Error",
                ServerStatus.Restarting => "Server: Restarting...",
                _ => "Server: Unknown"
            };
        }

        public string LastCheckTime
        {
            get => _lastCheckTime;
            set { _lastCheckTime = value; OnPropertyChanged(); }
        }

        public bool CanStart => ServerStatus is ServerStatus.Stopped or ServerStatus.Error;
        public bool CanStop => ServerStatus is ServerStatus.Running;
        public bool CanRestart => ServerStatus is ServerStatus.Running;

        // Commands
        public ICommand StartCommand { get; }
        public ICommand StopCommand { get; }
        public ICommand RestartCommand { get; }
        public ICommand OpenBrowserCommand { get; }
        public ICommand OpenFolderCommand { get; }
        public ICommand OpenSettingsCommand { get; }
        public ICommand ClearLogsCommand { get; }

        public MainViewModel()
        {
            _uiContext = SynchronizationContext.Current;
            _configService = new ConfigService();
            _serverController = new ServerController();
            _healthCheck = new HealthCheckService();
            _portService = new PortService();
            _logService = new LogService();
            _startupService = new StartupService();

            StartCommand = new RelayCommand(async () => await StartServerAsync(), () => CanStart);
            StopCommand = new RelayCommand(async () => await StopServerAsync(), () => CanStop);
            RestartCommand = new RelayCommand(async () => await RestartServerAsync(), () => CanRestart);
            OpenBrowserCommand = new RelayCommand(() => OpenBrowser());
            OpenFolderCommand = new RelayCommand(() => OpenFolder());
            OpenSettingsCommand = new RelayCommand(() => OpenSettings());
            ClearLogsCommand = new RelayCommand(() => { _logService.ClearLogs(); _logService.Append("Logs cleared."); });

            _logService.LogAppended += (s, line) => AppendLog(line);

            _serverController.OutputReceived += (s, msg) =>
            {
                if (!string.IsNullOrEmpty(msg))
                    _logService.AppendServerOutput(msg);
            };
            _serverController.ErrorReceived += (s, msg) =>
            {
                if (!string.IsNullOrEmpty(msg))
                    _logService.AppendError(msg);
            };
            _serverController.StatusChanged += (s, status) =>
            {
                if (_uiContext != null && _uiContext != SynchronizationContext.Current)
                {
                    _uiContext.Post(_ =>
                    {
                        ServerStatus = status;
                        NotifyCommandsChanged();
                    }, null);
                }
                else
                {
                    ServerStatus = status;
                    NotifyCommandsChanged();
                }
            };
        }

        public void Initialize()
        {
        }

        public async Task CheckStatusAsync()
        {
            try
            {
                LastCheckTime = DateTime.Now.ToString("HH:mm:ss");

                if (ServerStatus == ServerStatus.Starting || ServerStatus == ServerStatus.Restarting)
                    return;

                var health = await _healthCheck.CheckAsync(Config.Url);

                if (health == ServerHealth.Online)
                {
                    ServerStatus = ServerStatus.Running;
                }
                else if (_serverController.IsRunning)
                {
                    ServerStatus = ServerStatus.Error;
                }
                else
                {
                    ServerStatus = ServerStatus.Stopped;
                }
                NotifyCommandsChanged();
            }
            catch
            {
                if (!_serverController.IsRunning)
                    ServerStatus = ServerStatus.Stopped;
                NotifyCommandsChanged();
            }
        }

        public async Task StartServerAsync()
        {
            if (_serverController.IsRunning)
            {
                AppendLog("[WARN] Server is already running.");
                return;
            }

            if (_portService.IsPortOpen(Config.Port))
            {
                // Port in use, warn
            }

            string cmd = GetEffectiveStartCommand();
            string args = GetEffectiveStartArguments();
            AppendLog($"Starting server: {cmd} {args}");
            await _serverController.StartAsync(cmd, args, Config.ProjectPath);
            await Task.Delay(3000);
            await CheckStatusAsync();
        }

        public async Task StopServerAsync()
        {
            AppendLog("Stopping server...");
            await _serverController.StopAsync();
            await CheckStatusAsync();
        }

        public void StopServerSync()
        {
            _serverController.StopAsync().GetAwaiter().GetResult();
        }

        public async Task RestartServerAsync()
        {
            string cmd = GetEffectiveStartCommand();
            string args = GetEffectiveStartArguments();
            AppendLog("Restarting server...");
            await _serverController.RestartAsync(cmd, args, Config.ProjectPath);
            await Task.Delay(3000);
            await CheckStatusAsync();
        }

        public void OpenBrowser()
        {
            try
            {
                Process.Start(new ProcessStartInfo { FileName = Config.Url, UseShellExecute = true });
                AppendLog($"Opened browser: {Config.Url}");
            }
            catch (Exception ex)
            {
                AppendLog($"[ERROR] Failed to open browser: {ex.Message}");
            }
        }

        public void OpenFolder()
        {
            try
            {
                Process.Start("explorer.exe", Config.ProjectPath);
            }
            catch (Exception ex)
            {
                AppendLog($"[ERROR] Failed to open folder: {ex.Message}");
            }
        }

        public void OpenSettings()
        {
            var window = new SettingsWindow(_configService, _startupService, this);
            window.Owner = System.Windows.Application.Current.MainWindow;
            window.ShowDialog();
            Initialize();
        }

        public void AppendLog(string message)
        {
            _logService.Append(message);
        }

        private string GetEffectiveStartCommand()
        {
            string psPath = Path.Combine(Config.ProjectPath, "run_producao.ps1");
            return File.Exists(psPath) ? Config.StartCommand : Config.FallbackCommand;
        }

        private string GetEffectiveStartArguments()
        {
            string psPath = Path.Combine(Config.ProjectPath, "run_producao.ps1");
            return File.Exists(psPath) ? Config.StartArguments : Config.FallbackArguments;
        }

        private void NotifyCommandsChanged()
        {
            if (_uiContext != null && _uiContext != SynchronizationContext.Current)
            {
                _uiContext.Post(_ => NotifyCommandsChanged(), null);
                return;
            }
            OnPropertyChanged(nameof(CanStart));
            OnPropertyChanged(nameof(CanStop));
            OnPropertyChanged(nameof(CanRestart));
            (StartCommand as RelayCommand)?.RaiseCanExecuteChanged();
            (StopCommand as RelayCommand)?.RaiseCanExecuteChanged();
            (RestartCommand as RelayCommand)?.RaiseCanExecuteChanged();
        }

        protected void OnPropertyChanged([CallerMemberName] string? name = null)
        {
            if (PropertyChanged == null) return;
            if (_uiContext != null && _uiContext != SynchronizationContext.Current)
                _uiContext.Post(_ => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name)), null);
            else
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
    }

    public class RelayCommand : ICommand
    {
        private readonly Action _execute;
        private readonly Func<bool>? _canExecute;
        public event EventHandler? CanExecuteChanged;

        public RelayCommand(Action execute, Func<bool>? canExecute = null)
        {
            _execute = execute;
            _canExecute = canExecute;
        }

        public bool CanExecute(object? parameter) => _canExecute?.Invoke() ?? true;
        public void Execute(object? parameter) => _execute();
        public void RaiseCanExecuteChanged() => CanExecuteChanged?.Invoke(this, EventArgs.Empty);
    }
}
