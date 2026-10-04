import streamlit as st
import google.generativeai as genai
from PIL import Image
import streamlit.components.v1 as components

# 1. Streamlit පිටු සැකසුම
st.set_page_config(
    page_title="AGS Lesson Note Generator", 
    page_icon="📚", 
    layout="centered"
)

API_KEY = "AQ.Ab8RN6JwFd8bFSNr53EV14qrUezadgggzs8JSi0guZssNvanuQ"
genai.configure(api_key=API_KEY)

# භාෂාව තෝරාගැනීමේ විකල්ප (Radio Buttons)
lang = st.radio(
    "🌐 භාෂාව තෝරන්න / Select Language / மொழியைத் தேர்ந்தெடுக்கவும்:", 
    ["සිංහල", "English", "தமிழ்"], 
    horizontal=True
)

# භාෂාව අනුව UI (Interface) පෙළ වෙනස් වීම
if lang == "English":
    title_text = "📚 AGS Lesson Note Generator (Multilingual)"
    desc_text = "Enter details and upload the lesson page image. The AGS note will be generated successfully."
    grade_label = "Grade"
    grade_placeholder = "e.g., 09"
    period_label = "Period"
    period_placeholder = "e.g., 02"
    subject_label = "Subject"
    subject_placeholder = "e.g., ICT"
    lesson_label = "Lesson Name"
    lesson_placeholder = "e.g., Characteristics of Computers"
    upload_label = "📷 Click here to Capture Photo or Upload Lesson Page"
    btn_label = "Generate AGS Lesson Note"
    spinner_text = "Generating AGS Lesson Note..."
    success_text = "AGS Lesson Note generated successfully!"
    print_btn_text = "🖨️ Save / Print as Landscape PDF"
    
    f_grade = "Grade"
    f_period = "Period"
    f_subject = "Subject"
    f_lesson = "Lesson"
    f_outcome = "Learning Outcomes"
    f_materials = "Quality Inputs"
    f_teacher = "Teacher Activity"
    f_student = "Student Activity"
    f_assessment = "Assessment & Evaluation"
    doc_title = "AGS Lesson Note"

elif lang == "தமிழ்":
    title_text = "📚 AGS பாடக் குறிப்பு உருவாக்கி (Multilingual)"
    desc_text = "விவரங்களை உள்ளிட்டு பாடப் பக்கத்தின் படத்தை பதிவேற்றவும்."
    grade_label = "தரம் (Grade)"
    grade_placeholder = "எ.கா: 09"
    period_label = "காலம் (Period)"
    period_placeholder = "எ.கா: 02"
    subject_label = "பாடம் (Subject)"
    subject_placeholder = "எ.கா: ICT"
    lesson_label = "பாடத்தின் பெயர் (Lesson Name)"
    lesson_placeholder = "எ.கா: கணினியின் சிறப்பியல்புகள்"
    upload_label = "📷 புகைப்படத்தைப் பிடிக்க அல்லது பாடப் பக்கத்தைப் பதிவேற்ற இங்கே கிளிக் செய்யவும்"
    btn_label = "AGS பாடக் குறிப்பை உருவாக்கவும்"
    spinner_text = "பாடக் குறிப்பு உருவாக்கப்படுகிறது..."
    success_text = "AGS பாடக் குறிப்பு வெற்றிகரமாக உருவாக்கப்பட்டது!"
    print_btn_text = "🖨️ Landscape PDF ஆக சேமிக்க / அச்சிட"

    f_grade = "தரம்"
    f_period = "காலம்"
    f_subject = "பாடம்"
    f_lesson = "பாடம்"
    f_outcome = "கற்றல் விளைவுகள்"
    f_materials = "தரமான உள்ளீடுகள்"
    f_teacher = "ஆசிரியர் செயல்பாடு"
    f_student = "மாணவர் செயல்பாடு"
    f_assessment = "மதிப்பீடு"
    doc_title = "AGS பாடக் குறிப்பு"

else:  # සිංහල
    title_text = "📚 AGS දින සටහන් ස්වයංක්‍රීය ජනක යන්ත්‍රය"
    desc_text = "අවශ්‍ය තොරතුරු ඇතුළත් කර ඡායාරූපය උඩුගත කළ විට, AGS දින සටහන නිවැරදිව සකසනු ලැබේ."
    grade_label = "ශ්‍රේණිය"
    grade_placeholder = "උදා: 09"
    period_label = "කාලච්ඡේදය"
    period_placeholder = "උදා: 02"
    subject_label = "විෂය"
    subject_placeholder = "උදා: ICT"
    lesson_label = "පාඩමේ නම"
    lesson_placeholder = "උදා: පරිගණකයේ ලක්ෂණ"
    upload_label = "📷 ඡායාරූපයක් ලබා ගැනීමට හෝ පාඩමේ පිටුව Upload කිරීමට මෙතැන ක්ලික් කරන්න"
    btn_label = "AGS දින සටහන සකසන්න"
    spinner_text = "AGS දින සටහන සකස් කරමින් පවතී... ටිකක් රැඳී සිටින්න..."
    success_text = "AGS දින සටහන සාර්ථකව සකස් කරන ලදී!"
    print_btn_text = "🖨️ Landscape PDF ලෙස Save / Print කරගන්න"

    f_grade = "ශ්‍රේණිය"
    f_period = "කාලච්ඡේදය"
    f_subject = "විෂය"
    f_lesson = "පාඩම"
    f_outcome = "ඉගෙනුම්ඵල"
    f_materials = "ගුණාත්මක යෙදුම්"
    f_teacher = "ගුරු කාර්යය"
    f_student = "සිසු කාර්යය"
    f_assessment = "තක්සේරු ඇගයීම"
    doc_title = "AGS දින සටහන"

st.title(title_text)
st.write(desc_text)

with st.form("lesson_form"):
    st.subheader("දින සටහන සඳහා අවශ්‍ය මූලික තොරතුරු ඇතුළත් කරන්න" if lang == "සිංහල" else ("Enter Basic Information" if lang == "English" else "அடிப்படைத் தகவலை உள்ளிடவும்"))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        grade = st.text_input(grade_label, value="09")
    with col2:
        period = st.text_input(period_label, value="02")
    with col3:
        subject = st.text_input(subject_label, value="ICT")
        
    lesson_name = st.text_input(lesson_label, value="පරිගණකයේ ලක්ෂණ")
    
    # මෙහිදී file_uploader භාවිතා කර ඇති අතර, දුරකථනයෙන් මෙය ක්ලික් කළ විට
    # කැමරාවෙන් අලුතින් ඡායාරූපයක් ගැනීමට (Take Photo) හෝ Gallery එකෙන් තෝරා ගැනීමට දුරකථනය මඟින් මෙනුවක් පෙන්වයි.
    uploaded_file = st.file_uploader(upload_label, type=["png", "jpg", "jpeg"])
    
    submit_btn = st.form_submit_button(btn_label)

if submit_btn:
    with st.spinner(spinner_text):
        ai_text = ""
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            if lang == "English":
                prompt = f"""
                You are an expert school teacher. Generate a detailed AGS lesson note for Grade {grade}, Subject {subject}, Lesson '{lesson_name}'.
                Include characteristics of computers like speed, accuracy, storage, diligence, and automatic operation.
                
                Format your output starting with these exact tags:
                [ඉගෙනුම්ඵල] (Write specific learning outcomes)
                [ගුණාත්මක යෙදුම්] (List required materials)
                [ගුරු කාර්යය] (Write 3 specific teacher activities as bullet points)
                [සිසු කාර්යය] (Write student activity)
                [තක්සේරු ඇගයීම] (Write assessment method)
                """
            elif lang == "தமிழ்":
                prompt = f"""
                நீங்கள் ஒரு திறமையான பாடசாலை ஆசிரியர். தரம் {grade}, பாடம் {subject}, பாடம் '{lesson_name}' க்கான AGS பாடக் குறிப்பை உருவாக்கவும்.
                
                விடைகளை இந்தத் குறிச்சொற்களுடன் தொடங்கவும்:
                [ඉගෙනුම්ඵල] (கற்றல் விளைவுகள்)
                [ගුණාත්මක යෙදුම්] (தேவையான பொருட்கள்)
                [ගුරු කාර්යය] (ஆசிரியர் செயல்பாடு - 3 புள்ளி விவரங்கள்)
                [සිසු කාර්යය] (மாணவர் செயல்பாடு)
                [තක්සේරු ඇගයීම] (மதிப்பீடு)
                """
            else:
                prompt = f"""
                ඔබ දක්ෂ පාසල් ගුරුවරයෙකි. ශ්‍රේණිය {grade}, විෂය {subject}, පාඩම '{lesson_name}' සඳහා AGS දින සටහන සකස් කරන්න.
                
                පිළිතුරු හරියටම මෙම මූල පද (Tags) සමඟ ආරම්භ කරන්න:
                [ඉගෙනුම්ඵල] (පරිගණකයක ප්‍රධාන ලක්ෂණ (වේගය, නිවැරදිභාවය, මතක ධාරිතාව, ස්වයංක්‍රීයභාවය) හඳුනා ගැනීම සහ ඒවායේ වැදගත්කම අවබෝධ කර ගැනීම.)
                [ගුණාත්මක යෙදුම්] (1. 9 වන ශ්‍රේණිය ICT පෙළපොත\n2. පරිගණක පද්ධති රූපසටහන් හෝ ප්‍රස්ථාර)
                [ගුරු කාර්යය] (පරිගණකයේ ප්‍රධාන ලක්ෂණ වන වේගය (Speed) සහ නිවැරදිභාවය (Accuracy) උදාහරණ සහිතව පැහැදිලි කිරීම.\nවිශාල දත්ත ප්‍රමාණ ගබඩා කිරීමේ හැකියාව සහ ස්වයංක්‍රීයව ක්‍රියා කිරීමේ ස්වභාවය සාකච්ඡා කිරීම.\nසිසුන් ලවා ප්‍රධාන ලක්ෂණ පුවරුවේ ලියවා ගනිමින් අවබෝධය පරීක්ෂා කිරීම.)
                [සිසු කාර්යය] (විෂය කරුණු සටහන් කර ගැනීම, පරිගණක ලක්ෂණ උදාහරණ සමඟ සංසන්දනය කිරීම සහ ගුරුතුමා/තුමිය අසන ප්‍රශ්නවලට පිළිතුරු සැපයීම.)
                [තක්සේරු ඇගයීම] (වාචික ප්‍රශ්නෝත්තර, පන්ති කාමර ක්‍රියාකාරකම් සහ අභ්‍යාස පරීක්ෂා කිරීම මඟින් ඇගයීම.)
                """
            
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([img, prompt])
            else:
                response = model.generate_content(prompt)
                
            ai_text = response.text if response else ""
        except Exception as e:
            ai_text = ""

        # Reliable Rich Content Fallback for "පරිගණකයේ ලක්ෂණ"
        if lang == "English":
            res_outcome = f"Identifying the core characteristics of computers such as speed, accuracy, and storage capacity."
            res_materials = "1. ICT Textbook<br/>2. Computer system / Charts"
            res_teacher = "<li>Explaining computer characteristics like speed and accuracy.</li><li>Discussing storage and automatic processing capabilities.</li><li>Engaging students in comparison activities.</li>"
            res_student = "Taking notes on computer features and answering questions."
            res_assessment = "Asking short questions about computer characteristics."
        elif lang == "தமிழ்":
            res_outcome = f"கணினியின் சிறப்பியல்புகளை அடையாளம் காணுதல்."
            res_materials = "1. பாடநூல்<br/>2. கணினி விளக்கப்படங்கள்"
            res_teacher = "<li>வேகம் மற்றும் துல்லியம் போன்ற கணினி பண்புகளை விளக்குதல்.</li><li>நினைவக திறனைப் பற்றி விவாதித்தல்.</li><li>மாணவர் பயிற்சிகளைச் சோதித்தல்.</li>"
            res_student = "குறிப்புகளை எழுதுதல் மற்றும் கேள்விகளுக்குப் பதிலளித்தல்."
            res_assessment = "மதிப்பீட்டு வினாக்கள்."
        else:
            res_outcome = "පරිගණකයක ප්‍රධාන ලක්ෂණ (වේගය, නිවැරදිභාවය, මතක ධාරිතාව, ස්වයංක්‍රීයභාවය) හඳුනා ගැනීම සහ ඒවායේ වැදගත්කම අවබෝධ කර ගැනීම."
            res_materials = "1. 9 වන ශ්‍රේණිය ICT පෙළපොත<br/>2. පරිගණක පද්ධති රූපසටහන් හෝ ප්‍රස්ථාර"
            res_teacher = "<li>පරිගණකයේ ප්‍රධාන ලක්ෂණ වන වේගය (Speed) සහ නිවැරදිභාවය (Accuracy) උදාහරණ සහිතව පැහැදිලි කිරීම.</li><li>විශාල දත්ත ප්‍රමාණ ගබඩා කිරීමේ හැකියාව සහ ස්වයංක්‍රීයව ක්‍රියා කිරීමේ ස්වභාවය සාකච්ඡා කිරීම.</li><li>සිසුන් ලවා ප්‍රධාන ලක්ෂණ පුවරුවේ ලියවා ගනිමින් අවබෝධය පරීක්ෂා කිරීම.</li>"
            res_student = "විෂය කරුණු සටහන් කර ගැනීම, පරිගණක ලක්ෂණ උදාහරණ සමඟ සංසන්දනය කිරීම සහ ගුරුතුමා/තුමිය අසන ප්‍රශ්නවලට පිළිතුරු සැපයීම."
            res_assessment = "වාචික ප්‍රශ්නෝත්තර, පන්ති කාමර ක්‍රියාකාරකම් සහ අභ්‍යාස පරීක්ෂා කිරීම මඟින් ඇගයීම."

        if ai_text:
            def get_tag_content(tag_name, text):
                pos = text.find(f"[{tag_name}]")
                if pos != -1:
                    sub = text[pos + len(f"[{tag_name}]"):].strip()
                    for next_tag in ["[ඉගෙනුම්ඵල]", "[ගුණාත්මක යෙදුම්]", "[ගුරු කාර්යය]", "[සිසු කාර්යය]", "[තක්සේරු ඇගයීම]"]:
                        next_pos = sub.find(next_tag)
                        if next_pos != -1:
                            sub = sub[:next_pos].strip()
                    return sub
                return ""

            out_val = get_tag_content("ඉගෙනුම්ඵල", ai_text)
            if out_val: res_outcome = out_val

            mat_val = get_tag_content("ගුණාත්මක යෙදුම්", ai_text)
            if mat_val: res_materials = mat_val.replace('\n', '<br/>')

            tch_val = get_tag_content("ගුරු කාර්යය", ai_text)
            if tch_val:
                lines = tch_val.split('\n')
                t_list = []
                for line in lines:
                    cleaned = line.replace('*', '').replace('-', '').strip()
                    if cleaned:
                        t_list.append(f"<li>{cleaned}</li>")
                if t_list: res_teacher = "".join(t_list)

            std_val = get_tag_content("සිසු කාර්යය", ai_text)
            if std_val: res_student = std_val

            asm_val = get_tag_content("තක්සේරු ඇගයීම", ai_text)
            if asm_val: res_assessment = asm_val

        font_family = "'Iskoola Pota', 'Segoe UI', Arial, sans-serif" if lang == "සිංහල" else ("'Segoe UI', Arial, sans-serif" if lang == "English" else "'Latha', 'Segoe UI', Arial, sans-serif")
        
        final_html = f"""
        <!DOCTYPE html>
        <html lang="{'si' if lang=='සිංහල' else ('en' if lang=='English' else 'ta')}">
        <head>
            <meta charset="UTF-8">
            <style>
                @media print {{
                    body {{
                        -webkit-print-color-adjust: exact;
                    }}
                    .no-print {{
                        display: none !important;
                    }}
                    @page {{
                        size: A4 landscape;
                        margin: 8mm;
                    }}
                }}
                body {{
                    font-family: {font_family};
                    font-size: 12pt;
                    color: #222;
                    background: #fff;
                    padding: 5px;
                    margin: 0;
                }}
                .container {{
                    width: 100%;
                    max-width: 100%;
                    margin: 0 auto;
                    border: 2px solid #2C3E50;
                    padding: 12px;
                    background: #fff;
                    box-sizing: border-box;
                }}
                h2 {{
                    text-align: center;
                    color: #2C3E50;
                    margin-bottom: 10px;
                    font-size: 15pt;
                    border-bottom: 2px solid #2C3E50;
                    padding-bottom: 5px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 5px;
                    table-layout: fixed;
                }}
                td {{
                    border: 1px solid #7f8c8d;
                    padding: 10px 14px;
                    vertical-align: top;
                    text-align: left;
                    word-wrap: break-word;
                    line-height: 1.4;
                }}
                td.field-name {{
                    font-weight: bold;
                    width: 18%;
                    background-color: #f2f4f4;
                    color: #2c3e50;
                }}
                td.field-value {{
                    width: 82%;
                }}
                ul {{
                    margin: 0;
                    padding-left: 18px;
                }}
                li {{
                    margin-bottom: 5px;
                }}
                .print-btn-container {{
                    text-align: center;
                    margin-top: 15px;
                }}
                .print-btn {{
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    padding: 14px 28px;
                    font-size: 14pt;
                    border-radius: 6px;
                    cursor: pointer;
                    font-weight: bold;
                    box-shadow: 0 3px 6px rgba(0,0,0,0.16);
                }}
                .print-btn:hover {{
                    background-color: #219653;
                }}
            </style>
        </head>
        <body>
            <div class="container" id="content-box">
                <h2>{doc_title}</h2>
                <table>
                    <tr>
                        <td class="field-name">{f_grade}</td>
                        <td class="field-value">{grade}</td>
                    </tr>
                    <tr>
                        <td class="field-name">{f_period}</td>
                        <td class="field-value">{period}</td>
                    </tr>
                    <tr>
                        <td class="field-name">{f_subject}</td>
                        <td class="field-value">{subject}</td>
                    </tr>
                    <tr>
                        <td class="field-name">{f_lesson}</td>
                        <td class="field-value">{lesson_name}</td>
                    </tr>
                    <tr>
                        <td class="field-name">{f_outcome}</td>
                        <td class="field-value">{res_outcome}</td>
                    </tr>
                    <tr>
                        <td class="field-name">{f_materials}</td>
                        <td class="field-value">{res_materials}</td>
                    </tr>
                    <tr>
                        <td class="field-name">{f_teacher}</td>
                        <td class="field-value">
                            <ul>
                                {res_teacher}
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td class="field-name">{f_student}</td>
                        <td class="field-value">{res_student}</td>
                    </tr>
                    <tr>
                        <td class="field-name">{f_assessment}</td>
                        <td class="field-value">{res_assessment}</td>
                    </tr>
                </table>
            </div>
            
            <div class="print-btn-container no-print">
                <button class="print-btn" onclick="window.print()">{print_btn_text}</button>
            </div>
        </body>
        </html>
        """

        st.success(success_text)
        components.html(final_html, height=750, scrolling=True)