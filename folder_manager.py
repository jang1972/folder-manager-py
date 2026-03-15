#!/usr/bin/env python3
# 리눅서일시 sudo ln -s "$(pwd)/folder_manager.py" /usr/local/bin/fm'을 권장합니다.
# Dry-run 기능 추가 및 01-99 제한/금지문자 필터링 버전
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
# [Notice] By contributing to this project, you agree to transfer 
# copyright or grant relicensing rights to the author. 
# The project will remain 'Free of Charge' and 'Open Source'.

import re
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path

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

# --- 1. 전역 설정 및 키워드 (오류 해결 지점) ---
ARCHIVE_FOLDER_NAME = "Archive"
MAX_FOLDER_NUMBER = 99
HISTORY_FILE = Path(".fm_history.json")
WINDOWS_RESERVED = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "LPT1", "LPT2"}
FORBIDDEN_CHARS = re.compile(r'[\\/:*?"<>|]')

# 명령어 별칭 정의
CREATE_KW = ['mk', 'new', 'create', 'n']
REMOVE_KW = ['rm', 'del', 'archive', 'a']
FILL_KW   = ['fill', 'f', 'reorder']
ROLLBACK_KW = ['rb', 'undo', 'rollback']

class FolderManager:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.folder_pattern = re.compile(r'^(\d+)\_(.*)$')
        self.history = []
        self.cwd = Path.cwd()

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
            print("❌ 오류: 금지 문자(\\ / : * ? \" < > |)가 포함되어 있습니다.")
            return False
        if suffix.upper() in WINDOWS_RESERVED:
            print(f"❌ 오류: '{suffix}'은(는) 시스템 예약어입니다.")
            return False
        return True

    def save_history(self, mode):
        if self.dry_run or not self.history: return
        data = {
            "mode": mode,
            "changes": self.history,
            "timestamp": datetime.now().isoformat()
        }
        # pathlib의 write_text로 간결하게 저장
        HISTORY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def add_history(self, old, new):
        self.history.append({
            "old": str(old) if old else None,
            "new": str(new) if new else None
        })

    def get_numbered_folders(self):
        """현재 디렉토리의 번호가 매겨진 폴더들을 Path 객체 딕셔너리로 반환"""
        folders = {}
        for path in self.cwd.iterdir():
            if path.is_dir() and path.name != ARCHIVE_FOLDER_NAME:
                match = self.folder_pattern.match(path.name)
                if match:
                    folders[int(match.group(1))] = path
        return folders

    def rename_folder(self, old_path, new_num):
        if not (1 <= new_num <= MAX_FOLDER_NUMBER): return
        match = self.folder_pattern.match(old_path.name)
        if match:
            new_name = f"{new_num:02d}_{match.group(2)}"
            new_path = old_path.with_name(new_name) # 같은 부모 내에서 이름만 교체
            if old_path == new_path: return

            self.log(f"이름 변경: {old_path.name} -> {new_name}", emoji="📝")
            if self.safe_execute(old_path.rename, new_path):
                self.add_history(old_path, new_path)

    def create_folder(self, target_num, suffix):
        if target_num is None:
            print("❌ 오류: 번호가 필요합니다. (예: fm mk 1 '폴더명')")
            return
        if not (1 <= target_num <= MAX_FOLDER_NUMBER) or not self.is_valid_suffix(suffix): return

        folders = self.get_numbered_folders()
        if target_num in folders:
            # 밀어내기 로직
            if max(folders.keys(), default=0) + 1 > MAX_FOLDER_NUMBER:
                print("❌ 오류: 99번을 초과하여 폴더를 밀어낼 수 없습니다.")
                return
            for num in sorted(folders.keys(), reverse=True):
                if num >= target_num:
                    self.rename_folder(folders[num], num + 1)

        new_path = self.cwd / f"{target_num:02d}_{suffix}"
        self.log(f"폴더 생성: {new_path.name}")
        if self.safe_execute(new_path.mkdir, parents=True):
            self.add_history(None, new_path)
            self.save_history("create")

  def archive_folder(self, target_num):
        if target_num is None: return
        folders = self.get_numbered_folders()
        
        # 1. 대상 폴더 존재 확인 (안전장치)
        if target_num not in folders:
            print(f"⚠️ 경고: {target_num:02d}번 폴더를 찾을 수 없습니다. (작업 취소)")
            return

        target_path = folders[target_num]
        archive_dir = self.cwd / ARCHIVE_FOLDER_NAME
        dest_path = archive_dir / target_path.name

        # 2. 아카이브 내 충돌 해결 (Dry-run이 아닐 때만 실제 수행)
        if not self.dry_run:
            archive_dir.mkdir(exist_ok=True) # 아카이브 폴더 자동 생성
            
            if dest_path.exists():
                backup_path = archive_dir / f"old_{target_path.name}"
                
                # 2차 충돌 (old_... 도 이미 있을 때) -> 타임스탬프 처리
                if backup_path.exists():
                    ts = datetime.now().strftime('%Y%m%d%H%M%S')
                    timestamped_path = archive_dir / f"{ts}_{backup_path.name}"
                    self.log(f"아카이브 내 중복 해결: {backup_path.name} -> {timestamped_path.name}", emoji="♻️")
                    backup_path.rename(timestamped_path)

                # 기존 파일을 old_로 밀어내기
                self.log(f"아카이브 내 중복 해결: {dest_path.name} -> {backup_path.name}", emoji="♻️")
                dest_path.rename(backup_path)

        # 3. 실제 이동 수행
        self.log(f"아카이브 이동: {target_path.name} -> {ARCHIVE_FOLDER_NAME}/", emoji="📦")
        
        # shutil.move는 Path 객체를 직접 인자로 받을 수 있습니다 (Python 3.6+)
        if self.safe_execute(shutil.move, target_path, dest_path):
            self.add_history(target_path, dest_path)
            
            # 4. 번호 당기기 로직 (오름차순 정렬 후 처리)
            for num in sorted(folders.keys()):
                if num > target_num:
                    self.rename_folder(folders[num], num - 1)
            
            self.save_history("archive")
        if self.safe_execute(shutil.move, str(target_path), str(dest_path)):
            self.add_history(target_path, dest_path)
            # 빈자리 당기기
            for num in sorted(folders.keys()):
                if num > target_num:
                    self.rename_folder(folders[num], num - 1)
            self.save_history("archive")

    def fill_gaps(self):
        folders = self.get_numbered_folders()
        if not folders: return
        for i, old_num in enumerate(sorted(folders.keys()), 1):
            self.rename_folder(folders[old_num], i)
        self.save_history("fill")
        print("✅ 빈자리 채우기 완료.")

    def rollback(self):
        if not HISTORY_FILE.exists():
            print("❌ 오류: 되돌릴 작업 이력이 없습니다.")
            return

        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        changes = data["changes"]

        # 유효성 검사 (Path 객체 활용)
        for item in changes:
            curr = Path(item["new"]) if item["new"] else None
            if curr and curr.exists():
                if item["old"] is None and any(curr.iterdir()):
                    print(f"❌ 롤백 불가: '{curr.name}' 폴더가 비어있지 않습니다.")
                    return
            elif curr and not curr.exists():
                print(f"❌ 롤백 불가: 대상 '{curr.name}'가 사라졌습니다.")
                return

        for item in reversed(changes):
            old_p = Path(item["old"]) if item["old"] else None
            new_p = Path(item["new"]) if item["new"] else None

            if old_p is None: # mk 취소 -> 삭제
                self.log(f"삭제(취소): {new_p.name}")
                self.safe_execute(new_p.rmdir)
            else: # rename/archive 취소 -> 복구
                self.log(f"복구: {new_p.name} -> {old_p.name}")
                self.safe_execute(shutil.move, str(new_p), str(old_p))

        if not self.dry_run: HISTORY_FILE.unlink()
        print("✅ 롤백 완료.")

def main():
    print(ASCII_ART)

    parser = argparse.ArgumentParser(description="Pathlib 기반 폴더 관리자")
    parser.add_argument("mode", help="명령어 (mk, rm, fill, rb)")
    parser.add_argument("number", type=int, nargs='?', help="폴더 번호")
    parser.add_argument("name", nargs='?', default="새폴더", help="폴더 접미사")
    parser.add_argument("--dry-run", action="store_true", help="가상 실행")
    args = parser.parse_args()

    fm = FolderManager(dry_run=args.dry_run)
    mode = args.mode.lower()

    if mode in CREATE_KW:
        fm.create_folder(args.number, args.name)
    elif mode in REMOVE_KW:
        fm.archive_folder(args.number)
    elif mode in FILL_KW:
        fm.fill_gaps()
    elif mode in ROLLBACK_KW:
        fm.rollback()
    else:
        print(f"❓ 알 수 없는 명령입니다: {mode}")

if __name__ == "__main__":
    main()
