from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,HttpResponseNotFound
from models import Issue
from django.utils.cache import add_never_cache_headers
import requests
from wobeissues import settings

GITHUB_USER = settings.GITHUB_USER
GITHUB_PASSWORD = settings.GITHUB_PASSWORD
AUTH = (settings.GITHUB_USER, settings.GITHUB_PASSWORD)

COMPANY = settings.COMPANY
REPOS = settings.REPOS
           
def get_issues(r,REPO):
  "output a list of issues to csv"
  print REPO
  if not r.status_code == 200:
    raise Exception(r.status_code)
  ret = r.json()
  for issue in ret:
    issue["repository"] = REPO
  return ret
#    for issue in r.json():
#        labels = issue['state']
#        #for label in labels:
#        #if label['name'] == "Client Requested":
#        if issue['state'] == 'open':
#            #csvout.writerow([issue['number'], issue['title'].encode('utf-8'), issue['body'].encode('utf-8'), issue['created_at'], issue['updated_at']])
#            csvout.writerow([ str(x).replace(',','-') for x in [REPO, issue['number'], issue['title'].encode('utf-8'), issue['url'], issue['created_at'], issue['updated_at']]])
# 
def pull_issues(REPO):
  ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues' % REPO
  r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
  issues=[]
  issues.extend(get_issues(r,REPO))

  #more pages? examine the 'link' header returned
  if 'link' in r.headers:
    pages = dict(
      [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
        [link.split(';') for link in
        r.headers['link'].split(',')]])
    while 'last' in pages and 'next' in pages:
      r = requests.get(pages['next'], auth=AUTH)
      issues.extend(get_issues(r,REPO))
      if pages['next'] == pages['last']:
        break
  return issues

def create_new(issue):
  saved = Issue()
  saved.repository = issue['repository']
  saved.issueid = str(issue['number'])
  saved.title = issue['title'].encode('utf-8')
  saved.url = "https://github.com/"+issue['repository']+"/issues/"+str(issue['number'])
  saved.created = issue['created_at'].split("T")[0]
  saved.updated = issue['updated_at'].split("T")[0]
  if "assignee" not in issue or not issue["assignee"]:
    saved.assigned="None"
  else:
    print issue['assignee']
    saved.assigned = issue['assignee']['login']
  saved.status = issue['state']
  saved.changed = False
  saved.release = "None"
  saved.comments = "None"
  saved.save()
   
def copy_existing(saved,issue):
  saved.changed = False
  if saved.repository != issue['repository']:
    saved.changed = True
    saved.repository = issue['repository']
  if saved.issueid != str(issue['number']):
    saved.changed = True
    saved.issueid = str(issue['number'])
  if saved.title != issue['title'].encode('utf-8'):
    saved.changed = True
    saved.title = issue['title'].encode('utf-8')
  if saved.url != "https://github.com/"+issue['repository']+"/issues/"+str(issue['number']):
    saved.changed = True
    saved.url = issue['url']
  if saved.created != issue['created_at'].split("T")[0]:
    saved.changed = True
    saved.created = issue['created_at'].split("T")[0]
  if saved.updated != issue['updated_at'].split("T")[0]:
    saved.changed = True
    saved.updated = issue['updated_at'].split("T")[0]
  if "assignee" not in issue or not issue["assignee"]:
    saved.assigned="None"
  else:
    if saved.assigned != issue["assignee"]["login"]:
      saved.changed = True
      saved.assigned = issue['assignee']['login']
  if saved.status != issue['state']:
    saved.changed = True
    saved.status = issue['state']
  saved.save()

# Create your views here.
def issues_refresh(request):
  issues=[]
  for i in REPOS:
    issues.extend(pull_issues(COMPANY+i))
  for issue in issues:
    try:
      saved_issue = Issue.objects.get(issueid = str(issue['number']))
      copy_existing(saved_issue, issue)
    except:
      create_new(issue)
  ret  = HttpResponseRedirect("/issueview/")
  add_never_cache_headers(ret)
  return ret

def issues_update(request,issueid):
  if request.method == "POST":
    print issueid
    issue = Issue.objects.get(pk=issueid)
    release = request.POST.get('release') 
    comments = request.POST.get('comments')
    issue.release = release
    issue.comments = comments
    issue.save()
  ret = HttpResponseRedirect("/issueview/")
  add_never_cache_headers(ret)
  return ret

def apply_filter(issues, filt):
  filtlist = filt.split(",")
  print "filt:"+str(filtlist)
  for f in filtlist:
    fvals = f.split(":")
    fname = fvals[0]
    fv = fvals[1]
    print fname+":"+fv
    if fname == 'release':
      issues= issues.filter(release=fv)
    elif fname == 'assigned':
      issues= issues.filter(assigned=fv)
    elif fname == 'status':
      issues= issues.filter(status=fv)
  return issues

def issues_show(request):
  if request.method == "GET":
    filt = request.GET.get("filter","")
    issue_list = Issue.objects.all()
    if filt != "":
      issue_list = apply_filter(issue_list, str(filt))
    ret =  render(request, "issueview/list.html", { "issues":issue_list })
    add_never_cache_headers(ret)
    return ret
