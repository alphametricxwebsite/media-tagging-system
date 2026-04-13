"""
Agentic AI Tagging System for Media Intelligence
Obsidian Ink Theme · Crisp Modern Design
Split-screen: Results + Chat Agent
Built with Streamlit + Claude API
"""
import streamlit as st
import json, time, re, zipfile, csv
import xml.etree.ElementTree as ET
from io import BytesIO, StringIO
from datetime import datetime

st.set_page_config(page_title="Media Intelligence Agent", page_icon="🏷️", layout="wide", initial_sidebar_state="expanded")

# ============================================================
# CLEAN LIGHT DASHBOARD — SOFT CARDS, PASTEL ACCENTS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #f2f3f7; }
header[data-testid="stHeader"] { background: #f2f3f7 !important; }
.block-container { padding-top: 1rem !important; max-width: 100% !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e8e9ee !important;
    box-shadow: 2px 0 12px rgba(0,0,0,0.03) !important;
}
section[data-testid="stSidebar"] * { color: #4a5568 !important; }
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] strong { color: #1a202c !important; }

#MainMenu, footer { visibility: hidden; }

/* === HEADER === */
.main-header {
    background: #ffffff;
    border: 1px solid #e8e9ee;
    border-radius: 20px;
    padding: 1.1rem 1.8rem;
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.main-header .icon { font-size: 1.6rem; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.main-header h1 { color: #1a202c; font-size: 1.3rem; font-weight: 700; margin: 0; }
.main-header p { color: #8892a4; font-size: 0.8rem; margin: 0.1rem 0 0 0; }

/* === STATUS BAR === */
.status-bar {
    background: #ffffff;
    border: 1px solid #e8e9ee;
    border-radius: 14px;
    padding: 0.55rem 1.1rem;
    margin-bottom: 0.8rem;
    display: flex; align-items: center; gap: 0.7rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.03);
}
.status-dot { width: 8px; height: 8px; border-radius: 50%; }
.status-dot-done { background: #48bb78; box-shadow: 0 0 6px rgba(72,187,120,0.4); }
.status-dot-processing { background: #ecc94b; box-shadow: 0 0 6px rgba(236,201,75,0.4); animation: pulse 1.5s ease-in-out infinite; }
.status-dot-error { background: #fc8181; box-shadow: 0 0 6px rgba(252,129,129,0.4); }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.4;} }
.status-text { font-size: 0.8rem; font-weight: 600; color: #2d3748; }
.status-detail { font-size: 0.72rem; color: #a0aec0; margin-left: auto; font-family: 'JetBrains Mono', monospace; }

/* === STAT CHIPS === */
.stat-chip {
    display: inline-flex; align-items: center; gap: 0.35rem;
    background: linear-gradient(135deg, rgba(255,235,245,0.6), rgba(235,245,255,0.6));
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 14px; padding: 0.5rem 0.9rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.03);
    backdrop-filter: blur(8px);
}
.stat-chip .stat-num { font-size: 1.15rem; font-weight: 800; color: #1a202c; }
.stat-chip .stat-label { font-size: 0.62rem; color: #a0aec0; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }

/* === ARTICLE CARDS — soft pastel gradient glass === */
.article-card {
    background: linear-gradient(135deg, rgba(255,230,240,0.5) 0%, rgba(230,240,255,0.5) 40%, rgba(220,245,255,0.5) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 18px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.55rem;
    transition: all 0.25s ease;
    position: relative;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.article-card:hover {
    box-shadow: 0 8px 28px rgba(0,0,0,0.08);
    transform: translateY(-2px);
    border-color: rgba(200,180,220,0.5);
}
.article-card .card-num {
    position: absolute; top: 0.5rem; right: 0.7rem;
    font-size: 0.6rem; font-weight: 700; color: #d0d5dd;
    font-family: 'JetBrains Mono', monospace;
}
.article-card .pub-name {
    font-size: 0.68rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;
    color: #667eea; margin-bottom: 0.25rem;
}
.article-card .headline { font-size: 0.88rem; font-weight: 600; color: #1a202c; margin-bottom: 0.4rem; line-height: 1.35; }
.article-card .headline a { color: #1a202c; text-decoration: none; }
.article-card .headline a:hover { color: #667eea; text-decoration: underline; }

/* === PAYWALL CARD — BOLD AMBER HIGHLIGHT === */
.article-card-paywall {
    background: #fffbf0 !important;
    border: 2px solid #f6ad55 !important;
    border-left: 5px solid #ed8936 !important;
}
.article-card-paywall::after {
    content: '🔒 PAYWALL';
    position: absolute; top: 0; right: 0;
    background: linear-gradient(135deg, #ed8936, #f6ad55);
    color: #fff; font-size: 0.58rem; font-weight: 800;
    padding: 0.2rem 0.7rem 0.2rem 0.5rem;
    border-radius: 0 16px 0 10px;
    letter-spacing: 0.06em;
    box-shadow: 0 2px 8px rgba(237,137,54,0.3);
}
.paywall-banner {
    background: #fef3cd;
    border: 1px solid #fbd38d;
    border-radius: 8px;
    padding: 0.2rem 0.6rem;
    font-size: 0.65rem; font-weight: 600; color: #c05621;
    margin-bottom: 0.3rem;
    display: inline-block;
}

/* === TAG CHIPS — soft pastel on white === */
.tag-chip {
    display: inline-block; padding: 0.18rem 0.55rem; border-radius: 8px;
    font-size: 0.63rem; font-weight: 600; margin: 0.08rem 0.08rem;
}
.tag-positive { background: #f0fff4; color: #276749; border: 1px solid #c6f6d5; }
.tag-negative { background: #fff5f5; color: #9b2c2c; border: 1px solid #fed7d7; }
.tag-neutral { background: #f7fafc; color: #718096; border: 1px solid #e2e8f0; }
.tag-topic { background: #ebf4ff; color: #3182ce; border: 1px solid #bee3f8; }
.tag-paywall { background: #fffaf0; color: #c05621; border: 1px solid #feebc8; }
.tag-translated { background: #faf5ff; color: #6b46c1; border: 1px solid #e9d8fd; }
.tag-expansion { background: #e6fffa; color: #234e52; border: 1px solid #b2f5ea; }
.tag-ceo { background: #fff5f7; color: #b83280; border: 1px solid #fed7e2; }
.tag-high { background: #f0fff4; color: #276749; border: 1px solid #c6f6d5; }
.tag-medium { background: #fffaf0; color: #c05621; border: 1px solid #feebc8; }
.tag-low { background: #fff5f5; color: #9b2c2c; border: 1px solid #fed7d7; }

/* === CHAT === */
.chat-header {
    background: #ffffff;
    border: 1px solid #e8e9ee;
    border-radius: 16px;
    padding: 0.7rem 1rem; margin-bottom: 0.5rem;
    display: flex; align-items: center; gap: 0.5rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.03);
}
.chat-header .dot { width: 8px; height: 8px; border-radius: 50%; background: #48bb78; box-shadow: 0 0 6px rgba(72,187,120,0.4); }
.chat-header h3 { margin: 0; font-size: 0.82rem; font-weight: 700; color: #1a202c; }
.chat-header span { font-size: 0.68rem; color: #a0aec0; }

[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #e8e9ee !important;
    border-radius: 14px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.02) !important;
}
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] li, [data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] strong, [data-testid="stChatMessage"] em { color: #2d3748 !important; }

/* === BUTTONS === */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: 0 3px 12px rgba(102,126,234,0.3) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover { box-shadow: 0 5px 20px rgba(102,126,234,0.45) !important; transform: translateY(-1px) !important; }
.stDownloadButton > button {
    background: #ffffff !important;
    color: #4a5568 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important; font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}
.stDownloadButton > button:hover {
    border-color: #667eea !important; color: #667eea !important;
    box-shadow: 0 3px 12px rgba(102,126,234,0.12) !important;
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    border-radius: 14px; padding: 0.25rem; gap: 0.15rem;
    border: 1px solid #e8e9ee;
    box-shadow: 0 1px 4px rgba(0,0,0,0.02);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important; font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important; font-size: 0.76rem !important; color: #8892a4 !important;
    padding: 0.4rem 0.8rem !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: #fff !important; font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(102,126,234,0.25) !important;
}

.stRadio label {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important; color: #4a5568 !important;
}

[data-testid="stFileUploader"] {
    background: #ffffff;
    border: 2px dashed #d0d5dd;
    border-radius: 16px; padding: 0.5rem;
}

.stProgress > div > div > div { background: linear-gradient(90deg, #667eea, #764ba2) !important; border-radius: 6px !important; }

[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; border: 1px solid #e8e9ee; box-shadow: 0 1px 6px rgba(0,0,0,0.03); }

/* All text */
.stApp p, .stApp span, .stApp li, .stApp div, .stApp label { color: #4a5568; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown strong { color: #1a202c !important; }
.stCode, code, pre { color: #2d3748 !important; background: #f7fafc !important; border: 1px solid #e2e8f0 !important; }
[data-testid="stAlert"] p, [data-testid="stAlert"] div { color: #2d3748 !important; }
.stCaption, [data-testid="stCaptionContainer"] p { color: #a0aec0 !important; }
.stSpinner > div, .stSpinner > div > div { color: #667eea !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #d0d5dd; border-radius: 3px; }

.upload-panel {
    background: linear-gradient(135deg, rgba(255,230,240,0.4) 0%, rgba(230,240,255,0.4) 50%, rgba(220,250,250,0.4) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 18px; padding: 2.5rem; text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.upload-panel .icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
.upload-panel .title { font-size: 1rem; font-weight: 600; color: #1a202c; margin-bottom: 0.2rem; }
.upload-panel .sub { font-size: 0.78rem; color: #a0aec0; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# PAYWALL BLOCKLIST
# ============================================================
PAYWALL_DOMAINS = {
    'bloomberg.com','wsj.com','ft.com','economist.com','barrons.com','reuters.com',
    'nytimes.com','washingtonpost.com','businessinsider.com','fortune.com','forbes.com',
    'hbr.org','cnbc.com','seekingalpha.com','tikr.com','morningstar.com','zacks.com',
    'investopedia.com','thestreet.com','marketwatch.com','ainvest.com','stockstory.org',
    'simplywall.st','bitget.com','achrnews.com','contractingbusiness.com','hpac.com',
    'apnews.com','afp.com','ad-hoc-news.de','handelsblatt.com',
}

def is_paywall_url(url):
    if not url: return False
    url_lower = url.lower()
    for domain in PAYWALL_DOMAINS:
        if domain in url_lower: return True
    return False


# ============================================================
# PUBLICATION NAME NORMALIZATION (Fix #6)
# ============================================================
KNOWN_PUBLICATIONS = {
    'bloomberg': 'Bloomberg', 'reuters': 'Reuters', 'cnbc': 'CNBC',
    'the wall street journal': 'The Wall Street Journal', 'wsj': 'The Wall Street Journal',
    'the new york times': 'The New York Times', 'nyt': 'The New York Times',
    'the washington post': 'The Washington Post', 'forbes': 'Forbes',
    'fortune': 'Fortune', 'business insider': 'Business Insider',
    'the economist': 'The Economist', 'financial times': 'Financial Times',
    'associated press': 'Associated Press', 'ap news': 'AP News',
    'yahoo finance': 'Yahoo Finance', 'yahoo! finance': 'Yahoo Finance',
    'seeking alpha': 'Seeking Alpha', 'marketwatch': 'MarketWatch',
    'barron\'s': "Barron's", 'barrons': "Barron's",
    'morningstar': 'Morningstar', 'investopedia': 'Investopedia',
    'the motley fool': 'The Motley Fool', 'motley fool': 'The Motley Fool',
    'pr newswire': 'PR Newswire', 'business wire': 'Business Wire',
    'globe newswire': 'GlobeNewsWire', 'globenewswire': 'GlobeNewsWire',
    'achr news': 'ACHR News', 'achrnews': 'ACHR News',
    'contracting business': 'Contracting Business',
    'hpac engineering': 'HPAC Engineering', 'hpac': 'HPAC Engineering',
    'the air conditioning, heating & refrigeration news': 'ACHR News',
    'hvac insider': 'HVAC Insider', 'supply house times': 'Supply House Times',
    'cooling post': 'Cooling Post', 'the cooling post': 'Cooling Post',
    'zacks investment research': 'Zacks Investment Research', 'zacks': 'Zacks Investment Research',
    'stock story': 'StockStory', 'stockstory': 'StockStory',
    'ainvest': 'AInvest', 'simply wall st': 'Simply Wall St',
    'handelsblatt': 'Handelsblatt', 'afp': 'AFP',
}

def normalize_publication_name(pub):
    """Convert ALL CAPS pub names to proper case, using known mappings where possible."""
    if not pub: return pub
    pub_stripped = pub.strip()
    # Check known mappings (case-insensitive)
    lookup = pub_stripped.lower()
    if lookup in KNOWN_PUBLICATIONS:
        return KNOWN_PUBLICATIONS[lookup]
    # If it's ALL CAPS, convert to title case
    if pub_stripped == pub_stripped.upper() and len(pub_stripped) > 3:
        return pub_stripped.title()
    return pub_stripped


# ============================================================
# DOCX PARSER (unchanged logic)
# ============================================================
def parse_docx(file_bytes, filename=""):
    articles = []
    monitor_date = extract_monitor_date(filename)
    with zipfile.ZipFile(BytesIO(file_bytes)) as z:
        rels_xml = z.read("word/_rels/document.xml.rels")
        rels_root = ET.fromstring(rels_xml)
        hyperlinks = {}
        for rel in rels_root:
            if 'hyperlink' in rel.attrib.get('Type', '').lower():
                hyperlinks[rel.attrib.get('Id', '')] = rel.attrib.get('Target', '')
        doc_xml = z.read("word/document.xml")
        root = ET.fromstring(doc_xml)
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
              'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
        tables = root.findall('.//w:tbl', ns)
        if not tables: return [], monitor_date
        rows = tables[0].findall('.//w:tr', ns)
        current_section = "Trane Technologies"
        for ri, row in enumerate(rows):
            cells = row.findall('.//w:tc', ns)
            if not cells: continue
            paragraphs = cells[0].findall('.//w:p', ns)
            para_data = []
            # Track field code state ACROSS paragraphs (fldChar begin/end can span P1→P2)
            in_field = False
            field_url = ''
            field_text_parts = []
            field_start_para = -1
            for pi, p in enumerate(paragraphs):
                parts, hl_list = [], []
                # Method 1: Standard w:hyperlink elements
                for hl in p.findall('./w:hyperlink', ns):
                    rid = hl.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', '')
                    hl_t = ''.join(t.text for r in hl.findall('.//w:r', ns) for t in r.findall('.//w:t', ns) if t.text).strip()
                    url = hyperlinks.get(rid, '')
                    if hl_t or url: hl_list.append({'text': hl_t, 'url': url}); parts.append(hl_t)
                # Method 2: Field code hyperlinks (fldChar + instrText)
                runs = p.findall('./w:r', ns)
                for r in runs:
                    fld = r.find('.//w:fldChar', ns)
                    instr = r.find('.//w:instrText', ns)
                    if fld is not None:
                        fld_type = ''
                        for attr_key in fld.attrib:
                            if 'fldCharType' in attr_key:
                                fld_type = fld.attrib[attr_key]
                        if fld_type == 'begin':
                            in_field = True; field_url = ''; field_text_parts = []; field_start_para = pi
                        elif fld_type == 'separate':
                            pass
                        elif fld_type == 'end':
                            if field_url:
                                ft = ''.join(field_text_parts).strip()
                                if ft or field_url:
                                    if field_start_para == pi:
                                        hl_list.append({'text': ft, 'url': field_url})
                                        parts.append(ft)
                                    elif field_start_para >= 0 and field_start_para < len(para_data):
                                        para_data[field_start_para]['hyperlinks'].append({'text': ft, 'url': field_url})
                                        para_data[field_start_para]['text'] = (para_data[field_start_para]['text'] + ' ' + ft).strip()
                            in_field = False; field_url = ''; field_text_parts = []; field_start_para = -1
                    elif instr is not None and instr.text:
                        m = re.search(r'HYPERLINK\s+"([^"]+)"', instr.text)
                        if m: field_url = m.group(1)
                    elif in_field and field_url:
                        for t in r.findall('.//w:t', ns):
                            if t.text: field_text_parts.append(t.text)
                    else:
                        if not in_field:
                            for t in r.findall('.//w:t', ns):
                                if t.text: parts.append(t.text)
                para_data.append({'text': ''.join(parts).strip(), 'hyperlinks': hl_list})
            full = ' '.join(p['text'] for p in para_data).strip()
            fl = full.lower()
            if ri < 3: continue
            if 'benchmark companies' in fl: current_section = "Benchmark Companies"; continue
            if 'trends' in fl and ('issues' in fl or 'government' in fl): current_section = "Trends / Issues / Government Relations"; continue
            if fl in ('trane technologies', 'trane tech'): current_section = "Trane Technologies"; continue
            if not full or len(full) < 10: continue
            article = parse_article_cell(para_data, current_section, monitor_date)
            if article:
                articles.append(article)
                for exp in parse_expansion_pubs(para_data):
                    exp.update({'section': current_section, 'monitor_date': monitor_date,
                               'parent_headline': article['headline'], 'parent_summary': article.get('summary','')})
                    articles.append(exp)
    return articles, monitor_date

def extract_monitor_date(fn):
    """Extract monitor date from filename. Tries MM.DD.YY, MM.DD.YYYY, MM-DD-YY, etc."""
    names = {'01':'Jan.','02':'Feb.','03':'Mar.','04':'Apr.','05':'May','06':'Jun.',
             '07':'Jul.','08':'Aug.','09':'Sep.','10':'Oct.','11':'Nov.','12':'Dec.'}
    # Try MM.DD.YYYY or MM.DD.YY patterns
    for pat in [r'(\d{1,2})[._-](\d{1,2})[._-](\d{4})', r'(\d{1,2})[._-](\d{1,2})[._-](\d{2})']:
        m = re.search(pat, fn)
        if m:
            g1, g2, g3 = m.group(1).zfill(2), m.group(2).zfill(2), m.group(3)
            # g1=month, g2=day, g3=year
            month_str = names.get(g1, g1)
            day = int(g2)
            return f"{month_str} {day}"
    return ""

def parse_article_cell(para_data, section, monitor_date):
    if len(para_data) < 2: return None
    pub, hl, hl_url, summary, is_trans = "", "", "", "", False
    state = "pub"
    for p in para_data:
        text, hls = p['text'].strip(), p['hyperlinks']
        if not text: continue
        if text.lower().startswith('translated from'): is_trans = True; continue
        if 'also covered by' in text.lower(): continue
        if state == "pub":
            if not hls and text.upper() == text and len(text) < 100: pub = text; state = "headline"
            elif hls: pub = ""; hl = hls[0]['text']; hl_url = hls[0]['url']; state = "summary"
            else: pub = text; state = "headline"
        elif state == "headline":
            if hls: hl = hls[0]['text']; hl_url = hls[0]['url']
            else: hl = text
            state = "summary"
        elif state == "summary":
            if text.lower().startswith('summary:'): summary = text[8:].strip()
            elif text.lower() == 'summary:': continue
            elif not summary and not text.lower().startswith('this story'): summary += (" "+text) if summary else text
    if not pub and not hl: return None
    # Fix #2: For paywall articles (no URL), still keep the headline text from the docx
    # Fix #3: is_paywall is determined by blocklist later, not by absence of URL
    # Some articles legitimately have no hyperlink in the docx but have a headline
    # Fix #6: Normalize publication name from ALL CAPS
    pub = normalize_publication_name(pub)
    return {'publication': pub, 'headline': hl, 'url': hl_url, 'summary': summary[:1500],
            'section': section, 'monitor_date': monitor_date, 'is_translated': is_trans,
            'is_paywall': False, 'is_expansion': False}

def parse_expansion_pubs(para_data):
    exps = []
    for p in para_data:
        if 'also covered by' not in p['text'].lower(): continue
        for hl in p['hyperlinks']:
            if hl['text'] and hl['url']:
                exps.append({'publication': hl['text'], 'headline': '', 'url': hl['url'],
                            'summary': '', 'is_translated': False, 'is_paywall': False, 'is_expansion': True})
    return exps


# ============================================================
# TAGGER (parallel batching, confidence, Haiku fallback)
# ============================================================
def safe_extract_text(response):
    text = ""
    if not hasattr(response, 'content'): return text
    for block in response.content:
        bt = getattr(block, 'text', None)
        if bt is not None and isinstance(bt, str): text += bt
    return text

def _process_single_batch(client, batch, batch_num, total_batches, analyst_examples):
    sp = build_system_prompt(analyst_examples)
    # Enable web_search for: articles with URLs to read, AND articles without URLs that need searching
    has_url_articles = any(a.get('url') and not is_paywall_url(a.get('url','')) for a in batch)
    has_no_url_articles = any(not a.get('url') and not a.get('is_paywall') for a in batch)
    needs_web = has_url_articles or has_no_url_articles
    result = {'batch_num': batch_num, 'tagged': [], 'ok': False}
    try:
        atxt = build_articles_text(batch, summary_only=False)
        up = build_user_prompt(len(batch), atxt)
        kwargs = dict(model="claude-sonnet-4-20250514", max_tokens=4096, system=sp, messages=[{"role":"user","content":up}])
        if needs_web: kwargs['tools'] = [{"type":"web_search_20250305","name":"web_search"}]
        r = client.messages.create(**kwargs)
        parsed = extract_json(safe_extract_text(r))
        if parsed: merge_results(result['tagged'], batch, parsed); result['ok'] = True; return result
    except Exception: pass
    try:
        atxt2 = build_articles_text(batch, summary_only=True)
        up2 = build_user_prompt(len(batch), atxt2)
        r2 = client.messages.create(model="claude-haiku-4-5-20251001", max_tokens=4096, system=sp, messages=[{"role":"user","content":up2}])
        parsed2 = extract_json(safe_extract_text(r2))
        if parsed2: merge_results(result['tagged'], batch, parsed2); result['ok'] = True; return result
    except Exception: pass
    for a in batch: a['tags_failed'] = True; result['tagged'].append(a)
    return result

def tag_articles_batch(articles, api_key, analyst_examples="", progress_callback=None):
    import anthropic
    from concurrent.futures import ThreadPoolExecutor, as_completed
    client = anthropic.Anthropic(api_key=api_key)
    BATCH_SIZE, MAX_PARALLEL = 8, 3
    tagged, batches = [], [articles[i:i+BATCH_SIZE] for i in range(0, len(articles), BATCH_SIZE)]
    total_batches = len(batches)
    if progress_callback: progress_callback(0.05, f"Processing {len(articles)} articles in {total_batches} batches...")
    ok, fail, completed = 0, 0, 0
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL) as executor:
        futures = {executor.submit(_process_single_batch, client, b, bn, total_batches, analyst_examples): bn for bn, b in enumerate(batches, 1)}
        for future in as_completed(futures):
            completed += 1; pct = 0.05 + (completed / total_batches) * 0.90
            try:
                result = future.result(); tagged.extend(result['tagged'])
                if result['ok']: ok += 1
                else: fail += 1
                if progress_callback: progress_callback(pct, f"Batch {completed}/{total_batches} done ({ok} OK)")
            except Exception:
                fail += 1
                if progress_callback: progress_callback(pct, f"Batch error — {completed}/{total_batches}")
    if progress_callback: progress_callback(1.0, f"Done! {ok}/{total_batches} batches OK.")
    # Post-processing: fix common AI output issues
    tagged = post_process_tagged(tagged)
    return tagged


def post_process_tagged(tagged):
    """Fix common issues in AI-tagged output."""
    from datetime import datetime
    today_str = datetime.now().strftime('%b. %-d')  # e.g., "Apr. 9"
    today_alt = datetime.now().strftime('%B %-d')  # e.g., "April 9"

    seen_keys = set()
    deduped = []
    for art in tagged:
        # Fix None/missing sentiment — default to Neutral
        brands = art.get('brands', {})
        for bname, bdata in brands.items():
            if isinstance(bdata, dict):
                sent = bdata.get('sentiment', '')
                if not sent or sent == 'None' or sent not in ('Positive', 'Negative', 'Neutral'):
                    bdata['sentiment'] = 'Neutral'

        # Fix date_published — if it's today's date or empty, use monitor_date
        dp = art.get('date_published', '')
        if not dp or dp == 'None' or dp == today_str or dp == today_alt:
            md = art.get('monitor_date', '')
            if md:
                art['date_published'] = md
            # else leave as-is

        # Normalize publication name
        pub = art.get('publication', '')
        if pub:
            art['publication'] = normalize_publication_name(pub)

        # Fix article_or_pr — ensure it's never empty
        if not art.get('article_or_pr') or art['article_or_pr'] == 'None':
            art['article_or_pr'] = 'Article'

        # Deduplicate exact duplicate entries (same headline + pub + url)
        # NOTE: The same article CAN and SHOULD appear in multiple brand tabs.
        # We only remove cases where the AI/parser returned the exact same article
        # object multiple times in the results (e.g., batch overlap or AI duplication).
        hl = (art.get('headline', '') or '').strip().lower()
        pub_key = (art.get('publication', '') or '').strip().lower()
        url_key = (art.get('url', '') or '').strip().lower()
        dedup_key = f"{pub_key}|||{hl}|||{url_key}"
        if dedup_key in seen_keys and hl:
            continue  # Skip exact duplicate entry
        if hl:
            seen_keys.add(dedup_key)

        deduped.append(art)

    return deduped

def build_articles_text(batch, summary_only=False):
    text = ""
    for j, art in enumerate(batch):
        md = art.get('monitor_date', '')
        text += f"\n--- ARTICLE {j+1} ---\nPublication: {art['publication']}\nHeadline: {art['headline']}\nURL: {art.get('url','NONE')}\nSection: {art['section']}\nMonitor Date: {md}\n"
        url = art.get('url',''); blocked = is_paywall_url(url)
        if summary_only or blocked:
            # Truly paywalled — use summary only
            s = art.get('summary','') or art.get('parent_summary','')
            text += f"PAYWALLED - Tag from summary only:\n{s[:800]}\n"
            art['is_paywall'] = True
        elif not url:
            # No URL in docx but NOT paywalled — search for it by headline
            s = art.get('summary','') or art.get('parent_summary','')
            text += f"NO URL IN DOCUMENT - Search for this article by headline to find the actual URL and publication date. Use web_search with the headline.\n"
            text += f"Summary for context: {s[:600]}\n"
            text += f"IMPORTANT: Return the actual article URL in the 'url' field so we can hyperlink the headline.\n"
        else:
            # Has URL — read the full article
            text += f"HAS URL - Read full article via web search. Extract the actual article publication date.\n"
            if art.get('summary'): text += f"Backup summary: {art['summary'][:500]}\n"
    return text

def build_user_prompt(count, atxt):
    return f"""Tag these {count} articles. Read URLs via web_search where indicated.

{atxt}

Respond ONLY with JSON array. No markdown. Each item:
{{"publication":"Proper Title Case Name","headline":"...","url":"...","date_published":"Mon. DD","article_or_pr":"Article",
"brands":{{"Trane Technologies":{{"sentiment":"Positive/Negative/Neutral","mentioned":true/false}},"Carrier":{{"sentiment":"...","mentioned":true/false}},"Honeywell":{{"sentiment":"...","mentioned":true/false}},"JCI":{{"sentiment":"...","mentioned":true/false}},"Daikin":{{"sentiment":"...","mentioned":true/false}},"Lennox":{{"sentiment":"...","mentioned":true/false}}}},
"topics":{{"Sustainability":true/false,"Decarbonization":true/false,"Innovation":true/false,"Energy Efficiency":true/false,"Digitization":true/false,"Electrification":true/false,"Workforce Development":true/false,"Financial Performance":true/false,"No Category Match":true/false}},
"confidence":{{"sentiment":"high/medium/low","topics":"high/medium/low","overall":"high/medium/low"}},
"ceo_mention":"","is_paywall":true/false,"publication_flagged":true/false}}

CRITICAL REMINDERS:
- date_published: Extract the ACTUAL article publication date from the article content. Format: "Mon. DD" (e.g., "Mar. 15", "Feb. 8"). If the article says "March 15, 2026" → "Mar. 15". If the article says "15 March 2026" → "Mar. 15". NEVER use today's date as a default. If you truly cannot determine the date, use the monitor date from the section header.
- Publication names in PROPER title case (not ALL CAPS). Convert ALL CAPS to proper case.
- publication_flagged=true if pub name is unfamiliar or you're unsure of correct format.
- article_or_pr: Default "Article". Only "Press Release" for content from PR wire services (PR Newswire, Business Wire, GlobeNewsWire, ACCESS Newswire, EIN Presswire, OpenPR) or official company newsroom posts with PR formatting.
- Sentiment MUST always be one of: "Positive", "Negative", or "Neutral". Never null/empty/None.
- Sentiment is BRAND-SPECIFIC. A stock article with favorable outlook = Positive for that brand. "Faces Pressure" = Negative.
- Topics: Tag ONLY when a tracked brand is taking CONCRETE ACTION (not planning/aspiring). A stock decline article about Carrier should be tagged "Financial Performance" ONLY, not Digitization/Electrification unless the article specifically discusses those topics.
- ALL stock/financial/investment coverage → Financial Performance = true. If stock article ALSO discusses specific topics (sustainability initiatives, new products), tag those too. But don't add topics just because the company works in that space.
- CEO: ONLY flag CEOs of the 6 tracked brands (Trane Technologies, Carrier, Honeywell, JCI, Daikin, Lennox). AHRI, industry association, or other company CEOs = leave empty "".
- No topic match → "No Category Match": true (and all other topics false).
- Each article should appear ONCE in the JSON array. Do not duplicate articles.
CONFIDENCE: high=clear evidence, medium=inferred, low=guessing."""

def build_system_prompt(examples=""):
    base = """You are a Media Intelligence Tagging Agent for Trane Technologies.
Tag HVAC/climate articles with structured metadata + confidence scores.

=== BRANDS ===
The 6 tracked brands: Trane Technologies (includes METUS, Mitsubishi Electric Trane, Thermo King), Carrier, Honeywell, JCI (Johnson Controls), Daikin, Lennox.
Set "mentioned": true ONLY for brands that are actually named or discussed in the article. If an article is purely about Carrier's stock, ONLY Carrier.mentioned=true. Do NOT set mentioned=true for brands that are not in the article.

=== SENTIMENT RULES ===
Sentiment MUST be brand-specific and reflect how the coverage portrays that brand:
- Positive: Coverage portrays the brand favorably — awards, growth, innovation, positive stock outlook, product wins, executive praise.
- Negative: Coverage portrays the brand unfavorably — lawsuits, recalls, poor earnings, layoffs, scandals, downgrades, stock pressure.
- Neutral: Brand is mentioned factually without positive or negative framing, or brand is mentioned only in passing.

IMPORTANT NUANCES (learned from analyst patterns):
- "Faces Pressure" / "Headwinds" / "Slowdown" in a stock headline = NEGATIVE for that brand, not Neutral
- "Why It Shines" / "Smart Investors" / "Monster Win" / "Can't Stop Buying" = depends on article content:
  * If article discusses sustainability/innovation/growth alongside stock → POSITIVE
  * If article is purely a stock clickbait aggregator with no substance → NEUTRAL
- Stock articles about Nvidia/Jensen Huang impacting HVAC cooling stocks = NEUTRAL (external market force, not brand-specific)
- Sentiment MUST always be "Positive", "Negative", or "Neutral". NEVER null or empty.

=== TOPIC DEFINITIONS & ACTIONABLE CODING RULE ===
Topics MUST be tagged in the context of the tracked brands mentioned in the article. The brand must be DOING something related to the topic, not just adjacent to it.

CRITICAL ACTIONABLE RULE: Only tag a topic if the article describes CONCRETE ACTIONS TAKEN or CURRENTLY UNDERWAY — not plans, intentions, goals, or aspirations.
- "Company X plans to reduce emissions" = NOT Sustainability (just planning)
- "Company X reduced emissions by 30% this year" = Sustainability (action taken)
- "Company X is investing in heat pump manufacturing" = Electrification (action underway)
- "Company X aims to electrify its product line" = NOT Electrification (just an aim)

This actionable rule applies to ALL topics below:

1. Sustainability — Climate change ACTION: A tracked brand is actively implementing sustainability initiatives, has achieved sustainability milestones, or is executing climate programs. NOT just stating goals.
2. Decarbonization — Reducing carbon emissions: A tracked brand is actively reducing carbon footprint, implementing low-carbon tech, has achieved emission reductions. NOT just pledging to decarbonize.
3. Innovation — Advancing HVAC tech: A tracked brand is launching new products, deploying new technology, has patents or R&D breakthroughs. NOT just talking about future innovation.
4. Energy Efficiency — Optimized energy use: A tracked brand is delivering measurably more efficient products/systems, implementing efficiency upgrades. NOT just promising efficiency.
5. Digitization — Digital tech, AI, IoT: A tracked brand is deploying digital solutions, AI, smart building tech, connected systems. NOT just exploring digital options.
6. Electrification — Electrification of heat: A tracked brand is manufacturing/deploying heat pumps, electric HVAC, converting from gas to electric. NOT just considering electrification.
7. Workforce Development — Training, upskilling: A tracked brand is running training programs, hiring initiatives, apprenticeships, DEI programs. NOT just announcing workforce plans.
8. Financial Performance — Revenue, earnings, stock: Coverage discusses a tracked brand's financial results, stock performance, market cap, analyst ratings, earnings, revenue, acquisitions, deals. ALL stock-related coverage must be tagged Financial Performance.
9. No Category Match — Use ONLY when none of the above 8 topics apply. Broader HVAC industry news that doesn't fit specific categories.

CRITICAL TOPIC RULES:
- A stock/financial article should ONLY get Financial Performance unless the article ALSO substantively discusses specific topics (sustainability programs, new products, etc.)
- Do NOT tag Digitization/Electrification/Innovation just because a company operates in that space. The ARTICLE must discuss those topics specifically.
- "No Category Match" is used liberally — tangential articles, industry mentions, electromobility in general, unrelated awards, etc.
- An article can have MULTIPLE topics (e.g., Sustainability + Decarbonization + Energy Efficiency + Financial Performance) if it genuinely covers all of them.

=== CEO / EXECUTIVE MENTION ===
ONLY flag CEO mentions for the 6 tracked brands' CEOs/executives:
- Trane Technologies CEO (Dave Regnery), Carrier CEO, Honeywell CEO, JCI CEO, Daikin CEO, Lennox CEO
- Use "CEO mention" if the CEO is named/referenced
- Use "CEO quote" if the CEO is directly quoted
- Use "CEO interview" if the article is an interview with the CEO
- Leave EMPTY ("") if no tracked brand CEO is mentioned. Do NOT flag AHRI, industry association, supplier, or other company CEOs.

=== PUBLICATION NAMES ===
Use proper mixed-case publication names as they appear on the publication's own website. NOT all-caps.
If the publication name from the parsed document is ALL CAPS, convert it to proper title case.
Flag: set "publication_flagged": true if you encounter a publication you haven't seen before or if the name seems unusual.

=== ARTICLE vs PRESS RELEASE ===
Default is "Article". Only classify as "Press Release" if:
- Content is from a PR wire service: PR Newswire, Business Wire, GlobeNewsWire, ACCESS Newswire, EIN Presswire, OpenPR
- Content is from a company's own newsroom with PR formatting
- Content reads as an official company announcement, not a journalist's reporting
If in doubt, classify as "Article".

=== DATE FORMAT ===
date_published should be in format: "Mon. DD" (e.g., "Apr. 7", "Mar. 15"). Use 3-letter month abbreviation with period, space, then day number without leading zero.
CRITICAL: Extract the ACTUAL publication date from the article. NEVER default to today's date.

ALWAYS respond with ONLY valid JSON array."""
    if examples: base += f"\nANALYST EXAMPLES:\n{examples}"
    return base

def merge_results(tagged, batch, parsed):
    for j, td in enumerate(parsed):
        if j < len(batch):
            orig = batch[j]
            # Start with parser data, overlay AI tags
            m = {**orig, **td}
            # ALWAYS preserve parser's authoritative metadata fields
            m['monitor_date'] = orig.get('monitor_date', '')
            m['section'] = orig.get('section', '')
            m['is_translated'] = orig.get('is_translated', False)
            m['is_expansion'] = orig.get('is_expansion', False)
            # URL: Use parser's URL if it exists (extracted from docx hyperlink).
            # If parser had NO URL, use the AI's URL (found via web_search).
            orig_url = (orig.get('url', '') or '').strip()
            ai_url = (td.get('url', '') or '').strip()
            if orig_url:
                m['url'] = orig_url
            elif ai_url and ai_url.lower() not in ('none', 'null', ''):
                m['url'] = ai_url
            else:
                m['url'] = ''
            # Headline: Prefer parser's headline (from docx), fall back to AI's
            orig_hl = (orig.get('headline', '') or orig.get('parent_headline', '') or '').strip()
            ai_hl = (td.get('headline', '') or '').strip()
            m['headline'] = orig_hl if orig_hl else ai_hl
            # Publication: Prefer parser's publication, fall back to AI's
            orig_pub = (orig.get('publication', '') or '').strip()
            ai_pub = (td.get('publication', '') or '').strip()
            m['publication'] = orig_pub if orig_pub else ai_pub
            tagged.append(m)
    for j in range(len(parsed), len(batch)): batch[j]['tags_failed'] = True; tagged.append(batch[j])

def extract_json(text):
    if not text or not text.strip(): return None
    text = re.sub(r'```json\s*','',text); text = re.sub(r'```\s*','',text); text = text.strip()
    s, e = text.find('['), text.rfind(']')
    if s >= 0 and e > s:
        try:
            r = json.loads(text[s:e+1])
            if isinstance(r, list): return r
        except json.JSONDecodeError: pass
    try:
        r = json.loads(text)
        if isinstance(r, list): return r
    except json.JSONDecodeError: pass
    return None


# ============================================================
# CHAT AGENT
# ============================================================
def process_chat_command(user_msg, tagged_articles, api_key):
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    articles_summary = []
    for i, art in enumerate(tagged_articles):
        td = art.get('topics', {}); conf = art.get('confidence', {})
        active = [t for t, v in td.items() if v]
        articles_summary.append(f"[{i+1}] {art.get('publication','')} — \"{art.get('headline','')[:70]}\" | Topics: {', '.join(active) or 'None'} | Conf: {conf.get('overall','?')} | PW: {art.get('is_paywall',False)} | CEO: {art.get('ceo_mention','')}")
    system = f"""You are an AI assistant helping a media analyst review tagged articles.
{len(tagged_articles)} articles tagged. Current state:
{chr(10).join(articles_summary)}

Commands: CHANGE tags, QUERY articles, EXPLAIN reasoning, BULK ops, GENERATE Excel.
For changes: {{"action":"update","changes":[{{"article_index":0,"field":"topics.Sustainability","value":true}}]}}
For export: {{"action":"generate"}}
Be concise."""
    try:
        r = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=2000, system=system, messages=[{"role":"user","content":user_msg}])
        return safe_extract_text(r)
    except Exception as e: return f"Error: {str(e)[:100]}"

def apply_chat_changes(tagged_articles, response_text):
    changes_made = 0
    try:
        start = response_text.find('{"action"')
        if start < 0: return 0
        depth = 0
        for i in range(start, len(response_text)):
            if response_text[i] == '{': depth += 1
            elif response_text[i] == '}': depth -= 1
            if depth == 0:
                data = json.loads(response_text[start:i+1])
                if data.get('action') == 'update':
                    for ch in data.get('changes', []):
                        idx, field, val = ch.get('article_index', -1), ch.get('field', ''), ch.get('value')
                        if 0 <= idx < len(tagged_articles) and field:
                            parts = field.split('.'); obj = tagged_articles[idx]
                            for p in parts[:-1]:
                                if p not in obj: obj[p] = {}
                                obj = obj[p]
                            obj[parts[-1]] = val; changes_made += 1
                elif data.get('action') == 'generate': return -1
                break
    except (json.JSONDecodeError, ValueError): pass
    return changes_made


# ============================================================
# EXCEL + CSV GENERATORS
# ============================================================
def generate_excel(tagged_articles, monitor_date):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    wb = Workbook()
    brands = ['Trane Technologies','Carrier','Honeywell','JCI','Daikin','Lennox']
    topics = ['Sustainability','Decarbonization','Innovation','Energy Efficiency','Digitization',
              'Electrification','Workforce Development','Financial Performance','No Category Match']
    headers = ['Monitor Date','Date Published','Publication','Headline','Article OR Press Release',
               'Sentiment'] + topics + ['CODED?','CEO/Executive Mention']
    hf=Font(name='Calibri',bold=True,size=10,color='FFFFFF')
    hfl=PatternFill(start_color='1e1e2a',end_color='1e1e2a',fill_type='solid')
    df=Font(name='Calibri',size=10);lf=Font(name='Calibri',size=10,color='6366F1',underline='single')
    pf=PatternFill(start_color='FFF2CC',end_color='FFF2CC',fill_type='solid')
    pub_flag_fill=PatternFill(start_color='FFFF00',end_color='FFFF00',fill_type='solid')  # Bright yellow for flagged publications
    bd=Border(left=Side(style='thin',color='D9D9D9'),right=Side(style='thin',color='D9D9D9'),top=Side(style='thin',color='D9D9D9'),bottom=Side(style='thin',color='D9D9D9'))
    wb.remove(wb.active)
    ws_tot=wb.create_sheet("Totals");ws_tot['B2']='Honeywell';ws_tot['C2']='Carrier';ws_tot['D2']='JCI';ws_tot['E2']='Daikin';ws_tot['F2']='Lennox';ws_tot['G2']='Trane'
    for brand in brands:
        ws=wb.create_sheet(brand)
        for ci,h in enumerate(headers,1):c=ws.cell(row=1,column=ci,value=h);c.font=hf;c.fill=hfl;c.alignment=Alignment(horizontal='center',wrap_text=True);c.border=bd
        ws.column_dimensions['A'].width=12;ws.column_dimensions['B'].width=14;ws.column_dimensions['C'].width=22;ws.column_dimensions['D'].width=55;ws.column_dimensions['E'].width=18;ws.column_dimensions['F'].width=12
        for ci in range(7,16):ws.column_dimensions[chr(64+ci)].width=14
        ws.column_dimensions['P'].width=8;ws.column_dimensions['Q'].width=20
        ba=get_brand_articles(tagged_articles,brand)
        for ri,art in enumerate(ba,2):
            brd=art.get('brands',{}).get(brand,{});td=art.get('topics',{})
            ws.cell(row=ri,column=1,value=art.get('monitor_date','')).font=df;ws.cell(row=ri,column=2,value=art.get('date_published','')).font=df
            pub_cell=ws.cell(row=ri,column=3,value=art.get('publication',''))
            pub_cell.font=df
            if art.get('publication_flagged'):
                pub_cell.fill=pub_flag_fill  # Highlight flagged publications in yellow
            hc=ws.cell(row=ri,column=4,value=art.get('headline','') or '(no headline)')
            url = art.get('url','')
            if url and art.get('headline','').strip():
                hc.hyperlink=url;hc.font=lf
            else:
                hc.font=df
            ws.cell(row=ri,column=5,value=art.get('article_or_pr','Article')).font=df;ws.cell(row=ri,column=6,value=brd.get('sentiment','Neutral')).font=df
            for ti,topic in enumerate(topics):v='x' if td.get(topic,False) else '';ws.cell(row=ri,column=7+ti,value=v).font=df;ws.cell(row=ri,column=7+ti).alignment=Alignment(horizontal='center')
            ws.cell(row=ri,column=16,value='x').font=df;ws.cell(row=ri,column=16).alignment=Alignment(horizontal='center');ws.cell(row=ri,column=17,value=art.get('ceo_mention','')).font=df
            if art.get('is_paywall'):
                for ci in range(1,18):ws.cell(row=ri,column=ci).fill=pf
            for ci in range(1,18):ws.cell(row=ri,column=ci).border=bd
        ws.freeze_panes='A2'
    cm={'Honeywell':'B','Carrier':'C','JCI':'D','Daikin':'E','Lennox':'F','Trane Technologies':'G'}
    for b in brands:ws_tot[f'{cm.get(b,"B")}3']=len(get_brand_articles(tagged_articles,b))
    ws_def=wb.create_sheet("Key Topics & Definitions");ws_def['A1']='Key Topics';ws_def['B1']='Definitions'
    for di,(t,d) in enumerate([
        ('Sustainability','Climate change action — brand actively implementing sustainability initiatives or achieving milestones'),
        ('Decarbonization','Reducing carbon emissions — brand actively reducing carbon footprint or deploying low-carbon tech'),
        ('Innovation','Advancing HVAC tech — brand launching new products, deploying new technology, R&D breakthroughs'),
        ('Energy Efficiency','Optimized energy use — brand delivering measurably more efficient products/systems'),
        ('Digitization','Digital tech, AI, IoT — brand deploying digital solutions, smart building tech, connected systems'),
        ('Electrification','Electrification of heat — brand manufacturing/deploying heat pumps, electric HVAC, gas-to-electric conversion'),
        ('Workforce Development','Training, upskilling — brand running training programs, hiring initiatives, apprenticeships'),
        ('Financial Performance','Revenue, earnings, stock — all financial results, stock performance, analyst ratings, deals'),
        ('No Category Match','Broader HVAC — none of the above 8 topics apply')
    ],2):ws_def[f'A{di}']=t;ws_def[f'B{di}']=d
    out=BytesIO();wb.save(out);out.seek(0);return out

def get_brand_articles(tagged, brand):
    """Get articles for a specific brand tab. Primary: AI's brand.mentioned flag.
    Fallback: section-based assignment for articles where AI didn't set mentioned flags."""
    result=[];bl=brand.lower()
    aliases={'trane technologies':['trane','metus','mitsubishi electric trane','thermo king'],
             'carrier':['carrier global','carrier'],'honeywell':['honeywell'],
             'jci':['johnson controls','jci'],'daikin':['daikin'],'lennox':['lennox']}
    ba=aliases.get(bl,[bl])
    for art in tagged:
        bi=art.get('brands',{}).get(brand,{})
        # Primary: AI explicitly said this brand is mentioned
        if bi.get('mentioned',False):
            result.append(art)
            continue
        # Fallback: Section-based assignment ONLY if no brand has mentioned=True
        # (means the AI didn't set any brand flags, so fall back to document section)
        any_brand_mentioned = any(
            art.get('brands',{}).get(b,{}).get('mentioned',False)
            for b in ['Trane Technologies','Carrier','Honeywell','JCI','Daikin','Lennox']
        )
        if not any_brand_mentioned:
            sec=art.get('section','').lower()
            txt=(art.get('headline','')+' '+art.get('summary','')).lower()
            if bl=='trane technologies' and 'trane' in sec:
                result.append(art); continue
            if 'benchmark' in sec or 'trends' in sec:
                for a in ba:
                    if a in txt:result.append(art);break
    return result

def generate_csv(tagged, topics):
    out=StringIO();w=csv.writer(out)
    w.writerow(['#','Monitor Date','Date Published','Publication','Headline','URL','Type','Sentiment','Section','Confidence']+topics+['CODED?','CEO','Paywall','Translated'])
    for i,art in enumerate(tagged):
        td=art.get('topics',{});conf=art.get('confidence',{})
        r=[i+1,art.get('monitor_date',''),art.get('date_published',''),art.get('publication',''),art.get('headline',''),art.get('url',''),art.get('article_or_pr','Article'),'',art.get('section',''),conf.get('overall','')]
        for t in topics:r.append('x' if td.get(t,False) else '')
        r.extend(['x',art.get('ceo_mention',''),'Yes' if art.get('is_paywall') else '','Yes' if art.get('is_translated') else ''])
        w.writerow(r)
    return out.getvalue()


# ============================================================
# TEMPLATE GENERATOR (Manual Tagging — columns A-E only)
# ============================================================
def generate_template_excel(articles, monitor_date):
    """Generate Excel template with only columns A-E populated (parser data).
    Columns F onwards have headers but are blank for manual analyst tagging."""
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    wb = Workbook()
    brands = ['Trane Technologies','Carrier','Honeywell','JCI','Daikin','Lennox']
    topics = ['Sustainability','Decarbonization','Innovation','Energy Efficiency','Digitization',
              'Electrification','Workforce Development','Financial Performance','No Category Match']
    headers = ['Monitor Date','Date Published','Publication','Headline','Article OR Press Release',
               'Sentiment'] + topics + ['CODED?','CEO/Executive Mention']
    hf=Font(name='Calibri',bold=True,size=10,color='FFFFFF')
    hfl=PatternFill(start_color='1e1e2a',end_color='1e1e2a',fill_type='solid')
    df=Font(name='Calibri',size=10);lf=Font(name='Calibri',size=10,color='6366F1',underline='single')
    pf=PatternFill(start_color='FFF2CC',end_color='FFF2CC',fill_type='solid')
    bd=Border(left=Side(style='thin',color='D9D9D9'),right=Side(style='thin',color='D9D9D9'),top=Side(style='thin',color='D9D9D9'),bottom=Side(style='thin',color='D9D9D9'))
    wb.remove(wb.active)
    ws_tot=wb.create_sheet("Totals");ws_tot['B2']='Honeywell';ws_tot['C2']='Carrier';ws_tot['D2']='JCI';ws_tot['E2']='Daikin';ws_tot['F2']='Lennox';ws_tot['G2']='Trane'

    # For template mode, distribute articles by section-based brand detection
    for brand in brands:
        ws=wb.create_sheet(brand)
        for ci,h in enumerate(headers,1):c=ws.cell(row=1,column=ci,value=h);c.font=hf;c.fill=hfl;c.alignment=Alignment(horizontal='center',wrap_text=True);c.border=bd
        ws.column_dimensions['A'].width=12;ws.column_dimensions['B'].width=14;ws.column_dimensions['C'].width=22;ws.column_dimensions['D'].width=55;ws.column_dimensions['E'].width=18;ws.column_dimensions['F'].width=12
        for ci in range(7,16):ws.column_dimensions[chr(64+ci)].width=14
        ws.column_dimensions['P'].width=8;ws.column_dimensions['Q'].width=20

        ba = get_brand_articles_template(articles, brand)
        for ri,art in enumerate(ba,2):
            # Column A: Monitor Date
            ws.cell(row=ri,column=1,value=art.get('monitor_date','')).font=df
            # Column B: Date Published (from parser — may be empty, analyst fills in)
            ws.cell(row=ri,column=2,value=art.get('date_published','')).font=df
            # Column C: Publication
            ws.cell(row=ri,column=3,value=art.get('publication','')).font=df
            # Column D: Headline (hyperlinked if URL exists)
            hc=ws.cell(row=ri,column=4,value=art.get('headline','') or '(no headline)')
            url = art.get('url','')
            if url and art.get('headline','').strip():
                hc.hyperlink=url;hc.font=lf
            else:
                hc.font=df
            # Column E: Article OR Press Release (blank — analyst fills in)
            ws.cell(row=ri,column=5,value='').font=df
            # Columns F-Q: ALL BLANK — analyst fills in manually
            # Just apply borders and paywall highlighting
            if art.get('is_paywall'):
                for ci in range(1,18):ws.cell(row=ri,column=ci).fill=pf
            for ci in range(1,18):ws.cell(row=ri,column=ci).border=bd
        ws.freeze_panes='A2'
    # Totals
    cm={'Honeywell':'B','Carrier':'C','JCI':'D','Daikin':'E','Lennox':'F','Trane Technologies':'G'}
    for b in brands:ws_tot[f'{cm.get(b,"B")}3']=len(get_brand_articles_template(articles,b))

    ws_def=wb.create_sheet("Key Topics & Definitions");ws_def['A1']='Key Topics';ws_def['B1']='Definitions'
    for di,(t,d) in enumerate([
        ('Sustainability','Climate change action — brand actively implementing sustainability initiatives or achieving milestones'),
        ('Decarbonization','Reducing carbon emissions — brand actively reducing carbon footprint or deploying low-carbon tech'),
        ('Innovation','Advancing HVAC tech — brand launching new products, deploying new technology, R&D breakthroughs'),
        ('Energy Efficiency','Optimized energy use — brand delivering measurably more efficient products/systems'),
        ('Digitization','Digital tech, AI, IoT — brand deploying digital solutions, smart building tech, connected systems'),
        ('Electrification','Electrification of heat — brand manufacturing/deploying heat pumps, electric HVAC, gas-to-electric conversion'),
        ('Workforce Development','Training, upskilling — brand running training programs, hiring initiatives, apprenticeships'),
        ('Financial Performance','Revenue, earnings, stock — all financial results, stock performance, analyst ratings, deals'),
        ('No Category Match','Broader HVAC — none of the above 8 topics apply')
    ],2):ws_def[f'A{di}']=t;ws_def[f'B{di}']=d
    out=BytesIO();wb.save(out);out.seek(0);return out


def get_brand_articles_template(articles, brand):
    """Distribute parsed articles to brand tabs based on section and keyword matching.
    Used for template mode (no AI tagging, so no brand.mentioned flags)."""
    result=[];bl=brand.lower()
    aliases={'trane technologies':['trane','metus','mitsubishi electric trane','thermo king'],
             'carrier':['carrier global','carrier'],'honeywell':['honeywell'],
             'jci':['johnson controls','jci'],'daikin':['daikin'],'lennox':['lennox']}
    ba=aliases.get(bl,[bl])
    for art in articles:
        sec=art.get('section','').lower()
        txt=(art.get('headline','')+' '+art.get('summary','')+' '+art.get('publication','')).lower()
        # Trane section articles go to Trane tab
        if bl=='trane technologies' and 'trane' in sec:
            result.append(art); continue
        # Benchmark and Trends articles: check if brand name or alias appears
        if 'benchmark' in sec or 'trends' in sec:
            for a in ba:
                if a in txt:result.append(art);break
    return result

def load_analyst_examples(ef):
    from openpyxl import load_workbook
    try:
        wb=load_workbook(BytesIO(ef.read()),read_only=True);exs=[]
        if 'Trane Technologies' in wb.sheetnames:
            ws=wb['Trane Technologies']
            tn=['Sustainability','Decarbonization','Innovation','Energy Efficiency','Digitization','Electrification','Workforce Development','Financial Performance','No Category Match']
            for ri,row in enumerate(ws.iter_rows(values_only=True)):
                if ri<2:continue
                if ri>12:break
                v=list(row)
                if len(v)>=16 and v[2]:
                    ts=[t for ti,t in enumerate(tn) if len(v)>6+ti and v[6+ti] and str(v[6+ti]).strip().lower()=='x']
                    exs.append(f"Pub:{v[2]}|HL:{str(v[3])[:60]}|Type:{v[4]}|Sent:{v[5]}|Topics:{','.join(ts) or 'NCM'}")
        wb.close();return '\n'.join(exs)
    except Exception:return ""


# ============================================================
# MAIN UI — SIDEBAR RESTORED + SPLIT SCREEN
# ============================================================
def main():
    # Header
    st.markdown("""<div class="main-header">
        <div class="icon">🏷️</div>
        <div><h1>Media Intelligence Agent</h1>
        <p>Upload · Tag · Review with AI · Export</p></div>
    </div>""", unsafe_allow_html=True)

    # === SIDEBAR (always visible) ===
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")

        # API Key
        saved_key = ""
        try: saved_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception: pass
        if saved_key:
            api_key = saved_key
            st.success("✅ API Key loaded from secrets")
        else:
            api_key = st.text_input("Claude API Key", type="password", help="From console.anthropic.com")

        st.markdown("---")

        # How it works
        st.markdown("### 📋 How It Works")
        st.markdown("""
1. **Upload** Daily Monitor `.docx`
2. **Parser** extracts articles, URLs, summaries
3. **AI** reads articles & tags each one
4. **Review** in tile or table view
5. **Chat** with AI to correct tags
6. **Download** Excel with all brand tabs
        """)

        st.markdown("---")

        # Brands
        st.markdown("### 🔖 Brand Tabs")
        st.markdown("Trane Technologies (+ METUS, Thermo King) · Carrier · Honeywell · JCI · Daikin · Lennox")

        st.markdown("---")

        # Paywall blocklist
        st.markdown("### 🔒 Paywall Blocklist")
        st.caption(f"{len(PAYWALL_DOMAINS)} domains blocked")
        with st.expander("View / Edit blocklist"):
            st.markdown("Sites that will **never** be crawled — tagged from summary only.")
            bt = st.text_area("Domains (one per line)", value='\n'.join(sorted(PAYWALL_DOMAINS)), height=200)
            if st.button("Update blocklist"):
                PAYWALL_DOMAINS.clear()
                PAYWALL_DOMAINS.update({d.strip().lower() for d in bt.split('\n') if d.strip()})
                st.success(f"✅ {len(PAYWALL_DOMAINS)} domains")

        st.markdown("---")

        # Section filter (only when tagged)
        if st.session_state.get('tagged_articles'):
            st.markdown("### 🗂️ Filter by Section")
            sections = list(set(a.get('section','') for a in st.session_state.tagged_articles))
            selected_section = st.selectbox("Section", ["All Sections"] + sorted(sections))
            st.session_state['section_filter'] = selected_section

            st.markdown("---")
            st.markdown("### 📊 Quick Stats")
            tagged = st.session_state.tagged_articles
            st.markdown(f"**Total:** {len(tagged)} articles")
            st.markdown(f"**Paywalled:** {sum(1 for a in tagged if a.get('is_paywall'))}")
            st.markdown(f"**Low confidence:** {sum(1 for a in tagged if a.get('confidence',{}).get('overall')=='low')}")
            st.markdown(f"**CEO mentions:** {sum(1 for a in tagged if a.get('ceo_mention'))}")

    # === Initialize session state ===
    for key in ['chat_messages', 'tagged_articles', 'monitor_date', 'parsed_articles', 'section_filter']:
        if key not in st.session_state:
            st.session_state[key] = [] if key == 'chat_messages' else (None if key in ('tagged_articles','parsed_articles') else '')

    # ==========================================
    # PRE-TAGGING: Upload + Parse
    # ==========================================
    if st.session_state.tagged_articles is None:
        col1, col2 = st.columns([2, 1])
        with col1:
            uploaded_docx = st.file_uploader("📄 Upload Daily Monitor (.docx)", type=['docx'])
            if not uploaded_docx:
                st.markdown("""<div class="upload-panel">
                    <div class="icon">📄</div>
                    <div class="title">Drop your Daily Monitor here</div>
                    <div class="sub">.docx file — articles will be parsed automatically</div>
                </div>""", unsafe_allow_html=True)
        with col2:
            uploaded_excel = st.file_uploader("📊 Analyst Reference (optional)", type=['xlsx'])
            if not uploaded_excel:
                st.markdown("""<div class="upload-panel" style="padding:1.8rem;">
                    <div class="icon" style="font-size:2rem;">📊</div>
                    <div class="title" style="font-size:0.85rem;">Analyst reference</div>
                    <div class="sub">Helps AI learn your tagging patterns</div>
                </div>""", unsafe_allow_html=True)

        if uploaded_docx and st.session_state.parsed_articles is None:
            with st.spinner("🔍 Parsing Word document..."):
                fb = uploaded_docx.read()
                articles, md = parse_docx(fb, uploaded_docx.name)
            if not articles:
                st.error("No articles found."); return
            for art in articles:
                if art.get('url') and is_paywall_url(art['url']):
                    art['is_paywall'] = True; art['paywall_reason'] = 'blocklist'
                elif not art.get('url'):
                    art['is_paywall'] = True; art['paywall_reason'] = 'no_url'
            st.session_state.parsed_articles = articles
            st.session_state.monitor_date = md
            st.rerun()

        if st.session_state.parsed_articles is not None and st.session_state.tagged_articles is None:
            articles = st.session_state.parsed_articles
            md = st.session_state.monitor_date
            total = len(articles)
            exp = sum(1 for a in articles if a.get('is_expansion'))
            pay = sum(1 for a in articles if a.get('is_paywall'))
            crawl = total - pay

            st.markdown(f"""<div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin:1rem 0;">
                <div class="stat-chip"><div class="stat-num">{total}</div><div class="stat-label">Articles</div></div>
                <div class="stat-chip"><div class="stat-num">{total-exp}</div><div class="stat-label">Main</div></div>
                <div class="stat-chip"><div class="stat-num">{exp}</div><div class="stat-label">Expansion</div></div>
                <div class="stat-chip"><div class="stat-num">{pay}</div><div class="stat-label">Paywalled</div></div>
                <div class="stat-chip"><div class="stat-num">{crawl}</div><div class="stat-label">Will Crawl</div></div>
                <div class="stat-chip"><div class="stat-num">{md or '—'}</div><div class="stat-label">Monitor Date</div></div>
            </div>""", unsafe_allow_html=True)

            if not api_key:
                st.warning("⚠️ Enter your Claude API Key in the sidebar to use AI Tagging.")

            st.markdown("---")
            st.markdown("**Choose your workflow:**")
            btn_col1, btn_col2 = st.columns(2)

            with btn_col1:
                st.markdown("""<div style="background:#f0fff4;border:1px solid #c6f6d5;border-radius:12px;padding:0.8rem;margin-bottom:0.5rem;">
                    <div style="font-weight:700;color:#276749;font-size:0.9rem;">📋 Template for Manual Tagging</div>
                    <div style="font-size:0.75rem;color:#4a5568;margin-top:0.3rem;">Parser fills columns A–D (Monitor Date, Date Published, Publication, Headline with hyperlinks). Columns E onwards are blank for analysts to tag manually.</div>
                </div>""", unsafe_allow_html=True)
                sd = md.replace(' ','_').replace('.','') if md else 'report'
                template_data = generate_template_excel(articles, md)
                st.download_button("📋 Download Template Excel", data=template_data,
                    file_name=f"TT_Template_{sd}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True)

            with btn_col2:
                st.markdown("""<div style="background:#ebf4ff;border:1px solid #bee3f8;border-radius:12px;padding:0.8rem;margin-bottom:0.5rem;">
                    <div style="font-weight:700;color:#3182ce;font-size:0.9rem;">🤖 AI Auto-Tagging</div>
                    <div style="font-size:0.75rem;color:#4a5568;margin-top:0.3rem;">AI reads each article, tags sentiment, topics, CEO mentions, article/PR type. Review and edit via chat agent. Requires API key.</div>
                </div>""", unsafe_allow_html=True)
                if api_key:
                    if st.button("🚀 Start AI Tagging", type="primary", use_container_width=True):
                        analyst_ex = load_analyst_examples(uploaded_excel) if uploaded_excel else ""
                        pbar = st.progress(0); stxt = st.empty(); larea = st.empty(); logs = []
                        def pcb(p, m):
                            pbar.progress(min(p,1.0))
                            stxt.markdown(f'<div style="font-size:0.85rem;font-weight:600;color:#667eea;padding:0.2rem 0;">{m}</div>', unsafe_allow_html=True)
                            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {m}")
                            larea.markdown(f'<div style="background:#ffffff;border:1px solid #e8e9ee;border-radius:12px;padding:0.5rem 0.8rem;font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#4a5568;white-space:pre-wrap;line-height:1.5;">{chr(10).join(logs[-8:])}</div>', unsafe_allow_html=True)
                        pcb(0.05, "Starting parallel processing...")
                        tagged = tag_articles_batch(articles, api_key, analyst_ex, pcb)
                        st.session_state.tagged_articles = tagged
                        low_conf = sum(1 for t in tagged if t.get('confidence',{}).get('overall') == 'low')
                        ok_count = sum(1 for t in tagged if not t.get('tags_failed'))
                        st.session_state.chat_messages = [{'role':'assistant','content':
                            f"✅ **{ok_count}/{len(tagged)}** articles tagged.\n\n"
                            + (f"⚠️ **{low_conf} articles** have low confidence. Ask: *'show low confidence articles'*\n\n" if low_conf > 0 else "")
                            + "**What you can do:**\n- Review articles (tiles/table) on the left\n- Chat here to correct: *'change #5 sentiment to Positive'*\n- Ask: *'why is article 8 tagged Decarbonization?'*\n- Export: *'generate Excel'*"}]
                        st.rerun()
                else:
                    st.info("Enter API key in sidebar to enable AI tagging.")
        return

    # ==========================================
    # POST-TAGGING: Status bar + Split Screen
    # ==========================================
    tagged = st.session_state.tagged_articles
    md = st.session_state.monitor_date
    brands = ['Trane Technologies','Carrier','Honeywell','JCI','Daikin','Lennox']
    topics = ['Sustainability','Decarbonization','Innovation','Energy Efficiency','Digitization',
              'Electrification','Workforce Development','Financial Performance','No Category Match']

    ok_count = sum(1 for t in tagged if not t.get('tags_failed'))
    low_c = sum(1 for t in tagged if t.get('confidence',{}).get('overall')=='low')
    med_c = sum(1 for t in tagged if t.get('confidence',{}).get('overall')=='medium')
    hi_c = sum(1 for t in tagged if t.get('confidence',{}).get('overall')=='high')
    pw_c = sum(1 for t in tagged if t.get('is_paywall'))
    sd = md.replace(' ','_').replace('.','') if md else 'report'

    dot = "status-dot-done" if ok_count == len(tagged) else "status-dot-error"
    st.markdown(f"""<div class="status-bar">
        <div class="status-dot {dot}"></div>
        <div class="status-text">Tagged {ok_count}/{len(tagged)} articles</div>
        <div class="status-detail">{hi_c} high · {med_c} med · {low_c} low · {pw_c} paywall · {md}</div>
    </div>""", unsafe_allow_html=True)

    # Download row
    dl1, dl2, dl3 = st.columns([2, 2, 6])
    with dl1:
        st.download_button("📥 Download Excel", data=generate_excel(tagged,md),
            file_name=f"TT_Tagged_{sd}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary", use_container_width=True)
    with dl2:
        st.download_button("📥 Download CSV", data=generate_csv(tagged,topics),
            file_name=f"TT_Tagged_{sd}.csv", mime="text/csv", use_container_width=True)

    # Split: 60% results, 40% chat
    left_col, right_col = st.columns([60, 40])

    with left_col:
        vc1, vc2 = st.columns([3,1])
        with vc2:
            view = st.radio("View", ["Tiles","Table"], horizontal=True, label_visibility="collapsed")

        # Apply section filter from sidebar
        section_filter = st.session_state.get('section_filter', 'All Sections')
        display_tagged = tagged if section_filter == 'All Sections' else [a for a in tagged if a.get('section') == section_filter]

        tabs = st.tabs(["All"] + brands)
        with tabs[0]:
            if view == "Tiles": tile_view(display_tagged, topics, "all")
            else: table_view(display_tagged, topics, "all")
        for bi, b in enumerate(brands):
            with tabs[bi+1]:
                ba = get_brand_articles(display_tagged, b)
                if ba:
                    if view == "Tiles": tile_view(ba, topics, b)
                    else: table_view(ba, topics, b)
                else: st.caption(f"No articles for {b}")

    with right_col:
        st.markdown("""<div class="chat-header">
            <div class="dot"></div>
            <div><h3>Tagging Agent</h3><span>Online — ask anything about the articles</span></div>
        </div>""", unsafe_allow_html=True)

        chat_area = st.container(height=500)
        with chat_area:
            for msg in st.session_state.chat_messages:
                with st.chat_message(msg['role'], avatar="🏷️" if msg['role']=='assistant' else "👤"):
                    st.markdown(msg['content'])

        if prompt := st.chat_input("e.g. 'show low confidence' or 'change #5 to Positive'"):
            st.session_state.chat_messages.append({'role':'user','content':prompt})
            with chat_area:
                with st.chat_message("user", avatar="👤"): st.markdown(prompt)
                with st.chat_message("assistant", avatar="🏷️"):
                    with st.spinner("Thinking..."):
                        response = process_chat_command(prompt, tagged, api_key)
                        changes = apply_chat_changes(tagged, response)
                        if changes == -1:
                            st.markdown("Generating report...")
                            st.download_button("📥 Download Excel", data=generate_excel(tagged,md), file_name=f"TT_Tagged_{sd}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                            rc = "📊 Report ready — click download above."
                        elif changes > 0:
                            rc = re.sub(r'\{[^}]*"action"[^}]*\}','',response,flags=re.DOTALL).strip()
                            rc += f"\n\n✅ **{changes} change(s) applied.**"
                            st.session_state.tagged_articles = tagged
                        else: rc = response
                        st.markdown(rc)
                        st.session_state.chat_messages.append({'role':'assistant','content':rc})
            st.rerun()

        st.caption("Try: *'show low confidence'* · *'change #5 to Positive'* · *'generate Excel'*")


# ============================================================
# TILE VIEW WITH PAYWALL HIGHLIGHTING
# ============================================================
def tile_view(articles, topics, brand_filter):
    if not articles: st.caption("No articles."); return
    for i, art in enumerate(articles):
        bd=art.get('brands',{});td=art.get('topics',{});conf=art.get('confidence',{})
        if brand_filter=="all":
            sent="Neutral"
            for b in ['Trane Technologies','Carrier','Honeywell','JCI','Daikin','Lennox']:
                if bd.get(b,{}).get('mentioned'):sent=bd[b].get('sentiment','Neutral');break
        else: sent=bd.get(brand_filter,{}).get('sentiment','Neutral')
        active=[t for t in topics if td.get(t,False)]
        sc='tag-positive' if sent=='Positive' else ('tag-negative' if sent=='Negative' else 'tag-neutral')
        hl=art.get('headline','No headline');url=art.get('url','')
        hl_html=f'<a href="{url}" target="_blank">{hl}</a>' if url else hl

        is_pw = art.get('is_paywall', False)
        card_class = "article-card article-card-paywall" if is_pw else "article-card"

        badges=""
        if is_pw: badges+='<span class="paywall-banner">🔒 Tagged from summary only — needs paywall access for full analysis</span><br>'
        if art.get('is_translated'):badges+='<span class="tag-chip tag-translated">🌐 Translated</span>'
        if art.get('is_expansion'):badges+='<span class="tag-chip tag-expansion">🔗 Expansion</span>'
        if art.get('ceo_mention'):badges+=f'<span class="tag-chip tag-ceo">{art["ceo_mention"]}</span>'
        if art.get('tags_failed'):badges+='<span class="tag-chip tag-low">⚠️ Fallback</span>'
        if art.get('publication_flagged'):badges+='<span class="tag-chip tag-paywall">⚠️ Check Pub Name</span>'

        overall_conf = conf.get('overall','')
        if overall_conf == 'high': badges += '<span class="tag-chip tag-high">✓ High</span>'
        elif overall_conf == 'medium': badges += '<span class="tag-chip tag-medium">~ Medium</span>'
        elif overall_conf == 'low': badges += '<span class="tag-chip tag-low">⚠ Low</span>'

        tchips=''.join(f'<span class="tag-chip tag-topic">{t}</span>' for t in active) or '<span class="tag-chip tag-neutral">No Category Match</span>'
        try: idx = st.session_state.tagged_articles.index(art) + 1
        except: idx = i + 1

        st.markdown(f"""<div class="{card_class}">
            <div class="card-num">#{idx}</div>
            <div class="pub-name">{art.get('publication','')} · {art.get('date_published','')} · <span class="{sc}" style="padding:0.1rem 0.4rem;border-radius:5px;font-size:0.62rem;">{sent}</span> · {art.get('article_or_pr','Article')}</div>
            {f'<div>{badges}</div>' if badges else ''}
            <div class="headline">{hl_html}</div>
            <div class="meta">{tchips}</div>
        </div>""", unsafe_allow_html=True)
    st.caption(f"{len(articles)} articles — use # in chat to edit")


def table_view(articles, topics, brand_filter):
    import pandas as pd
    if not articles: st.caption("No articles."); return
    rows=[]
    for i,art in enumerate(articles):
        bd=art.get('brands',{});td=art.get('topics',{});conf=art.get('confidence',{})
        if brand_filter=="all":
            sent="—"
            for b in ['Trane Technologies','Carrier','Honeywell','JCI','Daikin','Lennox']:
                if bd.get(b,{}).get('mentioned'):sent=bd[b].get('sentiment','Neutral');break
        else: sent=bd.get(brand_filter,{}).get('sentiment','Neutral')
        try: idx = st.session_state.tagged_articles.index(art)+1
        except: idx = i+1
        row={'#':idx,'Publication':art.get('publication',''),'Headline':art.get('headline','')[:60],
             'Type':art.get('article_or_pr','Article'),'Sentiment':sent,'Conf':conf.get('overall','?')}
        for t in topics:row[t]='x' if td.get(t,False) else ''
        row['CEO']=art.get('ceo_mention','')
        flags=[]
        if art.get('is_paywall'):flags.append('🔒 PW')
        if art.get('is_translated'):flags.append('🌐')
        if art.get('tags_failed'):flags.append('⚠️')
        row['Flags']=' '.join(flags)
        rows.append(row)
    st.dataframe(pd.DataFrame(rows),use_container_width=True,height=min(len(rows)*38+40,600))
    st.caption(f"{len(rows)} articles | 🔒 = Paywall (summary only)")


if __name__ == "__main__":
    main()
