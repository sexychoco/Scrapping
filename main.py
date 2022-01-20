from flask import Flask, render_template, request,redirect,send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

db={}

@app.route("/")
def home():
  return render_template("home.html")

#arg 란 url에서 ?다음에 제공되는 부분 
@app.route("/report")
def report():
  word=request.args.get('word')
  if word:
    #word를 소문자처리
    word=word.lower()
    #db에 word가 있는지 검색하는 과정 
    existingJobs = db.get(word)
    #db가 해당 값을 가지고 있으면 그것을 jobs에 넣어준다.
    if existingJobs:
      jobs = existingJobs
    #db가 해당 값을 가지고 있지 않으면 Scrapper를 돌려준다. 
    else:
      jobs=get_jobs(word)
      db[word] =jobs
  else:
    return redirect("/")
  return render_template("report.html",searchingBy=word,resultsNumber=len(jobs),jobs=jobs)

@app.route("/export")
def export():
  try:
    word= request.args.get('word')
    if not word:
      raise Exception()
    word=word.lower()
    #word로 jobs를 fakeDb에서 찾아야함
    jobs= db.get(word)
    if not jobs:
      raise Exception()
    #jobs가 fakedb에 있으면 save_to_file 을 돌림.
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

app.run(host="0.0.0.0")