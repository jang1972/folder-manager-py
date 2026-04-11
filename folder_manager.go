// Made by Michelle
// With Gemini
// Edit Tool is Kate, VSC
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
	ConfigFile     = ".fm_config.json"
	TagsFile       = ".fm_tags.json"
)

type Config struct {
	ArchivePath string `json:"archive_path"`
	DataDir     string `json:"data_dir"`
}

var (
	folderPattern  = regexp.MustCompile(`^(\d{2})_(.*)$`)
	forbiddenChars = regexp.MustCompile(`[\\/:*?"<>|]`)
	// 시스템 민감 경로 키워드
	sensitivePaths = []string{"/etc", "/usr", "/bin", "/sbin", "C:\\Windows", "C:\\Program Files"}
)

var windowsReserved = []string{"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "LPT1", "LPT2"}

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
	ConfigPath  string // .json/.fm_config.json
	HistoryPath string // .json/.fm_history.json
	TagsPath    string // .json/.fm_tags.json
	Config      Config
	DryRun      bool
	History     []HistoryItem
	lockFile    *os.File
}

// 태그 데이터를 로드하는 함수
func loadTags() map[string]string {
	tags := make(map[string]string)
	data, err := os.ReadFile(TagsFile)
	if err == nil {
		json.Unmarshal(data, &tags)
	}
	return tags
}

// 태그 데이터를 저장하는 함수
func saveTags(tags map[string]string) {
	data, _ := json.MarshalIndent(tags, "", "  ")
	os.WriteFile(TagsFile, data, 0644)
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

func loadConfig() Config {
	var config Config
	data, err := os.ReadFile(ConfigFile)
	if err == nil {
		json.Unmarshal(data, &config)
	}
	return config
}

func saveConfig(config Config) error {
	data, _ := json.MarshalIndent(config, "", "  ")
	return os.WriteFile(ConfigFile, data, 0644)
}

func (fm *FolderManager) SafePathCheck(path string) bool {
	if path == "" {
		return true
	}
	currPath, _ := os.Getwd()
	absBase, _ := filepath.Abs(currPath)
	absTarget, _ := filepath.Abs(path)
	// 현재 디렉토리의 하위 경로인지 확인
	return strings.HasPrefix(absTarget, absBase)
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

	var stack []HistoryData
	if data, err := os.ReadFile(HISTORY_FILE); err == nil {
		json.Unmarshal(data, &stack)
	}

	newAction := HistoryData{
		Mode:      mode,
		Changes:   fm.History,
		Timestamp: time.Now().Format(TIME_FORMAT),
	}
	stack = append(stack, newAction) // Stack에 추가

	file, _ := json.MarshalIndent(stack, "", "  ")
	os.WriteFile(HISTORY_FILE, file, 0600)
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

	upperSuffix := strings.ToUpper(suffix)
	for _, res := range windowsReserved {
		if upperSuffix == res || strings.HasPrefix(upperSuffix, res+".") {
			fmt.Printf("❌ 오류: '%s'은(는) 시스템 예약어입니다.\n", suffix)
			return
		}
	}

	folders := fm.GetNumberedFolders()
	if _, exists := folders[targetNum]; exists {
		// 밀어내기 시 99번 초과 검사
		maxNum := 0
		for k := range folders {
			if k > maxNum {
				maxNum = k
			}
		}
		if maxNum >= MAX_FOLDER_NUM {
			fmt.Println("❌ 오류: 99번을 초과하게 되어 밀어내기가 불가능합니다.")
			return
		}

		keys := []int{}
		for k := range folders {
			if k >= targetNum {
				keys = append(keys, k)
			}
		}
		sort.Sort(sort.Reverse(sort.IntSlice(keys)))
		for _, k := range keys {
			fm.RenameFolder(folders[k], k+1)
		}
	}

	newName := fmt.Sprintf("%02d_%s", targetNum, suffix)
	fm.Log("폴더 생성: "+newName, "📁")
	if !fm.DryRun {
		// 기존에 동일한 이름의 파일/폴더가 있는지 먼저 확인
		if _, err := os.Stat(newName); err == nil {
			fmt.Printf("❌ 오류: '%s'이(가) 이미 존재합니다.\n", newName)
			return
		}
		os.Mkdir(newName, 0755)
		fm.History = append(fm.History, HistoryItem{Old: "", New: newName})
		fm.SaveHistory("create")
	}
}

func (fm *FolderManager) RenameFolder(oldName string, newNum int) {
	match := folderPattern.FindStringSubmatch(oldName) // 상단에 정의된 regex 사용
	if match == nil {
		return
	}
	newName := fmt.Sprintf("%02d_%s", newNum, match[2])
	if oldName == newName {
		return
	}

	fm.Log(fmt.Sprintf("이름 변경: %s -> %s", oldName, newName), "📝")

	if !fm.DryRun {
		// [핵심] 실제 파일 시스템의 이름을 먼저 변경
		err := os.Rename(oldName, newName)
		if err == nil {
			// 성공 시에만 히스토리 기록
			fm.History = append(fm.History, HistoryItem{Old: oldName, New: newName})

			// [핵심] 이름이 바뀌었으므로 태그의 주인(Key)도 업데이트
			fm.UpdateTagKey(oldName, newName)
		} else {
			fmt.Printf("❌ 이름 변경 실패: %v\n", err)
		}
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
		// 인젝션 방어: targetName에서 순수 이름만 추출
		safeName := filepath.Base(targetName)
		dest := filepath.Join(ARCHIVE_DIR, safeName)

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
		for k := range folders {
			if k > targetNum {
				keys = append(keys, k)
			}
		}
		sort.Ints(keys)
		for _, num := range keys {
			fm.RenameFolder(folders[num], num-1)
		}
		fm.SaveHistory("archive")
	}
}

// 아카이브 경로 가져오기
func (fm *FolderManager) getArchivePath() string {
	config := loadConfig()
	if config.ArchivePath != "" {
		return config.ArchivePath
	}
	// 현재 실행 경로(.)의 Archive 폴더를 기본값으로 설정
	return filepath.Join(".", "Archive")
}

// 권한 및 경로 체크
func (fm *FolderManager) checkPathAccess(path string) bool {
	if path == "" {
		return false
	}
	if _, err := os.Stat(path); os.IsNotExist(err) {
		err := os.MkdirAll(path, 0755)
		if err != nil {
			fmt.Println("❌ 해당 디렉토리는 잠겨 있습니다. 권한을 해제하십시오.")
			return false
		}
	}
	return true
}

func (fm *FolderManager) AnalyzeFolder(num int) {
	folders := fm.GetNumberedFolders()
	name, ok := folders[num]
	if !ok {
		fmt.Printf("⚠️ %02d번 폴더를 찾을 수 없습니다.\n", num)
		return
	}

	// --- 태그 정보 가져오기 ---
	tags := make(map[string]string)
	tagData, err := os.ReadFile(TagsFile)
	folderTag := "없음"
	if err == nil {
		json.Unmarshal(tagData, &tags)
		if t, exists := tags[name]; exists {
			folderTag = t
		}
	}
	// -----------------------

	var totalSize int64
	filepath.Walk(name, func(path string, info os.FileInfo, err error) error {
		if err == nil && !info.IsDir() {
			totalSize += info.Size()
		}
		return nil
	})

	fmt.Printf("📊 [%s] 분석 결과:\n", name)
	fmt.Printf("  📌 부여된 태그: [%s]\n", folderTag)
	fmt.Printf("  💾 전체 용량: %.2f MB\n", float64(totalSize)/(1024*1024))
}

func (fm *FolderManager) SetTag(num int, tag string) {
	folders := fm.GetNumberedFolders()
	name, ok := folders[num]
	if !ok {
		return
	}

	tags := make(map[string]string)
	data, err := os.ReadFile(TagsFile)
	if err == nil {
		json.Unmarshal(data, &tags)
	}

	tags[name] = tag
	newData, _ := json.MarshalIndent(tags, "", "  ")
	os.WriteFile(TagsFile, newData, 0644)
	fmt.Printf("✅ 태그 등록 완료: %s -> [%s]\n", name, tag)
}

func (fm *FolderManager) Rollback() {
	data, err := os.ReadFile(HISTORY_FILE)
	if err != nil {
		fmt.Println("❌ 오류: 되돌릴 작업 이력이 없습니다.")
		return
	}

	var stack []HistoryData
	if err := json.Unmarshal(data, &stack); err != nil {
		fmt.Println("❌ 오류: 로그 파일 형식이 유효하지 않습니다.")
		return
	}

	if len(stack) == 0 {
		fmt.Println("❌ 오류: 기록이 비어있습니다.")
		os.Remove(HISTORY_FILE)
		return
	}

	// 마지막 작업(Top) 꺼내기
	lastIdx := len(stack) - 1
	task := stack[lastIdx]

	fm.Log(fmt.Sprintf("롤백 시작: %s (%s)", task.Mode, task.Timestamp), "🔄")

	// 1. 사전 검증
	for _, item := range task.Changes {
		// 경로 인젝션 검증 (추가)
		if !fm.SafePathCheck(item.New) || !fm.SafePathCheck(item.Old) {
			fmt.Println("❌ 보안 경고: 허용되지 않은 경로가 로그에서 감지되었습니다.")
			return
		}

		if item.New != "" {
			info, err := os.Stat(item.New)
			if os.IsNotExist(err) {
				fmt.Printf("❌ 롤백 불가: 대상 '%s'가 존재하지 않습니다.\n", item.New)
				return
			}
			// 생성 취소 시 폴더 내부 검사
			if item.Old == "" && info.IsDir() {
				entries, _ := os.ReadDir(item.New)
				if len(entries) > 0 {
					fmt.Printf("❌ 롤백 불가: '%s' 내부에 파일이 존재합니다.\n", item.New)
					return
				}
			}
		}
	}

	// 2. 실제 실행 (역순)
	for i := len(task.Changes) - 1; i >= 0; i-- {
		item := task.Changes[i]
		if !fm.DryRun {
			if item.Old == "" {
				fm.Log("삭제(취소): "+item.New, "🗑️")
				os.Remove(item.New)
			} else {
				fm.Log(fmt.Sprintf("복구: %s -> %s", item.New, item.Old), "↩️")
				os.Rename(item.New, item.Old)
			}
		}
	}

	// 3. 남은 스택 업데이트
	if !fm.DryRun {
		stack = stack[:lastIdx] // 마지막 요소 제거
		if len(stack) > 0 {
			newData, _ := json.MarshalIndent(stack, "", "  ")
			os.WriteFile(HISTORY_FILE, newData, 0600)
		} else {
			os.Remove(HISTORY_FILE)
		}
	}

	fmt.Printf("✅ [%s] 작업 롤백 완료. (남은 기록: %d개)\n", task.Mode, len(stack))
}

func (fm *FolderManager) FillGaps() {
	folders := fm.GetNumberedFolders()
	if len(folders) == 0 {
		fmt.Println("❌ 정리할 폴더가 없습니다.")
		return
	}
	keys := []int{}
	for k := range folders {
		keys = append(keys, k)
	}
	sort.Ints(keys)
	for i, k := range keys {
		if k != i+1 {
			fm.RenameFolder(folders[k], i+1)
		}
	}
	fm.SaveHistory("fill")
	fmt.Println("✅ 빈자리 채우기 완료.")
}

func (fm *FolderManager) ClearHistory() {
	if _, err := os.Stat(HISTORY_FILE); err == nil {
		if fm.DryRun {
			fm.Log("기록 삭제 시뮬레이션", "🔍")
		} else {
			err := os.Remove(HISTORY_FILE)
			if err != nil {
				fmt.Println("❌ 오류: 기록 삭제 실패")
				return
			}
			fmt.Println("✅ 모든 작업 이력이 삭제되었습니다. (롤백 불가)")
		}
	} else {
		fmt.Println("💡 삭제할 이력이 없습니다.")
	}
}

func (fm *FolderManager) UpdateTagKey(oldName, newName string) {
	tags := loadTags()

	// 1. 대소문자 및 경로 구분자 이슈 해결을 위해 정규화된 키로 비교
	standardOld := filepath.Clean(oldName)
	found := false
	var actualKey string

	for k := range tags {
		if filepath.Clean(k) == standardOld {
			actualKey = k
			found = true
			break
		}
	}

	if found {
		tagValue := tags[actualKey]
		delete(tags, actualKey)                  // 확실하게 기존 키 삭제
		tags[filepath.Clean(newName)] = tagValue // 새 키는 정규화해서 저장
		saveTags(tags)
	}
}

func (fm *FolderManager) AcquireLock() error {
	// .json 폴더가 없으면 생성 (OS 의존성 없음)
	if err := os.MkdirAll(fm.Config.DataDir, 0755); err != nil {
		return fmt.Errorf("데이터 디렉토리 생성 실패: %v", err)
	}

	lockPath := filepath.Join(fm.Config.DataDir, ".fm.lock")
	// os.O_EXCL: 파일이 이미 존재하면 에러를 발생시킴 (원자적 체크)
	f, err := os.OpenFile(lockPath, os.O_CREATE|os.O_EXCL|os.O_WRONLY, 0600)
	if err != nil {
		return fmt.Errorf("이미 이 경로에서 다른 fm 프로세스가 실행 중입니다.\n직압증인게 이닐시 락 파일을 확인하세요,")
	}

	// 실행 중인 PID 기록 (디버깅용, 필수는 아님)
	fmt.Fprintf(f, "%d", os.Getpid())
	fm.lockFile = f
	return nil
}

func (fm *FolderManager) ReleaseLock() {
	if fm.lockFile != nil {
		fm.lockFile.Close()
		os.Remove(fm.lockFile.Name())
	}
}

func InitManager(dryRun bool) *FolderManager {
	// 경로 설정 로직 삭제, 구조체만 반환
	return &FolderManager{
		DryRun: dryRun,
	}
}

// --- 4. 메인 실행부 및 도움말 ---
func main() {
	for _, arg := range os.Args {
		if arg == "--license" {
			fmt.Println("\nThis program is free software under GNU GPL v3.")
			fmt.Println("See <https://www.gnu.org/licenses/> for details.")
			return
		}
	}

	flag.Usage = func() {
		fmt.Println(ASCII_ART)
		fmt.Println("Michelle's Professional Folder Manager (FM-Go)")
		fmt.Println("Not glory for technology, but boundless possibilities.")
		fmt.Println("\nUsage:")
		fmt.Println("  fm [--dry-run] <mode> [number] [name]")
		fmt.Println("\nModes:")
		fmt.Println("  mk, make, mkdir, 만들기, 생성    : 폴더 생성 및 밀어내기 (예: fm mk 1 프로젝트)")
		fmt.Println("  rm, rmdir, archive, 지우기, 삭제    : 폴더 아카이브 및 당기기 (예: fm rm 5)")
		fmt.Println("  fill, gaps, 채우기    : 빈 번호 채우기 정리 (예: fm fill)")
		fmt.Println("  rollback, undo, 되돌리기     : 마지막 작업 되돌리기 (예: fm rollback)")
		fmt.Println("  clear, reset, 비우기, 초기화     : 기록을 삭제하기 (예: fm clear)")
		fmt.Println("  analyze, 분석     : 파일의 용량과 부여 된 태그를 분석 (예: fm analyze 3")
		fmt.Println("  tag, 태그, 유형     : 폴더에 태그 부여 (예: fm tag 3 실험)")
		fmt.Println("  license     : 라이선스 정보 출력")
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

	fm := InitManager(*dryRun)
	fm.CheckPathSafety() // 경로 안전 검사 실행

	if err := fm.AcquireLock(); err != nil {
		fmt.Printf("❌ %v\n", err)
		return
	}
	defer fm.ReleaseLock()

	mode := strings.ToLower(args[0])

	switch mode {
	case "mk", "make", "mkdir", "생성", "만들기":
		if len(args) < 2 {
			fmt.Println("❌ 오류: 번호를 입력하세요.")
			return
		}
		num, err := strconv.Atoi(args[1])
		if err != nil {
			fmt.Println("❌ 오류: 번호는 숫자로 입력해야 합니다.")
			return
		}
		name := "새폴더"
		if len(args) >= 3 {
			name = args[2]
		}
		fm.CreateFolder(num, name)

	case "rm", "rmdir", "archive", "del", "삭제", "지우기":
		if len(args) < 2 {
			fmt.Println("❌ 오류: 번호를 입력하세요.")
			return
		}
		num, _ := strconv.Atoi(args[1])
		fm.ArchiveFolder(num)

	case "fill", "gaps", "채우기", "정렬":
		fm.FillGaps()

	case "rollback", "undo", "되돌리기":
		fm.Rollback()

	case "clear", "reset", "비우기", "초기화":
		fm.ClearHistory()

	case "set-archive", "경로설정":
		path := ""
		if len(args) >= 2 {
			path = args[1]
		}
		if fm.checkPathAccess(path) {
			config := loadConfig()
			config.ArchivePath = path
			saveConfig(config)
			fmt.Printf("✅ 아카이브 경로가 설정되었습니다: %s\n", path)
		}

	case "tag", "태그", "유형":
		if len(args) < 3 {
			fmt.Println("❌ 번호와 태그명이 필요합니다.")
			return
		}
		num, _ := strconv.Atoi(args[1])
		fm.SetTag(num, args[2])

	case "analyze", "분석":
		if len(args) < 2 {
			fmt.Println("❌ 번호가 필요합니다.")
			return
		}
		num, _ := strconv.Atoi(args[1])
		fm.AnalyzeFolder(num)

	default:
		fmt.Printf("❌ 알 수 없는 모드: %s. 'fm --help'를 확인하세요.\n", mode)
	}
}
