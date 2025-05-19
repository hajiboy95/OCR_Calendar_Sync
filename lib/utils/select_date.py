import datetime
import streamlit as st


def select_event_date(key: str = "date"):
    """
    Allows the user to select a date for an event from a list of the next 7 days.

    This function renders a select box for the user to choose a day. It then stores the selected
    date in the session state.

    Args:
        key (str, optional): The key for the session state to store the selected date. Defaults to "date".
    """
    today = datetime.date.today()
    dates = [today + datetime.timedelta(days=i) for i in range(7)]
    date_labels = ["Heute", "Morgen"] + [d.strftime("%A, %d. %B") for d in dates[2:]]
    date_index = st.selectbox(
        "Für welchen Tag ist das?",
        range(len(date_labels)),
        format_func=lambda i: date_labels[i],
        index=1,
    )
    st.session_state[key] = (
        "\nDatum des Termins: "
        + dates[date_index].strftime("%Y-%m-%d")
        + " (Europe/Berlin)"
    )
