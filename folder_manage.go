// Made by Michelle
// With Gemini
// Edit Tool is Kate
// 리눅서일시 sudo ln -s "$(pwd)/folder_manager.py" /usr/local/bin/fm 또는 mkdir -p ~/.local/bin 후 ln -s "$(pwd)/folder_manager.py" ~/.local/bin/fm을 권장합니다.
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
	"strings"
	"time"
)

// --- 1. 상수 및 설정 ---
const (
	ASCII_ART = `
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
	TIME_FORMAT    = "20060102150405"
)

var (
	folderPattern  = regexp.MustCompile(`^(\d{2})_(.*)$`)
	forbiddenChars = regexp.MustCompile(`[\\/:*?"<>|]`)
		// 시스템 민감 경로 키워드
		sensitivePaths = []string{"/etc", "/usr", "/bin", "/sbin", "C:\\Windows", "C:\\Program Files"}
)

// --- 2. 데이터 구조 ---
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

// --- 3. 핵심 로직 메서드 ---

// 경로 안전성 검사 (추가된 기능 3)
func (fm *FolderManager) CheckPathSafety() {
	currPath, err := os.Getwd()
	if err != nil {
		fmt.Println("❌ 오류: 현재 경로를 가져올 수 없습니다.")
		os.Exit(1)
	}

	// 1. 루트 디렉토리 검사
	if currPath == filepath.Clean(string(os.PathSeparator)) || currPath == "C:\\" {
		fmt.Println("❌ 위험: 루트 디렉토리에서 작업을 수행할 수 없습니다.")
		os.Exit(1)
	}

	// 2. 민감 디렉토리 검사
	for _, sp := range sensitivePaths {
		if strings.HasPrefix(strings.ToLower(currPath), strings.ToLower(sp)) {
			fmt.Printf("❌ 위험: 시스템 경로(%s) 내에서 작업을 수행할 수 없습니다.\n", sp)
			os.Exit(1)
		}
	}
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
	data := HistoryData{
		Mode:      mode,
		Changes:   fm.History,
		Timestamp: time.Now().Format(TIME_FORMAT),
	}
	file, _ := json.MarshalIndent(data, "", "  ")
	_ = os.WriteFile(HISTORY_FILE, file, 0644)
}

func (fm *FolderManager) CreateFolder(targetNum int, suffix string) {
	if targetNum < 1 || targetNum > MAX_FOLDER_NUM {
		fmt.Println("❌ 오류: 번호는 01~99 사이여야 합니다.")
		return
	}
	if forbiddenChars.MatchString(suffix) {
		fmt.Println("❌ 오류: 폴더 이름에 금지 문자가 포함되어 있습니다.")
		return
	}

	folders := fm.GetNumberedFolders()
	if _, exists := folders[targetNum]; exists {
		// 밀어내기 시 99번 초과 검사
		maxNum := 0
		for k := range folders { if k > maxNum { maxNum = k } }
		if maxNum >= MAX_FOLDER_NUM {
			fmt.Println("❌ 오류: 99번을 초과하게 되어 밀어내기가 불가능합니다.")
			return
		}

		keys := []int{}
		for k := range folders { if k >= targetNum { keys = append(keys, k) } }
		sort.Sort(sort.Reverse(sort.IntSlice(keys)))
		for _, k := range keys {
			fm.RenameFolder(folders[k], k+1)
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
	if match == nil { return }
	newName := fmt.Sprintf("%02d_%s", newNum, match[2])
	if oldName == newName { return }

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

		if _, err := os.Stat(dest); err == nil {
			oldName := "old_" + targetName
			oldPath := filepath.Join(ARCHIVE_DIR, oldName)
			if _, err = os.Stat(oldPath); err == nil {
				ts := time.Now().Format(TIME_FORMAT)
				oldPath = filepath.Join(ARCHIVE_DIR, ts+"_"+oldName)
				fm.Log(fmt.Sprintf("중복 발생: 기존 파일을 타임스탬프 이름으로 변경합니다 -> %s", ts+"_"+oldName), "⏳")
			} else {
				fm.Log(fmt.Sprintf("중복 발생: 기존 파일을 '_old'로 변경합니다 -> %s", oldName), "♻️")
			}
			os.Rename(dest, oldPath)
		}

		os.Rename(targetName, dest)
		fm.Log("아카이브 이동: "+targetName, "♻️")
		fm.History = append(fm.History, HistoryItem{Old: targetName, New: dest})

		keys := []int{}
		for k := range folders { if k > targetNum { keys = append(keys, k) } }
		sort.Ints(keys)
		for _, num := range keys {
			fm.RenameFolder(folders[num], num-1)
		}
		fm.SaveHistory("archive")
	}
}

func (fm *FolderManager) Rollback() {
	data, err := os.ReadFile(HISTORY_FILE)
	if err != nil {
		fmt.Println("❌ 오류: 되돌릴 작업 이력이 없습니다.")
		return
	}

	var history HistoryData
	if err := json.Unmarshal(data, &history); err != nil {
		fmt.Println("❌ 오류: 로그 파일 형식이 유효하지 않습니다.") // 추가된 기능 2
		return
	}

	// 필드 유효성 검증
	if history.Mode == "" || len(history.Changes) == 0 {
		fmt.Println("❌ 오류: 정상적인 로그 기록 파일이 아닙니다.")
		return
	}

	fm.Log(fmt.Sprintf("롤백 시작: %s (%s)", history.Mode, history.Timestamp), "🔄")

	// 안전성 선검사
	for _, item := range history.Changes {
		if item.New != "" {
			if _, err := os.Stat(item.New); os.IsNotExist(err) {
				fmt.Printf("❌ 롤백 불가: 대상 '%s'가 존재하지 않습니다.\n", item.New)
				return
			}
		}
	}

	for i := len(history.Changes) - 1; i >= 0; i-- {
		item := history.Changes[i]
		if !fm.DryRun {
			if item.Old == "" {
				os.Remove(item.New)
			} else {
				os.Rename(item.New, item.Old)
			}
		}
	}

	if !fm.DryRun { os.Remove(HISTORY_FILE) }
	fmt.Println("✅ 롤백 완료.")
}

// --- 4. 메인 실행부 및 도움말 ---
func main() {
	flag.Usage = func() {
		fmt.Println(ASCII_ART)
		fmt.Println("Michelle's Professional Folder Manager (FM-Go)")
		fmt.Println("\nUsage:")
		fmt.Println("  fm <mode> [number] [name] [--dry-run]")
		fmt.Println("\nModes:")
		fmt.Println("  mk, make      : 폴더 생성 및 밀어내기 (예: fm mk 1 프로젝트)")
		fmt.Println("  rm, archive   : 폴더 아카이브 및 당기기 (예: fm rm 5)")
		fmt.Println("  fill, gaps    : 빈 번호 채우기 정리 (예: fm fill)")
		fmt.Println("  rollback, undo: 마지막 작업 되돌리기 (예: fm rollback)")
		fmt.Println("\nOptions:")
		flag.PrintDefaults()
	}

	dryRun := flag.Bool("dry-run", false, "실제 변경 없이 시뮬레이션 수행")
	flag.Parse()
	args := flag.Args()

	if len(args) < 1 {
		flag.Usage()
		return
	}

	fm := &FolderManager{DryRun: *dryRun}
	fm.CheckPathSafety() // 경로 안전 검사 실행

	mode := strings.ToLower(args[0])

	switch mode {
		case "mk", "make", "mkdir", "생성":
			if len(args) < 2 {
				fmt.Println("❌ 오류: 번호를 입력하세요."); return
			}
			num, _ := strconv.Atoi(args[1])
			name := "새폴더"
			if len(args) >= 3 { name = args[2] }
			fm.CreateFolder(num, name)

		case "rm", "archive", "del", "삭제":
			if len(args) < 2 {
				fmt.Println("❌ 오류: 번호를 입력하세요."); return
			}
			num, _ := strconv.Atoi(args[1])
			fm.ArchiveFolder(num)

		case "fill", "gaps", "채우기":
			fm.FillGaps() // 기존 로직 호출

		case "rollback", "undo", "되돌리기":
			fm.Rollback()

		default:
			fmt.Printf("❌ 알 수 없는 모드: %s. 'fm --help'를 확인하세요.\n", mode)
	}
}

func (fm *FolderManager) FillGaps() {
	folders := fm.GetNumberedFolders()
	if len(folders) == 0 {
		fmt.Println("❌ 정리할 폴더가 없습니다."); return
	}
	keys := []int{}
	for k := range folders { keys = append(keys, k) }
	sort.Ints(keys)
	for i, k := range keys {
		if k != i+1 {
			fm.RenameFolder(folders[k], i+1)
		}
	}
	fm.SaveHistory("fill")
	fmt.Println("✅ 빈자리 채우기 완료.")
}
