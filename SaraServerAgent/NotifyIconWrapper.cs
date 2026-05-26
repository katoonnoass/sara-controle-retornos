using System;
using System.Drawing;
using System.Windows;
using System.Windows.Forms;

namespace SaraServerAgent
{
    public class NotifyIconWrapper : IDisposable
    {
        private readonly NotifyIcon _notifyIcon;
        private readonly MainWindow _window;

        public NotifyIconWrapper(MainWindow window)
        {
            _window = window;

            var contextMenu = new ContextMenuStrip();
            contextMenu.Items.Add("Open Panel", null, (s, e) => _window.ShowWindow());
            contextMenu.Items.Add(new ToolStripSeparator());
            contextMenu.Items.Add("Start Server", null, (s, e) => _window.Dispatcher.Invoke(() => _window.BtnStart_Click(null, null)));
            contextMenu.Items.Add("Stop Server", null, async (s, e) => _window.Dispatcher.Invoke(() => _window.BtnStop_Click(null, null)));
            contextMenu.Items.Add(new ToolStripSeparator());
            contextMenu.Items.Add("Open SARA in Browser", null, (s, e) => _window.Dispatcher.Invoke(() => _window.BtnOpen_Click(null, null)));
            contextMenu.Items.Add(new ToolStripSeparator());
            contextMenu.Items.Add("Exit", null, (s, e) => _window.ExitApplication());

            _notifyIcon = new NotifyIcon
            {
                Icon = SystemIcons.Application,
                Text = "SARA Server Agent",
                ContextMenuStrip = contextMenu,
                Visible = true
            };
            _notifyIcon.DoubleClick += (s, e) => _window.ShowWindow();
        }

        public void ShowBalloon(string title, string text)
        {
            _notifyIcon.ShowBalloonTip(2000, title, text, ToolTipIcon.Info);
        }

        public void Dispose()
        {
            _notifyIcon.Visible = false;
            _notifyIcon.Dispose();
        }
    }
}
