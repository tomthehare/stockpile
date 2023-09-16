from flask import Flask, render_template, request, redirect, url_for
from models.item import Item
from utility.time_observer import get_current_time
import json
import os
import time

app = Flask(__name__)

DB_NAME = 'poor_db.txt'

def get_items_from_db():
    if not os.path.exists(DB_NAME):
        with open(DB_NAME, 'w') as f:
            f.write('[]')

    with open(DB_NAME, 'r') as f:
        items = json.load(f)

    loaded_items = []
    for item in items:
        test_item = Item(item['id'])
        test_item.description = item['description']
        test_item.location = item['location']
        test_item.set_created_ts(item.get('created_ts', ''))
        test_item.set_last_update_ts(item.get('last_update_ts', ''))
        test_item.set_deleted_ts(item.get('deleted_ts', None))

        if not test_item.get_deleted_ts_formatted():
            loaded_items.append(test_item)

    return loaded_items

def get_item(id) -> Item:
    items = get_items_from_db()

    found_item = None
    for item in items:
        if item.id == id:
            found_item = item
            break

    return found_item

@app.route('/', methods=['GET'])
def search_form():
    items =  get_items_from_db()

    return render_template('search.html', items=items)

@app.route('/search', methods=['GET'])
def search_submit():
    search_term = request.args.get('q', '').strip().lower()
    search_terms = search_term.split()

    items = get_items_from_db()

    matched_items = []
    for item in items:
        item_terms = item.description.split()
        item_terms.extend(item.location.split())
    
        item_terms = [a.strip().lower() for a in item_terms]

        matched = False
        for s_term in search_terms:
            if s_term in item_terms:
                matched_items.append(item)
                break

    return render_template('results.html', items=matched_items, search_term=search_term)

@app.route('/create_item')
def present_create_item():
    return render_template('new_item.html')

@app.route('/item')
def view_item():
    requested_id = int(request.args.get('id'))

    found_item = get_item(requested_id)
    if not found_item:
        return "No item found"

    return render_template('item.html', item=found_item)
            

@app.route('/submit_item', methods=['POST'])
def create_item():
    db_name = DB_NAME

    if os.path.exists(db_name):
        with open(db_name, 'r') as f:
            contents = json.load(f)
    else:
        contents = []

    max_id = 0
    for content in contents:
        if content['id'] > max_id:
            max_id = content['id']

    new_id = max_id + 1

    item = Item(new_id)
    item.description = request.form['description']
    item.location = request.form['location']
    item.set_last_update_ts(time.time())
    item.set_created_ts(time.time())

    contents.append(item.get_dict())

    with open('poor_db.txt', 'w+') as f:
        f.write(json.dumps(contents, indent=2))

    print(url_for('view_item', id=new_id))
    return redirect(url_for('view_item', id=new_id), code=302)

