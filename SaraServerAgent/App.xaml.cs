using System.Windows;

namespace SaraServerAgent
{
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);
            var w = new MainWindow();
            MainWindow = w;
            w.Show();
        }
    }
}
