import pandas as pd
import plotly.express as px
from utils import get_mode

if __name__ == "__main__":
    state_vac = pd.read_csv("/home/hoshi/ME/Coding/DAV-COVID-19-project/data/COVID_AU_vac_states.csv", header=0)

    states_labels = {
        'NSW_new': 'New South Wales',
        'VIC_new': 'Victoria',
        'QLD_new': 'Queensland',
        'WA_new': "West Australia",
        "SA_new": "South Australia",
        "TAS_new": "Tasmania",
        "ACT_new": "Australian Capital Territory",
        "NT_new": "Northern Territory",
    }

    # Summarize and reshape
    state_vac = state_vac[states_labels.keys()].rename(columns=states_labels).sum()
    state_vac = state_vac.reset_index()
    state_vac.columns = ['State', 'Vaccinated']

    # Create bar plot
    fig = px.bar(
        state_vac,
        x="State",
        y="Vaccinated",
        color="State",
        color_discrete_sequence=px.colors.qualitative.Pastel1,
        title="COVID-19 Vaccinations by State",
        labels={"Vaccinated": "People Vaccinated"},
        text="Vaccinated"
    )

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    fig.update_layout(
        showlegend=False,
        uniformtext_minsize=10,
        uniformtext_mode='hide',
        font=dict(size=24),
        title_font=dict(size=32),
        xaxis_title_font=dict(size=28),
        yaxis_title_font=dict(size=28)
    )

    # Show or save figure
    if get_mode() == 0:
        fig.show()
    else:
        fig.write_image(
            "/home/hoshi/ME/Coding/DAV-COVID-19-project/images/vac_bar.png",
            width=1500,
            height=1000
        )
