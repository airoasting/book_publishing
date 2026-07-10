"""book-writing harness verifier, standalone copy used by /publish 1단계.
This file lives in scripts/ as the canonical verifier.
/publish runs this file when generating verify-report.md.
"""
import re, sys, pathlib

if len(sys.argv) != 4:
    print("usage: verify.py <draft-final.md> <user-book-toc.md> <verify-report.md>", file=sys.stderr)
    sys.exit(2)

SRC = pathlib.Path(sys.argv[1])
TOC = pathlib.Path(sys.argv[2])
REPORT = pathlib.Path(sys.argv[3])

text = SRC.read_text(encoding="utf-8")
toc = TOC.read_text(encoding="utf-8")

issues = []  # [(severity, category, detail)]

# 1) em dash 잔존
for m in re.finditer(r"[—–]", text):
    issues.append(("🔴", "em dash 잔존", f"위치 {m.start()}"))

# 2) ** 마크다운 잔존
for m in re.finditer(r"\*\*[^*\n]+\*\*", text):
    issues.append(("🔴", "마크다운 ** 잔존", m.group(0)[:30]))

# 3) [그림 N] 참조 수
fig_refs = re.findall(r"\[그림\s*(\d+)[^\]]*\]", text)
issues.append(("ℹ️", "[그림 N] 참조 수", str(len(fig_refs))))

# 4) 어미 통일성 (간이 검사)
total_sentences = len(re.findall(r"[.!?]", text))
hapsoche = len(re.findall(r"습니다[\.\?\!]", text))
if total_sentences and hapsoche / total_sentences > 0.05:
    issues.append(("🟡", "합쇼체 혼용 의심", f"{hapsoche}/{total_sentences} 문장"))

# 5) 분량 검증
char_count = len(re.sub(r"\s", "", text))
m = re.search(r"목표 분량.*?([\d,]+)\s*[~∼]\s*([\d,]+)\s*자", toc)
if m:
    lo = int(m.group(1).replace(",", ""))
    hi = int(m.group(2).replace(",", ""))
    if char_count < lo:
        issues.append(("🔴", "분량 미달", f"{char_count}자 < {lo}자 (목표 {lo}~{hi})"))
    else:
        issues.append(("ℹ️", "분량", f"{char_count}자 (목표 {lo}~{hi})"))
else:
    issues.append(("ℹ️", "분량", f"{char_count}자"))

# 6) 목차 항목 누락 검사
#    목차 파일의 "## 목차" 섹션에서 부/장/활용법/프롤로그/에필로그/부록 같은 '구조 라벨'을
#    뽑아, 본문에 그 라벨이 실제로 등장하는지 확인한다. 제목 문구 전체가 아니라 라벨로 대조하므로
#    (예: "제3부", "[활용법 07]") 책마다 목차 표기가 조금씩 달라도, 띄어쓰기가 달라도 동작한다.
#    라벨은 한 챕터·활용법·부가 통째로 빠졌는지를 잡는 가장 안정적인 신호다.
def _despace(s):
    return re.sub(r"\s+", "", s)

toc_body = toc
sec = re.search(r"^#+\s*목차\s*$(.*?)(?:^#+\s|\Z)", toc, re.M | re.S)
if sec:
    toc_body = sec.group(1)  # 페르소나·작성 가이드 문구를 제외해 오탐을 줄인다

text_nospace = _despace(text)
seen_labels = set()
expected_labels = []  # (표시용 라벨, 본문에서 찾을 문자열)

def _add_label(display, needle):
    if display not in seen_labels:
        seen_labels.add(display)
        expected_labels.append((display, needle))

for n in re.findall(r"제\s*(\d+)\s*부", toc_body):
    _add_label(f"제{n}부", f"제{n}부")
for n in re.findall(r"제\s*(\d+)\s*장", toc_body):
    _add_label(f"제{n}장", f"제{n}장")
for n in re.findall(r"\[\s*활용법\s*(\d+)\s*\]", toc_body):
    _add_label(f"[활용법 {n}]", f"활용법{n}")
for kw in ["프롤로그", "에필로그", "부록"]:
    if kw in toc_body:
        _add_label(kw, kw)

for display, needle in expected_labels:
    if _despace(needle) not in text_nospace:
        issues.append(("🔴", "목차 항목 누락", display))

# 7) 상태 마커 확인
if "<!-- STAGE_COMPLETE: 11_draft-final -->" not in text:
    issues.append(("🔴", "상태 마커 누락", "11_draft-final 미완료"))

# 8) 부 끝 브릿지
parts_in_toc = re.findall(r"제\s*(\d+)\s*부", toc)
unique_parts = sorted(set(int(n) for n in parts_in_toc))
for n in unique_parts:
    if (f"{n}부를 마치며" not in text and
        f"제{n}부를 마치며" not in text and
        f"제 {n}부를 마치며" not in text):
        issues.append(("🟡", "브릿지 문단 누락 의심", f"{n}부 마치며"))

# 9) 용어 통일 — "커스텀 지시" 사용 금지
if "커스텀 지시" in text:
    issues.append(("🔴", "용어 위반", "'커스텀 지시' → '맞춤 지시'"))

# 10) 불릿 부호 — • 외 사용 (●, ▪) 검사
forbidden_bullets = ["●", "▪"]
for sym in forbidden_bullets:
    if sym in text:
        issues.append(("🟡", "불릿 부호 비통일", f"'{sym}' 사용"))

# 11) 영어 단독 표현 비율 (간이): "Before" / "After" 단독 사용
for w in ["Before/After", "Before / After"]:
    if w in text:
        issues.append(("🟡", "영어 표현 과다", f"'{w}' → '사용 전/후'"))

# 12) 자가 채점 (10점 만점) — SKILL.md "자가 채점" anchor를 그대로 따른다.
#     🔴과 🟡이 각각 허용하는 점수 상한을 따로 구한 뒤 더 낮은 쪽으로 확정한다.
#     한쪽이 심각하면 다른 쪽이 깨끗해도 점수가 끌려 내려가야 하기 때문이다
#     (예: 🔴 4건이면 🟡이 0건이어도 4점을 넘지 못한다).
red = sum(1 for s,_,_ in issues if s == "🔴")
yellow = sum(1 for s,_,_ in issues if s == "🟡")
info = sum(1 for s,_,_ in issues if s == "ℹ️")

if red == 0:
    red_cap = 10
elif red == 1:
    red_cap = 7
elif red == 2:
    red_cap = 6
else:  # 🔴 3건 이상
    red_cap = max(1, 5 - (red - 3))

if yellow == 0:
    yellow_cap = 10
elif yellow <= 2:
    yellow_cap = 9
elif yellow <= 5:
    yellow_cap = 8
elif yellow <= 10:
    yellow_cap = 7
elif yellow <= 15:
    yellow_cap = 6
else:  # 🟡 16건 이상
    yellow_cap = 5

score = min(red_cap, yellow_cap)

# 보고서 출력
lines = [
    "# verify-report",
    "",
    f"- 🔴 필수: {red}건",
    f"- 🟡 권장: {yellow}건",
    f"- ℹ️ 정보: {info}건",
    f"- **자가 채점: {score} / 10**",
    "",
    "## 상세",
]
for s, cat, detail in issues:
    lines.append(f"- {s} **{cat}** — {detail}")

REPORT.write_text("\n".join(lines), encoding="utf-8")
print(f"verify done: 🔴 {red}, 🟡 {yellow}, ℹ️ {info}, score={score}/10")
sys.exit(1 if red > 0 else 0)
