@echo off
setlocal enabledelayedexpansion
echo 'Julius start.'
cd /d %~dp0
julius -C am-gmm.jconf -module -w command.voca -fvad 3
