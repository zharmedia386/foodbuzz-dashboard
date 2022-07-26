import datetime
from flask import Flask, render_template
from get_data import get_data

app = Flask(__name__)


@app.route('/')
def dashboard():
    numbers_users, numbers_orders, numbers_items, status_users, total_profit, item_ordered, users_list, image_users = get_data()
    return render_template('index.html', numbers_users=numbers_users, numbers_orders=numbers_orders, numbers_items=numbers_items, status_users=status_users, total_profit=total_profit, item_ordered=item_ordered, users=users_list, image_users=image_users)

if __name__ == "__main__":
    app.run(port=5000)

    # for heroku
    # app.run(debug=True)