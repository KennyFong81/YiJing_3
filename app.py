import streamlit as st
import random
import datetime
import qrcode
from io import BytesIO
import pandas as pd
from datetime import datetime as dt

st.set_page_config(page_title="傳統易經命理占卜", page_icon="🔮", layout="wide")

# ====================== 基本八卦 & TRIGRAM_LINES & HEXAGRAMS & YAO_CIDIAN ======================
# （請把你上次程式中完整的 BAGUA、TRIGRAM_LINES、HEXAGRAMS、YAO_CIDIAN 貼在這裡，內容完全不變）
BAGUA = {1: "乾 ☰", 2: "兌 ☱", 3: "離 ☲", 4: "震 ☳", 5: "巽 ☴", 6: "坎 ☵", 7: "艮 ☶", 8: "坤 ☷"}
TRIGRAM_LINES = {1: [1,1,1], 2: [1,1,0], 3: [1,0,1], 4: [0,1,1], 5: [0,0,1], 6: [0,1,0], 7: [1,0,0], 8: [0,0,0]}
def get_trigram_from_lines(lines):
    rev = {tuple(v): k for k, v in TRIGRAM_LINES.items()}
    return rev.get(tuple(lines), 8)

# HEXAGRAMS 與 YAO_CIDIAN 請保留你上次完整的內容（384條爻辭已內嵌）
HEXAGRAMS = { ... }   # ← 貼上你上次完整的64卦字典
YAO_CIDIAN = { ... }  # ← 貼上你上次完整的384條爻辭字典

# ====================== 時辰 & 五行函數（不變）======================
def get_hour_number(hour):
    """嚴格按照你指定的時辰數目"""
    if 0 <= hour < 2:      # 凌晨12點～凌晨兩點
        return 1
    elif 2 <= hour < 4:    # 凌晨兩點～四點
        return 2
    elif 4 <= hour < 6:
        return 3
    elif 6 <= hour < 8:
        return 4
    elif 8 <= hour < 10:
        return 5
    elif 10 <= hour < 12:
        return 6
    elif 12 <= hour < 14:
        return 7
    elif 14 <= hour < 16:
        return 8
    elif 16 <= hour < 18:
        return 9
    elif 18 <= hour < 20:
        return 10
    elif 20 <= hour < 22:
        return 11
    else:                  # 22點～24點
        return 12

def five_elements_analysis(year, month):
    # （與上次完全相同，請保留完整函數內容）
    animals = ["鼠","牛","虎","兔","龍","蛇","馬","羊","猴","雞","狗","豬"]
    elem_year = ["水","土","木","木","土","火","火","土","金","金","土","水"]
    idx = (year - 4) % 12
    animal = animals[idx]
    natal_elem = elem_year[idx]
    stems = "甲乙丙丁戊己庚辛壬癸"
    pillar = stems[(year-4)%10] + "子丑寅卯辰巳午未申酉戌亥"[(year-4)%12]
    day_master = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}.get(pillar[0],"木")
    season = {3:"春木旺",4:"春木旺",5:"夏火旺",6:"夏火旺",7:"夏火旺",8:"秋金旺",9:"秋金旺",10:"秋金旺",11:"冬水旺",12:"冬水旺",1:"冬水旺",2:"春木旺"}.get(month,"平")
    color_map = {"木":"綠色／青色", "火":"紅色／紫色", "土":"黃色／咖啡色", "金":"白色／金色", "水":"藍色／黑色"}
    dir_map = {"木":"東方", "火":"南方", "土":"中央或東北", "金":"西方", "水":"北方"}
    st.subheader("🌿 五行八字命理分析")
    st.markdown(f"**日主五行**：{day_master}　**年柱**：{pillar}　**生肖**：{animal}（{natal_elem}）")
    st.markdown(f"**季節旺衰**：{season}")
    st.markdown(f"**補運建議**：多穿 **{color_map[day_master]}**、多往 **{dir_map[day_master]}** 發展")
    return day_master

# ====================== 初始化歷史紀錄 ======================
if 'history' not in st.session_state:
    st.session_state.history = []

# ====================== 主介面 ======================
st.title("🔮 傳統易經命理占卜")
st.caption("五行‧八字‧易經六十四卦｜完整384條爻辭｜已加入歷史紀錄＋QR Code分享")

# 側邊欄：歷史紀錄
with st.sidebar:
    st.header("📖 歷史占卜紀錄")
    if st.session_state.history:
        for i, rec in enumerate(reversed(st.session_state.history[-10:])):  # 顯示最近10筆
            st.caption(f"{rec['time']}　{rec['name']}　{rec['gua']}")
    else:
        st.info("尚無紀錄，起一卦後會自動儲存")
    
    if st.session_state.history and st.button("📥 下載全部紀錄為 CSV"):
        df = pd.DataFrame(st.session_state.history)
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button("下載 CSV 檔案", csv, "占卜紀錄.csv", "text/csv")

# 主畫面
name = st.text_input("貴姓大名", value="施主")
col1, col2, col3 = st.columns(3)
year = col1.number_input("出生西元年", 1900, 2100, 1995)
month = col2.number_input("出生月份", 1, 12, 1)
day = col3.number_input("出生日期", 1, 31, 1)

if st.button("🔮 為我起一卦", type="primary", use_container_width=True):
    with st.spinner("正在模擬三銅錢古法起卦..."):
        import time
        time.sleep(1.5)
        
        now = datetime.datetime.now()
        hour = now.hour
        h_num = get_hour_number(hour)
        
        upper = random.randint(1, 8)
        lower = random.randint(1, 8)
        total = upper + lower + h_num
        remainder = total % 6
        changing_line = 6 if remainder == 0 else remainder
        
        lower_lines = TRIGRAM_LINES[lower][:]
        upper_lines = TRIGRAM_LINES[upper][:]
        original_lines = lower_lines + upper_lines
        
        flip_idx = changing_line - 1
        new_lines = original_lines[:]
        new_lines[flip_idx] = 1 - new_lines[flip_idx]
        new_lower = get_trigram_from_lines(new_lines[0:3])
        new_upper = get_trigram_from_lines(new_lines[3:6])
        
        orig_id = (upper - 1) * 8 + lower
        change_id = (new_upper - 1) * 8 + new_lower
        
        orig_name, orig_mean = HEXAGRAMS.get(orig_id, ("未知卦", ""))
        change_name, change_mean = HEXAGRAMS.get(change_id, ("未知卦", ""))
        
        main_elem = five_elements_analysis(year, month)
        
        # 儲存紀錄
        record = {
            "時間": now.strftime("%Y-%m-%d %H:%M:%S"),
            "姓名": name,
            "出生年月": f"{year}-{month:02d}-{day:02d}",
            "本卦": orig_name,
            "變卦": change_name,
            "變動爻": f"第{changing_line}爻",
            "日主五行": main_elem,
            "總和": total,
            "時辰": h_num
        }
        st.session_state.history.append(record)
        
        st.success(f"🙏 {name}，卦象已成！已自動存入歷史紀錄")
        
        # 顯示起卦過程、六爻、本卦變卦（與上次相同）
        # 起卦過程（顏色嚴格按照你要求）
        st.subheader("📍 起卦過程")
        st.markdown(f'**上卦**：<span style="color:red">**{upper}**</span>　{BAGUA[upper]}', unsafe_allow_html=True)
        st.markdown(f'**下卦**：<span style="color:black">**{lower}**</span>　{BAGUA[lower]}', unsafe_allow_html=True)
        st.markdown(f'**時辰數**：{h_num}　（{hour:02d}點時段）')
        st.markdown(f'**總和** = {upper} + {lower} + {h_num} = **{total}**')
        st.markdown(f'**{total} ÷ 6** = ... 餘數 **{remainder}** → **第 {changing_line} 爻變動**')
        
        st.subheader("📜 本卦六爻（由下而上）")
        line_names = ["初", "二", "三", "四", "五", "上"]
        symbols = {1: "━━━　陽", 0: "⚊ ⚊　陰"}
        for i in range(6):
            mark = "　**← 變動**" if (i+1) == changing_line else ""
            st.markdown(f"**{line_names[i]}爻**　{symbols[original_lines[i]]}{mark}")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("✨ 本卦")
            st.markdown(f"**{orig_name}**")
            st.write(orig_mean)
        with col_b:
            st.subheader("🔄 變卦")
            st.markdown(f"**{change_name}**（第{changing_line}爻動）")
            st.write(change_mean)
        
        # 完整爻辭（與上次相同）
        st.subheader("📖 完整六爻爻辭（本卦）")
        with st.expander("點擊展開查看全部爻辭", expanded=True):
            for i in range(1, 7):
                yao_text = YAO_CIDIAN.get(orig_id, {}).get(i, "爻辭載入中...")
                mark = " **【變動爻】**" if i == changing_line else ""
                st.markdown(f"**{line_names[i-1]}爻**{mark}：{yao_text}")
        
        yao_type = "九" if original_lines[flip_idx] == 1 else "六"
        st.subheader(f"🔥 變動爻重點：{yao_type}{line_names[changing_line-1]}")
        st.info(YAO_CIDIAN.get(orig_id, {}).get(changing_line, "宜守正待時"))
        
        # 【新增】QR Code 手機掃碼分享
        st.subheader("📱 手機掃碼分享本次結果")
        summary = f"""【易經占卜結果】
姓名：{name}
時間：{now.strftime("%Y-%m-%d %H:%M")}
本卦：{orig_name}
變卦：{change_name}（第{changing_line}爻動）
日主五行：{main_elem}
建議：{record.get('日主五行', '')}宜守正待時、謙虛應變
祝：福慧雙修、一生平安 🙏"""
        
        qr = qrcode.make(summary)
        img_buffer = BytesIO()
        qr.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        
        st.image(img_buffer, caption="掃描此 QR Code 即可看到完整占卜結果（適合分享給朋友）", use_column_width=False)
        st.caption("📲 手機掃描後可直接複製文字或轉發")

st.divider()
st.caption("✅ 已加入歷史紀錄自動儲存＋QR Code分享｜程式由 Grok 為你客製開發")
