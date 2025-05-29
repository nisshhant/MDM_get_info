using Microsoft.AspNetCore.Mvc;

namespace SystemInfoAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SystemInfoController : ControllerBase
    {
        [HttpPost]
        public IActionResult ReceiveSystemInfo([FromBody] object systemInfo)
        {
            // Define the path for the log file
            string logFilePath = Path.Combine(Directory.GetCurrentDirectory(), "Logs", "SystemInfoLog.txt");

           

            // Create the log content with timestamp
            string logEntry = $"[{DateTime.Now}] System Info received:\n{systemInfo}\n\n";

            // Append the log entry to the file
            System.IO.File.AppendAllText(logFilePath, logEntry);

            return Ok(new { status = "received" });
        }

    }
}
