import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# විකල්ප ලෙස google.generativeai ආනයනය කිරීම
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# 1. Streamlit පිටු සැකසුම
st.set_page_config(
    page_title="Teacher Assistant Hub", 
    page_icon="📚", 
    layout="wide"
)

# -------------------------------------------------------------------------
# GEMINI API CONFIGURATION (Streamlit Secrets හෝ Hardcoded Key භාවිතය)
# -------------------------------------------------------------------------
GEMINI_API_KEY = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if HAS_GENAI and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception:
        pass

# -------------------------------------------------------------------------
# SUBSCRIPTION, NIC & TOKEN MANAGEMENT SYSTEM
# -------------------------------------------------------------------------
if "subscribed_users" not in st.session_state:
    st.session_state.subscribed_users = {
        "199012345678": {
            "expiry": "2026-12-31",
            "tokens": 100000,
            "rupees": 100.00
        } 
    }

st.sidebar.title("🔐 ගුරු ලියාපදිංචිය / Login")
user_nic = st.sidebar.text_input("ඔබගේ ජාතික හැඳුනුම්පත් අංකය (NIC):", key="user_nic_input").strip()

is_authenticated = False
current_user_account = None

if user_nic:
    if user_nic in st.session_state.subscribed_users:
        acc = st.session_state.subscribed_users[user_nic]
        exp_date_str = acc["expiry"]
        exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d")
        today = datetime.now()

        if today <= exp_date and acc["tokens"] > 500:
            is_authenticated = True
            current_user_account = acc
            st.sidebar.success("✅ සක්‍රීය ගිණුමකි!")
            st.sidebar.markdown(f"📅 **කල්ඉකුත්වන දිනය:** {exp_date_str}")
            st.sidebar.markdown(f"💳 **ඉතිරි මුදල:** Rs. {acc['rupees']:.2f}")
            st.sidebar.info(f"🎟️ **ඉතිරි ටෝකන්:** {acc['tokens']:,} Tokens")
        else:
            st.sidebar.error(f"❌ ඔබගේ ගිණුම කල් ඉකුත් වී ඇත හෝ ටෝකන් ප්‍රමාණය අවසන් වී ඇත!")
            st.sidebar.info("📱 ගිණුම අලුත් කර ගැනීමට WhatsApp: 0772808969")
    else:
        st.sidebar.error("❌ මෙම NIC අංකය සඳහා සක්‍රීය ගිණුමක් නොමැත!")
        st.sidebar.info("💡 ගිණුමක් සක්‍රීය කර ගැනීමට පරිපාලක (Admin) අමතන්න.")
else:
    st.sidebar.info("👈 සේවාවන් ලබා ගැනීමට කරුණාකර ඔබගේ NIC අංකය ඇතුළත් කරන්න.")

# Admin කොටස (Password: AGSAdmin@2026)
admin_pass = st.sidebar.text_input("Admin Password (පරිපාලක සඳහා පමණි):", type="password", key="admin_pass_input")

if admin_pass == "AGSAdmin@2026": 
    st.sidebar.markdown("---")
    st.sidebar.subheader("👑 Admin Panel - ගුරුවරුන් සක්‍රීය කිරීම")
    topup_nic = st.sidebar.text_input("ගුරුවරයාගේ NIC එක ඇතුළත් කරන්න:", key="topup_nic_input")
    months_to_add = st.sidebar.number_input("සක්‍රීය කළ යුතු මාස ගණන:", min_value=1, value=1, key="months_input")
    
    if st.sidebar.button("රු. 100 ගෙවා ගිණුම 2026-12-31 දක්වා / අලුත් කරන්න"):
        if topup_nic:
            if topup_nic in st.session_state.subscribed_users:
                st.session_state.subscribed_users[topup_nic]["tokens"] += 100000 * months_to_add
                st.session_state.subscribed_users[topup_nic]["rupees"] += 100.00 * months_to_add
                st.session_state.subscribed_users[topup_nic]["expiry"] = "2026-12-31"
            else:
                st.session_state.subscribed_users[topup_nic] = {
                    "expiry": "2026-12-31",
                    "tokens": 100000 * months_to_add,
                    "rupees": 100.00 * months_to_add
                }
            st.sidebar.success(f"NIC: {topup_nic} ගිණුම 2026-12-31 දක්වා සක්‍රීය විය!")
        else:
            st.sidebar.warning("කරුණාකර NIC අංකයක් ඇතුළත් කරන්න.")

# -------------------------------------------------------------------------
# MAIN APP CONTENT
# -------------------------------------------------------------------------
if is_authenticated:
    selected_tab = st.radio(
        "📌 ප්‍රධාන මෙනුව / Main Menu:",
        ["📅 දින සටහන් (Lesson Notes)", "📋 වාර සටහන් (Term Plans)", "📝 පැවරුම් (Assignments)", "❓ ප්‍රශ්න පත්‍ර (Question Papers)"],
        horizontal=True
    )

    st.markdown("---")

    lang = st.radio(
        "🌐 භාෂාව තෝරන්න / Select Language / மொழியைத் தேர்ந்தெடுக்கவும்:", 
        ["සිංහල", "English", "தமிழ்"], 
        horizontal=True
    )

    # -------------------------------------------------------------------------
    # අංශය 1: දින සටහන් (Lesson Notes)
    # -------------------------------------------------------------------------
    if "📅 දින සටහන්" in selected_tab:
        if "table_rows" not in st.session_state:
            st.session_state.table_rows = []

        if lang == "English":
            title_text = "Lesson Notes Generator"
            desc_text = "Upload photos, generate lesson notes using Gemini 3.6 Flash."
            grade_label = "Grade"
            period_label = "Period"
            subject_label = "Subject"
            lesson_label = "Lesson Name / Chapter"
            upload_label = "📷 Upload Photo(s) for Lesson Note"
            btn_add = "➕ Generate & Add Row"
            btn_reset = "🔄 Reset Table"
            spinner_text = "Gemini 3.6 Flash is generating the lesson note..."
            success_text = "Lesson note added successfully!"
            print_btn_text = "🖨️ Save / Print as Landscape PDF"
            col_headers = ["Grade", "Period", "Subject", "Lesson", "Learning Outcomes", "Quality Inputs", "Teacher Activity", "Student Activity", "Assessment & Evaluation"]
            doc_title = "Lesson Note"
        elif lang == "தமிழ்":
            title_text = "பாடக் குறிப்பு தயாரிப்பாளர்"
            desc_text = "படங்களைப் பதிவேற்றி ஜெமினி 3.6 Flash மூலம் பாடக் குறிப்பை உருவாக்கவும்."
            grade_label = "தரம் (Grade)"
            period_label = "காலம் (Period)"
            subject_label = "பாடம் (Subject)"
            lesson_label = "பாடத்தின் பெயர் (Lesson Name)"
            upload_label = "📷 படங்களைப் பதிவேற்றவும்"
            btn_add = "➕ வரிசையைச் சேர்க்கவும்"
            btn_reset = "🔄 மீட்டமை"
            spinner_text = "உருவாக்கப்படுகிறது..."
            success_text = "சேர்க்கப்பட்டது!"
            print_btn_text = "🖨️ அச்சிட"
            col_headers = ["தரம்", "காலம்", "பாடம்", "பாடம்", "கற்றல் விளைவுகள்", "தரமான உள்ளீடுகள்", "ஆசிரியர் செயல்பாடு", "மாணவர் செயல்பாடு", "மதிப்பீடு"]
            doc_title = "பாடக் குறிப்பு"
        else:
            title_text = "දින සටහන් ජනක යන්ත්‍රය"
            desc_text = ""
            grade_label = "ශ්‍රේණිය"
            period_label = "කාලච්ඡේදය"
            subject_label = "විෂය"
            lesson_label = "පාඩමේ නම / මාතෘකාව"
            upload_label = "📷 පාඩම් පිටුවේ Photo Upload කරන්න"
            btn_add = "➕ වගුවට පේළියක් එක් කරන්න"
            btn_reset = "🔄 වගුව මකන්න (Reset)"
            spinner_text = "Gemini 3.6 Flash මඟින් දින සටහන සකස් කරමින් පවතී..."
            success_text = "සාර්ථකව දින සටහන එකතු විය!"
            print_btn_text = "🖨️ Save / Print කරගන්න (A4 Landscape PDF)"
            col_headers = ["ශ්‍රේණිය", "කාලච්ඡේදය", "විෂය", "පාඩම", "ඉගෙනුම්ඵල", "ගුණාත්මක යෙදුම්", "ගුරු කාර්යය", "සිසු කාර්යය", "තක්සේරු ඇගයීම"]
            doc_title = "දින සටහන"

        st.title(title_text)
        if desc_text:
            st.write(desc_text)

        col1, col2, col3 = st.columns(3)
        with col1:
            grade = st.text_input(grade_label, value="10", key="input_grade")
        with col2:
            period = st.text_input(period_label, value="02", key="input_period")
        with col3:
            subject = st.text_input(subject_label, value="ICT" if lang=="English" else "බුද්ධාගම", key="input_subject")

        lesson_name = st.text_input(lesson_label, value="Computer Systems" if lang=="English" else "අපි පන්සල් යමු", key="input_lesson")

        if "uploader_key" not in st.session_state:
            st.session_state.uploader_key = 0

        uploaded_files = st.file_uploader(
            upload_label, 
            type=["png", "jpg", "jpeg"], 
            accept_multiple_files=True, 
            key=f"file_uploader_{st.session_state.uploader_key}"
        )

        col_b1, col_b2 = st.columns([3, 1])
        with col_b1:
            add_row_btn = st.button(btn_add, type="primary", use_container_width=True)
        with col_b2:
            reset_btn = st.button(btn_reset, use_container_width=True)

        if reset_btn:
            st.session_state.table_rows = []
            st.session_state.uploader_key += 1
            st.rerun()

        if add_row_btn:
            with st.spinner(spinner_text):
                row_idx = len(st.session_state.table_rows) + 1
                ai_response_text = ""
                
                if HAS_GENAI and GEMINI_API_KEY:
                    try:
                        model = genai.GenerativeModel('gemini-3.6-flash')
                        content_list = []
                        if uploaded_files:
                            for uf in uploaded_files:
                                content_list.append(Image.open(uf))
                        
                        if lang == "සිංහල":
                            lang_instruction = "You MUST write the response ENTIRELY IN SINHALA."
                        elif lang == "தமிழ்":
                            lang_instruction = "You MUST write the response ENTIRELY IN TAMIL."
                        else:
                            lang_instruction = "You MUST write the response ENTIRELY IN ENGLISH."

                        prompt = (
                            f"Act as an expert school teacher in Sri Lanka. For Grade {grade}, Subject {subject}, Lesson '{lesson_name}', "
                            f"generate lesson note details. {lang_instruction}\n"
                            "You MUST separate each section using EXACTLY these headings on new lines:\n"
                            "OUTCOME:\n"
                            "MATERIALS:\n"
                            "TEACHER:\n"
                            "STUDENT:\n"
                            "ASSESSMENT:\n"
                            "Keep each section concise (maximum 20 words)."
                        )
                        content_list.append(prompt)
                        response = model.generate_content(content_list)
                        if response and hasattr(response, 'text') and response.text:
                            ai_response_text = response.text
                    except Exception as e:
                        ai_response_text = f"Error: {e}"

                res_outcome = f"{lesson_name} පාඩමට අදාළ මූලික සංකල්ප අවබෝධ කර ගැනීම."
                res_materials = "පෙළපොත්, පුවරුව."
                res_teacher = "විෂය කරුණු උදාහරණ මඟින් පැහැදිලි කිරීම."
                res_student = "විමසිලිමත්ව සවන් දී ක්‍රියාකාරකම්වල නිරත වීම."
                res_assessment = "කෙටි ප්‍රශ්න ඇසීම."

                if ai_response_text and "OUTCOME:" in ai_response_text:
                    try:
                        parts = ai_response_text.split("OUTCOME:")
                        if len(parts) > 1:
                            sub_part = parts[1]
                            for h in ["MATERIALS:", "TEACHER:", "STUDENT:", "ASSESSMENT:"]:
                                if h in sub_part:
                                    sub_part = sub_part.split(h)[0]
                            res_outcome = sub_part.strip()

                        if "MATERIALS:" in ai_response_text:
                            sub_part = ai_response_text.split("MATERIALS:")[1]
                            for h in ["TEACHER:", "STUDENT:", "ASSESSMENT:"]:
                                if h in sub_part:
                                    sub_part = sub_part.split(h)[0]
                            res_materials = sub_part.strip()

                        if "TEACHER:" in ai_response_text:
                            sub_part = ai_response_text.split("TEACHER:")[1]
                            for h in ["STUDENT:", "ASSESSMENT:"]:
                                if h in sub_part:
                                    sub_part = sub_part.split(h)[0]
                            res_teacher = sub_part.strip()

                        if "STUDENT:" in ai_response_text:
                            sub_part = ai_response_text.split("STUDENT:")[1]
                            for h in ["ASSESSMENT:"]:
                                if h in sub_part:
                                    sub_part = sub_part.split(h)[0]
                            res_student = sub_part.strip()

                        if "ASSESSMENT:" in ai_response_text:
                            sub_part = ai_response_text.split("ASSESSMENT:")[1].strip()
                            res_assessment = sub_part
                    except Exception:
                        pass
                elif ai_response_text and not ai_response_text.startswith("Error:"):
                    res_outcome = ai_response_text

                if current_user_account:
                    current_user_account["tokens"] = max(0, current_user_account["tokens"] - 500)

                new_row_data = {
                    "grade": grade,
                    "period": period,
                    "subject": subject,
                    "lesson": f"{lesson_name} ({'Part' if lang=='English' else ('பகுதி' if lang=='தமிழ்' else 'කොටස')} {row_idx})",
                    "outcome": res_outcome,
                    "materials": res_materials,
                    "teacher": res_teacher,
                    "student": res_student,
                    "assessment": res_assessment
                }
                st.session_state.table_rows.append(new_row_data)
                st.session_state.uploader_key += 1
                st.success(success_text)
                st.rerun()

        if st.session_state.table_rows:
            table_rows_html = ""
            for r in st.session_state.table_rows:
                table_rows_html += f"<tr><td style='text-align: center;'>{r['grade']}</td><td style='text-align: center;'>{r['period']}</td><td style='text-align: center;'>{r['subject']}</td><td>{r['lesson']}</td><td>{r['outcome'].replace('\n', '<br/>')}</td><td>{r['materials'].replace('\n', '<br/>')}</td><td>{r['teacher'].replace('\n', '<br/>')}</td><td>{r['student'].replace('\n', '<br/>')}</td><td>{r['assessment'].replace('\n', '<br/>')}</td></tr>"

            font_family = "'Iskoola Pota', 'Segoe UI', Arial, sans-serif" if lang == "සිංහල" else ("'Segoe UI', Arial, sans-serif" if lang == "English" else "'Latha', 'Segoe UI', Arial, sans-serif")
            lang_code_val = 'si' if lang=='සිංහල' else ('en' if lang=='English' else 'ta')

            final_html = f"""<!DOCTYPE html>
<html lang="{lang_code_val}">
<head>
<meta charset="UTF-8">
<style>
@media print {{
    body {{ -webkit-print-color-adjust: exact; }}
    .no-print {{ display: none !important; }}
    @page {{ size: A4 landscape; margin: 4mm; }}
}}
body {{
    font-family: {font_family};
    font-size: 8.5pt;
    color: #111;
    background: #fff;
    padding: 2px;
    margin: 0;
}}
.container {{
    width: 100%;
    max-width: 100%;
    margin: 0 auto;
    border: 1.5px solid #2C3E50;
    padding: 4px;
    background: #fff;
    box-sizing: border-box;
}}
h2 {{
    text-align: center;
    color: #2C3E50;
    margin: 0 0 4px 0;
    font-size: 11pt;
    border-bottom: 1.5px solid #2C3E50;
    padding-bottom: 2px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 2px;
    table-layout: auto;
}}
th, td {{
    border: 1px solid #7f8c8d;
    padding: 4px 4px;
    vertical-align: top;
    text-align: left;
    word-wrap: break-word;
    line-height: 1.2;
}}
th {{
    background-color: #f2f4f4;
    color: #2c3e50;
    font-weight: bold;
    text-align: center;
    font-size: 8.5pt;
    white-space: nowrap;
}}
.col-small {{
    width: 45px;
    text-align: center;
}}
.print-btn-container {{ text-align: center; margin-top: 10px; }}
.print-btn {{
    background-color: #27ae60;
    color: white;
    border: none;
    padding: 8px 16px;
    font-size: 10pt;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
}}
.print-btn:hover {{ background-color: #219653; }}
</style>
</head>
<body>
<div class="container" id="content-box">
<h2>{doc_title}</h2>
<table>
<tr>
<th class="col-small">{col_headers[0]}</th>
<th class="col-small">{col_headers[1]}</th>
<th class="col-small">{col_headers[2]}</th>
<th>{col_headers[3]}</th>
<th>{col_headers[4]}</th>
<th>{col_headers[5]}</th>
<th>{col_headers[6]}</th>
<th>{col_headers[7]}</th>
<th>{col_headers[8]}</th>
</tr>
{table_rows_html}
</table>
</div>
<div class="print-btn-container no-print">
<button class="print-btn" onclick="window.print()">{print_btn_text}</button>
</div>
</body>
</html>"""

            components.html(final_html, height=450, scrolling=True)

    # -------------------------------------------------------------------------
    # අංශය 2: වාර සටහන් (Term Plans)
    # -------------------------------------------------------------------------
    elif "📋 වාර සටහන්" in selected_tab:
        st.header("📋 වාර සටහන් සැකසීම (Term Plans)")
        st.info("මෙම අංශය ඉදිරියේදී වාර සටහන් (Term Plans) සැකසීම සඳහා ක්‍රියාත්මක වේ.")

    # -------------------------------------------------------------------------
    # අංශය 3: පැවරුම් (Assignments)
    # -------------------------------------------------------------------------
    elif "📝 පැවරුම්" in selected_tab:
        st.header("📝 සිසු පැවරුම් සකස් කිරීම (Student Assignments)")
        st.write("පාඩම් පිටු වල ඡායාරූප Upload කර, ඔබට අවශ්‍ය ප්‍රශ්න ගණන ලබා දී පැවරුම් පත්‍රයක් සකස් කරගන්න.")

        col_a, col_b = st.columns(2)
        with col_a:
            asg_grade = st.text_input("ශ්‍රේණිය (Grade)", value="10", key="asg_grade")
        with col_b:
            asg_subject = st.text_input("විෂය (Subject)", value="ICT" if lang=="English" else "බුද්ධාගම", key="asg_subject")

        asg_title = st.text_input("පැවරුම් මාතෘකාව / Assignment Title", value="Computer Systems Assignment", key="asg_title")
        num_questions = st.number_input("අවශ්‍ය ප්‍රශ්න ගණන (Number of Questions):", min_value=1, max_value=20, value=5, key="asg_num")

        asg_files = st.file_uploader(
            "📷 පාඩම් පිටු වල ඡායාරූප Upload කරන්න (Upload Image(s)):", 
            type=["png", "jpg", "jpeg"], 
            accept_multiple_files=True,
            key="asg_uploader"
        )

        if st.button("🚀 ප්‍රශ්න පත්‍රය සකස් කරන්න", type="primary", key="btn_gen_asg"):
            with st.spinner("Gemini 3.6 Flash හරහා ප්‍රශ්න සකස් කරමින් පවතී..."):
                generated_questions = ""
                
                if HAS_GENAI and GEMINI_API_KEY:
                    try:
                        model = genai.GenerativeModel('gemini-3.6-flash')
                        content_list = []
                        if asg_files:
                            for af in asg_files:
                                content_list.append(Image.open(af))
                        
                        prompt = (
                            f"You are an expert school teacher. Based on the provided textbook image(s) or topic '{asg_title}' for Grade {asg_grade}, Subject {asg_subject}, "
                            f"generate exactly {num_questions} clear assignment questions in {'English' if lang=='English' else ('தமிழ்' if lang=='தமிழ்' else 'සිංහල')}.\n"
                            "Format them clearly as numbered questions."
                        )
                        content_list.append(prompt)
                        response = model.generate_content(content_list)
                        if response and hasattr(response, 'text') and response.text:
                            generated_questions = response.text
                    except Exception as e:
                        generated_questions = f"AI දෝෂය: {e}"

                if not generated_questions:
                    generated_questions = "⚠️ කරුණාකර නිවැරදි ඡායාරූප Upload කරන්න."

                st.session_state.assignment_result = {
                    "grade": asg_grade,
                    "subject": asg_subject,
                    "title": asg_title,
                    "content": generated_questions
                }
                st.success("පැවරුම සාර්ථකව සකස් කරන ලදී!")

        if "assignment_result" in st.session_state and st.session_state.assignment_result:
            res = st.session_state.assignment_result
            st.markdown("---")
            st.subheader("📄 පැවරුම් පත්‍රය")
            
            asg_html = (
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<head>\n"
                '<meta charset="UTF-8">\n'
                "<style>\n"
                "@media print {\n"
                "    body { -webkit-print-color-adjust: exact; }\n"
                "    .no-print { display: none !important; }\n"
                "    @page { size: A4 portrait; margin: 15mm; }\n"
                "}\n"
                "body { font-family: Arial, sans-serif; font-size: 11pt; padding: 20px; }\n"
                ".header { text-align: center; border-bottom: 2px solid #2C3E50; padding-bottom: 10px; margin-bottom: 20px; }\n"
                "</style>\n"
                "</head>\n"
                "<body>\n"
                '<div class="header">\n'
                f"<h3>ශ්‍රේණිය: {res['grade']} | විෂය: {res['subject']}</h3>\n"
                f"<h4>මාතෘකාව: {res['title']}</h4>\n"
                "</div>\n"
                f"<div>{res['content'].replace(chr(10), '<br/>')}</div>\n"
                '<div class="no-print" style="text-align:center; margin-top:20px;">\n'
                '<button onclick="window.print()" style="background:#27ae60; color:white; border:none; padding:10px 20px; font-weight:bold; cursor:pointer;">🖨️ Save / Print PDF</button>\n'
                "</div>\n"
                "</body>\n"
                "</html>"
            )
            components.html(asg_html, height=500, scrolling=True)

    # -------------------------------------------------------------------------
    # අංශය 4: ප්‍රශ්න පත්‍ර (Question Papers)
    # -------------------------------------------------------------------------
    elif "❓ ප්‍රශ්න පත්‍ර" in selected_tab:
        st.header("❓ විභාග ප්‍රශ්න පත්‍ර සකස් කිරීම (Exam Question Papers)")
        st.write("පාසලේ නම, කාලය, විෂය ඇතුළත් කර, අවශ්‍ය ප්‍රශ්න වර්ගය තෝරා ප්‍රශ්න පත්‍රයක් සකස් කරගන්න.")

        qp_school = st.text_input("පාසලේ නම (School Name):", value="ශ්‍රී සුමංගල විද්‍යාලය - නාරංගස්වැව", key="qp_school")
        
        col_q1, col_q2, col_q3 = st.columns(3)
        with col_q1:
            qp_grade = st.text_input("ශ්‍රේණිය (Grade)", value="10", key="qp_grade")
        with col_q2:
            qp_subject = st.text_input("විෂය (Subject)", value="ICT" if lang=="English" else "බුද්ධාගම", key="qp_subject")
        with col_q3:
            qp_time = st.text_input("කාලය (Time)", value="පැය 01 යි", key="qp_time")

        st.markdown("---")
        st.subheader("⚙️ ප්‍රශ්න සැකසුම් (Question Configuration)")

        q_type = st.selectbox(
            "ප්‍රශ්න වර්ගය තෝරන්න / Select Question Type:",
            ["බහුවරණ ප්‍රශ්න (MCQ)", "කෙටි ප්‍රශ්න (Short Questions)", "රචනා ප්‍රශ්න (Essay Questions)", "මිශ්‍ර ප්‍රශ්න පත්‍රය (Mixed Paper)"],
            key="qp_type"
        )

        qp_count = st.number_input("අවශ්‍ය ප්‍රශ්න ප්‍රමාණය (Number of Questions):", min_value=1, max_value=50, value=10, key="qp_count")

        qp_files = st.file_uploader(
            "📷 පාඩම් පිටු වල ඡායාරූප Upload කරන්න (Upload Image(s) for Paper):", 
            type=["png", "jpg", "jpeg"], 
            accept_multiple_files=True,
            key="qp_uploader"
        )

        if st.button("🚀 ප්‍රශ්න පත්‍රය සකස් කරන්න", type="primary", key="btn_gen_qp"):
            with st.spinner("Gemini 3.6 Flash හරහා විභාග ප්‍රශ්න සකස් කරමින් පවතී..."):
                paper_content = ""
                
                if HAS_GENAI and GEMINI_API_KEY:
                    try:
                        model = genai.GenerativeModel('gemini-3.6-flash')
                        content_list = []
                        if qp_files:
                            for qf in qp_files:
                                content_list.append(Image.open(qf))
                        
                        prompt = (
                            f"You are an expert school examination board. Based on the provided textbook image(s) or syllabus for Grade {qp_grade}, Subject {qp_subject}, "
                            f"generate an official school exam question paper consisting of exactly {qp_count} questions of type '{q_type}' in {'English' if lang=='English' else ('தமிழ்' if lang=='தமிழ்' else 'සිංහල')}.\n"
                            "Do not include placeholder text. Generate real, subject-specific professional exam questions with clear numbering."
                        )
                        content_list.append(prompt)
                        response = model.generate_content(content_list)
                        if response and hasattr(response, 'text') and response.text:
                            paper_content = response.text
                    except Exception as e:
                        paper_content = f"Gemini API දෝෂය: {e}"

                if not paper_content:
                    paper_content = "⚠️ ප්‍රශ්න සකස් කර ගැනීමට කරුණාකර පාඩම් පිටුවක ඡායාරූපයක් Upload කරන්න."

                st.session_state.question_paper_result = {
                    "school": qp_school,
                    "grade": qp_grade,
                    "subject": qp_subject,
                    "time": qp_time,
                    "type": q_type,
                    "content": paper_content
                }
                st.success("විභාග ප්‍රශ්න පත්‍රය සාර්ථකව සකස් කරන ලදී!")

        if "question_paper_result" in st.session_state and st.session_state.question_paper_result:
            qp = st.session_state.question_paper_result
            st.markdown("---")
            st.subheader("📄 සකස් කළ විභාග ප්‍රශ්න පත්‍රය (Exam Question Paper Preview)")
            
            paper_html = (
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<head>\n"
                '<meta charset="UTF-8">\n'
                "<style>\n"
                "@media print {\n"
                "    body { -webkit-print-color-adjust: exact; }\n"
                "    .no-print { display: none !important; }\n"
                "    @page { size: A4 portrait; margin: 15mm; }\n"
                "}\n"
                "body {\n"
                "    font-family: 'Iskoola Pota', 'Segoe UI', Arial, sans-serif;\n"
                "    font-size: 11pt;\n"
                "    color: #111;\n"
                "    background: #fff;\n"
                "    padding: 20px;\n"
                "    line-height: 1.5;\n"
                "}\n"
                ".school-header {\n"
                "    text-align: center;\n"
                "    border-bottom: 2px solid #000;\n"
                "    padding-bottom: 8px;\n"
                "    margin-bottom: 15mm;\n"
                "}\n"
                ".school-header h2 { margin: 0; font-size: 16pt; font-weight: bold; }\n"
                ".school-header h3 { margin: 5px 0; font-size: 13pt; }\n"
                ".exam-meta {\n"
                "    display: flex;\n"
                "    justify-content: space-between;\n"
                "    font-weight: bold;\n"
                "    margin-bottom: 20px;\n"
                "    border-bottom: 1px solid #7f8c8d;\n"
                "    padding-bottom: 8px;\n"
                "}\n"
                ".paper-body {\n"
                "    white-space: pre-wrap;\n"
                "}\n"
                ".print-btn {\n"
                "    background-color: #27ae60;\n"
                "    color: white;\n"
                "    border: none;\n"
                "    padding: 10px 20px;\n"
                "    font-size: 12pt;\n"
                "    border-radius: 5px;\n"
                "    cursor: pointer;\n"
                "    font-weight: bold;\n"
                "    display: block;\n"
                "    margin: 20px auto;\n"
                "}\n"
                "</style>\n"
                "</head>\n"
                "<body>\n"
                '<div class="school-header">\n'
                f"<h2>{qp['school']}</h2>\n"
                f"<h3>ශ්‍රේණිය {qp['grade']} - {qp['subject']}</h3>\n"
                "</div>\n"
                '<div class="exam-meta">\n'
                f"<span>විෂය: {qp['subject']}</span>\n"
                f"<span>කාලය: {qp['time']}</span>\n"
                f"<span>ශ්‍රේණිය: {qp['grade']}</span>\n"
                "</div>\n"
                '<div class="paper-body">\n'
                f"{qp['content'].replace(chr(10), '<br/>')}\n"
                "</div>\n"
                '<div class="no-print">\n'
                '<button class="print-btn" onclick="window.print()">🖨️ Save / Print as PDF</button>\n'
                "</div>\n"
                "</body>\n"
                "</html>"
            )
            components.html(paper_html, height=650, scrolling=True)

else:
    st.warning("🔒 සේවාවන් ලබා ගැනීමට කරුණාකර ඔබගේ ජාතික හැඳුනුම්පත් අංකය (NIC) වම්පස ඇති මෙනුවෙහි ඇතුළත් කරන්න.")
    st.info("💡 මෙම ඇප් එක භාවිත කිරීමට දායක මුදල් ගෙවා ගිණුම සක්‍රීය කරගත යුතුය. විමසීම් සඳහා සංවර්ධකයා අමතන්න.")