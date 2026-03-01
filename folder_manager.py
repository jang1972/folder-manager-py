#!/usr/bin/env python3
# 리눅서일시 sudo ln -s "$(pwd)/folder_manager.py" /usr/local/bin/fm'을 권장합니다.
# 시발 최종본 완성이다...
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
⣿⠿⠟⡯⠶⠟⣋⠑⣼⢹⣿⣿⣿⣿⣰⣿⣿⣿⣷⡹⣧⡙⣿⣿⣿⣿⢸⣿⣿⣷⣮⣛⢸⣿⣿⣿⢳⣜⠿⣷⣌⡻⢿⣿⣿⣿
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

# --- 1. 환경 설정 및 상수 정의 ---

# 현재 스크립트가 실행되는 디렉토리를 작업 디렉토리로 설정
CURRENT_DIR = os.getcwd()
ARCHIVE_FOLDER_NAME = "Archive"
MAX_FOLDER_NUMBER = 99

# Windows 예약어 및 금지 문자 정의
WINDOWS_RESERVED_NAMES = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
WINDOWS_INVALID_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
WINDOWS_INVALID_CHARS_PATTERN = f'[{re.escape("".join(WINDOWS_INVALID_CHARS))}]'


def check_os():
    """운영체제를 확인하고 POSIX 또는 Windows 모드를 반환합니다."""
    if sys.platform.startswith('win'):
        print("✅ 운영체제 감지: Windows 모드")
        return 'Windows'
    else:
        print("✅ 운영체제 감지: POSIX 모드 (Linux, macOS 등)")
        return 'POSIX'

# --- 2. 유틸리티 함수 ---

def get_numbered_folders():
    """
    현재 디렉토리에서 'XX_' 패턴을 가진 폴더 목록과 그 번호를 딕셔너리로 반환합니다.
    {번호: 폴더명} 형식으로 반환됩니다.
    """
    folders = {}
    pattern = re.compile(r"^(\d{2})_.*") # 맨 앞 두 자리 숫자만 인식

    # 현재 디렉토리의 모든 항목을 검사
    for item in os.listdir(CURRENT_DIR):
        item_path = os.path.join(CURRENT_DIR, item)
        # 디렉토리인지 확인하고 아카이브 폴더는 제외
        if os.path.isdir(item_path) and item != ARCHIVE_FOLDER_NAME:
            match = pattern.match(item)
            if match:
                folder_number = int(match.group(1))
                folders[folder_number] = item
    
    # 번호 순서대로 정렬된 딕셔너리 반환
    return dict(sorted(folders.items()))

def rename_folder(old_name, new_number):
    """폴더의 이름을 새 번호로 변경합니다."""
    # 기존 폴더명에서 뒤쪽 문자열(_ 뒤의 부분)을 추출
    match = re.search(r"^\d{2}_(.*)", old_name)
    suffix = match.group(1) if match else ""
    
    # 새 폴더명 생성 (예: 09 -> 10, 10_프로젝트 -> 11_프로젝트)
    new_name = f"{new_number:02d}_{suffix}"
    
    old_path = os.path.join(CURRENT_DIR, old_name)
    new_path = os.path.join(CURRENT_DIR, new_name)
    
    print(f"   [이름 변경]: {old_name} -> {new_name}")
    try:
        os.rename(old_path, new_path)
    except OSError as e:
        print(f"❌ 폴더 이름 변경 오류: {e}")

def show_alert(message):
    """간단한 경고 메시지를 출력하고 아무 키 입력을 기다립니다."""
    print("\n" + "="*50)
    print(f"🚨 경고: {message}")
    print("="*50)
    input("아무 키나 누르면 닫힙니다...")


# --- 2.1. OS별 이름 유효성 검사 로직 ---

def validate_folder_name_windows(suffix):
    """Windows용 폴더 이름 유효성 검사"""
    # 1. 예약어 검사
    base_name = suffix.split('.')[0].upper()
    if base_name in WINDOWS_RESERVED_NAMES:
        return False, f"'{suffix}'는 Windows 예약어입니다."
    
    # 2. 금지 문자 검사
    if re.search(WINDOWS_INVALID_CHARS_PATTERN, suffix):
        return False, f"Windows에서는 다음 문자들을 사용할 수 없습니다: {', '.join(WINDOWS_INVALID_CHARS)}"
        
    # 3. 마지막 문자 공백/점 검사 (Windows 제한)
    if suffix.endswith((' ', '.')):
        return False, "Windows 폴더 이름은 공백이나 점(.)으로 끝날 수 없습니다."
        
    return True, ""

def validate_folder_name_posix(suffix):
    """POSIX용 폴더 이름 유효성 검사"""
    # POSIX는 대부분의 문자를 허용하며, 경로는 "/"로만 제한됩니다.
    if '/' in suffix:
        return False, "POSIX에서는 폴더 이름에 경로 구분자('/')를 사용할 수 없습니다."
        
    return True, ""

def validate_folder_name(current_os, suffix):
    """현재 OS에 맞는 유효성 검사를 실행합니다."""
    if current_os == 'Windows':
        return validate_folder_name_windows(suffix)
    else: # POSIX
        return validate_folder_name_posix(suffix)
        
# --- 2.2. 아카이브 충돌 처리 로직 (수정 및 강화) ---

def rename_archive_folder_safely(old_path, new_path, old_name):
    """shutil.move를 사용하여 폴더 이름을 안전하게 변경하고, 내부 파일 이동을 보장합니다."""
    
    # 임시 폴더 경로 (현재 디렉터리에 임시로 이동)
    temp_dir = os.path.join(os.path.dirname(old_path), f"TEMP_{old_name}_{datetime.now().microsecond}")
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # 1. 기존 폴더를 임시 위치로 이동 (이름 변경 효과)
        shutil.move(old_path, temp_dir)
        
        # 2. 임시 폴더 이름을 새 이름으로 변경
        new_path_in_archive = os.path.join(os.path.dirname(old_path), new_path)
        os.rename(temp_dir, new_path_in_archive)
        
        return True
    except Exception as e:
        print(f"❌ 아카이브 폴더 안전 변경 실패: {e}")
        # 오류 발생 시 임시 폴더가 남아있을 수 있으므로 정리 시도 (필요시)
        if os.path.exists(temp_dir):
            try:
                os.rename(temp_dir, old_path) # 실패하면 원래 이름으로 되돌리기 시도
            except Exception:
                pass
        return False


def handle_archive_collision(archive_path, conflict_name):
    """
    아카이브 내의 기존 폴더와 이동하려는 폴더 이름이 충돌할 경우, 
    기존 폴더의 이름을 변경하여 충돌을 해결합니다.
    """
    current_conflict_name = conflict_name
    current_conflict_path = os.path.join(archive_path, current_conflict_name)
    
    old_conflict_name = f"old_{conflict_name}"
    old_conflict_path = os.path.join(archive_path, old_conflict_name)
    
    # 1. 아카이브 내에 이동할 폴더와 이름이 같은 폴더(current_conflict_path)가 존재하는지 확인
    if os.path.exists(current_conflict_path):
        print(f"   [충돌 감지]: {current_conflict_name} 폴더가 아카이브에 이미 존재합니다. 이름 변경 시도.")
        
        # 2. **2차 충돌 해결 (Old 폴더 처리)**: old_conflict_name이 이미 존재하는지 확인
        if os.path.exists(old_conflict_path):
            
            # old 폴더가 존재하므로, 이 폴더를 타임스탬프 처리하여 공간을 확보해야 합니다.
            original_old_name = old_conflict_name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_old_name = f"{timestamp}_{original_old_name}"
            new_old_path = os.path.join(archive_path, new_old_name)
            
            print(f"   [2차 충돌]: old_{conflict_name} 폴더도 이미 존재합니다. 타임스탬프 처리.")
            
            # 2-A. 타임스탬프 붙인 이름이 또 충돌할 경우 대비 (매우 드물지만 안전장치)
            while os.path.exists(new_old_path):
                print(f"   [3차 충돌]: 타임스탬프 처리 이름도 충돌. 재시도.")
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                new_old_name = f"{timestamp}_{original_old_name}"
                new_old_path = os.path.join(archive_path, new_old_name)
            
            # 2-B. 기존 old 폴더 이름 변경 실행 (이 폴더의 파일들이 타임스탬프 폴더로 이동함)
            # os.rename 대신 shutil.move를 사용
            try:
                shutil.move(old_conflict_path, new_old_path)
                print(f"   ✅ Old 폴더 해결: {original_old_name} -> {new_old_name}")
            except Exception as e:
                print(f"❌ Old 폴더 이름 변경 오류 (타임스탬프 적용 실패): {e}")
                return False
                
        # 3. **1차 충돌 해결 실행**: 이제 old_conflict_name이 비었으므로,
        #    current_conflict_path (현재 충돌하는 01_폴더)를 old_conflict_name으로 변경합니다.
        try:
            # 안정성등을 위해 os.rename 대신 shutil.move를 사용
            shutil.move(current_conflict_path, old_conflict_path)
            print(f"   ✅ 현재 충돌 폴더 해결: {current_conflict_name} -> {old_conflict_name}")
            return True
        except Exception as e:
            print(f"❌ 현재 충돌 폴더 이름 변경 오류 (old_ 적용 실패): {e}")
            return False
            
    return True # 충돌하는 폴더가 없다면 True 반환

# --- 3. 핵심 기능 함수 ---

def create_folder_mode(target_num, folder_suffix, current_os):
    """
    폴더 생성 모드: 지정된 번호부터 기존 폴더의 번호를 +1씩 일괄 조정합니다.
    """
    print(f"\n➡️ 폴더 생성 모드 진입: {target_num:02d}번 폴더 생성 시도")
    
    # 새로운 유효성 검사 로직 적용
    is_valid, reason = validate_folder_name(current_os, folder_suffix)
    if not is_valid:
        show_alert(f"유효하지 않은 폴더 이름입니다: {folder_suffix}\n이유: {reason}")
        return
        
    numbered_folders = get_numbered_folders()
    
    if target_num > MAX_FOLDER_NUMBER:
        show_alert(f"지정 번호 {target_num}은 최대 번호 {MAX_FOLDER_NUMBER}를 초과합니다.")
        return

    # 99개 꽉 찼는지 확인
    if len(numbered_folders) >= MAX_FOLDER_NUMBER and target_num in numbered_folders:
        show_alert(f"이미 {MAX_FOLDER_NUMBER}개의 폴더가 존재하며, 번호 조정 시 {MAX_FOLDER_NUMBER}번 폴더가 밀려납니다.")
        return
        
    # 역순으로 순회하며 +1씩 번호 조정
    for number in sorted(numbered_folders.keys(), reverse=True):
        if number >= target_num:
            # 99번 폴더가 100번으로 밀려날 경우 건너뜀
            if number + 1 > MAX_FOLDER_NUMBER:
                print(f"   [스킵]: {number:02d}번 폴더는 {MAX_FOLDER_NUMBER}번을 초과하므로 스킵합니다.")
                continue 
            
            old_name = numbered_folders[number]
            rename_folder(old_name, number + 1)

    # 새 폴더 생성
    new_folder_name = f"{target_num:02d}_{folder_suffix}"
    new_folder_path = os.path.join(CURRENT_DIR, new_folder_name)
    try:
        os.mkdir(new_folder_path)
        print(f"\n🎉 새 폴더 생성 완료: {new_folder_name}")
    except FileExistsError:
        print(f"\n❌ 오류: {new_folder_name} 폴더가 이미 존재합니다. (재시도 필요)")
    except OSError as e:
        print(f"\n❌ 폴더 생성 오류: {e}")

def archive_folder_mode(target_num):
    """
    아카이브 모드: 지정된 번호의 폴더를 아카이브로 이동하고 이후 폴더의 번호를 -1씩 일괄 조정합니다.
    """
    print(f"\n➡️ 아카이브 모드 진입: {target_num:02d}번 폴더 아카이브 시도")
    numbered_folders = get_numbered_folders()
    
    if target_num not in numbered_folders:
        print(f"❌ {target_num:02d}번 폴더를 찾을 수 없습니다. (현재 폴더 목록: {list(numbered_folders.keys())})")
        return

    # 1. 아카이브 폴더 생성 (없다면)
    archive_path = os.path.join(CURRENT_DIR, ARCHIVE_FOLDER_NAME)
    os.makedirs(archive_path, exist_ok=True)

    # 2. 타겟 폴더를 아카이브로 이동 (충돌 처리)
    target_name = numbered_folders[target_num]
    target_path = os.path.join(CURRENT_DIR, target_name)
    
    # 아카이브 내 충돌 해결 (충돌하는 폴더의 이름이 변경됨)
    if not handle_archive_collision(archive_path, target_name):
        print(f"❌ 아카이브 충돌 해결에 실패하여 {target_name} 이동을 중단합니다.")
        return
        
    try:
        # 충돌이 해결되었으므로, 현재 작업 디렉터리의 폴더를 아카이브로 이동합니다.
        shutil.move(target_path, archive_path)
        print(f"\n✅ 아카이브 완료: {target_name} -> {ARCHIVE_FOLDER_NAME}/")
    except shutil.Error as e:
        print(f"❌ 아카이브 이동 오류: {e}")
        return

    # 3. 순차적으로 번호 조정 (밀어 올리기)
    # 삭제된 번호 이후의 폴더만 순회
    for number in sorted(numbered_folders.keys()):
        if number > target_num:
            old_name = numbered_folders[number]
            rename_folder(old_name, number - 1)
            
    print("\n✅ 나머지 폴더 번호 조정 완료.")

# --- 4. 메인 실행 함수 ---

def main():
    """프로그램의 진입점 역할을 하며 모드를 파싱하고 함수를 호출합니다."""

    # 1. OS 감지
    print(ASCII_ART)
    current_os = check_os()

    # 2. 실행 인자 파싱 (최소 모드 키워드는 있어야 함)
    if len(sys.argv) < 2:
        print("\n사용법:")
        print("  [생성]: python folder_manager.py make [번호] [이름_선택사항]")
        print("  [삭제]: python folder_manager.py rm [번호]")
        print("  [정리]: python folder_manager.py fill")
        print("  [기타 유효한 키워드]: 생성, 만들기, mk, mkdir, 삭제, 지우기, del, rmdir, archive, fillup, 채우기, 정리")
        return

    mode_keyword = sys.argv[1].lower()

    # 모드별 키워드 정의
    CREATE_KEYWORDS = ['생성', '만들기', 'mk', 'make', 'mkdir']
    DELETE_KEYWORDS = ['삭제', '지우기', 'del', 'rm', 'rmdir', 'archive']
    FILL_KEYWORDS = ['fill', 'fillup', '채우기', '정리']

    # --- 로직 분기 ---

    # A. 생성 또는 삭제 모드 (번호 인자가 '필수'인 경우)
    if mode_keyword in CREATE_KEYWORDS or mode_keyword in DELETE_KEYWORDS:
        if len(sys.argv) < 3:
            print(f"❌ 오류: '{mode_keyword}' 모드를 사용하려면 [번호] 인자가 필요합니다.")
            print(f"예시: python folder_manager.py {mode_keyword} 05")
            return

        try:
            target_num = int(sys.argv[2])
        except ValueError:
            print("❌ 오류: 폴더 번호는 숫자로 입력해야 합니다.")
            return

        if mode_keyword in CREATE_KEYWORDS:
            # 폴더 이름 인자 (선택 사항)
            suffix = sys.argv[3] if len(sys.argv) > 3 else "새폴더"
            create_folder_mode(target_num, suffix, current_os)
        else:
            archive_folder_mode(target_num)

    # B. 정리 모드 (번호 인자가 '필수'가 아닌 경우)
    elif mode_keyword in FILL_KEYWORDS:
        fill_gaps_mode()

    # C. 알 수 없는 키워드
    else:
        print(f"❌ 알 수 없는 모드 키워드 '{mode_keyword}'입니다.")

# --- 5. 채우기 함수 ---
def fill_gaps_mode():
    """
    채우기 모드: 중간에 비어 있는 번호를 제거하고
    현재 폴더들을 01번부터 순차적으로 다시 번호 매김합니다.
    """
    print("\n➡️ 빈 번호 채우기(정리) 모드 진입")
    numbered_folders = get_numbered_folders() #

    if not numbered_folders:
        print("❌ 정리할 폴더가 없습니다.")
        return

    # 현재 번호들을 리스트로 추출
    current_numbers = sorted(numbered_folders.keys())

    print(f"   [현황 분석]: 총 {len(current_numbers)}개의 폴더 감지")

    # 1번부터 순차적으로 새 번호 부여
    for index, old_number in enumerate(current_numbers, start=1):
        if old_number != index:
            old_name = numbered_folders[old_number]
            # rename_folder 함수를 재사용하여 이름 변경 실행
            rename_folder(old_name, index) #
        else:
            # 번호가 이미 순서대로라면 건너뜀
            continue

    print("\n✅ 모든 폴더의 번호 정리가 완료되었습니다.")

if __name__ == "__main__":
    main()
