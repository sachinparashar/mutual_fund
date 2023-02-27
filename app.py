# Flask modules
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from passlib.hash import pbkdf2_sha256
from bson import BSON

# Other modules
import os
import json
import pandas as pd
import locale

# Local imports
from user import User
from goals import get_goal_data, goal_performance_comparison, get_graph_data, get_user_goal_distribution, get_user_goal
from connection import get_connection

# Get database connection Object
db = get_connection()

app = Flask(__name__)
app.secret_key = "#%#$#^574574547%&$%^#$%@@%"

# Create login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"

# Set the locale to India
locale.setlocale(locale.LC_ALL, 'en_IN')


def get_goals():
    # Getting Goals from goals collection
    goal_dict = {}
    data = db.user_goals.find({"email": current_user.email})
    if data:
        for d in data:
            goal_dict[d['goal_id']] = d['goal_name']
    return goal_dict


@app.template_filter()
def numberFormat(value):
    amount = locale.currency(value, grouping=True)
    currency_string = amount.replace('₹', '')
    currency_string = currency_string.lstrip()
    if '.' in currency_string:
        currency_string = currency_string[:currency_string.index('.')]
    return currency_string.replace('? ', '')


# ROUTES
# Index
@app.route('/')
def index():
    return render_template('index.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            # Redirect to index if already authenticated
            return redirect(url_for('/profile_details'))
        # Render login page
        return render_template('login.html')
    else:
        # Trim input data
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        user_data = db.users.find_one({"email": email})
        if user_data and pbkdf2_sha256.verify(password, user_data['password']):
            # Create user object to login (note password hash not stored in session)
            user = User.make_from_dict(user_data)
            login_user(user)
            # Check for next argument (direct user to protected page they wanted)
            next_link = request.args.get('next')
            # Go to profile page after login
            return redirect(next_link or url_for('profile_details'))

            # Redirect to login page on error
        return redirect(url_for('login'))


# Register
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Trim input data
        email = request.form['email'].strip()
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        password = request.form['password'].strip()
        new_user = User(first_name, last_name, email)
        # Create dictionary data to save to database
        user_data_to_save = new_user.dict()
        user_data_to_save['password'] = pbkdf2_sha256.encrypt(password)

        # Insert user record to database
        if db.users.insert_one(user_data_to_save):
            login_user(new_user)
            return redirect(url_for('profile_details'))
    return render_template('register.html')


# Summary-dashboard
@app.route('/summary_dashboard', methods=['GET'])
@login_required
def summary_dashboard():
    goal_list = get_goals()
    context_data = {
        "title": "Investment Summary",
        "goals": goal_list
    }

    portfolio_value = 0
    total_returns = 0
    ongoing_goals = 0
    total_invested = 0
    total_return_percent = []
    goals_data = []
    goals_list = db.user_goals.find({"email": current_user.email})

    if goals_list.alive:
        for ug in goals_list:
            details = db.goal_stats.find({"goal_id": ug['goal_id']}).sort("month", -1).limit(1)
            portfolio_value = portfolio_value+int(details[0]['portfolio_value'])
            total_invested = total_invested+int(details[0]['total_invested'])
            ongoing_goals = ongoing_goals+1
            goals_data.append({"goal_name": ug['goal_name'],
                               "goal_id": ug['goal_id'],
                           "portfolio_value": details[0]['portfolio_value'],
                           "target_amount": ug['target_amount'],
                           "total_return_percent": details[0]['return'],
                           "goal_status": ug['status']})

    graph_data = get_graph_data()

    match_stage = {
        '$match': {
            'email': current_user.email
        }
    }

    lookup_stage = {
            "$lookup": {
                "from": "fund_scheme",
                "localField": "fund_id",
                "foreignField": "fund_id",
                "as": "result"
            }
        }

    pipeline = [
        lookup_stage,
        match_stage,
    ]

    distribution_dict = {}
    fund_distribution_data = db.user_goal_distribution.aggregate(pipeline)
    for d in fund_distribution_data:
        if d['result'][0]['fund_category'] in distribution_dict.keys():
            distribution_dict[d['result'][0]['fund_category']] = float(float(distribution_dict[d['result'][0]['fund_category']])+float(d['invested_amount']))
        else:
            distribution_dict[d['result'][0]['fund_category']] = float(d['invested_amount'])
    # print(distribution_dict)
    distribution_values = list(distribution_dict.values())

#####################################################################################################
    goal_distribution = get_user_goal_distribution()
    total_return_for_now = 0.3  # 20% return over the investment period
    goal_dist = {}
    lst = []
    total_wt = 0
    final_weighted_percentage = 0
    mf_lst = []
    inv_amt_lst = []
    ann_ret_lst = []
    weight_lst = []
    wt_ret_per = []
    for d in goal_distribution:
        # get_usr_goal = get_user_goal(d['user_goal_id'])
        # duration = get_usr_goal['duration']
        if d['fund_name'] in goal_dist.keys():
            goal_dist[d['fund_name']] = float(float(goal_dist[d['fund_name']])+float(d['invested_amount']))
        else:
            goal_dist[d['fund_name']] = float(d['invested_amount'])

    for mf in goal_dist:
        annualized_return = (((1 + total_return_for_now) ** (1 / 2)) - 1)*100
        mf_lst.append(mf)
        inv_amt_lst.append(goal_dist[mf])
        ann_ret_lst.append("{:.2f}".format(annualized_return))
    print(ann_ret_lst)
    # Calculating Weights
    for i in range(len(inv_amt_lst)):
        ignored_value = inv_amt_lst[i]
        remaining_sum = sum(inv_amt_lst[:i] + inv_amt_lst[i + 1:])
        wt = "{:.2f}".format(ignored_value/remaining_sum)
        weight_lst.append(wt)

    for i in range(len(weight_lst)):
        total_wt = total_wt+float(weight_lst[i])
        percentage = float(weight_lst[i])*float(ann_ret_lst[i])
        wt_ret_per.append(percentage)
    if total_wt >0:
        fnl_percentage = sum(wt_ret_per)/total_wt
    else:
        fnl_percentage = 0
    final_weighted_percentage = "{:.2f}".format(fnl_percentage)

    data = {
        "portfolio_value": int(portfolio_value),
        "total_return": int(portfolio_value - total_invested),
        "total_goals": ongoing_goals,
        "goals_list": goals_data,
        "distribution_dict": distribution_values,
        "final_weighted_percentage": final_weighted_percentage
    }
    return render_template('summary-dashboard.html', data=data, graph_data=graph_data, context_data=context_data)


# Profile-details
@app.route('/profile_details', methods=['GET'])
@login_required
def profile_details():
    goal_list = get_goals()
    context_data = {
        "title": "Profile Detail",
        "goals": goal_list
    }

    # Getting User Details from user_details collection
    details = db.user_details.find_one({"email": current_user.email})
    return render_template('profile-detail.html', details=details, context_data=context_data)


# Goals
@app.route('/goals/<goal_id>', methods=['GET'])
@login_required
def goals(goal_id):
    goal_list = get_goals()
    context_data = {
        "goals": goal_list
    }
    data, graph_data = get_goal_data(goal_id)
    return render_template('goals.html', data=data, graph_data= graph_data, context_data=context_data)


@app.route('/goals/get_goal_comparision', methods=['POST'])
@login_required
def get_goal_comparision():
    duration = request.form['duration']
    goal_id = request.form['goal_id']
    details = db.goal_stats.find({"email": current_user.email, 'goal_id': goal_id}).sort("month", -1)
    nifty_amount, goal_amount = goal_performance_comparison(duration, details[0]['return'])
    data = {
        "goal_returns": goal_amount,
        "nifty_returns": nifty_amount
    }
    return data


# Transaction-details
@app.route('/transaction_summary', methods=['GET'])
@login_required
def transaction_summary():
    goal_list = get_goals()
    context_data = {
        "title": "Transaction Summary",
        "goals": goal_list
    }

    # Getting Transaction Summary from transaction_summary collection
    summary = db.transaction_summary.find_one({"email": current_user.email})
    return render_template('transaction-summary.html', summary=summary, context_data=context_data)


# Banking-details
@app.route('/bank_details', methods=['GET'])
@login_required
def bank_details():
    goal_list = get_goals()
    context_data = {
        "title": "Banking Details",
        "goals": goal_list
    }

    # Getting Banking Details from bank_details collection
    details = db.bank_details.find_one({"email": current_user.email})
    return render_template('banking-info.html', details=details, context_data=context_data)


# Load user from user ID
@login_manager.user_loader
def load_user(email):
    # Return user object or none
    user = db.users.find_one({"email": email})
    if user:
        return User.make_from_dict(user)
    return None


# Logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
