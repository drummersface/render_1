import pandas as pd
import scipy.stats
import streamlit as st
import time

# Stateful variables in Streamlit
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('Tossing a Coin')

# Initialize chart with starting data
chart = st.line_chart([0.5])

def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    
    outcome_no = 0
    outcome_1_count = 0
    mean_list = []  # Collect mean values for chart updates

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        mean_list.append([mean])

        # Update chart less frequently for performance
        if outcome_no % 10 == 0 or outcome_no == n:
            chart.add_rows(mean_list)
            mean_list = []  # Clear after updating chart
        time.sleep(0.01)  # Optional: Smaller delay for smoother experience
    
    return mean

# Select number of trials with slider
number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experiment of {number_of_trials} trials.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)

    # Update experiment results DataFrame
    new_data = pd.DataFrame([[st.session_state['experiment_no'], number_of_trials, mean]],
                            columns=['no', 'iterations', 'mean'])
    st.session_state['df_experiment_results'] = pd.concat([st.session_state['df_experiment_results'], new_data], axis=0)
    st.session_state['df_experiment_results'].reset_index(drop=True, inplace=True)

# Display experiment results
st.write(st.session_state['df_experiment_results'])
