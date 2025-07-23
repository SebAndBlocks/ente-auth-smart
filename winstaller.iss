[Setup]
AppName=Ente Auth Tray
AppVersion=1.0
DefaultDirName={autopf}\TurquoiseTNT\EnteAuthTray
DefaultGroupName=EnteAuthTray
OutputDir=dist
OutputBaseFilename=EnteAuthTrayInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Ente Auth Tray.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Ente Auth Tray"; Filename: "{app}\Ente Auth Tray.exe"
Name: "{userstartup}\Ente Auth Tray"; Filename: "{app}\Ente Auth Tray.exe"; Tasks: addtostartup

[Tasks]
Name: "addtostartup"; Description: "Start Ente Tray on Windows startup"; GroupDescription: "Additional Options";

[Run]
Filename: "{app}\Ente Auth Tray.exe"; Description: "Launch Ente Tray"; Flags: nowait postinstall skipifsilent
