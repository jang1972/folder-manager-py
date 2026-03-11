@echo off
chcp 949 > nul
title 폴더 매니저 전용 터미널

:loop
echo.
echo --------------------------------------------------
echo 만들기, 생성, mk 입력시 폴더가 생성 됩니다.
echo 삭제, 지우기, rm 입력시 폴더가 아카이브 폴더로 이동 되며 폴더명 충돌시 1차적으로 _old 처리, 2차적으로 년도:월:일:시간:분:초 타임스탬프로 처리가 됩니다.
echo 채우기, fill 입력시 비어 있는 번호가 자동으로 당겨집니다.
echo 되돌리기, undo 입력시 직전에 수행한 작업이 취소되나, 취소 대상이 되는 폴더내에 파일이 있을시 수동으로 사용자가 처리 해야합니다.
echo --------------------------------------------------
set /p input="folder_manager.exe "

if "%input%"=="exit" goto eof
if "%input%"=="" goto loop

:: 입력값을 번호(num)와 이름(name)으로 분리하여 실행
folder_manager.exe %input%

goto loop

:eof
echo 프로그램을 종료합니다.
pause

