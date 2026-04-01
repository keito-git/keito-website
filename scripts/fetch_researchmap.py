#!/usr/bin/env python3
"""
researchmap 公開APIから業績データを取得して researchmap_data.json に保存する。
認証不要の公開エンドポイントのみ使用。
"""
import json, time, urllib.request, urllib.error, sys

RESEARCHER_ID = "keito_inoshita"
BASE = f"https://researchmap.jp/{RESEARCHER_ID}"

ENDPOINTS = {
    "published_papers": f"{BASE}/published_papers?format=json&limit=100",
    "misc":             f"{BASE}/misc?format=json&limit=100",
    "awards":           f"{BASE}/awards?format=json&limit=100",
    "research_projects":f"{BASE}/research_projects?format=json&limit=100",
    "presentations":    f"{BASE}/presentations?format=json&limit=100",
    "committee_memberships": f"{BASE}/committee_memberships?format=json&limit=100",
    "academic_contribution": f"{BASE}/academic_contribution?format=json&limit=100",
    "social_contribution":   f"{BASE}/social_contribution?format=json&limit=100",
    "profile":          f"https://researchmap.jp/{RESEARCHER_ID}.json",
}

def fetch(url, retries=3):
    headers = {"Accept": "application/json", "User-Agent": "keito-website-bot/1.0"}
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code} for {url}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"  Error ({i+1}/{retries}): {e}", file=sys.stderr)
            time.sleep(2)
    return None

def extract_text(obj, *keys):
    """ネストしたdict/listから日本語 → 英語の順でテキストを取り出す"""
    for k in keys:
        obj = obj.get(k) if isinstance(obj, dict) else None
        if obj is None:
            return ""
    if isinstance(obj, dict):
        return obj.get("ja") or obj.get("en") or ""
    return str(obj) if obj else ""

def parse_papers(items):
    out = []
    for p in items:
        authors_raw = p.get("authors", {})
        authors_list = []
        for lang in ("ja", "en"):
            al = authors_raw.get(lang, [])
            if isinstance(al, list) and al:
                authors_list = [a.get("name","") for a in al]
                break
        # 自分の名前を bold にする
        formatted = []
        for a in authors_list:
            if "inoshita" in a.lower() or "井下" in a:
                formatted.append(f"<strong>{a}</strong>")
            else:
                formatted.append(a)
        authors_str = ", ".join(formatted)

        title = extract_text(p, "paper_title")
        journal = extract_text(p, "journal_title")
        year = str(p.get("published_at", ""))[:4] if p.get("published_at") else ""
        volume = p.get("volume","")
        pages  = p.get("pages","")
        venue_parts = [journal]
        if volume: venue_parts.append(f"vol.{volume}")
        if pages:  venue_parts.append(f"pp.{pages}")
        venue = ", ".join(filter(None, venue_parts))
        if p.get("published_at"):
            venue += f", {p['published_at'][:7]}"

        badges = []
        if p.get("referee"):        badges.append("peer")
        if p.get("invited"):        badges.append("invited")
        # 筆頭著者判定（著者リスト1番目が自分）
        if authors_list and ("inoshita" in authors_list[0].lower() or "井下" in authors_list[0]):
            badges.append("first")

        # カテゴリ推定
        cat = "journal"
        title_lower = title.lower()
        venue_lower = venue.lower()
        if any(x in venue_lower for x in ["proceedings","conference","workshop","symposium","arxiv","biorxiv"]):
            cat = "conf"
        if "arxiv" in venue_lower or "biorxiv" in venue_lower:
            cat = "preprint"

        out.append({
            "rm_id":   p.get("id",""),
            "source":  "researchmap",
            "year":    year,
            "title":   title,
            "authors": authors_str,
            "venue":   venue,
            "cat":     cat,
            "badges":  badges,
            "url":     p.get("url",""),
        })
    return out

def parse_misc(items):
    out = []
    for p in items:
        title = extract_text(p, "paper_title") or extract_text(p, "misc_title") or extract_text(p, "title")
        authors_raw = p.get("authors", {})
        authors_list = []
        for lang in ("ja", "en"):
            al = authors_raw.get(lang, [])
            if isinstance(al, list) and al:
                authors_list = [a.get("name","") for a in al]
                break
        formatted = []
        for a in authors_list:
            if "inoshita" in a.lower() or "井下" in a:
                formatted.append(f"<strong>{a}</strong>")
            else:
                formatted.append(a)
        authors_str = ", ".join(formatted)
        journal = extract_text(p, "journal_title") or extract_text(p, "publication_title")
        year = str(p.get("published_at",""))[:4] if p.get("published_at") else ""
        venue_parts = [journal]
        if p.get("volume"): venue_parts.append(f"vol.{p['volume']}")
        if p.get("pages"):  venue_parts.append(f"pp.{p['pages']}")
        if p.get("published_at"): venue_parts.append(p["published_at"][:7])
        venue = ", ".join(filter(None, venue_parts))
        badges = ["first"] if (authors_list and ("inoshita" in authors_list[0].lower() or "井下" in authors_list[0])) else []
        if p.get("invited"): badges.append("invited")
        out.append({"rm_id":p.get("id",""),"source":"researchmap","year":year,"title":title,"authors":authors_str,"venue":venue,"cat":"misc","badges":badges})
    return out

def parse_awards(items):
    out = []
    for a in items:
        text = extract_text(a, "award_name")
        org  = extract_text(a, "associated_institution_name")
        if org: text = f"{text} ({org})"
        year = str(a.get("date",""))[:4] if a.get("date") else ""
        icon = "🏆" if "best paper" in text.lower() or "最優秀" in text or "一位" in text or "1位" in text else "🎖️"
        cat  = "research" if any(x in text.lower() for x in ["best paper","paper","award","賞","prize"]) else "other"
        out.append({"rm_id":a.get("id",""),"source":"researchmap","icon":icon,"text":text,"year":year,"cat":cat})
    return out

def parse_grants(items):
    out = []
    for g in items:
        title  = extract_text(g, "research_project_title")
        org    = extract_text(g, "funding_organization_name")
        fund   = extract_text(g, "fund_name")
        if fund and org: org = f"{org} — {fund}"
        elif fund: org = fund
        start  = str(g.get("start_date",""))[:7].replace("-","/") if g.get("start_date") else ""
        end    = str(g.get("end_date",""))[:7].replace("-","/") if g.get("end_date") else ""
        period = f"{start}–{end}" if start else ""
        amount = str(g.get("total_funding","")) or "採択"
        out.append({"rm_id":g.get("id",""),"source":"researchmap","title":title,"org":org,"amount":amount,"period":period})
    return out

def parse_presentations(items):
    out = []
    for p in items:
        text = extract_text(p, "presentation_title")
        event= extract_text(p, "event_title")
        date = str(p.get("date",""))[:7] if p.get("date") else "—"
        if event: text = f"{text}（{event}）"
        out.append({"rm_id":p.get("id",""),"source":"researchmap","year":date,"text":text})
    return out

def parse_committees(items):
    out = []
    for c in items:
        text = extract_text(c, "committee_name") or extract_text(c, "activity")
        org  = extract_text(c, "organization")
        role = extract_text(c, "role")
        if org:  text = f"{org} — {text}"
        if role: text = f"{text} ({role})"
        start= str(c.get("start_date",""))[:7] if c.get("start_date") else "—"
        end  = str(c.get("end_date",""))[:7] if c.get("end_date") else "現在"
        period = f"{start}–{end}" if start!="—" else "—"
        out.append({"rm_id":c.get("id",""),"source":"researchmap","year":period,"text":text})
    return out

def parse_reviewers(items):
    out = []
    for r in items:
        text = extract_text(r, "activity") or extract_text(r, "committee_name")
        out.append({"rm_id":r.get("id",""),"source":"researchmap","year":"—","text":text})
    return out

def parse_profile(data):
    if not data: return {}
    affils = []
    for a in data.get("affiliations", []):
        name = extract_text(a, "institution", "name") or extract_text(a, "name")
        dept = extract_text(a, "department", "name") or ""
        pos  = extract_text(a, "position", "name") or ""
        affils.append({"name": name, "dept": dept, "position": pos})
    return {
        "name_ja":      data.get("family_name",{}).get("ja","") + data.get("given_name",{}).get("ja",""),
        "name_en":      data.get("given_name",{}).get("en","") + " " + data.get("family_name",{}).get("en",""),
        "affiliations": affils,
        "degree":       [extract_text(d,"degree_name") for d in data.get("degree",[])]
    }

def main():
    print("Fetching researchmap data...")
    result = {"fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    raw = {}
    for key, url in ENDPOINTS.items():
        print(f"  GET {url}")
        data = fetch(url)
        raw[key] = data
        time.sleep(0.5)

    # Profile
    result["profile"] = parse_profile(raw.get("profile"))

    # Publications
    papers_raw = (raw.get("published_papers") or {}).get("items", [])
    result["publications"] = parse_papers(papers_raw)
    result["pub_total"] = (raw.get("published_papers") or {}).get("metadata", {}).get("total", len(papers_raw))

    # MISC
    misc_raw = (raw.get("misc") or {}).get("items", [])
    result["misc"] = parse_misc(misc_raw)

    # Awards
    awards_raw = (raw.get("awards") or {}).get("items", [])
    result["awards"] = parse_awards(awards_raw)

    # Grants
    grants_raw = (raw.get("research_projects") or {}).get("items", [])
    result["grants"] = parse_grants(grants_raw)

    # Presentations / Talks
    pres_raw = (raw.get("presentations") or {}).get("items", [])
    result["talks"] = parse_presentations(pres_raw)

    # Committees
    comm_raw = (raw.get("committee_memberships") or {}).get("items", [])
    result["committees"] = parse_committees(comm_raw)

    # Reviewers (academic_contribution)
    rev_raw = (raw.get("academic_contribution") or {}).get("items", [])
    result["reviewers"] = parse_reviewers(rev_raw)

    # Social
    soc_raw = (raw.get("social_contribution") or {}).get("items", [])
    result["social"] = [{"rm_id":s.get("id",""),"source":"researchmap","year":str(s.get("date",""))[:7] if s.get("date") else "—","text":extract_text(s,"activity_title")} for s in soc_raw]

    with open("researchmap_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Done. {len(result['publications'])} papers, {len(result['awards'])} awards, {len(result['grants'])} grants.")

if __name__ == "__main__":
    main()
