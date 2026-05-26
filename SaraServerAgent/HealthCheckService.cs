using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace SaraServerAgent
{
    public enum ServerHealth
    {
        Offline,
        Online,
        Error
    }

    public class HealthCheckService
    {
        private readonly HttpClient _client;

        public HealthCheckService()
        {
            _client = new HttpClient
            {
                Timeout = TimeSpan.FromSeconds(5)
            };
        }

        public async Task<ServerHealth> CheckAsync(string url)
        {
            try
            {
                string healthUrl = url.TrimEnd('/') + "/health";
                var response = await _client.GetAsync(healthUrl);
                if (response.IsSuccessStatusCode)
                    return ServerHealth.Online;
                return ServerHealth.Error;
            }
            catch (TaskCanceledException)
            {
                return ServerHealth.Offline;
            }
            catch (HttpRequestException)
            {
                return ServerHealth.Offline;
            }
            catch
            {
                return ServerHealth.Error;
            }
        }
    }
}
