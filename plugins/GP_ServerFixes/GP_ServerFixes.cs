using System.Globalization;
using System.Text.Json.Serialization;
using CounterStrikeSharp.API;
using CounterStrikeSharp.API.Core;
using CounterStrikeSharp.API.Modules.Cvars;
using CounterStrikeSharp.API.Modules.Timers;
using Microsoft.Extensions.Logging;

namespace GP_ServerFixes;

public class ServerListPlayersConfig
{
    [JsonPropertyName("Enabled")] public bool Enabled { get; set; } = true;

    /// <summary>Seconds between pushes of the player list to Steam (min 1).</summary>
    [JsonPropertyName("UpdateInterval")] public float UpdateInterval { get; set; } = 5f;
}

public class SlowAnimationConfig
{
    [JsonPropertyName("Enabled")] public bool Enabled { get; set; } = true;

    /// <summary>Seconds between empty-server checks (min 60). An empty server reloads its map.</summary>
    [JsonPropertyName("ReloadInterval")] public float ReloadInterval { get; set; } = 1800f;
}

public class GpServerFixesConfig : BasePluginConfig
{
    [JsonPropertyName("ServerListPlayers")] public ServerListPlayersConfig ServerListPlayers { get; set; } = new();
    [JsonPropertyName("SlowAnimation")] public SlowAnimationConfig SlowAnimation { get; set; } = new();
}

/// <summary>
/// Two fixes from GameFixes_mm, reimplemented on CounterStrikeSharp:
///  - server_list_players: CS2 reports no players to Steam, so the server browser and
///    A2S_PLAYER queries (sites, monitoring) show an empty list. Every few seconds each
///    connected player's SteamID, name and score is pushed via ISteamGameServer::BUpdateUserData.
///  - slow_animation: curtime is a 32-bit float and loses precision after a day or two on one
///    map (sluggish animations / movement / lag compensation). While the server is empty at a
///    check, the current map is reloaded; the remaining mp_timelimit is carried over.
/// </summary>
public class GpServerFixes : BasePlugin, IPluginConfig<GpServerFixesConfig>
{
    public override string ModuleName => "GP_ServerFixes";
    public override string ModuleVersion => "0.1.0";
    public override string ModuleAuthor => "GAMEPOINT";
    public override string ModuleDescription => "Server list players + slow animation fix (from GameFixes_mm)";

    public GpServerFixesConfig Config { get; set; } = new();

    private SteamGameServer? _steam;
    private bool _steamWarned;

    private string _mapName = string.Empty;
    private DateTime _mapStartUtc = DateTime.UtcNow;
    private float _pendingTimelimit = -1f;

    public void OnConfigParsed(GpServerFixesConfig config)
    {
        config.ServerListPlayers.UpdateInterval = Math.Max(1f, config.ServerListPlayers.UpdateInterval);
        config.SlowAnimation.ReloadInterval = Math.Max(60f, config.SlowAnimation.ReloadInterval);
        Config = config;
    }

    public override void Load(bool hotReload)
    {
        if (Config.ServerListPlayers.Enabled)
        {
            _steam = SteamGameServer.TryCreate(Server.GameDirectory, out var error);
            if (_steam == null)
            {
                Logger.LogError("[server_list_players] disabled: {Error}", error);
            }
            else
            {
                AddTimer(Config.ServerListPlayers.UpdateInterval, PushPlayersToSteam, TimerFlags.REPEAT);
                Logger.LogInformation("[server_list_players] pushing players to Steam every {Interval}s ({Lib})",
                    Config.ServerListPlayers.UpdateInterval, _steam.LibraryPath);
            }
        }

        if (Config.SlowAnimation.Enabled)
        {
            RegisterListener<Listeners.OnMapStart>(OnMapStart);
            AddTimer(Config.SlowAnimation.ReloadInterval, CheckReload, TimerFlags.REPEAT);
            Logger.LogInformation("[slow_animation] checking for an empty server every {Interval}s",
                Config.SlowAnimation.ReloadInterval);

            if (hotReload)
            {
                // Loaded mid-map: the map has been running for an unknown time, count from now.
                _mapName = Server.MapName;
                _mapStartUtc = DateTime.UtcNow;
            }
        }
    }

    // ---------------- server_list_players ----------------

    private void PushPlayersToSteam()
    {
        if (_steam == null)
            return;

        var gameServer = _steam.GetInterface();
        if (gameServer == IntPtr.Zero)
        {
            if (!_steamWarned)
            {
                Logger.LogWarning("[server_list_players] Steam game server interface not available yet");
                _steamWarned = true;
            }
            return;
        }
        _steamWarned = false;

        foreach (var player in Utilities.GetPlayers())
        {
            if (!player.IsValid || player.IsBot || player.IsHLTV || player.SteamID == 0 ||
                player.Connected != PlayerConnectedState.Connected)
                continue;

            var score = (uint)Math.Max(0, player.Score);
            _steam.UpdateUserData(gameServer, player.SteamID, player.PlayerName ?? string.Empty, score);
        }
    }

    // ---------------- slow_animation ----------------

    private void OnMapStart(string mapName)
    {
        _mapName = mapName;
        _mapStartUtc = DateTime.UtcNow;

        if (_pendingTimelimit < 0f)
            return;

        var remaining = _pendingTimelimit > 0f ? _pendingTimelimit : 0.1f;
        _pendingTimelimit = -1f;

        // The map's configs run after map start and would overwrite the value; set it a bit later.
        AddTimer(3.0f, () =>
        {
            var value = remaining.ToString("0.0", CultureInfo.InvariantCulture);
            Logger.LogInformation("[slow_animation] restoring remaining timelimit -> mp_timelimit {Value}", value);
            Server.ExecuteCommand($"mp_timelimit {value}");
        }, TimerFlags.STOP_ON_MAPCHANGE);
    }

    private void CheckReload()
    {
        if (string.IsNullOrEmpty(_mapName))
            return;

        var humans = Utilities.GetPlayers().Count(p =>
            p.IsValid && !p.IsBot && !p.IsHLTV && p.Connected == PlayerConnectedState.Connected);
        if (humans > 0)
            return;

#pragma warning disable CS0618 // ConVar is enough for one read
        var timelimit = ConVar.Find("mp_timelimit")?.GetPrimitiveValue<float>() ?? 0f;
#pragma warning restore CS0618
        if (timelimit > 0f)
        {
            var elapsedMinutes = (float)(DateTime.UtcNow - _mapStartUtc).TotalMinutes;
            _pendingTimelimit = timelimit - elapsedMinutes;
        }

        var map = _mapName;
        var command = Server.IsMapValid(map) ? $"changelevel {map}" : $"ds_workshop_changelevel {map}";
        Logger.LogInformation("[slow_animation] server empty -> {Command}", command);
        Server.ExecuteCommand(command);
    }
}
