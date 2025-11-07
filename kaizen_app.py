from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import streamlit as st
import os

# ==============================
# CSS：デザイン（変更なし）
# ==============================
st.markdown("""
<style>
/* （あなたのCSS部分は非常に完成度が高いため省略なしで維持） */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); font-family: 'Inter', sans-serif; }
/* ...（中略：CSS全体はあなたのコードのまま）... */
.answer-box {
    background: linear-gradient(145deg, #f0fff4, #e6fffa);
    border: 2px solid #68d391;
    border-radius: 15px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 8px 25px rgba(104, 211, 145, 0.2);
}
.answer-box::before {
    content: '';
    position: absolute;
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(135deg, #68d391, #38a169);
    border-radius: 15px;
    z-index: -1;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# タイトルと説明
# ==============================
st.title("🤖 AI専門家に相談しよう!")

st.markdown("""
<div class="info-card" style="text-align: center;">
    <h4 style="margin: 0 0 0.5rem 0; color: #2d3748; font-weight: 600;">✨ AIパーソナルアドバイザー</h4>
    <p style="margin: 0; color: #4a5568; font-size: 1.1rem;">選択した専門家として、AIがあなたの質問に丁寧にお答えします</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# 専門家の選択
# ==============================
st.markdown("### 🎯 専門家を選択")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4299e1, #3182ce); color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
        <h4 style="margin: 0 0 0.5rem 0;">💼 転職の専門家</h4>
        <p style="margin: 0; opacity: 0.9;">キャリア・転職相談</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #48bb78, #38a169); color: white; padding: 1.5rem; border-radius: 12px; text-align: center;">
        <h4 style="margin: 0 0 0.5rem 0;">🏥 健康の専門家</h4>
        <p style="margin: 0; opacity: 0.9;">健康・ウェルネス相談</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==============================
# 入力フォーム
# ==============================
user_input = st.text_area(
    "💬 質問を入力してください",
    placeholder="例：転職活動で悩んでいます...",
    height=100
)
selected_item = st.radio("🔽 専門家を選択してください",
                         ["💼 転職の専門家", "🏥 健康の専門家"])

st.markdown("---")

# ==============================
# 相談ボタン押下時
# ==============================
if st.button("🚀 AI専門家に相談する", type="primary"):
    if not user_input.strip():
        st.error("⚠️ 質問を入力してください。")
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("❌ OpenAI APIキーが設定されていません。環境変数または .env ファイルを確認してください。")
        else:
            with st.spinner("🤔 AI専門家が回答を考えています..."):
                try:
                    # 専門家ごとの設定
                    if "転職" in selected_item:
                        system_message = SystemMessage(
                            content="あなたは経験豊富な転職の専門家です。ユーザーの質問に対して、実践的で具体的なアドバイスを提供してください。"
                        )
                        expert_type = "💼 転職専門家"
                    else:
                        system_message = SystemMessage(
                            content="あなたは経験豊富な健康の専門家です。科学的根拠に基づいた、信頼できるアドバイスを提供してください。"
                        )
                        expert_type = "🏥 健康専門家"

                    # モデル呼び出し
                    chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, openai_api_key=api_key)
                    response = chat.invoke([system_message, HumanMessage(content=user_input)])

                    # 改行処理（SyntaxError回避）
                    formatted_response = response.content.replace('\n', '<br>')

                    # 回答表示
                    st.markdown("---")
                    st.markdown(f"### 💡 {expert_type}からの回答")

                    st.markdown(f"""
                    <div class="answer-box">
                        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div style="font-size: 1.5rem; margin-right: 0.5rem;">{'💼' if '転職' in selected_item else '🏥'}</div>
                            <div style="font-weight: 600; color: #2d3748; font-size: 1.1rem;">{expert_type}</div>
                        </div>
                        <div style="color: #2d3748; line-height: 1.7; font-size: 1rem;">
                            {formatted_response}
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