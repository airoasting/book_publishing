---
name: book_publishing
description: "AI 에이전트 팀이 한국어 책 한 권을 리서치부터 Word 문서(.docx)까지 끝까지 쓰는 스킬. 사용자가 '책 써줘', '책쓰기 시작', '리서치 시작해줘', '초안 써줘', '원고 리뷰해줘', '출판해줘', '/research', '/write', '/review', '/publish'라고 하거나 book/user-book-toc.md 기반의 책 작업(집필·리뷰·docx 변환)을 요청하면 반드시 이 스킬을 쓴다. 리서치, 구조 설계와 초안, 9인 리뷰 사이클, 자동 검증과 Word 변환의 4단계를 상태 마커로 이어가며 진행한다."
---

# AI 책쓰기 스킬 (book_publishing)

## 프로젝트 구조

이 스킬은 AI 에이전트 팀이 전문적인 Word 문서(.docx)로 책 한 권을 작성한다.
콘텐츠(제목, 목차, 페르소나, 작성 스타일, 퍼블리싱 사양)는 `book/user-book-toc.md`에 정의되어 있다. 다른 책을 쓸 때는 그 파일만 교체하면 된다.

| 파일 | 역할 | 교체 대상 |
|------|------|-----------|
| `SKILL.md` | 프로세스, 범용 규칙 (이 파일) | 아니오 |
| `book/user-book-toc.md` | 제목, 페르소나, 목차, 작성 스타일, 퍼블리싱 사양 | **예** (다른 책 쓸 때 이 파일만 교체) |
| `references/*.md` | 단계별 실행 문서 (아래 워크플로우에서 로드) | 아니오 |
| `scripts/verify.py` | 원고 자동 검증기 (`/publish` 단계에서 실행) | 아니오 |

## 단계 별칭

아래 문서 전체에서 `/research`, `/write`, `/review`, `/publish`는 각 단계의 별칭이다. 사용자가 별칭을 말하든 "초안 써줘"처럼 자연어로 말하든, 해당 단계의 references 문서를 읽고 그대로 실행한다.

| 별칭 | 실행 문서 |
|------|-----------|
| `/research` | `references/research.md` |
| `/write` | `references/write.md` |
| `/review` | `references/review.md` |
| `/publish` | `references/publish.md` |

references 문서와 `scripts/verify.py`의 경로는 **이 스킬 폴더 기준**이다 (스킬 호출 시 안내되는 Base directory). 작업 산출물(`draft/`, `output/`)은 현재 작업 폴더 기준이다.

`book/user-book-toc.md`는 **현재 작업 폴더에서 먼저 찾고, 없으면 스킬 폴더에서 찾는다**. 두 곳 모두 없으면 작업을 시작하지 않고 사용자에게 파일 위치를 묻는다 (책 정보 없이 진행하면 모든 단계가 잘못된 전제로 돌기 때문이다).

## 작성 규칙 (모든 단계가 준수)

### 범용 규칙 (어떤 책이든 적용)

1. 문서의 모든 섹션은 `book/user-book-toc.md`의 페르소나로 작성한다
2. 최종 산출물에는 에이전트 내부 역할명이 등장하지 않는다
3. 작성자 표기는 `book/user-book-toc.md`의 "필명"으로만 한다
4. 전문 용어가 나올 때는 괄호 안에 영문을 병기한다
5. 각 장 끝에 수평선(---)을 넣지 않는다. 장 구분은 제목(Heading)으로만 한다
6. 장 제목, 활용법 제목 형식은 `book/user-book-toc.md`의 형식을 따른다
7. 독자 지칭은 `book/user-book-toc.md`의 "독자 지칭"을 따른다
8. 예시의 연도는 `book/user-book-toc.md`의 "기준 연도"를 따른다 (기능 출시일 등 사실 정보는 실제 연도 유지)

### 스타일 규칙 (책마다 다를 수 있음)

`book/user-book-toc.md`의 "작성 스타일" 섹션을 따른다.

## 작업 폴더 규칙

### 날짜 기반 프로젝트 폴더

모든 작업 산출물은 **날짜 기반 폴더** 안에 저장한다. 한 권의 책 = 하나의 날짜 폴더.

폴더 명명 규칙:
- 기본: `YYYYMMDD` (예: `20260504`)
- 같은 날 새 프로젝트를 또 시작하면 접미: `YYYYMMDD_01`, `YYYYMMDD_02`, ...
- 날짜는 `bash`의 `date +%Y%m%d`로 얻는다

폴더 구조:
```
draft/
└── 20260504/                  ← 활성 프로젝트 폴더 (이 책 작업 전체가 여기 있음)
    ├── 01_research-notes.md
    ├── 02_outline.md
    ├── 03_draft-v1.md
    ├── 03_draft-v1_part1.md   ← /write 청크 작업 중간물
    ├── 03_draft-v1_part2.md
    ├── ...
    ├── 04_review-red.md
    └── ... (14_review-proofreader.md 까지)

output/
└── 20260504/                  ← 같은 날짜의 출판 산출물
    ├── final.docx
    ├── metadata.md
    ├── verify-report.md
    └── images/
        ├── fig01.png
        ├── fig02.png
        └── ...
```

### 활성 프로젝트 폴더 결정 로직

모든 단계는 시작할 때 다음 규칙으로 "활성 폴더"를 결정한다:

| 단계 | 동작 |
|------|------|
| `/research` | 오늘 날짜의 폴더를 **새로 만든다**. 같은 이름이 이미 있으면 `_01`, `_02`로 접미를 붙인다 |
| `/write`, `/review`, `/publish` | `draft/` 하위 폴더 중 **사전순 가장 최신** 폴더를 활성으로 사용한다 |

`/research`가 새 폴더를 만드는 시점에 동일한 이름의 `output/YYYYMMDD/` 폴더도 함께 만든다 (이미지·docx 출력용).

활성 폴더가 결정되면 그 경로를 사용자에게 한 줄로 알리고 작업을 시작한다:
```
활성 프로젝트 폴더: draft/20260504/
```

## 상태 마커 (Stage Completion Marker)

각 산출물 md 파일이 **완성**되었을 때, 파일 마지막에 다음 한 줄을 추가한다:

```
<!-- STAGE_COMPLETE: 01_research-notes -->
```

`STAGE_COMPLETE:` 뒤의 식별자는 파일명에서 `.md`를 뗀 값과 동일하다 (예: `02_outline`, `03_draft-v1`, `08_ensemble-review-1`).

다음 단계로 넘어갈지 판단할 때 이 마커의 유무를 본다.
- 마커 있음 → 그 단계는 완료된 것으로 본다
- 마커 없음 → 부분 작성 상태로 보고 같은 파일에 이어쓰기(append)한다

부분 작성 상태에서 절대 다음 단계를 시작하지 않는다.

## 작업 흐름

4개의 핵심 단계를 순서대로 실행한다. 각 단계를 시작하기 전에 해당 references 문서를 읽고, 문서 내부의 세부 단계는 자동으로 진행한다.

각 단계가 완료되면 해당 파일의 상태 마커를 확인한 뒤 다음 단계로 넘어간다. 한 단계가 끝나기 전에 다음 단계를 시작하지 않는다. 대화가 끊기거나 새 세션에서 이어 작업할 때는, 활성 폴더를 자동 감지하고 마커가 없는 파일부터 이어쓰기로 재개한다. 기존 내용을 덮어쓰지 않는다.

### 핵심 워크플로우 (순서대로)

표의 경로에서 `{ACTIVE}`는 위 규칙으로 결정되는 활성 프로젝트 폴더(예: `20260504`)를 말한다.

| 순서 | 단계 | 내부 단계 | 최종 산출물 |
|------|------|-----------|------------|
| 1 | `/research` | 웹 검색 조사 | `draft/{ACTIVE}/01_research-notes.md` |
| 2 | `/write` | 구조 설계 → 초안 작성 | `draft/{ACTIVE}/02_outline.md`, `draft/{ACTIVE}/03_draft-v1.md` |
| 3 | `/review` | 내부 리뷰(비평, 독자, 합평) → 외부 리뷰(편집자, 마케터, 프루프리더) → 최종 수정 | `draft/{ACTIVE}/04_review-red.md` ~ `draft/{ACTIVE}/14_review-proofreader.md` |
| 4 | `/publish` | 검증 → Word 변환 → 메타데이터 생성 | `output/{ACTIVE}/final.docx`, `output/{ACTIVE}/metadata.md`, `output/{ACTIVE}/verify-report.md` |

표지는 이 하네스에서 다루지 않는다. 필요하면 외부 도구(예: `adobe-design-from-template`)나 디자이너에게 맡긴다.

### 산출물 번호 체계

활성 폴더 안의 모든 md 파일은 생성 순서대로 번호 prefix를 붙인다.

| 번호 | 파일명 | 단계 | 산출 단계 |
|------|--------|------|-----------|
| 01 | `01_research-notes.md` | `/research` | 웹 조사 |
| 02 | `02_outline.md` | `/write` | 구조 설계 |
| 03 | `03_draft-v1.md` | `/write` | 초안 (Part별 `03_draft-v1_partN.md`로 청크 후 병합) |
| 04 | `04_review-red.md` | `/review` | 내부: 비평가 |
| 05 | `05_draft-v2.md` | `/review` | 내부: 비평 반영 |
| 06 | `06_review-pink.md` | `/review` | 내부: 독자 |
| 07 | `07_draft-v3.md` | `/review` | 내부: 독자 반영 |
| 08 | `08_ensemble-review-1.md` | `/review` | 내부: 합평 1라운드 (5인) |
| 09 | `09_draft-v4.md` | `/review` | 내부: 합평1 반영 |
| 10 | `10_ensemble-review-2.md` | `/review` | 내부: 합평 2라운드 (5인) |
| 11 | `11_draft-final.md` | `/review` | 내부: 합평 통과본 |
| 12 | `12_review-editor.md` | `/review` | 외부: 편집자 |
| 13 | `13_review-marketer.md` | `/review` | 외부: 마케터 (참고용) |
| 14 | `14_review-proofreader.md` | `/review` | 외부: 프루프리더 |

번호는 항상 두 자리(01, 02, ...)이고, 같은 번호의 파일은 덮어쓰기로 갱신한다.

## 품질 기준

- 문서 구조가 `book/user-book-toc.md`의 목차와 완전히 일치해야 한다
- 문서 분량이 `book/user-book-toc.md`의 목표 분량을 충족해야 한다
- 페르소나가 처음부터 끝까지 일관되어야 한다
- 내부 참조가 실제 내용과 일치해야 한다
- 기능 정보가 문서 전체에서 일관되어야 한다
- [그림] 플레이스홀더는 matplotlib으로 생성한 실제 이미지로 대체한다
- Word 문서에 `**` 마크다운 기호가 남아 있으면 안 된다
- em dash(—, –)가 본문에 남아 있으면 안 된다
- 어미는 해라체로 통일되어야 한다 (인용 대화·프롬프트 예시 제외)

이 항목 중 자동 검사 가능한 것은 `/publish` 1단계의 `scripts/verify.py`로 강제한다. verify.py가 강제하는 세부 규칙(어미, em dash 허용, 불릿 기호, 금지 용어, 금지 영어 표현, 부 브릿지 문구)은 `book/user-book-toc.md`의 "## 검증 규칙" 섹션에서 읽는다. 다른 책은 그 섹션만 바꾸면 검사기까지 그 책 기준으로 맞춰지고, 섹션이 없으면 기본값(이 책 기준)으로 동작한다.

## 변경 로그 표준

수정 단계(05, 07, 09, 11번 파일)는 본문 첫머리에 다음 형식의 "변경 로그" 섹션을 둔다.

```markdown
## 변경 로그

| 항목 | 심각도 | 출처 | 반영 | 사유 (미반영 시) |
|------|--------|------|------|------------------|
| 5부 활용법 09 도입부 통계 | 🔴 | 04_review-red | ✅ | |
| 어미 통일 (3장) | 🟡 | 14_review-proofreader | ✅ | |
| 6장 위트 보강 | 🟡 | 12_review-editor | ❌ | 페르소나 톤과 충돌 |
| 5부 챕터 순서 재배치 | 🟢 | 12_review-editor | ❌ | 참고 의견, 미반영 |
```

🔴 항목은 모두 ✅로 끝나야 한다. 🔴이 ❌로 남으면 그 단계는 통과시키지 않는다.

## 백업 정책

다음 트리거에서만 자동 백업한다 (모든 백업은 `{ACTIVE}/_backup/`에 ISO 타임스탬프로 보관).

| 트리거 | 백업 대상 | 백업 파일명 |
|--------|-----------|-------------|
| 합평 3라운드 진입 | `09_draft-v4.md`, `10_ensemble-review-2.md` | `<원본>_YYYYMMDD_HHMM.md` |
| 9단계 최종 수정 시작 전 | `11_draft-final.md` | `11_draft-final_YYYYMMDD_HHMM.md` |
| `/publish` 검증 통과 시점 | `11_draft-final.md` | `11_draft-final_published_YYYYMMDD_HHMM.md` |

`_backup/` 폴더는 `.gitignore`에 포함된다.

## 출처 신뢰도 등급

`/research`가 모은 출처는 다음 3등급으로 표기한다. 합평 5단계의 사실 검증가가 인용 가능 여부를 판단할 때 이 등급을 참조한다.

| 등급 | 의미 | 예시 |
|------|------|------|
| Tier 1 | 1차 자료. 운영사·표준화 기구·정부·공식 발표 | Google 공식 docs, ISO/W3C, 정부 백서 |
| Tier 2 | 2차 자료. 검증된 분석·언론·학술 | 주요 일간지, 학술 논문, IDC/Gartner 리포트 |
| Tier 3 | 3차 자료. 블로그·SNS·익명 게시물 | 개인 블로그, X/Twitter, Reddit |

원칙:
- 본문에 인용되는 정보는 **Tier 1을 최우선**으로 한다
- Tier 3은 사실 주장의 근거로 쓰지 않는다 (트렌드 시그널 정도로만)
- 사실 검증가는 본문의 모든 통계·인용에 대해 인용 등급이 누락되면 🔴, Tier 3 단독 인용이면 🟡로 평가한다

## 자가 채점 (최종 산출물)

`/publish` 1단계 `verify.py`는 종료 시 다음 anchor로 10점 만점 자가 채점을 출력한다.

| 점수 | 결함 상태 |
|------|-----------|
| 10점 | 🔴 0건, 🟡 0건 |
| 9점 | 🔴 0건, 🟡 1~2건 |
| 8점 | 🔴 0건, 🟡 3~5건 |
| 7점 | 🔴 1건 또는 🟡 6~10건 |
| 6점 | 🔴 2건 또는 🟡 11~15건 |
| 5점 이하 | 🔴 3건 이상 |

이 점수는 `output/{ACTIVE}/verify-report.md` 상단에 박힌다. 9점 미만이면 사용자에게 명확히 경고하고 출판을 보류할 것을 권한다.
