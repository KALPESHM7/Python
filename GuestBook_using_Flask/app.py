from flask import Flask, render_template, request, redirect, url_for, abort, flash

app = Flask(__name__)
app.secret_key = "1997"  # Needed for flashing messages

messages = [] # This will store all messages in dictionary format

def get_next_id():
    return (messages[-1]['id'] + 1) if messages else 1

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        author = request.form.get("author", "").strip() # to display the form we are using form.get
        text = request.form.get("message", "").strip()

        if not text:
            flash("Message cannot be empty!", "error")
            return redirect(url_for("index"))

        new_msg = {
            "id": get_next_id(),
            "author": author or "Anonymous",
            "text": text,
        }
        messages.append(new_msg)
        flash("Your message was submitted successfully!", "success")
        return redirect(url_for("message_detail", msg_id=new_msg["id"]))

    return render_template("index.html", messages=messages)

@app.route("/message/<int:msg_id>")
def message_detail(msg_id):
    for m in messages:
        if m["id"] == msg_id:
            return render_template("message.html", message=m)
    abort(404)

if __name__ == "__main__":
    app.run(debug=True)
