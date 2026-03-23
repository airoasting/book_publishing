# AI 책쓰기 프로젝트

## 프로젝트 구조

이 프로젝트는 AI 에이전트 팀이 전문적인 Word 문서(.docx)를 작성하는 프로젝트다.
콘텐츠(제목, 목차, 페르소나, 작성 스타일, 퍼블리싱 사양)는 `.claude/book-toc.md`에 정의되어 있다. 다른 책을 쓸 때는 그 파일만 교체하면 된다.

| 파일 | 역할 | 교체 대상 |
|------|------|-----------|
| `CLAUDE.md` | 프로세스, 범용 규칙 (이 파일) | 아니오 |
| `.claude/book-toc.md` | 제목, 페르소나, 목차, 작성 스타일, 퍼블리싱 사양 | **예** (다른 책 쓸 때 이 파일만 교체) |
| `.claude/skills/*.md` | 단계별 실행 스킬 | 아니오 |

## 작성 규칙 (모든 스킬이 준수)

### 범용 규칙 (어떤 책이든 적용)

1. 문서의 모든 섹션은 `.claude/book-toc.md`의 페르소나로 작성한다
2. 최종 산출물에는 에이전트 내부 역할명이 등장하지 않는다
3. 작성자 표기는 `.claude/book-toc.md`의 "필명"으로만 한다
4. 전문 용어가 나올 때는 괄호 안에 영문을 병기한다
5. 각 장 끝에 수평선(---)을 넣지 않는다. 장 구분은 제목(Heading)으로만 한다
6. 장 제목, 활용법 제목 형식은 `.claude/book-toc.md`의 형식을 따른다
7. 독자 지칭은 `.claude/book-toc.md`의 "독자 지칭"을 따른다
8. 예시의 연도는 `.claude/book-toc.md`의 "기준 연도"를 따른다 (기능 출시일 등 사실 정보는 실제 연도 유지)

### 스타일 규칙 (책마다 다를 수 있음)

`.claude/book-toc.md`의 "작성 스타일" 섹션을 따른다.

## 작업 흐름

4개의 핵심 스킬을 순서대로 실행한다. 각 스킬 내부의 세부 단계는 자동으로 진행된다.
`/cover`는 독립 스킬로, 워크플로우 어느 시점에서든 실행할 수 있다.

각 단계가 완료되면 해당 파일이 정상적으로 저장되었는지 확인한 뒤 다음 단계로 넘어간다. 한 단계가 끝나기 전에 다음 단계를 시작하지 않는다. 대화가 끊기거나 새 세션에서 이어 작업할 때는, 해당 단계의 마지막 저장 파일을 읽고 마지막 작성 지점 이후부터 이어서 작성한다. 기존 내용을 덮어쓰지 않고 이어붙인다(append).

### 핵심 워크플로우 (순서대로)

| 순서 | 스킬 | 내부 단계 | 최종 산출물 |
|------|------|-----------|------------|
| 1 | `/research` | 웹 검색 조사 | `draft/01_research-notes.md` |
| 2 | `/write` | 구조 설계 → 초안 작성 | `draft/02_outline.md`, `draft/03_draft-v1.md` |
| 3 | `/review` | 내부 리뷰(비평, 독자, 합평) → 외부 리뷰(편집자, 마케터, 프루프리더) → 최종 수정 | `draft/04_review-red.md` ~ `draft/14_review-proofreader.md` |
| 4 | `/publish` | Word 변환 → 메타데이터 생성 | `output/final.docx`, `output/metadata.md` |

### 독립 스킬 (언제든 실행)

| 스킬 | 역할 | 최종 산출물 |
|------|------|------------|
| `/cover` | 표지 컨셉 기획 + 이미지 생성 (메인안/대안) | `output/cover_concept.md`, `output/images/cover_a.png`, `cover_b.png` |

### 산출물 번호 체계

draft/ 폴더의 모든 파일은 생성 순서대로 번호가 붙는다.

| 번호 | 파일명 | 스킬 |
|------|--------|------|
| 01 | `01_research-notes.md` | `/research` |
| 02 | `02_outline.md` | `/write` |
| 03 | `03_draft-v1.md` | `/write` |
| 04 | `04_review-red.md` | `/review` |
| 05 | `05_draft-v2.md` | `/review` |
| 06 | `06_review-pink.md` | `/review` |
| 07 | `07_draft-v3.md` | `/review` |
| 08 | `08_ensemble-review-1.md` | `/review` |
| 09 | `09_draft-v4.md` | `/review` |
| 10 | `10_ensemble-review-2.md` | `/review` |
| 11 | `11_draft-final.md` | `/review` |
| 12 | `12_review-editor.md` | `/review` |
| 13 | `13_review-marketer.md` | `/review` |
| 14 | `14_review-proofreader.md` | `/review` |

## 품질 기준

- 문서 구조가 `.claude/book-toc.md`의 목차와 완전히 일치해야 한다
- 문서 분량이 `.claude/book-toc.md`의 목표 분량을 충족해야 한다
- 페르소나가 처음부터 끝까지 일관되어야 한다
- 내부 참조가 실제 내용과 일치해야 한다
- 기능 정보가 문서 전체에서 일관되어야 한다
- [그림] 플레이스홀더는 matplotlib으로 생성한 실제 이미지로 대체한다
- Word 문서에 `**` 마크다운 기호가 남아 있으면 안 된다
