﻿#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance, Force
FileEncoding , UTF-8


:or:hello.::
FileRead, Clipboard, %A_ScriptDir%\responses\helloworld.txt
Send, ^v
return

