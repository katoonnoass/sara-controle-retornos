using System;
using System.IO;
using System.Windows;

namespace SaraServerAgent
{
    public partial class SettingsWindow : Window
    {
        private readonly ConfigService _configService;
        private readonly StartupService _startupService;
        private readonly MainViewModel _viewModel;

        public SettingsWindow(ConfigService configService, StartupService startupService, MainViewModel viewModel)
        {
            InitializeComponent();
            _configService = configService;
            _startupService = startupService;
            _viewModel = viewModel;

            LoadConfig();
        }

        private void LoadConfig()
        {
            var cfg = _configService.Config;
            txtProjectPath.Text = cfg.ProjectPath;
            txtUrl.Text = cfg.Url;
            txtPort.Text = cfg.Port.ToString();
            chkAutoStart.IsChecked = _startupService.IsAutoStartEnabled();
            chkMinimizeToTray.IsChecked = cfg.MinimizeToTrayOnClose;
        }

        private void Save_Click(object sender, RoutedEventArgs e)
        {
            var cfg = _configService.Config;
            cfg.ProjectPath = txtProjectPath.Text.Trim();
            cfg.Url = txtUrl.Text.Trim();

            if (int.TryParse(txtPort.Text.Trim(), out int port))
                cfg.Port = port;

            cfg.MinimizeToTrayOnClose = chkMinimizeToTray.IsChecked ?? true;

            bool wasAutoStart = _startupService.IsAutoStartEnabled();
            bool wantAutoStart = chkAutoStart.IsChecked ?? false;

            if (wasAutoStart != wantAutoStart)
            {
                if (wantAutoStart)
                {
                    string exePath = System.IO.Path.Combine(AppContext.BaseDirectory, "SARA Server Agent.exe");
                    _startupService.EnableAutoStart(exePath);
                }
                else
                {
                    _startupService.DisableAutoStart();
                }
            }

            _configService.Save(cfg);
            _viewModel.AppendLog("Settings saved.");
            if (wasAutoStart != wantAutoStart)
            {
                _viewModel.AppendLog(wantAutoStart ? "Auto-start enabled." : "Auto-start disabled.");
            }

            DialogResult = true;
            Close();
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }

        private void BrowsePath_Click(object sender, RoutedEventArgs e)
        {
            using var dialog = new System.Windows.Forms.FolderBrowserDialog();
            dialog.SelectedPath = txtProjectPath.Text;
            if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                txtProjectPath.Text = dialog.SelectedPath;
            }
        }

        private void TestPort_Click(object sender, RoutedEventArgs e)
        {
            var portService = new PortService();
            if (int.TryParse(txtPort.Text.Trim(), out int port))
            {
                bool open = portService.IsPortOpen(port);
                MessageBox.Show(
                    open ? $"Port {port} is in use." : $"Port {port} is available.",
                    "Port Test",
                    MessageBoxButton.OK,
                    open ? MessageBoxImage.Warning : MessageBoxImage.Information);
            }
        }
    }
}
