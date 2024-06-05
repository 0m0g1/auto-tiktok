from flask import Flask, request, render_template, url_for, redirect, jsonify
from main_script import main, run_all_items
import threading
from random import randint

app = Flask(__name__)

listofitems = []
temporarylistofitems = []

def start_main_function(video_link, username_input, repeat_no, callback):
    def target():
        result = main(video_link, username_input, repeat_no)
        callback(result)
    thread = threading.Thread(target=target)
    thread.start()

def start_run_all_function(callback):
    def target():
        result = run_all_items(listofitems)
        callback(result)
    thread = threading.Thread(target=target)
    thread.start()

def generateUniqueID():
    id = randint(1000, 9999)
    for item in listofitems:
        if id == item["id"]:
            return generateUniqueID()
    return id

def deleteItemWithID(id):
    for item in listofitems:
        if item["id"] == id:
            listofitems.remove(item)
            return True
    return False

def getItemWithID(id):
    for item in listofitems:
        if item["id"] == id:
            return item
    return None  # If no item with the given ID is found

@app.route("/", methods=["GET"])
def index():
    result = None
    alertUser = None  # Default value for alertUser
    return render_template("index.html", listofitems=listofitems[:][::-1], result=result, alertMessage=alertUser)

@app.route("/add", methods=["POST"])
def addItem():
    result = None
    alertUser = None  # Default value for alertUser
    if request.method == "POST":
        try:
            video_link = request.form["video_link"]
            username_input = request.form["username_input"]
            repeat_no = int(request.form["repeat_no"])
            added_item = {
                "id": generateUniqueID(),
                "url": video_link,
                "username": username_input,
                "repeat": repeat_no,
                "completed": False
            }
            listofitems.append(added_item)
        except Exception as e:
            result = f"An error occurred: {e}"
    return redirect(url_for("index"))

@app.route("/delete", methods=["POST"])
def delete():
    result = None  # Add this line to ensure result is defined
    if request.method == "POST":
        try:
            id = request.form["id"]
            deleteItemWithID(int(id))
        except Exception as e:
            result = f"An error occurred: {e}"
    return redirect(url_for("index"))

@app.route("/run", methods=["POST"])
def run():
    try:
        id = request.form["id"]
        item = getItemWithID(int(id))

        def callback(result):
            item["completed"] = True
            item["result"] = result

        start_main_function(item["url"], item["username"], item["repeat"], callback)
        return redirect(url_for("index"))  # Redirect back to index after running the script
    except KeyError as e:
        result = f"Missing form field: {e}"
    except ValueError:
        result = "Invalid input for 'repeat_no'. Please enter a valid number."
    except Exception as e:
        result = f"An error occurred: {e}"
    return redirect(url_for("index"))

@app.route("/run_all", methods=["POST"])
def run_all():
    try:
        temporarylistofitems = listofitems[:]
        
        def callback(result):
            for item in listofitems:
                item["completed"] = True
        
        start_run_all_function(callback)
    except KeyError as e:
        result = f"Missing form field: {e}"
    except ValueError:
        result = "Invalid input for 'repeat_no'. Please enter a valid number."
    except Exception as e:
        result = f"An error occurred: {e}"
    return jsonify("running all")


@app.route("/status")
def get_status():
    return jsonify(listofitems)

if __name__ == "__main__":
    app.run(debug=True)
