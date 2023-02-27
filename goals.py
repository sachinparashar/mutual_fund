from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from connection import get_connection
import pandas as pd

# Get database connection Object
db = get_connection()

df = pd.read_csv("goal_graph_2.csv")
# df=df.astype(str)
df['month'] = pd.to_datetime(df.month, format='%m/%d/%Y')
df['month'] = df['month'].dt.strftime('%Y-%m')
df = df.fillna('')
# df['portfolio_actual_value'] = df['portfolio_actual_value'].fillna(0)
# df['predicted_value'] = df['predicted_value'].fillna(0)
# df['portfolio_nifty_value'] = df['portfolio_nifty_value'].fillna(0)

def goal_performance_comparison(duration, goal_returns):
    if goal_returns:
        goal_returns = float(goal_returns.rstrip("%"))
    else:
        goal_returns = 15
    if duration == '3m':
        nifty_amount = 100000+int((((100000*12)/100)/12)*3)
        goal_amount = 100000+int((((100000*goal_returns)/100)/12)*3)
        return nifty_amount, goal_amount
    elif duration == '6m':
        nifty_amount = 100000+int((((100000 * 12) / 100) / 12) * 6)
        goal_amount = 100000+int((((100000 * goal_returns) / 100) / 12) * 6)
        return nifty_amount, goal_amount
    elif duration == '1y':
        nifty_amount = 100000+int((100000 * 12) / 100)
        goal_amount = 100000+int((100000 * goal_returns) / 100)
        return nifty_amount, goal_amount
    elif duration == '3y':
        nifty_amount = 100000+int(((100000 * 12) / 100) * 3)
        goal_amount = 100000+int(((100000 * goal_returns) / 100) * 3)
        return nifty_amount, goal_amount
    else:
        nifty_amount = 100000+int(((100000 * 12) / 100) * 5)
        goal_amount = 100000+int(((100000 * goal_returns) / 100) * 5)
        return nifty_amount, goal_amount


def get_goal_data(goal_id):
    distribution = {}
    # Getting goals Details from user_goals Collection
    user_goals = db.user_goals.find_one({"email": current_user.email, "goal_id": goal_id})
    details = db.goal_stats.find({"email": current_user.email,'goal_id': goal_id}).sort("month", -1)
    distribution_data = db.user_goal_distribution.find({"user_goal_id": user_goals['user_goal_id']})
    nifty_amount, goal_amount = goal_performance_comparison('3m', details[0]['return'])
    for dis in distribution_data:
        calc_percent = (float(dis['invested_amount'])/float(details[0]['total_invested']))*100
        distribution[dis['fund_name']] = [dis['fund_type'], "{:.2f}".format(calc_percent)]
    data = {
        "goal_detail": user_goals,
        "fund_distribution": distribution,
        "portfolio_value": details[0]['portfolio_value'],
        "total_return_percent": details[0]['return'],
        "amount_left": int(user_goals['target_amount']-details[0]['total_invested']),
        "invested_amount" : details[0]['total_invested'],
        "nifty_amount": nifty_amount,
        "goal_amount": goal_amount,
        "start_date": '01-10-2020'
    }

    df1 = df.loc[df['goal_id'] == goal_id]
    graph_data = {
        "month": list(df1['month']),
        "portfolio_actual_value": list(df1['portfolio_actual_value']),
        "portfolio_predicted_value": list(df1['portfolio_planned_value']),
        "portfolio_nifty_value": list(df1['portfolio_nifty_value'])
    }
    return data, graph_data


def get_graph_data():
    df1 = df.loc[df['email'] == current_user.email]
    df1 = df1.head(38)
    graph_data = {
        "month": list(df1['month']),
        "portfolio_actual_value": list(df1['portfolio_actual_value']),
        "portfolio_predicted_value": list(df1['portfolio_planned_value']),
        "portfolio_nifty_value": list(df1['portfolio_nifty_value'])
    }
    return graph_data


def get_user_goal_distribution(user_goal_id = ''):
    # For all data
    if user_goal_id:
        return db.user_goal_distribution.find({"email": current_user.email, "user_goal_id":user_goal_id})
    else:
        return db.user_goal_distribution.find({"email":current_user.email})


def get_user_goal(user_goal_id):
    # For all user goal data
    return db.user_goal.find_one({"email": current_user.email, "user_goal_id":user_goal_id})
