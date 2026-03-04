#!/usr/bin/env python3
# 리눅서일시 sudo ln -s "$(pwd)/folder_manager.py" /usr/local/bin/fm'을 권장합니다.
# Made by Michelle
# With Gemini
# Edit Tool is VSC, Kate
# 번호 기반 폴더 관리 및 자동 정렬 도구 (Folder Manager)
# A number-based folder management and auto-alignment tool.
# Copyright (C) 2026 Michelle (jang1972)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import re
import shutil
import argparse
import json
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
"""

ARCHIVE_FOLDER_NAME = "Archive"
MAX_FOLDER_NUMBER = 99
HISTORY_FILE = ".fm_history.json"
WINDOWS_RESERVED = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "LPT1", "LPT2"]
FORBIDDEN_CHARS = re.compile(r'[\\/:*?"<>|]')

CREATE_KW = ['생성', '만들기', 'mk', 'make', 'mkdir']
DELETE_KW = ['삭제', '지우기', 'del', 'rm', 'rmdir', 'archive']
FILL_KW = ['fill', 'fillup', '채우기', '정리']
ROLLBACK_KW = ['rollback', 'undo', '되돌리기']

class FolderManager:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.folder_pattern = re.compile(r'^(\d+)\_(.*)$')
        self.history = []

    def log(self, message, emoji="➡️"):
        prefix = "🔍 [DRY-RUN]" if self.dry_run else emoji
        print(f"{prefix} {message}")

    def safe_execute(self, func, *args, **kwargs):
        if self.dry_run: return True
        try:
            func(*args, **kwargs)
            return True
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return False

    def is_valid_suffix(self, suffix):
        if FORBIDDEN_CHARS.search(suffix):
            print(f"❌ 오류: 금지 문자(\\ / : * ? \" < > |)가 포함되어 있습니다.")
            return False
        if any(res == suffix.upper() or suffix.upper().startswith(res + ".") for res in WINDOWS_RESERVED):
            print(f"❌ 오류: '{suffix}'은(는) 시스템 예약어입니다.")
            return False
        return True

    def save_history(self, mode):
        if self.dry_run or not self.history: return
        data = {"mode": mode, "changes": self.history, "timestamp": str(datetime.now())}
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_history(self, old, new):
        self.history.append({"old": old, "new": new})

    def get_numbered_folders(self):
        folders = {}
        for entry in os.scandir('.'):
            if entry.is_dir() and entry.name != ARCHIVE_FOLDER_NAME:
                match = self.folder_pattern.match(entry.name)
                if match: folders[int(match.group(1))] = entry.name
        return folders

    def rename_folder(self, old_name, new_num):
        if not (1 <= new_num <= MAX_FOLDER_NUMBER): return
        match = self.folder_pattern.match(old_name)
        if match:
            new_name = f"{new_num:02d}_{match.group(2)}"
            if old_name == new_name: return
            self.log(f"이름 변경: {old_name} -> {new_name}", emoji="📝")
            if self.safe_execute(os.rename, old_name, new_name):
                self.add_history(old_name, new_name)

    def handle_archive_collision(self, archive_path, target_name):
        """레거시 스타일: 아카이브 내 충돌 시 기존 폴더를 old_로 변경"""
        dest_path = os.path.join(archive_path, target_name)
        if os.path.exists(dest_path):
            old_name = f"old_{target_name}"
            old_path = os.path.join(archive_path, old_name)
            if os.path.exists(old_path):
                # 2차 충돌 시 타임스탬프 처리
                ts_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{old_name}"
                self.log(f"아카이브 내 중복 해결: {old_name} -> {ts_name}", emoji="♻️")
                self.safe_execute(shutil.move, old_path, os.path.join(archive_path, ts_name))

            self.log(f"아카이브 내 중복 해결: {target_name} -> {old_name}", emoji="♻️")
            self.safe_execute(shutil.move, dest_path, old_path)
        return True

    def create_folder(self, target_num, suffix):
        if not (1 <= target_num <= MAX_FOLDER_NUMBER) or not self.is_valid_suffix(suffix): return
        new_name = f"{target_num:02d}_{suffix}"
        folders = self.get_numbered_folders()

        if target_num in folders:
            if max(folders.keys()) + 1 > MAX_FOLDER_NUMBER:
                print("❌ 오류: 99번을 초과하게 되어 밀어내기가 불가능합니다.")
                return
            for num in sorted(folders.keys(), reverse=True):
                if num >= target_num: self.rename_folder(folders[num], num + 1)

        self.log(f"폴더 생성: {new_name}")
        if self.safe_execute(os.makedirs, new_name):
            self.add_history(None, new_name)
            self.save_history("create")

    def archive_folder(self, target_num):
        folders = self.get_numbered_folders()
        
        # 1. 대상 폴더가 없는 경우에 대한 경고 문구 추가
        if target_num not in folders:
            print(f"⚠️ 경고: {target_num:02d}번 폴더를 찾을 수 없습니다. (작업 취소)")
            return

        target_name = folders[target_num]
        archive_path = os.path.join(os.getcwd(), ARCHIVE_FOLDER_NAME)

        if not self.dry_run:
            if not os.path.exists(archive_path):
                os.makedirs(archive_path)
            self.handle_archive_collision(archive_path, target_name)

        dest_path = os.path.join(archive_path, target_name)
        self.log(f"아카이브 이동: {target_name} -> {ARCHIVE_FOLDER_NAME}/")
        
        if self.safe_execute(shutil.move, target_name, dest_path):
            self.add_history(target_name, dest_path)
            for num in sorted(folders.keys()):
                if num > target_num:
                    self.rename_folder(folders[num], num - 1)
            self.save_history("archive")

    def fill_gaps(self):
        folders = self.get_numbered_folders()
        for i, old_num in enumerate(sorted(folders.keys()), 1):
            self.rename_folder(folders[old_num], i)
        self.save_history("fill")
        print("✅ 빈자리 채우기 완료.")

    def rollback(self):
        if not os.path.exists(HISTORY_FILE):
            print("❌ 오류: 되돌릴 작업 이력이 없습니다.")
            return

        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        changes = data["changes"]
        self.log(f"롤백 시작: {data['mode']} 작업을 되돌립니다.")

        # 유효성 검사 (사용자 임의 파일 투입 감지)
        for item in changes:
            curr = item["new"]
            if curr and os.path.exists(curr):
                if item["old"] is None and os.listdir(curr): # mk 작업 취소 시 폴더가 안 비어있으면
                    print(f"❌ 롤백 불가: '{curr}' 폴더 내부에 사용자가 추가한 파일이 있습니다. 수동 조치하세요.")
                    return
            elif curr and not os.path.exists(curr):
                print(f"❌ 롤백 불가: 대상 폴더 '{curr}'가 사라졌습니다.")
                return

        for item in reversed(changes):
            old, new = item["old"], item["new"]
            if old is None: # mk 취소
                self.log(f"삭제(취소): {new}")
                self.safe_execute(os.rmdir, new)
            else: # rename/archive 취소
                self.log(f"복구: {new} -> {old}")
                self.safe_execute(shutil.move, new, old)

        os.remove(HISTORY_FILE)
        print("✅ 롤백 완료.")

def main():
    print(ASCII_ART)
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="mk, rm, fill, rollback")
    parser.add_argument("number", type=int, nargs='?', help="번호")
    parser.add_argument("name", nargs='?', default="새폴더", help="이름")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    fm = FolderManager(dry_run=args.dry_run)
    mode = args.mode.lower()

    if mode in CREATE_KW: fm.create_folder(args.number, args.name)
    elif mode in DELETE_KW: fm.archive_folder(args.number)
    elif mode in FILL_KW: fm.fill_gaps()
    elif mode in ROLLBACK_KW: fm.rollback()
    else: print(f"❌ 알 수 없는 모드: {mode}")

if __name__ == "__main__":
    main()
