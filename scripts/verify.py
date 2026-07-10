"""book-writing harness verifier, standalone copy used by /publish 1단계.
This file lives in scripts/ as the canonical verifier.
/publish runs this file when generating verify-report.md.

책마다 달라지는 검사 규칙(금지 용어, 어미, em dash 허용 여부, 불릿 기호, 금지 영어 표현,
부 브릿지 문구)은 user-book-toc.md의 "## 검증 규칙" 섹션에서 읽는다. 그 섹션이나 개별 항목이
없으면 아래 기본값(이 책, NotebookLM 기준)으로 폴백하므로, 규칙을 지워도 검사기는 돈다.
덕분에 다른 책은 toc 한 파일만 바꾸면 검사기까지 그 책 기준으로 맞춰진다.
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

# ---------------------------------------------------------------------------
# 검증 규칙 로드 — user-book-toc.md "## 검증 규칙" 섹션을 정본으로 삼는다.
# 섹션이나 개별 항목이 없으면 기본값(이 책 기준)을 쓴다. 규칙을 지워도 검사기가 멈추지 않는다.
# ---------------------------------------------------------------------------
RULES = {
    "어미": "해라체",
    "em dash 허용": "아니오",
    "불릿 기호": "•",
    "금지 용어": "커스텀 지시 → 맞춤 지시",
    "금지 영어 표현": "Before/After → 사용 전/후",
    "부 브릿지 문구": "N부를 마치며",
}

rules_sec = re.search(r"^#+\s*검증\s*규칙\s*$(.*?)(?:^#+\s|\Z)", toc, re.M | re.S)
if rules_sec:
    for line in rules_sec.group(1).splitlines():
        line = line.strip().lstrip("-").strip()
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.split("#")[0].strip()  # 값 뒤 주석(#...) 제거
        if key in RULES and val:
            RULES[key] = val

def _parse_pairs(spec):
    """'A → B; C → D' 형식을 [(A, B), ...]로. 화살표는 →, ->, ⇒ 모두 허용."""
    pairs = []
    for chunk in spec.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = re.split(r"\s*(?:→|->|⇒)\s*", chunk, maxsplit=1)
        wrong = parts[0].strip()
        right = parts[1].strip() if len(parts) > 1 else ""
        if wrong:
            pairs.append((wrong, right))
    return pairs

allow_emdash = RULES["em dash 허용"].strip() in ("예", "yes", "허용", "true", "True")
ending = RULES["어미"].strip()
bullet = (RULES["불릿 기호"].strip() or "•")[0]
banned_terms = _parse_pairs(RULES["금지 용어"])
banned_english = _parse_pairs(RULES["금지 영어 표현"])
bridge_tmpl = RULES["부 브릿지 문구"].strip() or "N부를 마치며"

# 1) em dash 잔존 (규칙: em dash 허용)
if not allow_emdash:
    for m in re.finditer(r"[—–]", text):
        issues.append(("🔴", "em dash 잔존", f"위치 {m.start()}"))

# 2) ** 마크다운 잔존 (보편 규칙 — 어떤 책이든 마크다운 아티팩트는 남으면 안 된다)
for m in re.finditer(r"\*\*[^*\n]+\*\*", text):
    issues.append(("🔴", "마크다운 ** 잔존", m.group(0)[:30]))

# 3) [그림 N] 참조 수 (정보)
fig_refs = re.findall(r"\[그림\s*(\d+)[^\]]*\]", text)
issues.append(("ℹ️", "[그림 N] 참조 수", str(len(fig_refs))))

# 4) 어미 통일성 (규칙: 어미). 문장 끝 '다'로 끝나는 종결을 모집단으로,
#    지정한 어미가 아닌 종결이 5%를 넘으면 🟡. (해라체 ↔ 합쇼체 혼용 감지)
#    합쇼체 종결은 '습니다'와 '~ㅂ니다(입니다·갑니다·합니다)'를 함께 잡으려고 '니다'로 센다.
da_endings = len(re.findall(r"다[\.!?]", text))
hap = len(re.findall(r"니다[\.!?]", text))
hae = max(0, da_endings - hap)
if ending == "합쇼체":
    intrusion, base, other = hae, da_endings, "해라체"
else:  # 기본: 해라체
    intrusion, base, other = hap, da_endings, "합쇼체"
if base and intrusion / base > 0.05:
    issues.append(("🟡", "어미 혼용 의심", f"{other} 종결 {intrusion}/{base}"))

# 5) 분량 검증 — 기본 정보의 '목표 분량 ... N~N자'
char_count = len(re.sub(r"\s", "", text))
m = re.search(r"목표 분량.*?([\d,]+)\s*[~∼-]\s*([\d,]+)\s*자", toc)
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
#    "## 목차" 섹션에서 부/장/활용법/프롤로그/에필로그/부록 같은 '구조 라벨'을 뽑아,
#    본문에 그 라벨이 실제로 등장하는지 확인한다. 제목 문구 전체가 아니라 라벨로 대조하므로
#    (예: "제3부", "[활용법 07]") 목차 표기가 책마다 달라도, 띄어쓰기가 달라도 동작한다.
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

# 7) 상태 마커 확인 (하네스 보편)
if "<!-- STAGE_COMPLETE: 11_draft-final -->" not in text:
    issues.append(("🔴", "상태 마커 누락", "11_draft-final 미완료"))

# 8) 부 끝 브릿지 (규칙: 부 브릿지 문구 — N은 부 번호 자리표시자)
parts_in_toc = sorted(set(int(n) for n in re.findall(r"제\s*(\d+)\s*부", toc)))
for n in parts_in_toc:
    variants = {
        bridge_tmpl.replace("N", str(n)),
        bridge_tmpl.replace("N", f"제{n}"),
        bridge_tmpl.replace("N", f"제 {n}"),
    }
    if not any(v in text for v in variants):
        issues.append(("🟡", "브릿지 문단 누락 의심", bridge_tmpl.replace("N", str(n))))

# 9) 금지 용어 (규칙: 금지 용어) — 🔴
for wrong, right in banned_terms:
    if wrong in text:
        detail = f"'{wrong}'" + (f" → '{right}'" if right else "")
        issues.append(("🔴", "용어 위반", detail))

# 10) 불릿 부호 (규칙: 불릿 기호) — 지정 기호 외 타이포 불릿이 섞이면 🟡.
#     한국어 가운뎃점(·)은 정상 표기라 검출 목록에서 제외한다.
typo_bullets = ["●", "○", "▪", "▫", "■", "□", "◆", "◇", "‣", "⁃"]
for sym in typo_bullets:
    if sym != bullet and sym in text:
        issues.append(("🟡", "불릿 부호 비통일", f"'{sym}' 사용 (지정 기호 '{bullet}')"))

# 11) 금지 영어 표현 (규칙: 금지 영어 표현) — 🟡
for wrong, right in banned_english:
    if wrong in text:
        detail = f"'{wrong}'" + (f" → '{right}'" if right else "")
        issues.append(("🟡", "영어 표현 과다", detail))

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
