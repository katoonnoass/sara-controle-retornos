using Microsoft.Win32;
using System;

namespace SaraServerAgent
{
    public class StartupService
    {
        private const string RegistryKeyPath = @"Software\Microsoft\Windows\CurrentVersion\Run";
        private const string AppName = "SARA Server Agent";

        public bool IsAutoStartEnabled()
        {
            try
            {
                using var key = Registry.CurrentUser.OpenSubKey(RegistryKeyPath);
                if (key == null) return false;
                var value = key.GetValue(AppName) as string;
                return !string.IsNullOrEmpty(value);
            }
            catch
            {
                return false;
            }
        }

        public void EnableAutoStart(string executablePath)
        {
            try
            {
                using var key = Registry.CurrentUser.OpenSubKey(RegistryKeyPath, true);
                if (key != null)
                {
                    key.SetValue(AppName, executablePath);
                }
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException("Failed to enable auto-start: " + ex.Message, ex);
            }
        }

        public void DisableAutoStart()
        {
            try
            {
                using var key = Registry.CurrentUser.OpenSubKey(RegistryKeyPath, true);
                if (key != null)
                {
                    key.DeleteValue(AppName, false);
                }
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException("Failed to disable auto-start: " + ex.Message, ex);
            }
        }
    }
}
