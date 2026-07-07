"""
나만의 프롬프트 관리 프로그램
--------------------------------
GenAI 프롬프트(텍스트/이미지/영상/페르소나/자동화 등)를
카테고리, 검색, 즐겨찾기, 조회수 기준으로 관리하는 콘솔 프로그램.

실행: python3 prompt_manager.py
"""

# ------------------------------------------------------
# 상수 / 기본 데이터
# ------------------------------------------------------

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

prompts = [
    {
        "title": "블로그 글 작성 도우미",
        "content": "당신은 10년 경력의 전문 블로거입니다. 주어진 주제에 대해 SEO에 최적화된 블로그 글을 작성해주세요.",
        "category": "텍스트 생성",
        "favorite": False,
    },
    {
        "title": "SULSI 광고 영상 씬 프롬프트",
        "content": "2D 애니메이션 스타일, 신카이 마코토 감성의 4씬 30초 음료 광고. 극한의 청량감을 시각적으로 표현.",
        "category": "영상 생성",
        "favorite": False,
    },
    {
        "title": "노코드 자동화 시나리오 설계",
        "content": "Google Sheets에 새 행이 추가되면 OpenAI로 요약을 생성하고 Discord 웹훅으로 전송하는 Make 시나리오를 설계해주세요.",
        "category": "자동화",
        "favorite": False,
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
    print("0. 종료")

# ------------------------------------------------------
# 프롬프트 추가
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
        elif choice in ("3", "4", "5", "6", "7"):
            print("(아직 구현 예정인 기능입니다)")
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()