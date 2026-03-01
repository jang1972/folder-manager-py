# Folder Manager (fm)

번호 기반의 폴더 관리 및 자동 정렬 도구입니다.
A number-based folder management and auto-alignment tool.

---

## 🚀 개요 (Overview)

이 프로젝트는 프로그래밍 입문자가 취미로 만든 간단한 파이썬 스크립트입니다. 한국 사용자들을 위해 한국어 주석이 포함되어 있습니다.
This project is a simple Python script created as a hobby by a programming beginner. It includes Korean comments for Korean-speaking users.

이 코드는 Google Gemini 3.0-Flash 모델의 도움을 받아 생성 및 최적화되었습니다.
This code was generated and optimized with the assistance of Google Gemini 3.0-Flash.

---

## 🎨 아스키 아트 저작권 (ASCII Art Copyright)

코드 내에 포함된 아스키 아트는 *붕괴 3rd*의 '키아나 카스라나'를 바탕으로 제작되었습니다.
The ASCII art included in the code is based on 'Kiana Kaslana' from *Honkai Impact 3rd*.

해당 캐릭터 및 디자인의 근본적인 저작권은 **miHoYo Network Technology Co. Ltd. / 米哈游网络科技股份有限公司**에 있습니다. 이 프로젝트는 팬 창작의 일환이며, 저작권자의 요청이 있을 시 해당 아트는 변경 또는 삭제될 수 있습니다.

The fundamental copyright for the characters and designs belongs to **miHoYo Network Technology Co. Ltd. / 米哈游网络科技股份有限公司**. This project is a fan-made creation, and the art may be modified or removed upon request from the copyright holder.

---

## 🛠️ 주요 기능 (Main Features)

- **Make**: 번호를 지정하여 새 폴더를 생성하고, 기존 폴더들의 번호를 자동으로 밀어냅니다. (Create a new folder and shift existing folder numbers.)
- **Archive (rm)**: 폴더를 보관함으로 이동시키고 빈 번호를 채웁니다. (Move folders to the Archive and fill the gap.)
- **Fill**: 중간에 비어 있는 폴더 번호를 01번부터 순차적으로 다시 정렬합니다. (Re-align folder numbers sequentially starting from 01.)
- **Dry-run**: 실제 파일 변경 전에 작업 내용을 미리 확인합니다. (Preview changes before they are actually applied.)

---

## 🔧 설치 및 사용법 (Installation & Usage)

### Recommended for Linux:
```bash
sudo ln -s "$(pwd)/folder_manager.py" /usr/local/bin/fm
