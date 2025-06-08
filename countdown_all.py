import streamlit as st
from datetime import datetime,timedelta
from streamlit_option_menu import option_menu

if "events" not in st.session_state:
    st.session_state.events = []

st.set_page_config(page_title="倒计时管理器",page_icon="⏳",layout="centered")

st.markdown("<h1 style='text-align:center; color:#4B8BBE;'>⏳ 倒计时管理器</h1>",unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
        menu_title="菜单",
        options=["📅 添加倒计时", "📋 查看倒计时"],
        icons=["calendar-plus","list-task"],
        menu_icon="cast",
        default_index=0
    )

def format_time_diff(target_time):
    now = datetime.now()
    delta = target_time - now
    if delta.total_seconds()<0:
        return"⛔ 已过期"
    else:
        days = delta.days
        hours, remainder = divmod(delta.seconds,3600)
        minutes,_ = divmod(remainder,60)
        return f"{days}天{hours}小时{minutes}分钟"

if selected == "📅 添加倒计时":
    st.subheader("添加新的倒计时事件")

    with st.form("add_event_form",clear_on_submit=True):
        title = st.text_input("事件名称")
        target_date = st.date_input("目标日期")
        target_time = st.time_input("目标时间")
        submitted = st.form_submit_button("添加")

        if submitted:
            target_datetime = datetime.combine(target_date,target_time)
            st.session_state.events.append({
                "title":title,
                "datetime":target_datetime
            })
            st.success(f"事件“{title}”已添加！")

elif selected == "📋 查看倒计时":
    st.subheader("当前倒计时事件")

    sorted_events = sorted(st.session_state.events, key=lambda x: x["datetime"])

    if not sorted_events:
        st.info("暂无倒计时记录，请先添加。")
    else:
        for idx, event in enumerate(sorted_events):
            col1,col2 = st.columns([5,1])
            with col1:
                st.markdown(f"##### {event['title']}")
                st.write(f"🕒 剩余时间：{format_time_diff(event['datetime'])}")
                st.write(f"📆 目标时间:{event['datetime'].strftime('%Y-%m-%d %H:%M')}")
            with col2:
                if st.button("🗑 删除",key=f"del_{idx}"):
                    st.session_state.events.remove(event)
                    st.rerun()