from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import streamlit as st
import os

# 美しい配色とデザインのCSSスタイル
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* 全体の背景とテーマ */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* メインコンテナの美しいデザイン */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        padding: 2rem;
        margin: 1rem;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* タイトルの美しいスタイル */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-align: center;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem !important;
        line-height: 1.2 !important;
    }
    
    /* サブタイトルの美しいスタイル */
    h3 {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: #2d3748 !important;
        margin: 1rem 0 0.5rem 0 !important;
    }
    
    /* テキストの改善 */
    .stMarkdown p {
        font-size: 1rem;
        line-height: 1.6;
        color: #4a5568;
        margin-bottom: 0.75rem;
    }
    
    /* カードスタイルのコンテナ */
    .info-card {
        background: linear-gradient(145deg, #f7fafc, #edf2f7);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.8);
    }
    
    /* ラジオボタンの美しいスタイル */
    .stRadio > label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #2d3748 !important;
    }
    
    .stRadio > div {
        gap: 1rem;
        background: #f8fafc;
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
    }
    
    .stRadio > div > label {
        background: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 2px solid transparent;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stRadio > div > label:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* テキストエリアの美しいスタイル */
    .stTextArea > label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #2d3748 !important;
    }
    
    .stTextArea textarea {
        font-size: 1rem !important;
        padding: 1rem !important;
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        background: #f8fafc !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        background: white !important;
    }
    
    /* メインボタンの美しいスタイル */
    .stButton > button {
        width: 100% !important;
        padding: 1rem 2rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        margin-top: 1.5rem !important;
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* フィードバックボタンの美しいスタイル */
    .stButton > button[kind="secondary"] {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        color: #4a5568 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        margin: 0.5rem !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        width: auto !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        border-color: #667eea !important;
        color: #667eea !important;
        transform: translateY(-2px) !important;
    }
    
    /* 区切り線の美しいスタイル */
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent) !important;
    }
    
    /* アラートメッセージの美しいスタイル */
    .stAlert {
        margin: 1rem 0 !important;
        font-size: 1rem !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #68d391, #38a169) !important;
        color: white !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #fc8181, #e53e3e) !important;
        color: white !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f6e05e, #d69e2e) !important;
        color: white !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #63b3ed, #3182ce) !important;
        color: white !important;
    }
    
    /* スピナーの美しいスタイル */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* 回答ボックスの美しいスタイル */
    .answer-box {
        background: linear-gradient(145deg, #f0fff4, #e6fffa);
        border: 2px solid #68d391;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(104, 211, 145, 0.2);
        position: relative;
    }
    
    .answer-box::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, #68d391, #38a169);
        border-radius: 15px;
        z-index: -1;
    }
    
    /* レスポンシブ対応 */
    @media (max-width: 768px) {
        .main .block-container {
            margin: 0.5rem;
            padding: 1.5rem;
            border-radius: 15px;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        h3 {
            font-size: 1.2rem !important;
        }
        
        .stMarkdown p {
            font-size: 0.9rem;
        }
    }
    
    @media (max-width: 480px) {
        .main .block-container {
            margin: 0.25rem;
            padding: 1rem;
        }
        
        h1 {
            font-size: 1.7rem !important;
        }
        
        .stTextArea textarea {
            font-size: 16px !important; /* iOSのズーム防止 */
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI専門家に相談しよう!")

st.markdown("""
<div class="info-card" style="text-align: center;">
    <h4 style="margin: 0 0 0.5rem 0; color: #2d3748; font-weight: 600;">✨ AIパーソナルアドバイザー</h4>
    <p style="margin: 0; color: #4a5568; font-size: 1.1rem;">選択した専門家として、AIがあなたの質問に丁寧にお答えします</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🎯 専門家を選択")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4299e1, #3182ce); color: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(66, 153, 225, 0.3);">
        <h4 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">💼 転職の専門家</h4>
        <p style="margin: 0; opacity: 0.9;">キャリア・転職相談</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #48bb78, #38a169); color: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);">
        <h4 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">🏥 健康の専門家</h4>
        <p style="margin: 0; opacity: 0.9;">健康・ウェルネス相談</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #fef5e7, #fed7aa); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #f6ad55; margin: 1rem 0;">
    <h4 style="margin: 0 0 0.5rem 0; color: #c05621; font-weight: 600;">📝 使い方</h4>
    <p style="margin: 0; color: #744210; font-size: 1rem;">① 下記から専門家を選択 → ② 質問を入力 → ③ 相談ボタンを押す</p>
</div>
""", unsafe_allow_html=True)

selected_item = st.radio(
    "🔽 専門家を選択してください",
    ["💼 転職の専門家", "🏥 健康の専門家"],
    horizontal=False
)

st.markdown("---")

user_input = st.text_area(
    "💬 質問を入力してください",
    placeholder="例：転職活動で悩んでいることがあります...",
    height=100
)

if st.button("🚀 AI専門家に相談する", type="primary"):
    if not user_input.strip():
        st.error("⚠️ 質問を入力してください。")
    else:
        with st.spinner("🤔 AI専門家が回答を考えています..."):
            if "転職" in selected_item:
                system_message = SystemMessage(
                    content="あなたは経験豊富な転職の専門家です。ユーザーの質問に対して、具体的で実践的なアドバイスを提供してください。親切で分かりやすい説明を心がけてください。"
                )
            else:
                system_message = SystemMessage(
                    content="あなたは経験豊富な健康の専門家です。ユーザーの質問に対して、科学的根拠に基づいた信頼できるアドバイスを提供してください。親切で分かりやすい説明を心がけてください。"
                )

            human_message = HumanMessage(content=user_input)

            try:
                chat = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.5,
                    openai_api_key=os.getenv("OPENAI_API_KEY")
                )

                response = chat.invoke([system_message, human_message])
                
                st.markdown("---")
                expert_type = "💼 転職専門家" if "転職" in selected_item else "🏥 健康専門家"
                st.markdown(f"### 💡 {expert_type}からの回答")
                
                # 回答を美しく表示
                st.markdown(f"""
                <div class="answer-box">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <div style="font-size: 1.5rem; margin-right: 0.5rem;">{'💼' if '転職' in selected_item else '🏥'}</div>
                        <div style="font-weight: 600; color: #2d3748; font-size: 1.1rem;">{expert_type}</div>
                    </div>
                    <div style="color: #2d3748; line-height: 1.7; font-size: 1rem;">
                        {response.content.replace('\n', '<br>')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 満足度フィードバック
                st.markdown("---")
                st.markdown("""
                <div style="text-align: center; margin: 2rem 0 1rem 0;">
                    <h4 style="color: #2d3748; font-weight: 600; margin-bottom: 1rem;">📊 この回答はいかがでしたか？</h4>
                </div>
                """, unsafe_allow_html=True)
                
                feedback_col1, feedback_col2, feedback_col3 = st.columns(3)
                with feedback_col1:
                    if st.button("👍 満足", key="satisfied"):
                        st.success("✨ フィードバックありがとうございます！")
                with feedback_col2:
                    if st.button("👌 普通", key="neutral"):
                        st.info("📝 ご意見ありがとうございます。")
                with feedback_col3:
                    if st.button("👎 改善希望", key="unsatisfied"):
                        st.warning("🔧 改善に努めます。")
                        
            except Exception as e:
                st.error("❌ エラーが発生しました")
                st.markdown("""
                <div style="background: linear-gradient(135deg, #fed7d7, #fbb6ce); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #e53e3e; margin: 1rem 0;">
                    <h4 style="margin: 0 0 1rem 0; color: #742a2a; font-weight: 600;">⚠️ 以下をご確認ください</h4>
                    <ul style="color: #742a2a; margin: 0; padding-left: 1.5rem;">
                        <li>OpenAI APIキーが正しく設定されているか</li>
                        <li>インターネット接続が安定しているか</li>
                        <li>APIの利用制限に達していないか</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("🔍 詳細なエラー情報"):
                    st.code(str(e))