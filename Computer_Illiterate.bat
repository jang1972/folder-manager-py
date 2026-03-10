@echo off
set /p num="번호를 입력하세요: "
set /p name="이름을 입력하세요: "
folder_manager.exe mk %num% %name%
pause
