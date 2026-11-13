using System.Runtime.InteropServices;

namespace GP_ServerFixes;

/// <summary>
/// Minimal access to the game server's Steam API through the Steamworks flat C exports
/// (SteamAPI_SteamGameServer_v015, SteamAPI_ISteamGameServer_BUpdateUserData) of the
/// steam_api library the engine has already loaded. No signatures or offsets involved.
/// </summary>
internal sealed unsafe class SteamGameServer
{
    private const string AccessorExport = "SteamAPI_SteamGameServer_v015";
    private const string UpdateUserDataExport = "SteamAPI_ISteamGameServer_BUpdateUserData";

    private readonly delegate* unmanaged[Cdecl]<IntPtr> _getGameServer;
    private readonly delegate* unmanaged[Cdecl]<IntPtr, ulong, byte*, uint, byte> _updateUserData;

    public string LibraryPath { get; }

    private SteamGameServer(string libraryPath, IntPtr getGameServer, IntPtr updateUserData)
    {
        LibraryPath = libraryPath;
        _getGameServer = (delegate* unmanaged[Cdecl]<IntPtr>)getGameServer;
        _updateUserData = (delegate* unmanaged[Cdecl]<IntPtr, ulong, byte*, uint, byte>)updateUserData;
    }

    /// <summary>Finds steam_api in the running server. Returns null (with a reason) if it can't.</summary>
    public static SteamGameServer? TryCreate(string gameDirectory, out string error)
    {
        var candidates = new List<string>();
        if (OperatingSystem.IsWindows())
        {
            candidates.Add("steam_api64.dll");
            candidates.Add(Path.Combine(gameDirectory, "bin", "win64", "steam_api64.dll"));
        }
        else
        {
            // dlopen by soname returns the copy the engine already loaded.
            candidates.Add("libsteam_api.so");
            candidates.Add(Path.Combine(gameDirectory, "bin", "linuxsteamrt64", "libsteam_api.so"));
        }

        foreach (var candidate in candidates)
        {
            if (!NativeLibrary.TryLoad(candidate, out var handle))
                continue;

            if (NativeLibrary.TryGetExport(handle, AccessorExport, out var accessor) &&
                NativeLibrary.TryGetExport(handle, UpdateUserDataExport, out var update))
            {
                error = string.Empty;
                return new SteamGameServer(candidate, accessor, update);
            }
        }

        error = $"steam_api not found or missing {AccessorExport} (tried: {string.Join(", ", candidates)})";
        return null;
    }

    /// <summary>ISteamGameServer*, or zero while the game server is not logged on to Steam yet.</summary>
    public IntPtr GetInterface() => _getGameServer();

    public bool UpdateUserData(IntPtr gameServer, ulong steamId64, string name, uint score)
    {
        var bytes = System.Text.Encoding.UTF8.GetBytes(name + "\0");
        fixed (byte* pName = bytes)
        {
            return _updateUserData(gameServer, steamId64, pName, score) != 0;
        }
    }
}
