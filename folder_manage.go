// Made by Michelle
// With Gemini
// Edit Tool is Kate
// 리눅서일시 sudo ln -s "$(pwd)/folder_manager" /usr/local/bin/fm'을 권장합니다.
// 번호 기반 폴더 관리 및 자동 정렬 도구 (Folder Manager)
// Copyright (C) 2026 Michelle (jang1972)
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"time"
)

const (
	ASCII_ART      = `
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
	`
	ARCHIVE_DIR    = "Archive"
	MAX_FOLDER_NUM = 99
	HISTORY_FILE   = ".fm_history.json"
)

var (
	folderPattern   = regexp.MustCompile(`^(\d{2})_(.*)$`)
	forbiddenChars  = regexp.MustCompile(`[\\/:*?"<>|]`)
		windowsReserved = []string{"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "LPT1", "LPT2"}
)

type HistoryItem struct {
	Old string `json:"old"`
	New string `json:"new"`
}

type HistoryData struct {
	Mode      string        `json:"mode"`
	Changes   []HistoryItem `json:"changes"`
	Timestamp string        `json:"timestamp"`
}

type FolderManager struct {
	DryRun  bool
	History []HistoryItem
}

func (fm *FolderManager) Log(msg, emoji string) {
	prefix := "➡️"
	if fm.DryRun {
		prefix = "🔍 [DRY-RUN]"
	} else if emoji != "" {
		prefix = emoji
	}
	fmt.Printf("%s %s\n", prefix, msg)
}

func (fm *FolderManager) GetNumberedFolders() map[int]string {
	folders := make(map[int]string)
	files, _ := os.ReadDir(".")
	for _, f := range files {
		if f.IsDir() && f.Name() != ARCHIVE_DIR {
			match := folderPattern.FindStringSubmatch(f.Name())
			if match != nil {
				num, _ := strconv.Atoi(match[1])
				folders[num] = f.Name()
			}
		}
	}
	return folders
}

func (fm *FolderManager) SaveHistory(mode string) {
	if fm.DryRun || len(fm.History) == 0 {
		return
	}
	data := HistoryData{Mode: mode, Changes: fm.History, Timestamp: time.Now().String()}
	file, _ := json.MarshalIndent(data, "", "  ")
	_ = os.WriteFile(HISTORY_FILE, file, 0644)
}

func (fm *FolderManager) CreateFolder(targetNum int, suffix string) {
	if targetNum < 1 || targetNum > MAX_FOLDER_NUM {
		return
	}
	folders := fm.GetNumberedFolders()
	if _, exists := folders[targetNum]; exists {
		for i := MAX_FOLDER_NUM; i >= targetNum; i-- {
			if name, ok := folders[i]; ok {
				fm.RenameFolder(name, i+1)
			}
		}
	}
	newName := fmt.Sprintf("%02d_%s", targetNum, suffix)
	fm.Log("폴더 생성: "+newName, "📁")
	if !fm.DryRun {
		os.Mkdir(newName, 0755)
		fm.History = append(fm.History, HistoryItem{Old: "", New: newName})
		fm.SaveHistory("create")
	}
}

func (fm *FolderManager) RenameFolder(oldName string, newNum int) {
	match := folderPattern.FindStringSubmatch(oldName)
	newName := fmt.Sprintf("%02d_%s", newNum, match[2])
	fm.Log(fmt.Sprintf("이름 변경: %s -> %s", oldName, newName), "📝")
	if !fm.DryRun {
		os.Rename(oldName, newName)
		fm.History = append(fm.History, HistoryItem{Old: oldName, New: newName})
	}
}

func (fm *FolderManager) ArchiveFolder(targetNum int) {
	folders := fm.GetNumberedFolders()
	targetName, exists := folders[targetNum]
	if !exists {
		fmt.Printf("⚠️ 경고: %02d번 폴더를 찾을 수 없습니다.\n", targetNum)
		return
	}

	if !fm.DryRun {
		os.MkdirAll(ARCHIVE_DIR, 0755)
		dest := filepath.Join(ARCHIVE_DIR, targetName)

		// [충돌 방지] 아카이브 내 동일 이름 존재 시 처리
		if _, err := os.Stat(dest); err == nil {
			oldName := "old_" + targetName
			oldPath := filepath.Join(ARCHIVE_DIR, oldName)
			if _, err = os.Stat(oldPath); err == nil {
				ts := time.Now().Format("20060102150405")
				oldPath = filepath.Join(ARCHIVE_DIR, ts+"_"+oldName)
				fm.Log("충돌 발생: 타임스탬프 적용 -> "+oldPath, "⚠️")
			} else {
				fm.Log("충돌 발생: '_old' 폴더로 이름 변경 -> "+oldName, "⚠️")
			}
			os.Rename(dest, oldPath)
		}

		// 1. 대상 폴더를 아카이브로 이동
		os.Rename(targetName, dest)
		fm.Log("아카이브 이동: "+targetName, "♻️")
		fm.History = append(fm.History, HistoryItem{Old: targetName, New: dest})

		// 2. [덮어쓰기 방지] 나머지 폴더들 번호 당기기
		// targetNum보다 큰 번호들을 오름차순(1, 2, 3...)으로 정렬하여 앞에서부터 하나씩 당깁니다.
		keys := []int{}
		for k := range folders {
			if k > targetNum {
				keys = append(keys, k)
			}
		}
		sort.Ints(keys) // 오름차순 정렬: 03->02, 04->03 순서로 안전하게 변경

		for _, num := range keys {
			fm.RenameFolder(folders[num], num-1)
		}

		fm.SaveHistory("archive")
	}
}

func (fm *FolderManager) FillGaps() {
	folders := fm.GetNumberedFolders()
	keys := []int{}
	for k := range folders { keys = append(keys, k) }
	sort.Ints(keys)
	for i, k := range keys {
		if k != i+1 {
			fm.RenameFolder(folders[k], i+1)
		}
	}
	fm.SaveHistory("fill")
}

func (fm *FolderManager) Rollback() {
	// 1. 이력 파일 읽기
	data, err := os.ReadFile(HISTORY_FILE)
	if err != nil {
		fmt.Println("❌ 이력 없음")
		return
	}
	var history HistoryData
	json.Unmarshal(data, &history)

	// 2. [안전 검사] 롤백 실행 전, 각 폴더가 비어있는지 확인
	for _, item := range history.Changes {
		if item.New != "" {
			entries, err := os.ReadDir(item.New)
			if err == nil && len(entries) > 0 {
				fmt.Printf("❌ 롤백 취소: '%s' 폴더 내부에 파일이 있습니다 (수동 조치 필요)\n", item.New)
				return
			}
		}
	}

	// 3. [실행] 검사를 통과했으므로 역순으로 복구 작업 실행
	fm.Log(fmt.Sprintf("%s 작업을 되돌립니다.", history.Mode), "🔄")
	for i := len(history.Changes) - 1; i >= 0; i-- {
		item := history.Changes[i]
		if item.Old == "" {
			fm.Log("삭제(취소): "+item.New, "🗑️")
			os.Remove(item.New)
		} else {
			fm.Log(fmt.Sprintf("복구: %s -> %s", item.New, item.Old), "↩️")
			os.Rename(item.New, item.Old)
		}
	}

	os.Remove(HISTORY_FILE)
	fmt.Println("✅ 롤백 완료.")
}

func main() {
	fmt.Println(ASCII_ART)
	dryRun := flag.Bool("dry-run", false, "시뮬레이션")
	flag.Parse()
	args := flag.Args()
	if len(args) < 1 { return }
	fm := &FolderManager{DryRun: *dryRun}

	switch args[0] {
		case "mk", "mkdir", "make", "생성", "만들기":
			if len(args) < 2 { // 번호만 필수 확인
				fmt.Println("❌ 오류: 번호를 입력하세요.")
				return
			}

			// 이름 기본값 설정 로직
			name := "새폴더"
			if len(args) >= 3 {
				name = args[2]
			}

			num, err := strconv.Atoi(args[1]) // 여기서 err 선언 (첫 번째 사용)
			if err != nil {
				fmt.Println("❌ 오류: 번호는 숫자여야 합니다.")
				return
			}
			fm.CreateFolder(num, name)

		case "rm", "rmdir", "del", "삭제", "지우기", "archive":
			if len(args) < 2 {
				fmt.Println("❌ 오류: 번호를 입력하세요.")
				return
			}

			num, err := strconv.Atoi(args[1]) // 여기서도 err 선언
			if err != nil {
				fmt.Println("❌ 오류: 번호는 숫자여야 합니다.")
				return
			}
			fm.ArchiveFolder(num)

		case "fill", "채우기":
			fm.FillGaps()

		case "rollback", "undo", "되돌리기":
			fm.Rollback()

		default:
			fmt.Println("❌ 알 수 없는 모드입니다.")
	}
}
