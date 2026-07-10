# 프롬프트 관리 프로그램 - 과제 제출 문서

## 1. 프로젝트 개요

GenAI 프롬프트(텍스트/이미지/영상/페르소나/자동화 등)를 카테고리, 검색, 즐겨찾기, 조회수 기준으로 관리하는 **콘솔 기반 Python 프로그램**입니다. 파이썬 기초 문법(변수, 조건문, 반복문, 함수, 리스트/딕셔너리)과 Git/GitHub를 활용한 버전 관리를 실습하기 위해 제작했습니다.

- **GitHub 저장소**: https://github.com/parkhuke20-dot/prompt-manager
- **개발 환경**: macOS, VSCode, Python 3.12.12, Git 2.50.1
- **파일 구성**: `prompt_manager.py`(메인 프로그램), `README.md`, `.gitignore`

---

## 2. 실행 방법

Python 3.10 이상이 설치되어 있어야 합니다.

```bash
python3 prompt_manager.py
```

실행 후 메뉴에 표시되는 번호를 입력해 원하는 기능을 선택합니다.

### 입력 단축키

| 단축키 | 동작 |
|---|---|
| 숫자 | 해당 번호 선택 |
| `b` | 이전 화면으로 이동 |
| `0` | 전체 메뉴로 이동 |
| `/s` | 여러 줄 입력 저장 (추가/수정 시) |
| `a` | 전체 선택 (JSON/Markdown 내보내기 시) |

---

## 3. 기능 목록

### 기본 기능 (필수 요구사항)

| 번호 | 기능 | 설명 |
|---|---|---|
| 1 | 프롬프트 추가 | 제목, 내용(여러 줄 입력 가능), 카테고리를 입력해 새 프롬프트 등록 |
| 2 | 프롬프트 목록 | 전체 프롬프트를 번호, 카테고리, 즐겨찾기 여부와 함께 출력 |
| 3 | 카테고리별 조회 | 선택한 카테고리에 속한 프롬프트만 조회 |
| 4 | 프롬프트 검색 | 제목 또는 내용에 포함된 키워드로 검색 |
| 5 | 프롬프트 상세 보기 | 번호 선택 시 전체 내용 및 조회수 출력 |
| 6 | 즐겨찾기 관리 | 프롬프트 번호 선택으로 즐겨찾기 추가/해제 (토글) |
| 7 | 즐겨찾기 목록 | 즐겨찾기한 프롬프트만 모아서 조회 |

### 보너스 기능

| 번호 | 기능 | 설명 |
|---|---|---|
| 8 | JSON으로 저장 | 선택한 프롬프트를 JSON 파일로 저장 (단일/복수/전체 선택, 누적 저장 지원) |
| 9 | JSON 불러오기 | 저장된 JSON 파일에서 프롬프트 불러오기 |
| 10 | Markdown으로 내보내기 | 선택한 프롬프트를 카테고리별 Markdown 파일로 내보내기 |
| 11 | 프롬프트 수정 | 제목, 내용, 카테고리 수정 (Enter로 유지, 현재 내용 확인 후 수정 가능) |
| 12 | 프롬프트 삭제 | 확인 후 프롬프트 삭제 |
| 13 | 조회수 Top 목록 | 상세 보기 횟수 기준으로 정렬된 목록 조회 |

---

## 4. 카테고리

| 카테고리 | 설명 |
|---|---|
| 텍스트 생성 | 블로그, 이메일, 요약 등 텍스트 관련 프롬프트 |
| 이미지 생성 | 이미지 생성 AI용 프롬프트 |
| 영상 생성 | 영상 생성 AI용 프롬프트 |
| 페르소나 | 역할, 캐릭터 설정 프롬프트 |
| 자동화 | Make, Zapier 등 노코드 자동화 시나리오 |
| 기타 | 위 분류에 속하지 않는 프롬프트 |

---

## 5. 기본 등록 데이터

프로그램 실행 시 이전 미션에서 작성한 프롬프트 3개가 기본으로 등록되어 있습니다.

| 제목 | 카테고리 |
|---|---|
| 블로그 글 작성 도우미 | 텍스트 생성 |
| SULSI 광고 영상 씬 프롬프트 | 영상 생성 |
| 노코드 자동화 시나리오 설계 | 자동화 |

---

## 6. 코드 구조 (함수별 분리)

모든 코드는 한 함수에 몰아넣지 않고 기능별로 함수를 분리했습니다.

| 함수 | 역할 |
|---|---|
| `show_menu()` | 메인 메뉴 출력 |
| `clear_screen()` | 화면 초기화(새 페이지처럼 동작) |
| `get_non_empty_input()` | 빈 값 방지 입력 헬퍼 |
| `get_multiline_input()` | 여러 줄 입력 헬퍼 |
| `choose_category()` | 카테고리 선택 헬퍼 |
| `print_prompt_line()` | 목록 한 줄 출력 형식 통일 |
| `browse_prompts()` | 목록 브라우징(번호 선택→상세, b/0 이동) |
| `show_detail_view()` | 상세 보기 + 조회수 증가 |
| `add_prompt()` | 프롬프트 추가 |
| `show_list()` | 프롬프트 목록 |
| `show_by_category()` | 카테고리별 조회 |
| `search_prompt()` | 프롬프트 검색 |
| `select_prompt_index()` | 번호 선택 헬퍼(관리/수정/삭제 공용) |
| `toggle_favorite()` | 즐겨찾기 추가/해제 |
| `show_favorites()` | 즐겨찾기 목록 |
| `select_prompts_for_export()` | 내보낼 프롬프트 선택 헬퍼 |
| `save_prompts_json()` | JSON 저장 |
| `load_prompts_json()` | JSON 불러오기 |
| `export_markdown()` | 카테고리별 Markdown 내보내기 |
| `edit_prompt()` | 프롬프트 수정 |
| `delete_prompt()` | 프롬프트 삭제 |
| `show_top_viewed()` | 조회수 Top 목록 |
| `main()` | 메인 실행 루프 |

---

## 7. Git / GitHub 활용 내역

### 사용한 Git 명령어

| 명령어 | 사용 목적 |
|---|---|
| `git init` | 로컬 저장소 초기화 |
| `git add` | 변경사항 스테이징 |
| `git commit` | 변경사항 커밋(기능 단위) |
| `git push` | GitHub 원격 저장소 업로드 |
| `git pull` | 원격 저장소 최신 내용 받기(노트북/부트캠프 PC 동기화) |
| `git clone` | 다른 컴퓨터에서 저장소 복제 |
| `git checkout` | 브랜치 생성 및 전환 |
| `git merge` | 브랜치 병합 |

### 브랜치 생성 및 병합 기록

`feature/show-list` 브랜치를 생성하여 "프롬프트 목록" 기능을 개발한 뒤, `main` 브랜치로 병합했습니다.

```bash
git checkout -b feature/show-list   # 브랜치 생성 및 전환
# (목록 기능 개발 및 커밋)
git checkout main                    # main으로 이동
git merge feature/show-list          # 병합
```

### 커밋 히스토리 (17개 커밋)

기능 단위로 의미 있는 커밋을 작성했습니다. (최소 10개 요구사항 충족)

```
Update README with full feature list and shortcuts
Add clear screen for page-like navigation UX
Improve edit prompt UX with current value display and Enter to skip
Fix missing load_prompts_json function
Align prompt list columns for cleaner display
Fix JSON save to append instead of overwrite
Add edit and delete prompt features (CRUD)
Add load prompts from JSON file feature
Add save prompts to JSON file feature
Write README with description, usage, and feature list
Add search, detail view, favorite toggle, and favorite list features
Add show_list feature on feature branch (feature/show-list)
Add prompt creation feature (add_prompt)
Add menu skeleton and base prompt data
Initial commit: project structure setup
```

---

## 8. 제출 스크린샷

> 아래 자리에 실제 스크린샷 이미지를 삽입하세요.
> (GitHub에 이미지 파일을 업로드한 뒤 `![설명](이미지경로)` 형식으로 넣으면 됩니다.)

### 8-1. 개발 환경 설정 (VSCode, Python 버전, Git 설정)

```
python3 --version   # Python 3.12.12
git --version       # git version 2.50.1
git config --global --list
```

![개발 환경 스크린샷](screenshots/dev-environment.png)

### 8-2. 프로그램 실행 결과

**메뉴 화면**

![메뉴 스크린샷](screenshots/menu.png)

**프롬프트 추가**

![추가 스크린샷](screenshots/add.png)

**프롬프트 목록**

![목록 스크린샷](screenshots/list.png)

**프롬프트 검색**

![검색 스크린샷](screenshots/search.png)

### 8-3. git log --oneline --graph 결과

![git log 스크린샷](screenshots/git-log.png)

### 8-4. GitHub 저장소 화면

![GitHub 저장소 스크린샷](screenshots/github-repo.png)

---

