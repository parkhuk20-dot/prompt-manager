"""
나만의 프롬프트 관리 프로그램
--------------------------------
GenAI 프롬프트(텍스트/이미지/영상/페르소나/자동화 등)를
카테고리, 검색, 즐겨찾기, 조회수 기준으로 관리하는 콘솔 프로그램.

실행: python prompt_manager.py
"""

import json
import os

# ------------------------------------------------------------
# 상수 / 기본 데이터
# ------------------------------------------------------------

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

DATA_FILE = "prompts.json"
EXPORT_DIR = "exports"


def get_default_prompts():
    """이전 미션(GenAI 부트캠프 Mission 1~3)에서 실제로 사용했던 프롬프트를
    기본 데이터로 등록한다. (리스트 안에 딕셔너리로 저장)
    """
    return [
        {
            "title": "LLM 할루시네이션 점검 프롬프트",
            "content": (
                "당신은 사실 검증 전문가입니다. 아래 답변에서 확인되지 않은 주장이나 "
                "사실과 다를 수 있는 부분을 찾아 목록으로 정리해주세요. 각 항목마다 "
                "1) 의심되는 문장, 2) 왜 의심스러운지 이유, 3) 검증 방법을 함께 제시해주세요. "
                "확실하지 않으면 '확인 불가'라고 명시하고 추측하지 마세요."
            ),
            "category": "텍스트 생성",
            "favorite": True,
            "views": 0,
        },
        {
            "title": "SULSI 음료 광고 4씬 영상 프롬프트",
            "content": (
                "2030 직장인/학생을 타깃으로 한 음료 브랜드 'SULSI(설시, 雪時)'의 "
                "30초 광고 영상을 4개 씬으로 구성해주세요. 컨셉은 '극강의 청량감'이며 "
                "마코토 신카이 스타일의 2D 애니메이션 톤을 유지합니다. 각 씬마다 "
                "카메라 앵글, 배경, 캐릭터 동작, 대사/자막을 명시하고 인물의 성별과 "
                "외형은 씬 간에 절대 바뀌지 않도록 구체적으로 고정 묘사해주세요. "
                "건물/배경 오브젝트는 카메라 고정(static camera lock) 상태를 유지합니다."
            ),
            "category": "영상 생성",
            "favorite": False,
            "views": 0,
        },
        {
            "title": "SULSI 캐릭터 이미지 생성 프롬프트",
            "content": (
                "마코토 신카이풍 2D 애니메이션 스타일로 음료 브랜드 SULSI의 메인 캐릭터를 "
                "생성해주세요. 20대 후반 직장인 여성, 단발머리, 시원한 파란색과 흰색 톤의 "
                "의상, 청량하고 상쾌한 분위기의 배경(하늘, 얼음 결정 이펙트)을 함께 "
                "표현해주세요. 성별과 나이, 헤어스타일 묘사를 명확히 고정하여 이후 씬에서도 "
                "동일한 캐릭터로 유지되도록 해주세요."
            ),
            "category": "이미지 생성",
            "favorite": False,
            "views": 0,
        },
        {
            "title": "AI 자동화 컨설턴트 페르소나",
            "content": (
                "당신은 10년 경력의 노코드 자동화 컨설턴트입니다. Make, Zapier 등 "
                "자동화 툴에 정통하며, 클라이언트의 반복 업무를 분석해 최적의 워크플로우를 "
                "설계합니다. 답변할 때는 1) 현재 프로세스의 비효율 지점, 2) 추천 자동화 "
                "구조(트리거-액션 흐름도), 3) 예상되는 예외 상황과 에러 핸들링 방안, "
                "4) 무료/유료 플랜 중 적합한 선택지를 순서대로 설명해주세요."
            ),
            "category": "페르소나",
            "favorite": True,
            "views": 0,
        },
        {
            "title": "Google Sheets 신규 행 알림 자동화 프롬프트",
            "content": (
                "Make(구 Integromat) 시나리오를 설계해주세요. 트리거는 Google Sheets의 "
                "'Watch New Rows'이며, 새로운 행이 추가되면 내용을 요약해 Discord "
                "웹훅으로 알림을 전송합니다. 실패 시 Incomplete Executions로 라우팅되도록 "
                "에러 핸들러를 구성하고, 재시도(Retry) 모듈의 한계와 대안도 함께 "
                "설명해주세요."
            ),
            "category": "자동화",
            "favorite": False,
            "views": 0,
        },
    ]


# ------------------------------------------------------------
# 공통 입력 유틸
# ------------------------------------------------------------

def input_nonempty(label):
    """빈 값이 입력되면 다시 입력을 요청하는 공통 입력 함수."""
    while True:
        value = input(label).strip()
        if value:
            return value
        print("입력값이 비어있습니다. 다시 입력해주세요.\n")


def choose_category():
    """미리 정의된 카테고리 중 선택하거나 직접 입력한다."""
    print("\n카테고리 선택:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"{i}) {cat}")
    print(f"{len(CATEGORIES) + 1}) 직접 입력")

    while True:
        choice = input("선택: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(CATEGORIES):
                return CATEGORIES[idx - 1]
            if idx == len(CATEGORIES) + 1:
                return input_nonempty("카테고리명 입력: ")
        print("잘못된 입력입니다. 목록에 있는 번호를 입력해주세요.")


def get_valid_index(prompts, label="번호 입력: "):
    """번호를 입력받아 유효성을 검사하고 해당 인덱스(0-based)를 반환한다.
    잘못된 입력이면 None을 반환한다."""
    choice = input(label).strip()
    if not choice.isdigit():
        print("숫자를 입력해주세요.")
        return None
    idx = int(choice) - 1
    if idx < 0 or idx >= len(prompts):
        print("존재하지 않는 번호입니다.")
        return None
    return idx


def format_prompt_line(number, prompt):
    """'1. [카테고리] 제목 ⭐' 형태의 한 줄 요약을 만든다."""
    star = " ⭐" if prompt["favorite"] else ""
    return f"{number}. [{prompt['category']}] {prompt['title']}{star}"


# ------------------------------------------------------------
# 메뉴
# ------------------------------------------------------------

def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 추가/해제")
    print("7. 즐겨찾기 목록")
    print("8. 프롬프트 수정")
    print("9. 프롬프트 삭제")
    print("10. 조회수 Top 목록")
    print("11. JSON으로 저장")
    print("12. JSON 불러오기")
    print("13. 카테고리별 Markdown 내보내기")
    print("0. 종료")


# ------------------------------------------------------------
# 1. 프롬프트 추가
# ------------------------------------------------------------

def add_prompt(prompts):
    print("\n=== 프롬프트 추가 ===")
    title = input_nonempty("제목: ")
    content = input_nonempty("내용: ")
    category = choose_category()

    prompts.append({
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
        "views": 0,
    })
    print("\n프롬프트가 추가되었습니다!")


# ------------------------------------------------------------
# 2. 프롬프트 목록
# ------------------------------------------------------------

def show_list(prompts):
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    for i, p in enumerate(prompts, start=1):
        print(format_prompt_line(i, p))

    print(f"\n총 {len(prompts)}개의 프롬프트")


# ------------------------------------------------------------
# 3. 카테고리별 조회
# ------------------------------------------------------------

def show_by_category(prompts):
    print("\n=== 카테고리별 조회 ===")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"{i}) {cat}")

    choice = input("선택: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(CATEGORIES)):
        print("잘못된 입력입니다.")
        return

    category = CATEGORIES[int(choice) - 1]
    filtered = [p for p in prompts if p["category"] == category]

    print(f"\n[{category}] 카테고리 프롬프트:")
    if not filtered:
        print("해당 카테고리에 프롬프트가 없습니다.")
        return

    for i, p in enumerate(filtered, start=1):
        print(format_prompt_line(i, p))
    print(f"\n총 {len(filtered)}개의 프롬프트")


# ------------------------------------------------------------
# 4. 프롬프트 검색
# ------------------------------------------------------------

def search_prompt(prompts):
    print("\n=== 프롬프트 검색 ===")
    keyword = input_nonempty("검색어: ")

    results = [
        p for p in prompts
        if keyword in p["title"] or keyword in p["content"]
    ]

    print("\n검색 결과:")
    if not results:
        print("검색 결과가 없습니다.")
        return

    for i, p in enumerate(results, start=1):
        print(format_prompt_line(i, p))
    print(f"\n{len(results)}개의 프롬프트를 찾았습니다.")


# ------------------------------------------------------------
# 5. 프롬프트 상세 보기
# ------------------------------------------------------------

def show_detail(prompts):
    print("\n=== 프롬프트 상세 보기 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    idx = get_valid_index(prompts)
    if idx is None:
        return

    p = prompts[idx]
    p["views"] += 1  # 보너스: 조회수 기록

    star = "⭐" if p["favorite"] else "-"
    print("\n" + "─" * 30)
    print(f"제목: {p['title']}")
    print(f"카테고리: {p['category']}")
    print(f"즐겨찾기: {star}")
    print(f"조회수: {p['views']}")
    print("─" * 30)
    print("내용:")
    print(p["content"])
    print("─" * 30)


# ------------------------------------------------------------
# 6/7. 즐겨찾기
# ------------------------------------------------------------

def manage_favorite(prompts):
    print("\n=== 즐겨찾기 관리 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    idx = get_valid_index(prompts, "프롬프트 번호 입력: ")
    if idx is None:
        return

    p = prompts[idx]
    p["favorite"] = not p["favorite"]
    status = "추가" if p["favorite"] else "해제"
    print(f"'{p['title']}' 프롬프트를 즐겨찾기에 {status}했습니다!")


def show_favorites(prompts):
    print("\n=== 즐겨찾기 목록 ===")
    favorites = [p for p in prompts if p["favorite"]]

    if not favorites:
        print("즐겨찾기한 프롬프트가 없습니다.")
        return

    for i, p in enumerate(favorites, start=1):
        print(format_prompt_line(i, p))
    print(f"\n총 {len(favorites)}개의 즐겨찾기")


# ------------------------------------------------------------
# 8/9. 보너스: 프롬프트 수정 / 삭제 (CRUD)
# ------------------------------------------------------------

def edit_prompt(prompts):
    print("\n=== 프롬프트 수정 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    show_list(prompts)
    idx = get_valid_index(prompts, "\n수정할 번호 입력: ")
    if idx is None:
        return

    p = prompts[idx]
    print("변경하지 않으려면 그대로 Enter를 누르세요.")

    new_title = input(f"제목 ({p['title']}): ").strip()
    new_content = input(f"내용 ({p['content'][:20]}...): ").strip()

    if new_title:
        p["title"] = new_title
    if new_content:
        p["content"] = new_content

    change_category = input("카테고리도 변경할까요? (y/n): ").strip().lower()
    if change_category == "y":
        p["category"] = choose_category()

    print(f"\n'{p['title']}' 프롬프트가 수정되었습니다!")


def delete_prompt(prompts):
    print("\n=== 프롬프트 삭제 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    show_list(prompts)
    idx = get_valid_index(prompts, "\n삭제할 번호 입력: ")
    if idx is None:
        return

    confirm = input(f"'{prompts[idx]['title']}'을(를) 삭제할까요? (y/n): ").strip().lower()
    if confirm == "y":
        removed = prompts.pop(idx)
        print(f"'{removed['title']}' 프롬프트가 삭제되었습니다.")
    else:
        print("삭제를 취소했습니다.")


# ------------------------------------------------------------
# 10. 보너스: 조회수 Top 목록
# ------------------------------------------------------------

def show_top_viewed(prompts):
    print("\n=== 조회수 Top 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    ranked = sorted(prompts, key=lambda p: p["views"], reverse=True)
    for i, p in enumerate(ranked, start=1):
        star = " ⭐" if p["favorite"] else ""
        print(f"{i}. [{p['category']}] {p['title']}{star} - 조회수 {p['views']}")


# ------------------------------------------------------------
# 11/12. 보너스: JSON 저장 / 불러오기
# ------------------------------------------------------------

def save_prompts_json(prompts, filename=DATA_FILE):
    print("\n=== JSON으로 저장 ===")
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(prompts, f, ensure_ascii=False, indent=2)
        print(f"'{filename}' 파일로 저장했습니다. (총 {len(prompts)}개)")
    except OSError as e:
        print(f"저장에 실패했습니다: {e}")


def load_prompts_json(filename=DATA_FILE):
    print("\n=== JSON 불러오기 ===")
    if not os.path.exists(filename):
        print(f"'{filename}' 파일이 없습니다.")
        return None

    try:
        with open(filename, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        print(f"'{filename}'에서 {len(loaded)}개의 프롬프트를 불러왔습니다.")
        return loaded
    except (OSError, json.JSONDecodeError) as e:
        print(f"불러오기에 실패했습니다: {e}")
        return None


# ------------------------------------------------------------
# 13. 보너스: 카테고리별 Markdown 내보내기
# ------------------------------------------------------------

def export_markdown(prompts, export_dir=EXPORT_DIR):
    print("\n=== 카테고리별 Markdown 내보내기 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    os.makedirs(export_dir, exist_ok=True)

    for category in CATEGORIES:
        filtered = [p for p in prompts if p["category"] == category]
        if not filtered:
            continue

        filename = os.path.join(export_dir, f"{category}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {category} 프롬프트 모음\n\n")
            for p in filtered:
                star = " ⭐" if p["favorite"] else ""
                f.write(f"## {p['title']}{star}\n\n")
                f.write(f"- 조회수: {p['views']}\n\n")
                f.write(f"{p['content']}\n\n")
                f.write("---\n\n")

    print(f"'{export_dir}/' 폴더에 카테고리별 Markdown 파일을 저장했습니다.")


# ------------------------------------------------------------
# 메인 루프
# ------------------------------------------------------------

def main():
    prompts = get_default_prompts()

    actions = {
        "1": lambda: add_prompt(prompts),
        "2": lambda: show_list(prompts),
        "3": lambda: show_by_category(prompts),
        "4": lambda: search_prompt(prompts),
        "5": lambda: show_detail(prompts),
        "6": lambda: manage_favorite(prompts),
        "7": lambda: show_favorites(prompts),
        "8": lambda: edit_prompt(prompts),
        "9": lambda: delete_prompt(prompts),
        "10": lambda: show_top_viewed(prompts),
        "11": lambda: save_prompts_json(prompts),
        "13": lambda: export_markdown(prompts),
    }

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "0":
            print("\n프로그램을 종료합니다.")
            break
        elif choice == "12":
            loaded = load_prompts_json()
            if loaded is not None:
                prompts.clear()
                prompts.extend(loaded)
        elif choice in actions:
            actions[choice]()
        else:
            print("\n잘못된 번호입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()
