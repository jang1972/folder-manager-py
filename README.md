# Folder Manager (fm)

번호 기반의 폴더 관리 및 자동 정렬 도구입니다.

A number-based folder management and auto-alignment tool.

License: This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

---

## 🚀 개요 (Overview)

이 프로젝트는 프로그래밍 뉴비가 취미로 만든 간단한 파이썬 스크립트입니다. 이 뉴비는 한국인이기에 한국어 주석이 포함 되어 있습니다.

This project is a simple Python script created as a hobby by a programming newbie. Since this newbie is Korean, Korean comments are included.

이 코드는 Google Gemini 3.0-Flash 모델의 도움을 받아 생성 및 최적화되었습니다.

This code was generated and optimized with the assistance of Google Gemini 3.0-Flash.

---

## 왜 만들었는가 ( Why was it created ? )
유튜브 쇼츠에서 '구글 직원의 폴더 관리법' 이런 것만 던져주고 자동화 기법은 안 알려줘서 한번 만들어 보았습니다.

I saw that YouTube shorts only showed things like 'How Google Employees Manage Folders' but didn't teach any automation techniques, so I tried making one.

---

## 🎨 아스키 아트 저작권 (ASCII Art Copyright)

코드 내에 포함된 아스키 아트는 *붕괴 3rd*의 '키아나 카스라나'를 바탕으로 제작되었습니다.

The ASCII art included in the code is based on 'Kiana Kaslana' from *Honkai Impact 3rd*.

해당 캐릭터 및 디자인의 근본적인 저작권은 **miHoYo Network Technology Co. Ltd. / 米哈游网络科技股份有限公司**에 있습니다. 이 프로젝트는 팬 창작의 일환이며, 저작권자의 요청이 있을 시 해당 아트는 변경 또는 삭제될 수 있습니다.

The fundamental copyright for the characters and designs belongs to **miHoYo Network Technology Co. Ltd. / 米哈游网络科技股份有限公司**. This project is a fan-made creation, and the art may be modified or removed upon request from the copyright holder.

---

## 🛠️ 주요 기능 (Main Features)
- **Make**: 번호를 지정하여 새 폴더를 생성하며, 해당 번호 이상의 기존 폴더들을 자동으로 뒤로 밀어냅니다. (Create a new folder at a specific index and automatically shift subsequent folders forward.)

- **Archive (rm)**:  지정한 번호의 폴더를 타임스탬프와 함께 보관 처리하고, 뒤에 남은 폴더들의 번호를 앞으로 당겨 빈자리를 채웁니다. (Archive a folder with a timestamp and shift subsequent folders back to fill the gap.)

- **Fill**: 중간에 누락된 번호가 있다면 01번부터 순차적으로 다시 정렬하여 구조를 최적화합니다. (Re-align all folder numbers sequentially starting from 01 to optimize the structure.)

- **Dry-run**: --dry-run 플래그를 통해 실제 파일 시스템을 변경하기 전, 수행될 작업을 콘솔에서 미리 안전하게 확인할 수 있습니다. (Safely preview all planned operations in the console using the --dry-run flag before any actual file system changes occur.)

- **Smart Parsing**: argparse를 도입하여 더 전문적인 CLI 인터페이스를 제공하며, 01_Name 형식의 명명 규칙을 지원합니다. (Features a professional CLI interface via argparse and supports the 01.Name naming convention.)

---

## 🔧 설치 및 사용법 (Installation & Usage)

### Recommended for Linux:
```bash
sudo ln -s "$(pwd)/folder_manager.py" /usr/local/bin/fm
