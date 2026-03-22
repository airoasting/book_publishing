# 노트북LM 리서치 노트

> 조사일: 2026-03-21
> 조사자: 그린(리서처)
> 목적: "노트북LM으로 다 됨: 팀장을 위한 실전 활용법 20선" 집필을 위한 최신 정보 수집

---

## 1. NotebookLM 개요

### 1.1 정의
NotebookLM은 Google이 개발한 생성형 AI 기반 리서치 도구이다. 사용자가 직접 업로드한 문서(소스)만을 기반으로 요약, 질문 응답, 인사이트 추출 등의 기능을 수행한다. "내 자료만 읽는 AI"라는 점이 ChatGPT, Perplexity 등 범용 AI와의 결정적 차이점이다.

### 1.2 핵심 철학: 소스 기반(Source-Grounded) 설계
- 사용자가 업로드한 소스만 참조하여 답변을 생성한다
- 답변에 숫자로 출처를 표기하며, 클릭하면 원문 해당 위치로 이동한다
- 사용자의 프라이빗 데이터가 모델 학습에 사용되지 않음을 보장한다

### 1.3 접속 및 기본 사용법
- 18세 이상 Google 계정으로 notebooklm.google에 접속하여 사용한다
- 인터페이스 구성: 왼쪽 패널(소스 목록), 중앙 패널(AI 채팅), 오른쪽 패널(노트, 참조, 인용 정보)
- 노트북 생성 후 소스를 업로드하고 질문하는 것이 기본 워크플로우이다

---

## 2. 지원 소스 유형

NotebookLM에 업로드할 수 있는 소스 유형은 다음과 같다:

| 소스 유형 | 설명 |
|-----------|------|
| PDF | 문서, 보고서, 논문 등 |
| Google Docs | 구글 문서 (Drive 연동, 자동 동기화) |
| Google Slides | 구글 슬라이드 |
| Google Sheets | 구글 시트 (2025년 11월 추가) |
| YouTube 동영상 | URL 입력으로 영상 내용 분석 |
| 웹사이트 URL | 웹페이지 내용 분석 |
| 오디오 파일 | 음성 파일 업로드 |
| 이미지 | 이미지 파일 분석 |
| EPUB | 전자책 파일 (2026년 추가) |
| .docx | Word 문서 (2025년 11월 추가) |
| Drive URL | Google Drive 내 PDF 등 |

---

## 3. 요금제 및 플랜별 차이 (2026년 3월 기준)

Google은 NotebookLM을 4개 티어로 구성하고 있다:

| 항목 | Free | Plus | Pro | Ultra |
|------|------|------|-----|-------|
| 월 요금 | 무료 | ~$14/월 | $19.99/월 (Google One AI Premium) | $249.99/월 (Google AI Ultra) |
| 노트북 수 | 100개 | 200개 | 500개 | 500개 |
| 노트북당 소스 수 | 50개 | 100개 | 300개 | 600개 |
| 일일 Audio Overview | 3개 | 확대 | 확대 | 200개 |
| 일일 Video Overview | 제한적 | 확대 | 확대 | 200개 |
| Deep Research | 제한적 | 확대 | 확대 | 200개/일 |
| 일일 채팅 질문 | 제한적 | 확대 | 500개 | 대폭 확대 |
| 워터마크 제거 | X | X | X | O (슬라이드, 인포그래픽) |
| Cinematic Video | X | X | X | O |

- 학생 할인: Google One AI Premium 50% 할인
- 무료 플랜으로도 핵심 기능 대부분을 사용할 수 있다

---

## 4. 2026년 주요 신기능

### 4.1 Cinematic Video Overviews (2026년 3월 4일 출시)
- PDF, 노트, 문서를 완전히 애니메이션화된 내레이션 영상 설명으로 변환하는 기능
- Gemini 3, Nano Banana Pro, Veo 3 등 복합 AI 모델을 사용하여 유동적인 애니메이션과 풍부한 시각 자료를 생성한다
- Gemini가 "크리에이티브 디렉터" 역할을 수행하며, 수백 가지 구조적, 스타일적 결정을 내린다
- Google AI Ultra 구독자($249.99/월)에게 제공되며, 영어로 먼저 출시되었다

### 4.2 Video Overview (기존 기능 강화)
- 텍스트 소스를 설명 영상으로 변환하는 기능
- 2026년에는 슬라이드 기반에서 더 풍부한 시각 표현으로 발전

### 4.3 슬라이드 편집 기능 (2026년 2월)
- AI가 생성한 프레젠테이션을 전체 다시 만들지 않고 개별 슬라이드를 직접 수정할 수 있게 되었다
- 데스크톱과 모바일 모두에서 스타일적, 사실적 피드백을 제출하여 슬라이드를 재생성할 수 있다
- PPTX로 내보내기 가능 (PDF에 추가로)

### 4.4 인포그래픽 스타일 10종 추가
- Sketch Note, Kawaii, Professional, Scientific, Anime, Clay, Editorial, Instructional, Bento Grid, Bricks
- 가로(16:9), 세로(9:16) 형식 모두 지원

### 4.5 EPUB 파일 지원
- 전자책 표준 형식인 EPUB 파일을 소스로 업로드 가능

### 4.6 대화 자동 저장
- 채팅 대화가 자동으로 저장되며, 세션을 닫고 나중에 재개해도 대화 이력이 유지된다

### 4.7 Gemini 100만 토큰 컨텍스트 윈도우
- 모든 플랜에서 Gemini의 전체 100만 토큰 컨텍스트 윈도우가 활성화되었다

### 4.8 플래시카드 및 퀴즈 진행 상황 저장
- 플래시카드와 퀴즈의 진행 상황이 세션 간에 저장되고 로드된다
- "Got it" 또는 "Missed it" 표시, 셔플, 틀린 카드 재실행 등의 기능이 추가되었다

### 4.9 채팅에서 바로 산출물 생성
- 채팅 대화를 Audio Overview, Video Overview, 맞춤 리포트 등으로 즉시 변환 가능

### 4.10 모바일 인포그래픽/슬라이드 커스터마이징
- Android 및 iOS 앱의 Studio 탭에서 연필 아이콘으로 커스터마이징 가능

---

## 5. 핵심 기능 상세

### 5.1 Audio Overview (오디오 오버뷰)
- 업로드한 소스를 두 AI 호스트가 진행하는 팟캐스트 스타일 토론으로 변환한다
- 형식 옵션: Deep Dive(6-15분 포괄적 탐색), Brief(1-2분 간결한 개요) 등 4가지
- 대화형 Audio Overview: "Join" 버튼으로 AI 호스트와 직접 대화에 참여 가능 (2024년 12월 도입)
- 80개 이상의 언어를 지원하며, 한국어 음성 지원 포함
- 커스텀 지시로 톤, 대상 청중, 특정 주제 등을 맞춤 설정 가능

### 5.2 Mind Map (마인드맵)
- 노트북에 포함된 주제의 전체적인 구조를 한눈에 보여주는 시각화 도구
- 복잡한 보고서를 한 장의 구조화된 지도로 변환한다
- 마인드맵을 소스로 재활용하여 2차 분석에 활용 가능

### 5.3 Slide Deck (슬라이드 덱)
- 소스를 기반으로 전문적인 프레젠테이션을 자동 생성한다
- 대상 청중(초보자 vs 전문가, C-레벨 vs 실무자)을 지정하여 맞춤 생성 가능
- 개별 슬라이드 편집 가능 (2026년 업데이트)
- PPTX 및 PDF로 내보내기 지원
- Ultra 플랜에서는 워터마크 제거 가능

### 5.4 Infographic (인포그래픽)
- 복잡한 정보를 시각적으로 자동 표현하는 기능
- 가로(16:9), 세로(9:16) 형식 지원
- 10종의 스타일 선택 가능 (2026년 추가)

### 5.5 Flashcard & Quiz (플래시카드 & 퀴즈)
- 소스 내용을 학습용 플래시카드와 퀴즈로 자동 변환
- 진행 상황 저장, Got it/Missed it 마킹, 셔플, 틀린 카드 재실행 기능

### 5.6 Deep Research (딥 리서치)
- 사용자의 질문을 받아 리서치 계획을 수립하고, 수백 개의 웹사이트를 탐색하여 상세 보고서를 생성한다
- 최대 50개의 소스를 자동으로 수집하고 종합한다
- 보고서와 소스를 노트북에 직접 추가 가능
- Fast Research(소스 목록 제공)와 Deep Research(소스를 읽고 보고서 작성)로 구분된다
- 소스 밖의 정보까지 확장 가능한 유일한 기능

### 5.7 Custom Instructions (맞춤 지시)
- 최대 10,000자의 커스텀 지시를 설정 가능
- 두 가지 수준: 노트북 수준 페르소나 (전체 대화 및 Studio 산출물에 적용), 일회성 채팅 지시 (현재 응답에만 적용)
- AI의 역할, 톤, 대상 청중, 특정 주제 등을 정의 가능
- 같은 소스에서 전혀 다른 결과를 만들 수 있다

### 5.8 Data Table (데이터표)
- 소스 내용을 비교표, 요약표, 타임라인 등으로 구조화
- Google Sheets로 내보내기 가능

### 5.9 Report/Briefing Doc (리포트/브리핑 문서)
- 소스를 기반으로 구조화된 보고서, 브리핑 문서, 학습 가이드 등을 자동 생성

---

## 6. 공유 및 협업 기능

### 6.1 노트북 공유
- Share 버튼으로 "Viewer"(읽기 전용) 또는 "Editor"(편집 가능) 권한을 부여할 수 있다
- Editor는 소스와 노트를 추가/삭제하고, 다른 사용자에게 공유를 확장할 수 있다
- 노트북을 공개(Public)로 설정하여 Google 계정이 있는 누구나 접근하도록 할 수 있다

### 6.2 Google Docs 연동
- Google Docs와 Slides를 소스로 직접 가져오면 Drive에서 문서를 편집할 때 NotebookLM 분석에 자동 반영된다
- Studio Panel에서 Study Guide, Briefing Docs, Notes 등을 Google Docs 또는 Sheets로 내보내기 가능
- 단, 내보낸 문서의 수정은 원본 NotebookLM에 동기화되지 않는다
- 공유 권한도 내보내기 시 별도로 설정해야 한다

---

## 7. NotebookLM vs ChatGPT vs Perplexity vs Claude 비교

| 비교 항목 | NotebookLM | ChatGPT | Perplexity | Claude |
|-----------|------------|---------|------------|--------|
| 데이터 소스 | 사용자 업로드 소스만 | 학습 데이터 + 웹 검색 | 실시간 웹 검색 | 학습 데이터 + 파일 업로드 |
| 핵심 강점 | 소스 기반 분석, 환각 최소화 | 범용 콘텐츠 생성, 아이디어 발상 | 실시간 정보 검색, 출처 인용 | 긴 문서 분석, 코딩 |
| 프라이버시 | 데이터 학습에 미사용 보장 | 옵트아웃 필요 | 검색 기록 저장 | 옵트아웃 가능 |
| 최적 사용 사례 | 내부 문서 분석, 리서치 정리 | 창의적 글쓰기, 코딩, 다목적 | 최신 정보 검색, 팩트체크 | 장문 분석, 코딩, 추론 |
| 멀티미디어 출력 | 오디오, 비디오, 슬라이드, 인포그래픽 | 텍스트, 이미지 | 텍스트, 출처 링크 | 텍스트, 코드 |

### 역할 분담 패턴
1. Perplexity로 최신 정보를 넓게 수집하고, NotebookLM으로 정리/분석한다
2. ChatGPT로 창의적 아이디어를 발상하고, NotebookLM으로 관련 자료를 구조화한다
3. Claude로 깊은 분석/추론을 하고, NotebookLM으로 팀과 공유할 산출물을 만든다

---

## 8. 한국어 지원 현황 및 한계

### 8.1 지원 현황
- 오디오 및 비디오 오버뷰를 포함하여 80개 이상의 언어를 지원한다
- 한국어 음성 지원: 문서나 YouTube 자료를 한국어 팟캐스트로 변환 가능
- 설정에서 출력 언어를 '한국어'로 변경 가능

### 8.2 알아야 할 한계점
1. 한국어 문서의 미묘한 뉘앙스를 놓칠 수 있다
2. AI 생성 결과물을 세밀하게 편집하고 확장하기에는 한계가 있다
3. 일부 최신 기능(Cinematic Video 등)은 영어 우선 출시

---

## 9. 환각(Hallucination) 대응

### 9.1 설계적 대응
- 소스 기반 설계로 환각 현상을 근본적으로 최소화한다
- 2026년 업데이트에서 환각 현상이 현저히 줄어들었다 (이전 모델 대비 약 40% 속도 향상과 함께)

### 9.2 팩트체크 방법
- 답변의 숫자 출처를 클릭하면 원문 해당 위치로 이동하여 즉시 검증 가능
- Google 공식 안내: "NotebookLM이 부정확한 정보를 표시할 수 있으므로 답변을 다시 한번 확인" 권고

### 9.3 소스 밖 질문 대처
- NotebookLM은 소스에 없는 정보에 대해 "모른다"고 답한다
- Deep Research 기능을 활용하면 소스 밖 웹 정보까지 확장 가능

---

## 10. 소스 제한 우회 및 팁

### 10.1 소스 50개 제한 우회
- 여러 문서를 하나의 PDF로 합쳐서 업로드한다
- 핵심 내용만 추출하여 요약본을 소스로 사용한다
- 여러 노트북을 목적별로 분리하여 운영한다

### 10.2 노트북 간 교차 불가 대처
- 한 노트북의 결과물(노트)을 다른 노트북에 소스로 업로드하는 방식으로 우회한다
- Google Docs로 내보낸 뒤 다른 노트북에 소스로 추가한다

---

## 11. 기업 활용 사례

### 11.1 마케팅 팀장의 팀 지식 관리
- 팀원들이 제출하는 기획서, 보고서, 회의록을 노트북에 모아 팀 지식 관리 시스템으로 활용
- "자료 찾기"와 "반복 질문" 문제를 해결

### 11.2 EV 제조사 Rivian
- 기술 문서에서 창의적 계획으로 수분 내에 이동할 수 있도록 활용
- 제품 팀이 혁신에 더 많은 시간을 쓸 수 있게 됨

### 11.3 온보딩 및 지식베이스
- 사내 문서를 모아 "팀만의 AI 비서" 구축
- 팀원들이 같은 노트북에 접속하여 AI에게 질문하고 필요한 정보를 스스로 탐색

---

## 12. 소스 출처

- [What's New in NotebookLM (2026)](https://levelup.gitconnected.com/whats-new-in-notebooklm-2026-a-deep-dive-into-its-latest-features-4c73ac6dee8a)
- [Google Blog: Cinematic Video Overviews](https://blog.google/innovation-and-ai/products/notebooklm/generate-your-own-cinematic-video-overviews-in-notebooklm/)
- [9to5Google: NotebookLM Cinematic Video](https://9to5google.com/2026/03/04/notebooklm-cinematic-video-overviews-ai-mode/)
- [Google Workspace Updates](https://workspaceupdates.googleblog.com/2026/03/new-ways-to-customize-and-interact-with-your-content-in-NotebookLM.html)
- [NotebookLM 고객센터](https://support.google.com/notebooklm/?hl=ko)
- [NotebookLM Plans](https://notebooklm.google/plans)
- [NotebookLM Limits Explained](https://elephas.app/blog/notebooklm-source-limits)
- [Google Blog: Audio Overviews](https://blog.google/technology/ai/notebooklm-audio-overviews/)
- [Google Blog: Deep Research](https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-deep-research-file-types/)
- [NotebookLM vs ChatGPT (2026)](https://toolscompare.ai/compare/notebooklm-vs-chatgpt)
- [DigitalOcean: What Is NotebookLM](https://www.digitalocean.com/resources/articles/what-is-notebooklm)
- [노트북LM 마케팅 팀장 활용법](https://peekaboolabs.ai/blog/notebooklm-marketing-team-productivity)
- [NotebookLM Advanced Guide 2026](https://www.shareuhack.com/en/posts/notebooklm-advanced-guide-2026)
- [Google Cloud: Share Notebooks](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/share-notebooks)
- [NotebookLM Custom Instructions](https://www.ai-supremacy.com/p/notebooklm-custom-instructions)
