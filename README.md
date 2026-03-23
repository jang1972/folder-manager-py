# 📁 Folder Manager (fm)

번호 기반의 폴더 관리 및 자동 정렬 도구입니다.

A number-based folder management and auto-alignment tool.

License: This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

---

## ⛓️‍💥 기술적 자유를 위하여

구글이 안드로이드에서 제3자 앱을 실행 차단하여 사용자의 권리를 침해하려 하고 있습니다. 이를 막기 위해 도움을 보태 주시길 부탁 드립니다.

Google is trying to violate users' rights by blocking third-party apps from Android. Please help me stop this.

**[keepandroidopen Project](https://keepandroidopen.org)**

---

## 🚀 개요 (Overview)

이 프로젝트는 프로그래밍 뉴비가 취미로 만든 간단한 파이썬 스크립트입니다. 이 뉴비는 한국인이기에 한국어 주석이 포함 되어 있습니다.

This project is a simple Python script created as a hobby by a programming newbie. Since this newbie is Korean, Korean comments are included.

이 코드는 Google Gemini 3.0-Flash 모델의 도움을 받아 생성 및 최적화되었습니다.

This code was generated and optimized with the assistance of Google Gemini 3.0-Flash.

---

## ❓ 왜 만들었는가 ( Why was it created ?)
유튜브 쇼츠에서 ['구글 직원의 폴더 관리법'](https://www.youtube.com/watch?v=fRYw09PzHvM) 이런 것만 던져주고 자동화 기법은 안 알려줘서 한번 만들어 보았습니다.

I saw that YouTube shorts only showed things like 'How Google Employees Manage Folders' but didn't teach any automation techniques, so I tried making one.

---

## 🔗 파생 버전
- [Golang-version](https://github.com/jang1972/folder-manager-py/tree/golang-version)

인터프리터 설치도 싫거나 어려운 사람들이 사용하면 됩니다. (It is suitable for people who dislike or find it difficult to install interpreter.)

- [pathlib-version](https://github.com/jang1972/folder-manager-py/tree/pathlib-version)

사실상 유지보수 되지 않는 버전이니 사용을 비권장 드립니다. (This version is effectively not maintained. We do not recommend using it.)

- [PyPl-version](https://pypi.org/project/folder-manager-py/)

PyPl에 올린 버전입니다. 심볼릭 링크가 불필요 합니다. 대신 pipx나 venv등 실행 난이도가 역으로 높을 수 있습니다. 물론 표준 라이브러리만 사용해서 의존성 요구가 극단적으로 널널한 만큼(CPtyhon 3.7 이상이기만 하면 됨.) 시스템 패키지 부수고(--break-system-packages) 설치하셔도 될 것 같긴한데 책임은 못 집니다.

(This is the version uploaded to PyPl. Symbolic links are not required. If you do not use symbols, the difficulty of running applications like pipx or venv may actually increase. Of course, since it uses only standard libraries and has extremely loose dependency requirements (as long as you have CP107 or higher), it seems like you could install it by breaking system packages (--break-system-packages), but I cannot be held responsible for the consequences.)

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

- **Rollback**: 이전 작업들을 되돌립니다. Rollback 작업 자체와 Dry-run을 제외한 해당 스크립트의 모든 기능이 이에 해당 됩니다. (Reverts previous operations. This applies to all functions of the script except for the Rollback operation itself and Dry-run.)

- **Clear**: 남아 있는 json 로그들을 전부 초기화시킵니다. Rollback이 불가능합니다. (All remaining JSON logs are initialized. Rollback is not possible.)

- **Dry-run**: --dry-run 플래그를 통해 실제 파일 시스템을 변경하기 전, 수행될 작업을 콘솔에서 미리 안전하게 확인할 수 있습니다. (Safely preview all planned operations in the console using the --dry-run flag before any actual file system changes occur.)

- **Analysis**: 폴더의 용량과 폴더 안에 있는 파일의 타입등을 확인 가능. 태그가 있을시 태그도 확인 가능. (Check folder size and file types within the folder. Tags can also be checked if they exist.)

- **Tagging**: 특정 폴더에 태그를 붙여서 이후 folder_manager의 분석 기능으로 확인 가능함. (Tag specific folders can be attached to view them later using the folder_manager analysis function.)

- **Archive Path Setting Function**: 아카이브 저장 위치를 자유롭게 변경 가능. 권한 필요시 경고 후 작동하지 않음. (Freely change the archive save location. If permissions are required, a warning will be issued and the function will not operate.)

- **Smart Parsing**: argparse를 도입하여 더 전문적인 CLI 인터페이스를 제공하며, 01_Name 형식의 명명 규칙을 지원합니다. (Features a professional CLI interface via argparse and supports the 01.Name naming convention.)

---

## 🔧 설치 및 사용법 (Installation & Usage)

파일명 변경 : 자주 사용하실거라면 심볼릭 링크를 걸지 않을 경우 'fm'으로 파일명을 교체하는 것을 권장 드립니다.

### Recommended for Linux:
```bash
mkdir -p ~/.local/bin
ln -s "$(pwd)/folder_manager.py" ~/.local/bin/fm
```

---

## ♾️ 권고 사항 (Recommendation)
**이 항목은 프로젝트 저작권자의 권장 사항입니다. (This item is a recommendation from the project copyright holder)**

이 소프트웨어는 자동화를 통한 효율성 향상을 위해 개발되었습니다.
특정 플랫폼에 대한 체계적인 차별이나 지속 가능한 소프트웨어 건전성을 의도적으로 무시하는 행위 등 '기술적 악'을 추구하는 데 이 소프트웨어를 사용하는 것은 절대 권장하지 않습니다.
저희는 사용자 경험과 기술적 무결성이 모두에게 존중받는 디지털 환경을 지향합니다.

사용자를 존중하고, 기술을 존중하십시오.

기술에 영광따위가 아닌 무궁무진한 가능성을.

This software is intended for the advancement of organized efficiency.
Its use in the pursuit of 'technical evil'—including but not limited to
the systematic discrimination against specific platforms or the intentional
disregard for sustainable software health—is explicitly not recommended.
We advocate for a digital environment where the user experience
and technical integrity are respected by all.

Respect the user' respect the craft.

Not glory for technology, but boundless possibilities.

---

## 기여 안내 (Contributing)
이 프로젝트 레포지토리에 속하는 모든 브랜치에 기여(Issue 제기나 Pull Request 제출 등)하는 것은 프로젝트의 **[권리 양도 및 라이선스 변경 동의(CLA)](CLA.md)** 에 동의하는 것으로 간주됩니다.

By contributing to any branch within this project repository (including but not limited to Issues or Pull Requests), you are deemed to have agreed to the project's **[Contributor License Agreement (CLA)](CLA.md)**.
