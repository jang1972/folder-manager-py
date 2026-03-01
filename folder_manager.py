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
import argparse
from datetime import datetime

# --- 1. 상수 및 설정 ---
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
""" # (공간상 일부 생략, 실제 코드에는 전체를 넣으시면 됩니다)

WINDOWS_RESERVED = ["CON", "PRN", "AUX", "NUL", "COM1", "LPT1"]
CREATE_KW = ['생성', '만들기', 'mk', 'make', 'mkdir']
DELETE_KW = ['삭제', '지우기', 'del', 'rm', 'rmdir', 'archive']
FILL_KW = ['fill', 'fillup', '채우기', '정리']

class FolderManager:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.current_os = self._check_os()
        self.folder_pattern = re.compile(r'^(\d+)\.(.*)$')

    def _check_os(self):
        if 'linux' in sys.platform: return 'Linux'
        if 'win32' in sys.platform: return 'Windows'
        if 'darwin' in sys.platform: return 'macOS'
        return 'Unknown'

    def log(self, message, emoji="➡️"):
        prefix = "🔍 [DRY-RUN]" if self.dry_run else emoji
        print(f"{prefix} {message}")

    def safe_execute(self, func, *args, **kwargs):
        """실제 작업을 수행하거나 드라이런 메시지를 출력하는 래퍼"""
        if self.dry_run:
            return True
        try:
            func(*args, **kwargs)
            return True
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return False

    def get_numbered_folders(self):
        numbered_folders = {}
        for entry in os.scandir('.'):
            if entry.is_dir():
                match = self.folder_pattern.match(entry.name)
                if match:
                    numbered_folders[int(match.group(1))] = entry.name
        return numbered_folders

    def create_folder(self, target_num, suffix):
        new_name = f"{target_num:02d}.{suffix}"
        if any(res in new_name.upper() for res in WINDOWS_RESERVED):
            print(f"❌ 오류: '{new_name}'은 예약어 포함으로 생성 불가.")
            return

        numbered_folders = self.get_numbered_folders()
        if target_num in numbered_folders:
            self.log(f"밀어내기 수행: {target_num}번 이상 폴더들의 번호를 +1 합니다.")
            for num in sorted(numbered_folders.keys(), reverse=True):
                if num >= target_num:
                    self.rename_folder(numbered_folders[num], num + 1)

        self.log(f"폴더 생성: {new_name}")
        self.safe_execute(os.makedirs, new_name)

    def archive_folder(self, target_num):
        numbered_folders = self.get_numbered_folders()
        if target_num not in numbered_folders:
            print(f"❌ 오류: {target_num:02d}번 폴더가 없습니다.")
            return

        folder_name = numbered_folders[target_num]
        archive_name = f"archived_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{folder_name}"

        self.log(f"폴더 아카이브: {folder_name} -> {archive_name}")
        if self.safe_execute(shutil.move, folder_name, archive_name):
            self.log(f"빈자리 채우기: {target_num}번 이후 폴더들의 번호를 -1 합니다.")
            for num in sorted(numbered_folders.keys()):
                if num > target_num:
                    self.rename_folder(numbered_folders[num], num - 1)

    def fill_gaps(self):
        self.log("빈 번호 채우기 정리 모드 진입")
        numbered_folders = self.get_numbered_folders()
        if not numbered_folders:
            print("❌ 정리할 폴더가 없습니다.")
            return

        for index, old_num in enumerate(sorted(numbered_folders.keys()), start=1):
            if old_num != index:
                self.rename_folder(numbered_folders[old_num], index)
        print("\n✅ 모든 정리 공정 완료.")

    def rename_folder(self, old_name, new_num):
        match = self.folder_pattern.match(old_name)
        if match:
            suffix = match.group(2)
            new_name = f"{new_num:02d}.{suffix}"
            self.log(f"이름 변경: {old_name} -> {new_name}", emoji="📝")
            self.safe_execute(os.rename, old_name, new_name)

def main():
    print(ASCII_ART)

    parser = argparse.ArgumentParser(description="Michelle's Professional Folder Manager")
    parser.add_argument("mode", help="작업 모드 (make, rm, fill 등)")
    parser.add_argument("number", type=int, nargs='?', help="대상 폴더 번호")
    parser.add_argument("name", nargs='?', default="새폴더", help="폴더 이름 (생성 시)")
    parser.add_argument("--dry-run", action="store_true", help="실제 변경 없이 시뮬레이션 수행")

    args = parser.parse_args()

    fm = FolderManager(dry_run=args.dry_run)
    mode = args.mode.lower()

    if args.dry_run:
        print("⚠️  [DRY-RUN MODE] 실제 파일 변경이 일어나지 않습니다.\n")

    if mode in CREATE_KW:
        if args.number is None:
            print("❌ 오류: 생성할 폴더 번호가 필요합니다.")
            return
        fm.create_folder(args.number, args.name)
    elif mode in DELETE_KW:
        if args.number is None:
            print("❌ 오류: 삭제할 폴더 번호가 필요합니다.")
            return
        fm.archive_folder(args.number)
    elif mode in FILL_KW:
        fm.fill_gaps()
    else:
        print(f"❌ 알 수 없는 모드: {mode}")

if __name__ == "__main__":
    main()
