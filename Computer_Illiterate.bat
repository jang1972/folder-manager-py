@echo off
chcp 65001 > nul
title 폴더 매니저 전용 터미널

echo.
echo --------------------------------------------------
echo 만들기, 생성, mk 입력시 폴더가 생성 됩니다.
echo 삭제, 지우기, rm 입력시 폴더가 아카이브 폴더로 이동 되며 폴더명 충돌시 1차적으로 _old 처리, 2차적으로 년도:월:일:시간:분:초 타임스탬프로 처리가 됩니다.
echo 채우기, fill 입력시 비어 있는 번호가 자동으로 당겨집니다.
echo 되돌리기, undo 입력시 직전에 수행한 작업이 취소되나, 취소 대상이 되는 폴더내에 파일이 있을시 수동으로 사용자가 처리 해야합니다.
echo 태그, 유형, tag 입력시 해당 폴더에 태그를 부여합니다.
echo 초기화, 비우기, reset, clear 입력시 이 프로그램의 로그(기록)이 초기화 되며 롤백이 불가능합니다.
echo 분석, analyze 입력시 해당 폴더의 크기와 태그를 확인 가능합니다.
echo https://github.com/jang1972/folder-manager-py/releases에 방문하시면 최신 버전을 다운로드 가능합니다
echo 본 도구는 GNU 공중 이용 허가서 3.0 제15조항과 제16조항에 따라 어떠한 형태의 보증도 제공하지 않습니다.
echo 구글이 안드로이드에서 제3자 앱을 실행 차단하여 사용자의 권리를 침해하려 하고 있습니다. 이를 막기 위해 도움을 보태 주시길 부탁 드립니다.
echo https://keepandroidopen.org
echo --------------------------------------------------

:loop
set /p input="folder_manager.exe "

if "%input%"=="exit" goto eof
if "%input%"=="" goto loop

:: 입력값을 번호(num)와 이름(name)으로 분리하여 실행
folder_manager.exe %input%

goto loop

:eof
echo 프로그램을 종료합니다.
pause

