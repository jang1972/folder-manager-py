#!/usr/bin/env python3
# 리눅서일시 sudo ln -s "$(pwd)/folder_manager.py" /usr/local/bin/fm'을 권장합니다.
# Dry-run 기능 추가 버전
# Made by Michelle
# With Gemini
# Edit Tool is VSC, Kate

import os
import sys
import re
import shutil
from datetime import datetime

ASCII_ART = r"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢠⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣾⡌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⢫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⢠⣿⣧⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⣛⣉⣭⣭⣭⣭⣭⣍⣙⡓⠀⠉⠸⣿⣿⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡜⣏⢿⣿⣿⣿⣿⣿⠿⣋⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠈⠹⠡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣇⢻⣷⣝⣛⠿⣛⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣠⣀⡀⣤⠘⠟⠈⠉⠉⣙⣛⣋⠉⣹⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣦⣙⠻⠿⠿⢛⣭⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠉⠉⠙⠉⢁⢀⣀⢠⣾⣿⠟⣡⣾⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⣰⢫⣾⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣷⡹⣿⣿⠏⠀⠀⠀⣠⡾⢀⠀⠉⠃⠉⣴⣾⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟⣰⢣⣿⣿⣿⣿⣿⣧⢿⣿⣿⣿⣿⣿⣿⣷⡹⣿⣿⣷⣶⣷⣝⠁⠀⠁⠀⠀⢠⢹⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⢁⡇⣿⣿⣿⣿⣿⣿⣿⡸⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⣿⡆⣄⠀⠀⠀⠈⣇⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠏⣼⢳⣿⣿⣿⣿⣿⣿⡿⣡⢻⣿⣿⣿⣿⣿⣿⣿⡆⡝⢿⣿⣿⣿⣷⢹⣷⣄⠀⠀⢿⠘⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⢫⣾⣿⢸⡿⣿⣿⣿⣿⠻⣣⣿⣦⢻⣿⢻⣿⣿⣿⣿⡇⣿⣦⣙⢿⣿⣿⢸⣿⣿⣷⣄⣼⣧⠻⣿⣿⣿⣿⣿⣿
⣿⠿⠟⡯⠶⠟⣋⠙⣼⢹⣿⣿⣿⣿⣰⣿⣿⣿⣷⡹⣧⡙⣿⣿⣿⣿⢸⣿⣿⣷⣮⣛⢸⣿⣿⣿⢳⣜⠿⣷⣌⡻⢿⣿⣿⣿
⣿⣿⣷⣶⣾⣿⣿⡇⢹⠘⣿⣿⣿⣿⠿⠛⠛⠛⠛⠙⣮⡃⢮⡻⢿⣿⠙⠛⠛⠛⠻⠿⣼⣿⣿⣿⢸⡟⣰⣶⣬⣭⣥⣬⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠘⣦⡹⣿⣿⣿⢶⣶⣶⣶⣾⣿⣿⣿⣾⣿⣷⣭⣾⣶⣶⣶⡶⢰⣿⣿⣿⢇⡼⣱⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠀⣾⣿⣌⣻⠿⡞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣱⣿⡿⢛⣵⣯⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢀⣿⣿⣿⣿⣷⣴⣾⠿⣿⣿⣿⣿⣿⣴⣦⣿⣿⣿⣿⣯⠼⣭⣤⣶⣿⣿⣿⡇⢿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⢸⣿⣿⣿⣿⡿⠀⠉⠀⠈⠉⠈⠻⢿⣿⣿⡿⠛⠁⠉⠀⠈⠉⠐⣿⣿⣿⣿⣷⢸⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⠛⠛⠀⠀⠀⠀⠀⠀⢀⠈⡭⡋⣀⠀⠀⠀⠀⠀⠀⠈⠛⢻⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠄⠀⠀⠀⠀⠀⠀⣁⣀⢀⡁⠀⠀⠀⠀⠀⠀⢠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣆⢀⡔⢛⣕⢂⢲⡝⠓⢄⢀⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
"""

# --- 1. 환경 설정 및 전역 변수 ---

CURRENT_DIR = os.getcwd()
ARCHIVE_FOLDER_NAME = "Archive"
MAX_FOLDER_NUMBER = 99
DRY_RUN = False  # 드라이 런 플래그

# Windows 예약어 및 금지 문자
WINDOWS_RESERVED_NAMES = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
WINDOWS_INVALID_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
WINDOWS_INVALID_CHARS_PATTERN = f'[{re.escape("".join(WINDOWS_INVALID_CHARS))}]'

# --- 2. 시스템 변경 제어 함수 (Dry-run의 핵심) ---

def sys_call(func, *args, **kwargs):
    """실제로 시스템을 변경하는 함수들을 래핑합니다."""
    func_name = func.__name__
    if DRY_RUN:
        print(f"   🔍 [DRY-RUN] 실행 예정: {func_name}({args})")
        return True
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"❌ [오류] {func_name} 실행 중 실패: {e}")
        return False

# --- 3. 유틸리티 함수 ---

def check_os():
    if sys.platform.startswith('win'):
        print("✅ 운영체제 감지: Windows 모드")
        return 'Windows'
    else:
        print("✅ 운영체제 감지: POSIX 모드 (Linux, macOS 등)")
        return 'POSIX'

def get_numbered_folders():
    folders = {}
    pattern = re.compile(r"^(\d{2})_.*")
    for item in os.listdir(CURRENT_DIR):
        item_path = os.path.join(CURRENT_DIR, item)
        if os.path.isdir(item_path) and item != ARCHIVE_FOLDER_NAME:
            match = pattern.match(item)
            if match:
                folder_number = int(match.group(1))
                folders[folder_number] = item
    return dict(sorted(folders.items()))

def rename_folder(old_name, new_number):
    match = re.search(r"^\d{2}_(.*)", old_name)
    suffix = match.group(1) if match else ""
    new_name = f"{new_number:02d}_{suffix}"
    
    old_path = os.path.join(CURRENT_DIR, old_name)
    new_path = os.path.join(CURRENT_DIR, new_name)
    
    print(f"   [이름 변경]: {old_name} -> {new_name}")
    sys_call(os.rename, old_path, new_path)

def show_alert(message):
    print("\n" + "="*50)
    print(f"🚨 경고: {message}")
    print("="*50)
    if not DRY_RUN:
        input("아무 키나 누르면 닫힙니다...")

def validate_folder_name(current_os, suffix):
    if current_os == 'Windows':
        base_name = suffix.split('.')[0].upper()
        if base_name in WINDOWS_RESERVED_NAMES:
            return False, f"'{suffix}'는 Windows 예약어입니다."
        if re.search(WINDOWS_INVALID_CHARS_PATTERN, suffix):
            return False, f"금지 문자 포함: {', '.join(WINDOWS_INVALID_CHARS)}"
        if suffix.endswith((' ', '.')):
            return False, "Windows 이름은 공백이나 점으로 끝날 수 없습니다."
    else:
        if '/' in suffix:
            return False, "POSIX에서는 '/'를 사용할 수 없습니다."
    return True, ""

# --- 4. 핵심 로직 ---

def handle_archive_collision(archive_path, conflict_name):
    current_conflict_path = os.path.join(archive_path, conflict_name)
    if os.path.exists(current_conflict_path):
        print(f"   [충돌 감지]: {conflict_name}이 아카이브에 이미 존재함.")
        old_conflict_name = f"old_{conflict_name}"
        old_conflict_path = os.path.join(archive_path, old_conflict_name)
        
        if os.path.exists(old_conflict_path):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_old_name = f"{timestamp}_{old_conflict_name}"
            new_old_path = os.path.join(archive_path, new_old_name)
            print(f"   [2차 충돌]: old 폴더도 존재. 타임스탬프 처리: {new_old_name}")
            if not sys_call(shutil.move, old_conflict_path, new_old_path): return False
            
        print(f"   [해결]: {conflict_name} -> {old_conflict_name}")
        if not sys_call(shutil.move, current_conflict_path, old_conflict_path): return False
    return True

def create_folder_mode(target_num, folder_suffix, current_os):
    print(f"\n➡️ 폴더 생성 모드 진입: {target_num:02d}번")
    is_valid, reason = validate_folder_name(current_os, folder_suffix)
    if not is_valid:
        show_alert(reason)
        return
        
    numbered_folders = get_numbered_folders()
    if target_num > MAX_FOLDER_NUMBER:
        show_alert(f"최대 번호 {MAX_FOLDER_NUMBER} 초과")
        return

    for number in sorted(numbered_folders.keys(), reverse=True):
        if number >= target_num:
            if number + 1 > MAX_FOLDER_NUMBER: continue 
            rename_folder(numbered_folders[number], number + 1)

    new_folder_name = f"{target_num:02d}_{folder_suffix}"
    new_folder_path = os.path.join(CURRENT_DIR, new_folder_name)
    print(f"\n🎉 새 폴더 생성: {new_folder_name}")
    sys_call(os.mkdir, new_folder_path)

def archive_folder_mode(target_num):
    print(f"\n➡️ 아카이브 모드 진입: {target_num:02d}번")
    numbered_folders = get_numbered_folders()
    if target_num not in numbered_folders:
        print(f"❌ {target_num:02d}번 폴더 없음.")
        return

    archive_path = os.path.join(CURRENT_DIR, ARCHIVE_FOLDER_NAME)
    if not os.path.exists(archive_path):
        sys_call(os.makedirs, archive_path)

    target_name = numbered_folders[target_num]
    target_path = os.path.join(CURRENT_DIR, target_name)
    
    if handle_archive_collision(archive_path, target_name):
        print(f"✅ 아카이브 이동: {target_name}")
        sys_call(shutil.move, target_path, archive_path)

    for number in sorted(numbered_folders.keys()):
        if number > target_num:
            rename_folder(numbered_folders[number], number - 1)

def fill_gaps_mode():
    print("\n➡️ 번호 채우기(정리) 모드 진입")
    numbered_folders = get_numbered_folders()
    if not numbered_folders: return

    for index, old_number in enumerate(sorted(numbered_folders.keys()), start=1):
        if old_number != index:
            rename_folder(numbered_folders[old_number], index)
    print("\n✅ 정리 완료.")

# --- 5. 메인 실행부 ---

def main():
    global DRY_RUN
    print(ASCII_ART)
    current_os = check_os()

    if "--dry-run" in sys.argv:
        DRY_RUN = True
        sys.argv.remove("--dry-run")
        print("⚠️  [DRY-RUN MODE] 실제 파일 변경이 일어나지 않습니다.\n")

    if len(sys.argv) < 2:
        print("사용법: fm [make|rm|fill] [번호] [이름]")
        return

    mode = sys.argv[1].lower()
    CREATE_KW = ['생성', '만들기', 'mk', 'make', 'mkdir']
    DELETE_KW = ['삭제', '지우기', 'del', 'rm', 'rmdir', 'archive']
    FILL_KW = ['fill', 'fillup', '채우기', '정리']

    if mode in CREATE_KW or mode in DELETE_KW:
        if len(sys.argv) < 3:
            print("❌ 번호가 필요합니다.")
            return
        target_num = int(sys.argv[2])
        if mode in CREATE_KW:
            suffix = sys.argv[3] if len(sys.argv) > 3 else "새폴더"
            create_folder_mode(target_num, suffix, current_os)
        else:
            archive_folder_mode(target_num)
    elif mode in FILL_KW:
        fill_gaps_mode()
    else:
        print(f"❌ 알 수 없는 모드: {mode}")

if __name__ == "__main__":
    main()
