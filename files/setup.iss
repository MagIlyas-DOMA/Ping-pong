; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{DF87B769-D497-405C-B95D-D21DE67E7014}
AppName=����-����
AppVersion=1.0
;AppVerName=����-���� 1.0
DefaultDirName={autopf}\Ping-pong
DefaultGroupName=����-����
AllowNoIcons=yes
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputBaseFilename=setup
SetupIconFile=C:\Users\���������� ������ 2\PycharmProjects\Game Project\dop\files\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\���������� ������ 2\PycharmProjects\Game Project\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\���������� ������ 2\PycharmProjects\Game Project\files"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\����-����"; Filename: "{app}\main.exe"
Name: "{group}\{cm:UninstallProgram,����-����}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\����-����"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,����-����}"; Flags: nowait postinstall skipifsilent

