using System;
using System.IO;
using System.Text.Json;

namespace SaraServerAgent
{
    public class ConfigService
    {
        private readonly string _configPath;
        public AgentConfig Config { get; private set; }

        public ConfigService()
        {
            string exeDir = AppDomain.CurrentDomain.BaseDirectory;
            _configPath = Path.Combine(exeDir, "config.json");
            Config = Load();
        }

        private AgentConfig Load()
        {
            try
            {
                if (File.Exists(_configPath))
                {
                    string json = File.ReadAllText(_configPath);
                    var cfg = JsonSerializer.Deserialize<AgentConfig>(json);
                    if (cfg != null) return cfg;
                }
            }
            catch { }
            return new AgentConfig();
        }

        public void Save(AgentConfig config)
        {
            try
            {
                Config = config;
                string json = JsonSerializer.Serialize(config, new JsonSerializerOptions { WriteIndented = true });
                File.WriteAllText(_configPath, json);
            }
            catch (Exception ex)
            {
                throw new IOException("Failed to save configuration: " + ex.Message, ex);
            }
        }

        public void Save()
        {
            Save(Config);
        }

        public string GetEffectiveStartCommand()
        {
            string psPath = Path.Combine(Config.ProjectPath, "run_producao.ps1");
            if (File.Exists(psPath))
            {
                return Config.StartCommand;
            }
            return Config.FallbackCommand;
        }

        public string GetEffectiveStartArguments()
        {
            string psPath = Path.Combine(Config.ProjectPath, "run_producao.ps1");
            if (File.Exists(psPath))
            {
                return Config.StartArguments;
            }
            return Config.FallbackArguments;
        }
    }
}
