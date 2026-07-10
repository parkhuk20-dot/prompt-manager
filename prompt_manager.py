"""
나만의 프롬프트 관리 프로그램
--------------------------------
GenAI 프롬프트(텍스트/이미지/영상/페르소나/자동화 등)를
카테고리, 검색, 즐겨찾기, 조회수 기준으로 관리하는 콘솔 프로그램.

실행: python3 prompt_manager.py
"""

import json
import os

# ------------------------------------------------------
# 상수 / 기본 데이터
# ------------------------------------------------------

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

DATA_FILE = "prompts.json"
EXPORT_DIR = "exports"

prompts = [
    {
        "title": "블로그 글 작성 도우미",
        "content": "당신은 10년 경력의 전문 블로거입니다. 주어진 주제에 대해 SEO에 최적화된 블로그 글을 작성해주세요.",
        "category": "텍스트 생성",
        "favorite": False,
        "views": 0,
    },
    {
        "title": "SULSI 광고 영상 씬 프롬프트",
        "content": "2D 애니메이션 스타일, 신카이 마코토 감성의 4씬 30초 음료 광고. 극한의 청량감을 시각적으로 표현.",
        "category": "영상 생성",
        "favorite": False,
        "views": 0,
    },
    {
        "title": "노코드 자동화 시나리오 설계",
        "content": "Google Sheets에 새 행이 추가되면 OpenAI로 요약을 생성하고 Discord 웹훅으로 전송하는 Make 시나리오를 설계해주세요.",
        "category": "자동화",
        "favorite": False,
        "views": 0,
    },
]


# ------------------------------------------------------
# 메뉴 출력
# ------------------------------------------------------

def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("8. JSON으로 저장")
    print("9. JSON 불러오기")
    print("10. Markdown으로 내보내기")
    print("11. 프롬프트 수정")
    print("12. 프롬프트 삭제")
    print("13. 조회수 Top 목록")
    print("0. 종료")


# ------------------------------------------------------
# 공용 헬퍼 함수
# ------------------------------------------------------

def get_non_empty_input(prompt_text):
    """빈 값이 입력되면 다시 입력받는 헬퍼 함수"""
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("입력값이 비어있습니다. 다시 입력해주세요.")


def choose_category():
    """카테고리를 목록에서 선택하거나 직접 입력"""
    print("\n카테고리 선택:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"{i}) {cat}")
    print("0) 직접 입력")

    choice = input("선택: ").strip()

    if choice == "0":
        return get_non_empty_input("카테고리 직접 입력: ")

    if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
        return CATEGORIES[int(choice) - 1]

    print("잘못된 선택입니다. 기본값 '기타'로 설정합니다.")
    return "기타"


def select_prompt_number():
    """목록을 보여주고 유효한 프롬프트 번호를 입력받는 헬퍼 함수.
    유효하면 인덱스(0부터 시작)를, 아니면 None을 반환."""
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return None

    show_list()
    choice = input("\n번호 입력: ").strip()

    if not choice.isdigit() or not (1 <= int(choice) <= len(prompts)):
        print("잘못된 번호입니다.")
        return None

    return int(choice) - 1


# ------------------------------------------------------
# 프롬프트 추가
# ------------------------------------------------------

def add_prompt():
    print("\n=== 프롬프트 추가 ===")
    title = get_non_empty_input("제목: ")
    content = get_non_empty_input("내용: ")
    category = choose_category()

    prompts.append({
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
        "views": 0,
    })

    print("\n프롬프트가 추가되었습니다!")


# ------------------------------------------------------
# 프롬프트 목록
# ------------------------------------------------------

def show_list():
    print("\n=== 프롬프트 목록 ===")

    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    for i, p in enumerate(prompts, start=1):
        star = " ⭐" if p["favorite"] else ""
        print(f"{i}. [{p['category']}] {p['title']}{star}")

    print(f"\n총 {len(prompts)}개의 프롬프트")


# ------------------------------------------------------
# 카테고리별 조회
# ------------------------------------------------------

def show_by_category():
    print("\n=== 카테고리별 조회 ===")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"{i}) {cat}")

    choice = input("선택: ").strip()

    if not choice.isdigit() or not (1 <= int(choice) <= len(CATEGORIES)):
        print("잘못된 선택입니다.")
        return

    selected_category = CATEGORIES[int(choice) - 1]
    filtered = [p for p in prompts if p["category"] == selected_category]

    print(f"\n[{selected_category}] 카테고리 프롬프트:")

    if not filtered:
        print("해당 카테고리에 프롬프트가 없습니다.")
        return

    for i, p in enumerate(filtered, start=1):
        star = " ⭐" if p["favorite"] else ""
        print(f"{i}. {p['title']}{star}")

    print(f"\n총 {len(filtered)}개의 프롬프트")


# ------------------------------------------------------
# 프롬프트 검색
# ------------------------------------------------------

def search_prompt():
    print("\n=== 프롬프트 검색 ===")
    keyword = get_non_empty_input("검색어: ")

    results = [
        p for p in prompts
        if keyword in p["title"] or keyword in p["content"]
    ]

    if not results:
        print("\n검색 결과가 없습니다.")
        return

    print("\n검색 결과:")
    for i, p in enumerate(results, start=1):
        star = " ⭐" if p["favorite"] else ""
        print(f"{i}. [{p['category']}] {p['title']}{star}")

    print(f"\n{len(results)}개의 프롬프트를 찾았습니다.")


# ------------------------------------------------------
# 프롬프트 상세 보기 (조회수 기록 포함)
# ------------------------------------------------------

def show_detail():
    print("\n=== 프롬프트 상세 보기 ===")

    index = select_prompt_number()
    if index is None:
        return

    p = prompts[index]
    p["views"] += 1  # 조회수 증가

    star = "⭐" if p["favorite"] else "없음"

    print("─" * 30)
    print(f"제목: {p['title']}")
    print(f"카테고리: {p['category']}")
    print(f"즐겨찾기: {star}")
    print(f"조회수: {p['views']}")
    print("─" * 30)
    print("내용:")
    print(p["content"])
    print("─" * 30)


# ------------------------------------------------------
# 즐겨찾기 관리 (추가/해제)
# ------------------------------------------------------

def toggle_favorite():
    print("\n=== 즐겨찾기 관리 ===")

    index = select_prompt_number()
    if index is None:
        return

    p = prompts[index]
    p["favorite"] = not p["favorite"]

    if p["favorite"]:
        print(f"\n'{p['title']}' 프롬프트를 즐겨찾기에 추가했습니다!")
    else:
        print(f"\n'{p['title']}' 프롬프트를 즐겨찾기에서 해제했습니다!")


# ------------------------------------------------------
# 즐겨찾기 목록
# ------------------------------------------------------

def show_favorites():
    print("\n=== 즐겨찾기 목록 ===")

    favorites = [p for p in prompts if p["favorite"]]

    if not favorites:
        print("즐겨찾기한 프롬프트가 없습니다.")
        return

    for i, p in enumerate(favorites, start=1):
        print(f"{i}. [{p['category']}] {p['title']} ⭐")

    print(f"\n총 {len(favorites)}개의 즐겨찾기")


# ------------------------------------------------------
# 보너스1: JSON 저장 / 불러오기
# ------------------------------------------------------

def save_prompts_json():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(prompts, f, ensure_ascii=False, indent=2)
        print(f"\n'{DATA_FILE}' 파일에 {len(prompts)}개의 프롬프트를 저장했습니다.")
    except OSError as e:
        print(f"저장에 실패했습니다: {e}")


def load_prompts_json():
    global prompts

    if not os.path.exists(DATA_FILE):
        print(f"\n'{DATA_FILE}' 파일이 존재하지 않습니다.")
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        prompts = loaded
        print(f"\n'{DATA_FILE}'에서 {len(loaded)}개의 프롬프트를 불러왔습니다.")
    except (OSError, json.JSONDecodeError) as e:
        print(f"불러오기에 실패했습니다: {e}")


# ------------------------------------------------------
# 보너스1: 카테고리별 Markdown 내보내기
# ------------------------------------------------------

def export_markdown():
    print("\n=== 카테고리별 Markdown 내보내기 ===")

    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    os.makedirs(EXPORT_DIR, exist_ok=True)

    exported_count = 0
    for category in CATEGORIES:
        filtered = [p for p in prompts if p["category"] == category]
        if not filtered:
            continue

        filename = os.path.join(EXPORT_DIR, f"{category}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {category} 프롬프트 모음\n\n")
            for p in filtered:
                star = " ⭐" if p["favorite"] else ""
                f.write(f"## {p['title']}{star}\n\n")
                f.write(f"- 조회수: {p['views']}\n\n")
                f.write(f"{p['content']}\n\n")
                f.write("---\n\n")
        exported_count += 1

    print(f"\n'{EXPORT_DIR}/' 폴더에 카테고리별 {exported_count}개의 Markdown 파일을 내보냈습니다.")


# ------------------------------------------------------
# 보너스2: 프롬프트 수정
# ------------------------------------------------------

def edit_prompt():
    print("\n=== 프롬프트 수정 ===")

    index = select_prompt_number()
    if index is None:
        return

    p = prompts[index]
    print(f"\n'{p['title']}' 프롬프트를 수정합니다.")
    print("(변경하지 않으려면 그냥 Enter를 누르세요)")

    new_title = input(f"제목 [{p['title']}]: ").strip()
    new_content = input("내용 (Enter 시 유지): ").strip()

    change_category = input("카테고리를 변경할까요? (y/N): ").strip().lower()

    if new_title:
        p["title"] = new_title
    if new_content:
        p["content"] = new_content
    if change_category == "y":
        p["category"] = choose_category()

    print(f"\n'{p['title']}' 프롬프트가 수정되었습니다!")


# ------------------------------------------------------
# 보너스2: 프롬프트 삭제
# ------------------------------------------------------

def delete_prompt():
    print("\n=== 프롬프트 삭제 ===")

    index = select_prompt_number()
    if index is None:
        return

    p = prompts[index]
    confirm = input(f"\n'{p['title']}' 프롬프트를 정말 삭제할까요? (y/N): ").strip().lower()

    if confirm == "y":
        prompts.pop(index)
        print(f"\n'{p['title']}' 프롬프트가 삭제되었습니다.")
    else:
        print("\n삭제를 취소했습니다.")


# ------------------------------------------------------
# 보너스2: 조회수 Top 목록
# ------------------------------------------------------

def show_top_viewed():
    print("\n=== 조회수 Top 목록 ===")

    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    sorted_prompts = sorted(prompts, key=lambda p: p["views"], reverse=True)

    for i, p in enumerate(sorted_prompts, start=1):
        star = " ⭐" if p["favorite"] else ""
        print(f"{i}. [{p['category']}] {p['title']}{star} - 조회수 {p['views']}")

    print(f"\n총 {len(sorted_prompts)}개의 프롬프트 (조회수 높은 순)")


# ------------------------------------------------------
# 메인 루프
# ------------------------------------------------------

def main():
    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        elif choice == "1":
            add_prompt()
        elif choice == "2":
            show_list()
        elif choice == "3":
            show_by_category()
        elif choice == "4":
            search_prompt()
        elif choice == "5":
            show_detail()
        elif choice == "6":
            toggle_favorite()
        elif choice == "7":
            show_favorites()
        elif choice == "8":
            save_prompts_json()
        elif choice == "9":
            load_prompts_json()
        elif choice == "10":
            export_markdown()
        elif choice == "11":
            edit_prompt()
        elif choice == "12":
            delete_prompt()
        elif choice == "13":
            show_top_viewed()
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()