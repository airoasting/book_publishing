# 노트북LM으로 다 됨: 팀장을 위한 실전 활용법 20선

> AI 도구에 관심은 있지만 기술 배경이 없는 팀장을 위한 노트북LM 실전 가이드북

## 프로젝트 개요

이 프로젝트는 Google NotebookLM의 실전 활용법 20가지를 정리한 B5 판형(240~250페이지) 분량의 도서 원고입니다.

- **저자**: AI ROASTING
- **대상 독자**: AI 도구에 관심이 있지만 기술 배경이 없는 팀장
- **구성**: 프롤로그 + 7부(20개 활용법) + 에필로그 + 부록
- **판형**: B5 (176mm x 250mm)

## 목차 구성

| 구분 | 제목 | 내용 |
|------|------|------|
| 프롤로그 | 일하는 방식, 노트북LM 이전과 이후로 나뉩니다 | 저자 소개, 책의 방향 |
| 제1부 | 고수는 이렇게 씁니다 | 4명의 실전 사례 (제1장~제4장) |
| 제2부 | 오늘 점심, 딱 한 번만 따라 하세요 | 시작하기 가이드 (제5장~제7장) |
| 제3부 | 분석과 검증의 기술 | 활용법 01~05 |
| 제4부 | 혼자 소화하는 기술 | 활용법 06~08 |
| 제5부 | 남에게 보여주는 기술 | 활용법 09~11 |
| 제6부 | 월요일 아침부터 바로 쓰는 실전 시나리오 | 활용법 12~16 |
| 제7부 | 나에서 팀으로, 도구에서 시스템으로 | 활용법 17~20 |
| 에필로그 | 지금 노트북을 여십시오 | 마무리 메시지 |
| 부록 | A~D + 참고문헌 | 프롬프트 템플릿, FAQ 등 |

## 에이전트 팀

이 프로젝트는 6명의 내부 에이전트와 3명의 외부 검증자가 협업하여 제작했습니다.

### 내부 에이전트 (6명)

| 에이전트 | 역할 | 담당 |
|----------|------|------|
| 그린 | 리서처 | 웹 검색으로 최신 정보 조사 |
| 실버 | 아키텍트 | 문서 구조와 목차 설계 |
| 블랙 | 라이터 | 프롤로그~부록 전체 집필 및 수정 |
| 레드 | 리뷰어 | 논리적 허점 비평 |
| 핑크 | 예상독자 | 팀장 관점 리뷰 |
| 라이트 | 퍼블리셔 | Word 문서 변환 및 서식 적용 |

### 외부 검증자 (3명)

| 검증자 | 역할 | 평가 기준 |
|--------|------|-----------|
| 편집자 | 출판 편집 | 구성력, 서사력, 톤 일관성, 완성도 등 8개 기준 |
| 마케터 | 시장성 평가 | 타겟 명확성, 제목 파워, SNS 잠재력 등 8개 기준 |
| 프루프리더 | 교정교열 | 맞춤법, 비문, 용어 일관성, 부호 사용 등 8개 기준 |

## 작업 흐름 (16단계)

```
1단계  그린 리서치 → research-notes.md
2단계  실버 구조 설계 → outline.md
3단계  블랙 초안 작성 → draft-v1.md
4단계  레드 비평 → review-red.md
5단계  블랙 1차 수정 → draft-v2.md
6단계  핑크 독자 리뷰 → review-pink.md
7단계  블랙 2차 수정 → draft-v3.md
8단계  합평 1라운드 (5명) → ensemble-review-1.md
9단계  블랙 3차 수정 → draft-v4.md
10단계 합평 2라운드 (5명) → ensemble-review-2.md
11단계 블랙 최종 반영 → draft-final.md
12단계 라이트 퍼블리싱 → NotebookLM_final.docx
13단계 편집자 평가 → review-editor.md
14단계 마케터 평가 → review-marketer.md
15단계 프루프리더 교정 → review-proofreader.md
16단계 블랙 최종 보강 → draft-final.md (갱신)
```

## 폴더 구조

```
.
├── CLAUDE.md                    # 프로젝트 지시 문서
├── README.md                    # 이 파일
├── .gitignore
├── draft/                       # 중간 산출물
│   ├── research-notes.md        # 리서치 결과
│   ├── outline.md               # 문서 구조 설계
│   ├── draft-v1.md              # 초안
│   ├── draft-v2.md              # 1차 수정본
│   ├── draft-v3.md              # 2차 수정본
│   ├── draft-v4.md              # 3차 수정본
│   ├── draft-final.md           # 최종 원고
│   ├── review-red.md            # 레드 비평
│   ├── review-pink.md           # 핑크 리뷰
│   ├── ensemble-review-1.md     # 합평 1라운드
│   ├── ensemble-review-2.md     # 합평 2라운드
│   ├── review-editor.md         # 편집자 평가
│   ├── review-marketer.md       # 마케터 평가
│   └── review-proofreader.md    # 프루프리더 평가
└── output/                      # 최종 산출물
    ├── NotebookLM_final.docx    # 최종 Word 문서
    ├── NotebookLM_final.pdf     # 최종 PDF
    ├── generate_docx.py         # Word 문서 생성 스크립트
    ├── generate_images.py       # 다이어그램 생성 스크립트
    ├── workflow-summary.md      # 작업 현황표
    └── images/                  # 다이어그램 이미지
        ├── fig01.png ~ fig39.png
        └── org_chart.png
```

## 기술 스택

- **원고 작성**: Markdown
- **문서 생성**: python-docx (Python)
- **다이어그램**: matplotlib (Python)
- **폰트**: Pretendard (대체: 맑은 고딕)

## 라이선스

이 프로젝트의 모든 콘텐츠는 AI ROASTING에게 저작권이 있습니다.
