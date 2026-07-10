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
# 공용 헬퍼 함수
# ------------------------------------------------------

def clear_screen():
    """터미널 화면을 지워서 새 화면처럼 보이게 함"""
    os.system("cls" if os.name == "nt" else "clear")


def get_non_empty_input(prompt_text):
    """빈 값이 입력되면 다시 입력받는 헬퍼 함수"""
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("입력값이 비어있습니다. 다시 입력해주세요.")


def get_multiline_input(guide_text, allow_empty=False):
    """여러 줄 입력을 받는 함수.
    Enter는 줄바꿈, 새 줄에 '/s'만 입력하면 저장(종료).
    allow_empty=True이면 첫 줄 Enter로 바로 유지 가능."""
    print(guide_text)
    print("(여러 줄 입력 가능 · 저장: /s · 첫 줄 Enter: 기존 내용 유지)")

    lines = []
    while True:
        line = input()
        if line.strip() == "/s":
            break
        if line.strip() == "" and not lines and allow_empty:
            return ""
        lines.append(line)

    content = "\n".join(lines).strip()

    if not content and not allow_empty:
        print("내용이 비어있습니다. 다시 입력해주세요.")
        return get_multiline_input(guide_text, allow_empty)

    return content


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


def print_prompt_line(index, p):
    """목록 한 줄 출력 형식 통일"""
    star = " ⭐" if p["favorite"] else ""
    category = f"[{p['category']}]"
    print(f"{index:>2}. {category:<10} {p['title']}{star}")


# ------------------------------------------------------
# 상세 보기 화면
# ------------------------------------------------------

def show_detail_view(p):
    """프롬프트 상세 정보를 출력하고 조회수를 올린다."""
    clear_screen()
    p["views"] += 1
    star = "⭐" if p["favorite"] else "없음"

    print("─" * 40)
    print(f"  제목     : {p['title']}")
    print(f"  카테고리 : {p['category']}")
    print(f"  즐겨찾기 : {star}")
    print(f"  조회수   : {p['views']}")
    print("─" * 40)
    print("  내용")
    print("─" * 40)
    print(p["content"])
    print("─" * 40)

    while True:
        choice = input("\nb) 뒤로  0) 전체 메뉴\n선택: ").strip().lower()
        if choice == "b":
            return "back"
        if choice == "0":
            return "menu"
        print("잘못된 입력입니다.")


def browse_prompts(items, title):
    """프롬프트 목록을 보여주고, 번호 선택 시 상세 보기로 진입."""
    while True:
        clear_screen()
        print(f"=== {title} ===\n")

        if not items:
            print("표시할 프롬프트가 없습니다.")
            while True:
                choice = input("\nb) 뒤로  0) 전체 메뉴\n선택: ").strip().lower()
                if choice == "b":
                    return "back"
                if choice == "0":
                    return "menu"
                print("잘못된 입력입니다.")

        for i, p in enumerate(items, start=1):
            print_prompt_line(i, p)
        print(f"\n총 {len(items)}개의 프롬프트")

        choice = input("\n번호) 상세 보기  b) 뒤로  0) 전체 메뉴\n선택: ").strip().lower()

        if choice == "0":
            return "menu"
        if choice == "b":
            return "back"
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            result = show_detail_view(items[int(choice) - 1])
            if result == "menu":
                return "menu"
        else:
            print("잘못된 입력입니다.")


# ------------------------------------------------------
# 메뉴 출력
# ------------------------------------------------------

def show_menu():
    clear_screen()
    print("=== 나만의 프롬프트 관리 ===\n")
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
    print("\n0. 종료")


# ------------------------------------------------------
# 프롬프트 추가
# ------------------------------------------------------

def add_prompt():
    clear_screen()
    print("=== 프롬프트 추가 ===\n")
    title = get_non_empty_input("제목: ")
    content = get_multiline_input("\n내용:")
    category = choose_category()

    prompts.append({
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
        "views": 0,
    })

    print("\n✅ 프롬프트가 추가되었습니다!")
    input("\nEnter를 누르면 메뉴로 돌아갑니다...")


# ------------------------------------------------------
# 프롬프트 목록
# ------------------------------------------------------

def show_list():
    browse_prompts(prompts, "프롬프트 목록")


# ------------------------------------------------------
# 카테고리별 조회
# ------------------------------------------------------

def show_by_category():
    while True:
        clear_screen()
        print("=== 카테고리별 조회 ===\n")
        for i, cat in enumerate(CATEGORIES, start=1):
            print(f"{i}) {cat}")

        choice = input("\n번호) 카테고리 선택  b) 뒤로  0) 전체 메뉴\n선택: ").strip().lower()

        if choice in ("0", "b"):
            return
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            selected_category = CATEGORIES[int(choice) - 1]
            filtered = [p for p in prompts if p["category"] == selected_category]
            result = browse_prompts(filtered, f"[{selected_category}] 카테고리 프롬프트")
            if result == "menu":
                return
        else:
            print("잘못된 입력입니다.")


# ------------------------------------------------------
# 프롬프트 검색
# ------------------------------------------------------

def search_prompt():
    while True:
        clear_screen()
        print("=== 프롬프트 검색 ===\n")
        keyword = input("검색어 (b: 뒤로, 0: 전체 메뉴): ").strip()

        if keyword == "0" or keyword.lower() == "b":
            return
        if not keyword:
            print("검색어가 비어있습니다.")
            continue

        results = [
            p for p in prompts
            if keyword in p["title"] or keyword in p["content"]
        ]

        result = browse_prompts(results, f"'{keyword}' 검색 결과")
        if result == "menu":
            return


# ------------------------------------------------------
# 프롬프트 상세 보기 (메뉴 5번)
# ------------------------------------------------------

def show_detail():
    show_list()


# ------------------------------------------------------
# 즐겨찾기 관리
# ------------------------------------------------------

def select_prompt_index(title):
    """목록을 보여주고 번호를 선택받아 인덱스를 반환."""
    clear_screen()
    print(f"=== {title} ===\n")

    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        input("\nEnter를 누르면 메뉴로 돌아갑니다...")
        return None

    for i, p in enumerate(prompts, start=1):
        print_prompt_line(i, p)

    choice = input("\n번호 입력 (b: 뒤로, 0: 전체 메뉴): ").strip().lower()

    if choice in ("b", "0"):
        return None
    if choice.isdigit() and 1 <= int(choice) <= len(prompts):
        return int(choice) - 1

    print("잘못된 번호입니다.")
    return None


def toggle_favorite():
    index = select_prompt_index("즐겨찾기 관리")
    if index is None:
        return

    p = prompts[index]
    p["favorite"] = not p["favorite"]

    if p["favorite"]:
        print(f"\n✅ '{p['title']}' 프롬프트를 즐겨찾기에 추가했습니다!")
    else:
        print(f"\n❌ '{p['title']}' 프롬프트를 즐겨찾기에서 해제했습니다!")
    input("\nEnter를 누르면 메뉴로 돌아갑니다...")


# ------------------------------------------------------
# 즐겨찾기 목록
# ------------------------------------------------------

def show_favorites():
    favorites = [p for p in prompts if p["favorite"]]
    browse_prompts(favorites, "즐겨찾기 목록")


# ------------------------------------------------------
# 내보낼 프롬프트 선택 헬퍼
# ------------------------------------------------------

def select_prompts_for_export(title):
    clear_screen()
    print(f"=== {title} ===\n")

    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return None

    for i, p in enumerate(prompts, start=1):
        print_prompt_line(i, p)

    raw = input(
        "\n내보낼 번호 입력 (쉼표로 여러 개: 1,3,5 / a: 전체 / b: 뒤로): "
    ).strip().lower()

    if raw in ("b", "0"):
        return None
    if raw == "a":
        return list(prompts)

    selected = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit() and 1 <= int(part) <= len(prompts):
            selected.append(prompts[int(part) - 1])
        else:
            print(f"잘못된 번호가 포함되어 있습니다: '{part}'")
            return None

    if not selected:
        print("선택된 프롬프트가 없습니다.")
        return None

    return selected


# ------------------------------------------------------
# 보너스1: JSON 저장 / 불러오기
# ------------------------------------------------------

def save_prompts_json():
    selected = select_prompts_for_export("JSON으로 저장")
    if selected is None:
        return

    try:
        existing = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)

        existing_titles = {p["title"] for p in existing}
        new_items = [p for p in selected if p["title"] not in existing_titles]
        duplicates = [p for p in selected if p["title"] in existing_titles]
        merged = existing + new_items

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)

        print(f"\n✅ '{DATA_FILE}'에 {len(new_items)}개 추가 저장되었습니다.")
        print(f"(전체 저장 수: {len(merged)}개)")
        if duplicates:
            print(f"이미 저장된 항목(스킵): {', '.join(p['title'] for p in duplicates)}")

    except (OSError, json.JSONDecodeError) as e:
        print(f"저장에 실패했습니다: {e}")

    input("\nEnter를 누르면 메뉴로 돌아갑니다...")


def load_prompts_json():
    global prompts
    clear_screen()
    print("=== JSON 불러오기 ===\n")

    if not os.path.exists(DATA_FILE):
        print(f"'{DATA_FILE}' 파일이 존재하지 않습니다.")
        input("\nEnter를 누르면 메뉴로 돌아갑니다...")
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        prompts = loaded
        print(f"✅ '{DATA_FILE}'에서 {len(loaded)}개의 프롬프트를 불러왔습니다.")
    except (OSError, json.JSONDecodeError) as e:
        print(f"불러오기에 실패했습니다: {e}")

    input("\nEnter를 누르면 메뉴로 돌아갑니다...")


# ------------------------------------------------------
# 보너스1: 카테고리별 Markdown 내보내기
# ------------------------------------------------------

def export_markdown():
    selected = select_prompts_for_export("Markdown으로 내보내기")
    if selected is None:
        return

    os.makedirs(EXPORT_DIR, exist_ok=True)

    exported_count = 0
    for category in CATEGORIES:
        filtered = [p for p in selected if p["category"] == category]
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

    print(f"\n✅ '{EXPORT_DIR}/' 폴더에 카테고리별 {exported_count}개의 Markdown 파일을 내보냈습니다.")
    input("\nEnter를 누르면 메뉴로 돌아갑니다...")


# ------------------------------------------------------
# 보너스2: 프롬프트 수정
# ------------------------------------------------------

def edit_prompt():
    index = select_prompt_index("프롬프트 수정")
    if index is None:
        return

    p = prompts[index]
    clear_screen()
    print(f"=== 프롬프트 수정 ===\n")
    print("(변경하지 않으려면 그냥 Enter로 넘어가세요)\n")

    # 제목 수정
    print(f"[현재 제목]\n{p['title']}")
    new_title = input("새 제목 (Enter: 유지): ").strip()

    # 내용 수정
    print(f"\n[현재 내용]\n{p['content']}")
    new_content = get_multiline_input("\n새 내용:", allow_empty=True)

    # 카테고리 수정
    print(f"\n[현재 카테고리]\n{p['category']}")
    change_category = input("카테고리를 변경할까요? (y/N): ").strip().lower()

    # 반영
    if new_title:
        p["title"] = new_title
    if new_content:
        p["content"] = new_content
    if change_category == "y":
        p["category"] = choose_category()

    print(f"\n✅ '{p['title']}' 프롬프트가 수정되었습니다!")
    input("\nEnter를 누르면 메뉴로 돌아갑니다...")


# ------------------------------------------------------
# 보너스2: 프롬프트 삭제
# ------------------------------------------------------

def delete_prompt():
    index = select_prompt_index("프롬프트 삭제")
    if index is None:
        return

    p = prompts[index]
    clear_screen()
    print(f"=== 프롬프트 삭제 ===\n")
    print(f"제목: {p['title']}")
    print(f"카테고리: {p['category']}")

    confirm = input(f"\n정말 삭제할까요? (y/N): ").strip().lower()

    if confirm == "y":
        prompts.pop(index)
        print(f"\n✅ '{p['title']}' 프롬프트가 삭제되었습니다.")
    else:
        print("\n삭제를 취소했습니다.")

    input("\nEnter를 누르면 메뉴로 돌아갑니다...")


# ------------------------------------------------------
# 보너스2: 조회수 Top 목록
# ------------------------------------------------------

def show_top_viewed():
    sorted_prompts = sorted(prompts, key=lambda p: p["views"], reverse=True)
    browse_prompts(sorted_prompts, "조회수 Top 목록")


# ------------------------------------------------------
# 메인 루프
# ------------------------------------------------------

def main():
    while True:
        show_menu()
        choice = input("\n선택: ").strip()

        if choice == "0":
            clear_screen()
            print("프로그램을 종료합니다. 안녕히 가세요!")
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
            input("Enter를 누르면 계속합니다...")


if __name__ == "__main__":
    main()