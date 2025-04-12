;--------------------------------
; WechatLauncher Installer Script
;--------------------------------

; Basic settings
Name "WechatLauncher"
OutFile "install.exe"
InstallDir "$PROGRAMFILES\WechatLauncher"
InstallDirRegKey HKLM "Software\WechatLauncher" "Install_Dir"
RequestExecutionLevel admin  ; Administrator privileges required

;--------------------------------
; Pages
;--------------------------------
Page directory       ; Let user select installation directory
Page instfiles       ; Installation progress page

;--------------------------------
; Registry settings for uninstaller entry in Control Panel
;--------------------------------
; These keys will make the uninstall entry appear in Programs and Features.
VIProductVersion "1.0.0.0"
VIAddVersionKey /LANG=1033 "ProductName" "Wechat Launcher"
VIAddVersionKey /LANG=1033 "CompanyName" "Zheng Huang"
VIAddVersionKey /LANG=1033 "LegalTrademarks" "YourTrademark"  ; Update if needed

;--------------------------------
; Installer Section
;--------------------------------
Section "Install" SecMain

  ; Set output path to the installation directory
  SetOutPath "$INSTDIR"

  ; Copy the main executable into the installation folder.
  File "Wechat Launcher.exe"

  ; Copy the logo file into the installation folder.
  File "Logo.ico"

  ; Create the uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"

  ; --- Add to system startup ---
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Run" "WechatLauncher" '"$INSTDIR\Wechat Launcher.exe"'

  ; --- Create uninstall registry keys ---
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WechatLauncher" "DisplayName" "WechatLauncher"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WechatLauncher" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WechatLauncher" "DisplayVersion" "1.0.0.0"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WechatLauncher" "Publisher" "Zheng Huang"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WechatLauncher" "DisplayIcon" "$INSTDIR\Logo.ico"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WechatLauncher" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WechatLauncher" "NoRepair" 1

SectionEnd

;--------------------------------
; Uninstaller Section
;--------------------------------
Section "Uninstall"

  ; Remove the startup registry entry
  DeleteRegValue HKLM "Software\Microsoft\Windows\CurrentVersion\Run" "WechatLauncher"

  ; Remove the uninstall registry entry
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WechatLauncher"

  ; Delete installed files
  Delete "$INSTDIR\Wechat Launcher.exe"
  Delete "$INSTDIR\Logo.ico"
  Delete "$INSTDIR\uninstall.exe"

  ; Remove installation directory if empty
  RMDir "$INSTDIR"

SectionEnd
