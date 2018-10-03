from flask import Flask, render_template, send_from_directory, request, jsonify, json, Response
from pymongo import MongoClient
from datetime import datetime

application = Flask(__name__)
application.config.from_pyfile('news.cfg')

#mongo = MongoClient('localhost:27017')
mongo = MongoClient(application.config['MONGODB_HOST'], application.config['MONGODB_PORT'])

db = mongo['news']
db.authenticate('admin', 'steven')


@application.route('/')
def index():
    return render_template('list.html')


@application.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


@application.route("/test")
def test():
    return "<strong>It's Alive!</strong>"


@application.route("/api/wenxue", methods=['GET', 'POST'])
def api_wenxue():
    msg = {"error": "None"}
    if request.method == 'GET':
        try:
            items = db.wenxue.find().sort('post_date', -1).limit(100)
            news_list = []
            for i in items:
                detail = {
                    'id': i['_id'],
                    'title': i['title'],
                    'source': i['source'],
                    'date': i['post_date'].strftime('%a, %b %d')
                }
                news_list.append(detail)
            return json.dumps(news_list, ensure_ascii=False).encode('utf-8')
        except Exception, e:
            return str(e)
    elif request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            req = request.get_json(silent=True)
            news_id = req['news_id']
            title = req['title']
            content = req['content']
            source = req['source']
            link = req['link']
            post_date = datetime.strptime(req['post_date'], '%Y-%m-%d %H:%M:%S')
            record = {
                "_id": news_id,
                "title": title,
                "content": content,
                "source": source,
                "post_date": post_date,
                "link": link
            }
            fd = db.wenxue.find({'_id': news_id}).count()
            if fd == 0:
                post_id = db.wenxue.insert_one(record).inserted_id
                msg = {
                    'message': "inserted successfully.",
                    "news_id": post_id
                }
            else:
                post_id = db.wenxue.replace_one({"_id": news_id}, record).upserted_id
                msg = {
                    'message': "updated successfully.",
                    "news_id": post_id
                }
        return json.dumps(msg)
    about(404)


@application.route("/api/wenxue/<id>", methods=['GET','DELETE'])
def api_detail(id):
    msg = {"error": "None"}
    try:
        if request.method == 'GET':
            item = db.wenxue.find_one({"_id": id})
            return json.dumps(item, ensure_ascii=False).encode('utf-8')
        elif request.method == 'DELETE':
            if int(id) <= 31:
                today = datetime.today()
                delta = datetime.timedelta(days=int(id))
                margin_date = today - delta
                db.wenxue.remove({'post_date':{'$lt': margin_date}})
                return json.dumps('{"message":"Done"}')
            else:
                post_id = db.wenxue.delete_one({"_id": id})
                msg = {
                    'message': "deleted successfully.",
                    "news_id": post_id.deleted_count
                    }
                return json.dumps(msg)
    except Exception,e:
        return e.args[0]


if __name__ == '__main__':
    application.run()
