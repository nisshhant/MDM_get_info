using Microsoft.AspNetCore.Mvc;

namespace SystemInfoAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class CommandController : ControllerBase
    {
        private static string _currentCommand = "start"; // or "idle"

        [HttpGet]
        public IActionResult GetCommand()
        {
            return Ok(new { command = _currentCommand });
        }

        [HttpPost]
        public IActionResult SetCommand([FromBody] CommandUpdate cmd)
        {
            if (string.IsNullOrWhiteSpace(cmd.Cmd))
                return BadRequest("Command cannot be empty.");

            _currentCommand = cmd.Cmd.ToLower();
            return Ok(new { status = "updated", newCommand = _currentCommand });
        }

        public class CommandUpdate
        {
            public string Cmd { get; set; }
        }
    }
}
