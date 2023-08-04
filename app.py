import streamlit as st
import openai
from gtts import gTTS
from io import BytesIO
from gtts import gTTS, gTTSError

# Tab
st.set_page_config(
    page_title="ICE Breaker",
    page_icon="⛄",
    layout="centered",
    initial_sidebar_state="auto",
)

# List
meeting_type_list = {
    '定例会議':'同じグループで仕事をしていて、お互いのことをまあまあ知っているメンバー',
    '部門連携会議':'異なるグループで仕事をしているメンバー',
    'キックオフ':'これまであまり一緒に仕事をしたことがなく、初めて顔を合わせる人もいるようなメンバー',
    'ワークショップ・研修':'価値観や性格が異なる人が入り混ざっているメンバー'
}
icebreak_type_list = {
    'わいわい':'ゲームやクイズを取り入れて盛り上がれるようなアイスブレイク',
    'おだやか':'自分の考えや価値観について話す機会を与えるようなアイスブレイク',
    'ほっこり':'プライベートの出来事について共有できるようなアイスブレイク'
}


# GPT
def run_gpt(
    participants_name,
    participants_number,
    meeting_type,
    icebreak_type,
    icebreak_time
):
    request_to_gpt = 'あなたは会議のファシリテーターです。会議の前に行う' + icebreak_type + 'をひとつ提案してください。参加者は、' + meeting_type + 'です。参加者の名前は、' + participants_name + 'です。参加者の人数は' + str(participants_number) + '人です。アイスブレイクの制限時間は' + str(icebreak_time) + '分です。参加者の発言時間の合計が制限時間以内に収まるように各発言者の制限時間を設けてください。出力は、会議のファシリテーターになりきり、司会進行するような口調で記述してください。初めに、アイスブレイクの「タイトル」を宣言した後、会議の参加者に対してアイスブレイク方法を説明しながら司会進行するセリフを出力してください。参加者に発言させる場合は、ひとりずつランダムに名前を「さん」付けで呼び、発言を促してください。参加者が発言する場面では、文末に制限時間を（）でくくって記載してください。参加者による回答のセリフや、正解者の発表のセリフは不要です。'

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role" : "user", "content" : request_to_gpt},
            ],
    )
    
    output_content = response.choices[0]["message"]["content"].strip()
    return output_content


# audio player
def show_audio_player(output_content_text: str) -> None:
    sound_file = BytesIO()
    try:
        tts = gTTS(text=output_content_text, lang="ja")
        tts.write_to_fp(sound_file)
        st.write(st.session_state.locale.stt_placeholder)
        st.audio(sound_file)
    except gTTSError as err:
        st.error(err)


# Settings @sidebar
st.sidebar.title('Settings')
openai.api_key = st.sidebar.text_input("OpenAI key")
participants_name = st.sidebar.text_input("参加者の名前")
participants_number = st.sidebar.number_input('参加者数', step=1)
meeting_type = st.sidebar.selectbox(
    '会議の種類',
    meeting_type_list.keys()
)
icebreak_type = st.sidebar.selectbox(
    'アイスブレイクのタイプ',
    icebreak_type_list.keys()
)
icebreak_time = st.sidebar.number_input('アイスブレイク時間（分）', step=1)


# Main
st.title("ICE Breaker⛄")
output_content = st.empty()
warning_text = st.empty()
if st.button('Start!'):
    if(participants_name !=""):
        output_content.write("考え中…")
        warning_text.write("")
        
        output_content_text = run_gpt(
            participants_name,
            participants_number,
            meeting_type,
            icebreak_type,
            icebreak_time
        )

        output_content.write(output_content_text)
        st.audio(sound, format="audio/wav", start_time=0, sample_rate=None)
        
    else:
        warning_text.write("参加者の名前を入力してください。")

# https://blog.streamlit.io/ai-talks-chatgpt-assistant-via-streamlit/


