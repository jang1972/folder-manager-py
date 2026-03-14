#!/usr/bin/env python3
# 리눅서일시 sudo ln -s "$(pwd)/folder_manager.py" /usr/local/bin/fm 또는 mkdir -p ~/.local/bin 후 ln -s "$(pwd)/folder_manager.py" ~/.local/bin/fm을 권장합니다.
# Dry-run, 01-99 제한, 롤백 및 경로 안전 검사 추가 버전
# Made by Michelle | With Gemini | 2026
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

# 키워드 그룹화
CREATE_KW = ['생성', '만들기', 'mk', 'make', 'mkdir']
DELETE_KW = ['삭제', '지우기', 'del', 'rm', 'rmdir', 'archive']
FILL_KW = ['fill', 'fillup', '채우기', '정리']
ROLLBACK_KW = ['rollback', 'undo', '되돌리기']
CLEAR_KW = ['clear', 'reset', '비우기', '초기화']

# --- 2. 로직 클래스 ---
class FolderManager:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.folder_pattern = re.compile(r'^(\d+)\_(.*)$')
        self.history = []
        self._check_path_safety()

    def _check_path_safety(self):
        """민감한 시스템 경로에서의 실행 방지"""
        curr_path = os.path.abspath(os.getcwd())
        # 루트 디렉토리 방지
        if curr_path == os.path.abspath(os.sep):
            sys.exit("❌ 위험: 루트 디렉토리에서 작업을 수행할 수 없습니다.")

        # 시스템 핵심 경로 키워드 차단
        sensitive_dirs = ['C:\\Windows', 'C:\\Program Files', '/etc', '/usr', '/bin', '/sbin']
        for sd in sensitive_dirs:
            if curr_path.startswith(sd):
                sys.exit(f"❌ 위험: 시스템 경로({sd}) 내에서 작업을 수행할 수 없습니다.")

    def safe_path_check(self, path):
        """경로가 현재 디렉토리 또는 아카이브 폴더 내에 있는지 검증 (인젝션 방어)"""
        if path is None: return True
        abs_base = os.path.abspath(os.getcwd())
        abs_target = os.path.abspath(path)
        # 대상 경로가 현재 작업 디렉토리의 하위 경로로 시작하는지 확인
        return abs_target.startswith(abs_base)

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
        if os.path.sep in suffix or (os.path.altsep and os.path.altsep in suffix):
            print("❌ 오류: 이름에 경로 구분자가 포함될 수 없습니다.")
            return False
        if FORBIDDEN_CHARS.search(suffix):
            print(f"❌ 오류: 금지 문자(\\ / : * ? \" < > |)가 포함되어 있습니다.")
            return False
        if any(res == suffix.upper() or suffix.upper().startswith(res + ".") for res in WINDOWS_RESERVED):
            print(f"❌ 오류: '{suffix}'은(는) 시스템 예약어입니다.")
            return False
        return True

    def save_history(self, mode):
        if self.dry_run or not self.history: return
        stack = []
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    stack = json.load(f)
                    if not isinstance(stack, list): stack = []
            except Exception:
                stack = []

        # 새 작업 추가 및 JSON 구조 완성
        data = {
            "mode": mode,
            "changes": self.history,
            "timestamp": datetime.now().strftime('%Y%m%d%H%M%S')
        }
        stack.append(data)

        # 안전한 직렬화: utf-8 명시 및 인젝션 방지를 위한 인자 설정
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(stack, f, ensure_ascii=False, indent=2)

        # 권한 제한 (600)
        if os.name == 'posix':
            try:
                os.chmod(HISTORY_FILE, 0o600)
            except Exception:
                pass

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
        safe_name = os.path.basename(target_name)
        dest_path = os.path.join(archive_path, safe_name)
        if os.path.exists(dest_path):
            old_name = f"old_{safe_name}"
            old_path = os.path.join(archive_path, old_name)
            if os.path.exists(old_path):
                ts_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{safe_name}"
                self.log(f"아카이브 내 중복 해결: {safe_name} -> {ts_name}", emoji="♻️")
                self.safe_execute(shutil.move, old_path, os.path.join(archive_path, ts_name))
            self.log(f"아카이브 내 중복 해결: {target_name} -> {safe_name}", emoji="♻️")
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
        if self.safe_execute(os.makedirs, new_name, exist_ok=False):
            self.add_history(None, new_name)
            self.save_history("create")
        else:
            print(f"❌ 오류: '{new_name}' 폴더를 생성하지 못했습니다.")

    def archive_folder(self, target_num):
        folders = self.get_numbered_folders()
        if target_num not in folders:
            print(f"⚠️ 경고: {target_num:02d}번 폴더를 찾을 수 없습니다.")
            return

        target_name = folders[target_num]
        archive_path = os.path.join(os.getcwd(), ARCHIVE_FOLDER_NAME)

        if not self.dry_run:
            if not os.path.exists(archive_path): os.makedirs(archive_path)
            self.handle_archive_collision(archive_path, target_name)

        dest_path = os.path.join(archive_path, target_name)
        self.log(f"아카이브 이동: {target_name} -> {ARCHIVE_FOLDER_NAME}/")

        if self.safe_execute(shutil.move, target_name, dest_path):
            self.add_history(target_name, dest_path)
            for num in sorted(folders.keys()):
                if num > target_num: self.rename_folder(folders[num], num - 1)
            self.save_history("archive")

    def fill_gaps(self):
        folders = self.get_numbered_folders()
        if not folders:
            print("❌ 정리할 폴더가 없습니다.")
            return
        for i, old_num in enumerate(sorted(folders.keys()), 1):
            self.rename_folder(folders[old_num], i)
        self.save_history("fill")
        print("✅ 빈자리 채우기 완료.")

    def rollback(self):
        if not os.path.exists(HISTORY_FILE):
            print("❌ 오류: 되돌릴 작업 이력이 없습니다.")
            return

        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                stack = json.load(f)
            
            if not stack or not isinstance(stack, list):
                print("❌ 오류: 기록이 비어있거나 유효하지 않습니다.")
                return
        except (json.JSONDecodeError, ValueError):
            print("❌ 오류: 로그 파일이 손상되었습니다.")
            return

        # 마지막 작업(Top) 꺼내기
        last_action = stack.pop()
        mode = last_action.get("mode", "알 수 없음")
        timestamp = last_action.get("timestamp", "N/A")
        changes = last_action.get("changes", [])

        self.log(f"롤백 시작: {mode} ({timestamp})", emoji="🔄")

        # 1. 사전 검증 (모든 변경 대상이 존재하는지 확인)
        for item in changes:
            # 1-1. 구조 검증
            if not all(k in item for k in ("old", "new")):
                print("❌ 오류: 유효하지 않은 히스토리 항목입니다.")
                return

            curr, old = item["new"], item["old"] # 변수 정의

            # 1-2. 경로 인젝션 검증 (핵심 보안)
            if not self.safe_path_check(curr) or not self.safe_path_check(old):
                print(f"❌ 보안 경고: 허용되지 않은 경로가 로그에서 감지되었습니다.")
                return

            # 1-3. 상태 검증
            if curr and os.path.exists(curr):
                if old is None and os.path.isdir(curr) and os.listdir(curr):
                    print(f"❌ 롤백 불가: '{curr}' 내부에 파일이 존재합니다.")
                    return
            elif curr and not os.path.exists(curr):
                print(f"❌ 롤백 불가: 대상 '{curr}'를 찾을 수 없습니다.")
                return

        # 2. 실제 실행 (역순으로 수행)
        for item in reversed(changes):
            old, new = item["old"], item["new"]
            if old is None: # 생성 취소
                self.log(f"삭제(취소): {new}", emoji="🗑️")
                self.safe_execute(os.rmdir, new)
            else: # 이름 변경/아카이브 취소
                self.log(f"복구: {new} -> {old}", emoji="↩️")
                self.safe_execute(shutil.move, new, old)

        # 3. 남은 스택 업데이트
        if stack:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(stack, f, ensure_ascii=False, indent=2)
        else:
            os.remove(HISTORY_FILE)
            
        print(f"✅ [{mode}] 작업 롤백 완료. (남은 기록: {len(stack)}개)")

    def clear_history(self):
        if os.path.exists(HISTORY_FILE):
            if self.dry_run:
                self.log("기록 삭제 시뮬레이션", emoji="🔍")
            else:
                os.remove(HISTORY_FILE)
                print("✅ 모든 작업 이력이 삭제되었습니다. (롤백 불가)")
        else:
            print("💡 삭제할 이력이 없습니다.")

# --- 3. 실행 인터페이스 ---
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--license":
        print("\nThis program is free software under GNU GPL v3.")
        print("See <https://www.gnu.org/licenses/> for details.")
        return

    print(ASCII_ART)
    parser = argparse.ArgumentParser(
        description="Michelle's Professional Folder Manager (FM)",
        epilog="예시: fm mk 1 프로젝트 | fm rm 5 | fm fill | fm rollback | fm clear |  fm --license",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("mode", help="작업 모드: mk (생성), rm (삭제), fill (정렬), rollback (되돌리기), clear (기록 삭제)")
    parser.add_argument("number", type=int, nargs='?', help="대상 폴더 번호 (1-99)")
    parser.add_argument("name", nargs='?', default="새폴더", help="폴더 이름 (생성 시 사용)")
    parser.add_argument("--dry-run", action="store_true", help="실제 변경 없이 시뮬레이션만 수행")

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()
    fm = FolderManager(dry_run=args.dry_run)
    mode = args.mode.lower()

    if args.dry_run:
        print("⚠️ [DRY-RUN] 시뮬레이션 모드입니다. 파일 시스템에 영향을 주지 않습니다.\n")

    try:
        if mode in CREATE_KW:
            if args.number is None: raise ValueError("번호가 필요합니다.")
            fm.create_folder(args.number, args.name)
        elif mode in DELETE_KW:
            if args.number is None: raise ValueError("번호가 필요합니다.")
            fm.archive_folder(args.number)
        elif mode in FILL_KW:
            fm.fill_gaps()
        elif mode in ROLLBACK_KW:
            fm.rollback()
        elif mode in CLEAR_KW:
            fm.clear_history()
        else:
            print(f"❌ 알 수 없는 모드: {mode}")
    except ValueError as e:
        print(f"❌ 입력 오류: {e}")

if __name__ == "__main__":
    main()
