using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Windows;
using System.Windows.Threading;

namespace SaraServerAgent
{
    public partial class MainWindow : Window
    {
        private Process? _serverProcess;
        private NotifyIconWrapper? _tray;
        private bool _forceClose;

        public MainWindow()
        {
            InitializeComponent();
            try { _tray = new NotifyIconWrapper(this); } catch { _tray = null; }
            UpdateStatus("Stopped", "#9CA3AF");
        }

        public void UpdateStatus(string status, string color)
        {
            try
            {
                StatusText.Text = "Server: " + status;
                StatusText.Foreground = new System.Windows.Media.SolidColorBrush(
                    (System.Windows.Media.Color)System.Windows.Media.ColorConverter.ConvertFromString(color));
            }
            catch { }
        }

        public async void BtnStart_Click(object? sender, RoutedEventArgs? e)
        {
            if (_serverProcess != null && !_serverProcess.HasExited)
            { MessageBox.Show("Server already running.", "SARA", MessageBoxButton.OK, MessageBoxImage.Information); return; }

            BtnStart.IsEnabled = false;
            UpdateStatus("Starting...", "#FBBF24");

            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = "run.py",
                    WorkingDirectory = @"C:\Users\joao.silva\Documents\SARA",
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                _serverProcess = new Process { StartInfo = psi, EnableRaisingEvents = true };
                _serverProcess.Exited += (s, e2) =>
                {
                    Dispatcher.Invoke(() =>
                    {
                        _serverProcess = null;
                        UpdateStatus("Stopped", "#9CA3AF");
                        BtnStart.IsEnabled = true;
                        BtnStop.IsEnabled = false;
                    });
                };

                _serverProcess.Start();
                await System.Threading.Tasks.Task.Delay(4000);
                UpdateStatus("Online", "#4ADE80");
                BtnStop.IsEnabled = true;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message, "SARA", MessageBoxButton.OK, MessageBoxImage.Error);
                UpdateStatus("Error", "#F87171");
                BtnStart.IsEnabled = true;
            }
        }

        public void BtnStop_Click(object? sender, RoutedEventArgs? e)
        {
            if (_serverProcess != null && !_serverProcess.HasExited)
            {
                try { _serverProcess.Kill(entireProcessTree: true); _serverProcess.WaitForExit(3000); } catch { }
                _serverProcess = null;
            }
            UpdateStatus("Stopped", "#9CA3AF");
            BtnStart.IsEnabled = true;
            BtnStop.IsEnabled = false;
        }

        public void BtnOpen_Click(object? sender, RoutedEventArgs? e)
        {
            try { Process.Start(new ProcessStartInfo { FileName = "http://127.0.0.1:5000", UseShellExecute = true }); } catch { }
        }

        public void ShowWindow()
        {
            Show();
            WindowState = WindowState.Normal;
            Activate();
            Topmost = true;
            Dispatcher.BeginInvoke(DispatcherPriority.Background, new Action(() => Topmost = false));
        }

        public void ExitApplication()
        {
            var r = MessageBox.Show("Stop the SARA server before exiting?", "Exit", MessageBoxButton.YesNoCancel, MessageBoxImage.Question);
            if (r == MessageBoxResult.Cancel) return;
            if (r == MessageBoxResult.Yes)
            {
                if (_serverProcess != null && !_serverProcess.HasExited)
                { try { _serverProcess.Kill(entireProcessTree: true); _serverProcess.WaitForExit(2000); } catch { } }
            }
            _forceClose = true;
            _tray?.Dispose();
            Application.Current.Shutdown();
        }

        private void Window_Closing(object? sender, CancelEventArgs e)
        {
            if (!_forceClose)
            {
                e.Cancel = true;
                Hide();
                _tray?.ShowBalloon("SARA Server Agent", "Agent continues running in the system tray.");
                return;
            }
            if (_serverProcess != null && !_serverProcess.HasExited)
            { try { _serverProcess.Kill(entireProcessTree: true); _serverProcess.WaitForExit(2000); } catch { } }
            _tray?.Dispose();
        }
    }
}
