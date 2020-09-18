from flask import Flask, render_template, request, session
import boto3

bucket_name = "winnie-analyzevid-ab2"
s3 = boto3.client("s3")
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

# EB looks for an 'application' callable by default.
application = Flask(__name__)


@application.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        try:
            img = request.files['img']
            filename = img.filename
            if img:
                s3.put_object(
                    Bucket = bucket_name,
                    Body = img,
                    Key=filename
                )
                # saves filename in session so it can be referenced later on
                session['filename'] = filename
                return render_template("uploading.html")
        except Exception as e:
            return (str(e))
    return render_template("index.html")


@application.route("/uploading")
def uploading():
    return render_template("uploading.html")


@application.route('/display')
def display():
    # identifies dynamoDB table we're querying from
    table = dynamodb.Table('CelebDetect')

    # grabs filename from upload
    filename = session.get('filename')

    # queries based on filename and returns info to display
    response = table.get_item(Key={'vid_name': filename})

    college_attended = response['Item']['college_attended']
    player_name = response['Item']['player_name']
    highschool_attended = response['Item']['highschool_attended']
    years_pro = response['Item']['years_pro']
    draft_year = response['Item']['draft_year']
    return render_template('display.html', college_attended=college_attended, player_name=player_name,
                           highschool_attended=highschool_attended, years_pro=years_pro,
                           draft_year=draft_year)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # adding secret key to be able to utilize sessions
    application.secret_key = 'some secret key'
    application.debug = True
    application.run()

