using System.Text.Json.Serialization;

namespace SaraServerAgent
{
    public class AgentConfig
    {
        [JsonPropertyName("ProjectPath")]
        public string ProjectPath { get; set; } = @"C:\Users\joao.silva\Documents\SARA";

        [JsonPropertyName("StartMode")]
        public string StartMode { get; set; } = "powershell";

        [JsonPropertyName("StartCommand")]
        public string StartCommand { get; set; } = "powershell";

        [JsonPropertyName("StartArguments")]
        public string StartArguments { get; set; } = "-ExecutionPolicy Bypass -File run_producao.ps1";

        [JsonPropertyName("FallbackCommand")]
        public string FallbackCommand { get; set; } = "python";

        [JsonPropertyName("FallbackArguments")]
        public string FallbackArguments { get; set; } = "app.py";

        [JsonPropertyName("Url")]
        public string Url { get; set; } = "http://127.0.0.1:5000";

        [JsonPropertyName("Port")]
        public int Port { get; set; } = 5000;

        [JsonPropertyName("AutoStartWithWindows")]
        public bool AutoStartWithWindows { get; set; } = false;

        [JsonPropertyName("MinimizeToTrayOnClose")]
        public bool MinimizeToTrayOnClose { get; set; } = true;
    }
}
