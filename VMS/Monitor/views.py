from django.shortcuts import *
from Monitor.models import *
from django.db import connection,transaction
from django.db.models import Q
import random as rd
import string
import csv
import os
import datetime
# import datetime as dt

import matplotlib
import matplotlib.pyplot as plt
# <제출본과 다른 부분> : 파이썬 환경문제로 추가하게 되었음
plt.switch_backend('agg')
# --<제출본과 다른 부분 끝>--
import matplotlib.dates as mdates
# import matplotlib as plot
# import matplotlib
positions=['ADMIN', 'TEAM_LEADER', 'DEPART_LEADER', 'EMPLOYEE']


def makeGraph(csvfile,savedir):
	# 메타로그 파일을 그래프 형태로 출력하는 프로그램
	# 파일 형태
	# 0: 시간 1: 객체번호 2: x 좌표 3: y 좌표 4: height 5: 객체의 움직임 속도 6: 색상
	# matplotlib.use('Agg')
	dates = [] # 시간
	objects={} # 객체
	object_id = []
	coord_x = [] # x좌표
	coord_y = [] # y좌표
	height = [] # 키
	color = [] # 색상
	size=[]

	# 첫번째 object 개수 파악
	with open(csvfile) as f:
		while True:
			line = f.readline()
			if not line: break
			temp = line.split(',')[1];
			if temp in object_id:
				continue
			object_id.append(temp)

	# objects 딕셔너리에 각 값들을 추가
	for i in object_id:
		dates = []
		coord_x = []
		coord_y = []
		height = []
		velocity = []
		with open(csvfile) as f:
			while True:
				line = f.readline()
				if not line: break

				temp = line.split(',')[1]
				if (i!=temp):continue;

				dates.append(line.split(',')[0])
				coord_x.append(float(line.split(',')[2]))
				coord_y.append(float(line.split(',')[3]))
				height.append(float(line.split(',')[4]))
				velocity.append(float(line.split(',')[5]))

		objects[i+"_date"] = dates
		objects[i+"_x"] = coord_x
		objects[i+"_y"] = coord_y
		objects[i+"_height"] = height
		objects[i+"_velocity"] = velocity

	# 그래프 출력
	# 1.객체 이동 경로 그래프
	plt.figure()
	plt.title("Transition of the position of objects")
	for i in range(0,len(object_id)):
		plt.plot(objects[object_id[i]+"_x"],objects[object_id[i]+"_y"], label=object_id[i])
	plt.legend()
	plt.xlabel('x-coordinate')
	plt.ylabel('y-coordinate')
	plt.grid()
	plt.savefig(savedir+'_tran_loc.png')

	# 2.객체 크기 변화 그래프
	# try:
	# 	plt.figure()
	# 	plt.title("Transition of Height of objects")
	# 	for i in range(0,len(object_id)):
	# 		x = [datetime.datetime(int('20'+d[:2]),int(d[2:4]),int(d[4:6]),int(d[6:8]),int(d[8:10])) for d in objects[object_id[i]+"_date"]]
	# 		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d-%H-%M'))
	# 		plt.plot(x,objects[object_id[i]+"_height"], label=object_id[i])
	# 	plt.xlabel('time')
	# 	plt.ylabel('size')
	# 	plt.legend()
	# 	plt.xticks(x, rotation=30)
	# 	plt.savefig(savedir+'_tran_size.png')
	# except:
	# 	pass

	# # 3.객체 평균 크기 그래프
	# plt.figure(0)
	# plt.title("Average Size")
	# data_id = []
	# data = []
	# for i in range(0,len(object_id)):
	# 	height = objects[object_id[i]+"_height"]
	# 	average = sum(height) / len(height)
	# 	data_id.append(object_id[i])
	# 	data.append(average)
	# try:
	# 	plt.bar(data_id,data, width = 0.3)
	# except:
	# 	pass
	# plt.ylabel('Size')
	# plt.savefig(savedir+'_avr_size.png')

	# # 3.객체 속도 변화 그래프
	# plt.figure(0)
	# plt.title("Transition of Velocity of objects")
	# for i in range(0,len(object_id)):
	# 	x = [datetime.datetime(int('20'+d[:2]),int(d[2:4]),int(d[4:6]),int(d[6:8]),int(d[8:10])) for d in objects[object_id[i]+"_date"]]
	# 	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d-%H-%M'))
	# 	plt.plot(x,objects[object_id[i]+"_velocity"],label=object_id[i])
	# plt.legend()
	# plt.xlabel('time')
	# plt.ylabel('velocity')
	# plt.xticks(x, rotation=30)
	# plt.savefig(savedir+'_tran_speed.png')

	# # 4.객체 평균 속도 그래프
	# plt.figure(0)
	# plt.title("Average Velocity")
	# data_id = []
	# data = []
	# for i in range(0,len(object_id)):
	# 	velocity = objects[object_id[i]+"_velocity"]
	# 	average = sum(velocity) / len(velocity)
	# 	data_id.append(object_id[i])
	# 	data.append(average)
	# try:
	# 	plt.bar(data_id,data, width = 0.3)
	# except:
	# 	pass
	# plt.ylabel('velocity')
	# plt.savefig(savedir+'_avr_speed.png')

def fetch(sql):
	with connection.cursor() as cursor:
		cursor.execute(sql)
		ret = cursor.fetchall()
	return ret

def execute(sql):
	with connection.cursor() as cursor:
		cursor.execute(sql)
	return cursor.lastrowid

# @구현완료
# -- 일반적인 함수들
def randomword(length):
	ret = ''
	for i in range(30):
		ret += rd.choice(string.ascii_lowercase)
	return ret

def timeparser(filename):
	date = '20'+filename.split('_')[-2]
	time = filename.split('_')[-1].split('.')[0]
	return (date,time)

def metaTimeParser(string):
	nextH = str(int(string[6:8])+1)
	if len(nextH) == 1:
		nextH = '0'+nextH
	return '20%s-%s-%s %s:%s:00'%(string[:2],string[2:4],string[4:6],string[6:8],string[8:10])

def DateTime(string):
	year = int('20'+string[:2])
	mon = int(string[2:4])
	day = int(string[4:6])
	hour = int(string[6:8])
	minute = int(string[8:10])
	return datetime.datetime(year,mon,day,hour,minute)

def count(something):
	ret = 0
	if something.id_NEI1 != None:
		ret+=1
	if something.id_NEI2 != None:
		ret+=1
	if something.id_NEI3 != None:
		ret+=1
	if something.id_NEI4 != None:
		ret+=1
	return ret

def searchTimeParser(string):
	if string is None: return
	return '20%s-%s-%s %s:%s00:00'%(string[:2],string[2:4],string[4:6],string[6:8],string[8:10])

# -- 실제 뷰 정의

# @구현완료
def Search(request):
	date_search = False
	startdate,enddate = None,None
	user = current_user(request)
	searchword = keyword = request.GET.getlist('keyword')[0]
	if ',' in keyword:
		# 시간대별로 검색을 함
		date_search = True
		copy_keyword = keyword
		keyword = copy_keyword.split(',')[0]
		startdate = copy_keyword.split(',')[1]
		enddate = copy_keyword.split(',')[2]

	#모델명으로 검색
	sql = "SELECT V.id, V.startTime, V.endTime, A.name, A.loc1,A.loc2,A.loc3, C.setup_date,A.address,C.model FROM Monitor_cctv AS C, Monitor_area AS A, Monitor_cctv_area AS CA, Monitor_video AS V WHERE  CA.id_CCTV_id = C.id and V.id_CCTV_AREA_id = CA.id AND C.model LIKE '%%%s%%' AND A.id = CA.id_AREA_id"%keyword
	if date_search:
		sql+=' and V.startTime >= "%s" and V.endTime <= "%s"'%(searchTimeParser(startdate),searchTimeParser(enddate))
	search_cctv = fetch(sql)

	#촬영공간 검색?
	sql = "SELECT V.id, V.startTime, V.endTime, A.name, A.loc1,A.loc2,A.loc3, C.setup_date,A.address,C.model FROM Monitor_cctv AS C, Monitor_area AS A, Monitor_cctv_area AS CA, Monitor_video AS V WHERE  CA.id_CCTV_id = C.id and V.id_CCTV_AREA_id = CA.id AND A.name LIKE '%%%s%%' AND A.id = CA.id_AREA_id"%keyword
	# sql = "SELECT * FROM Monitor_area as A, Monitor_cctv_area as CA, Monitor_video as V where A.id = CA.id_AREA_id and CA.id = V.id_CCTV_AREA_id and A.name like '%%%s%%'"%keyword
	if date_search:
		sql+=' and V.startTime >= "%s" and V.endTime <= "%s"'%(searchTimeParser(startdate),searchTimeParser(enddate))
	search_videos = fetch(sql)

	# 시퀀스검색?
	sql = "select SQ2.id as targetSQid, SQ2.id_NEI1_id as targetNEI1id, SQ2.id_NEI2_id as targetNEI2id, SQ2.id_NEI3_id as targetNEI3id, SQ2.id_NEI4_id as targetNEI4id from (select distinct temp.SQid from (select distinct SQ.id as SQid, id_AREA1_id as AA1_id, id_AREA2_id as AA2_id from Monitor_area_seq as SQ, Monitor_neighbor as NEI1 where SQ.id_NEI1_id = NEI1.id UNION select distinct SQ.id as SQid, id_AREA1_id as AA1_id, id_AREA2_id as AA2_id from Monitor_area_seq as SQ, Monitor_neighbor as NEI2 where SQ.id_NEI2_id = NEI2.id UNION select distinct SQ.id as SQid, id_AREA1_id as AA1_id, id_AREA2_id as AA2_id from Monitor_area_seq as SQ, Monitor_neighbor as NEI3 where SQ.id_NEI3_id = NEI3.id UNION select distinct SQ.id as SQid, id_AREA1_id as AA1_id, id_AREA2_id as AA2_id from Monitor_area_seq as SQ, Monitor_neighbor as NEI4 where SQ.id_NEI4_id = NEI4.id) as temp, Monitor_area as AA1, Monitor_area as AA2 where temp.AA1_id = AA1.id and temp.AA2_id = AA2.id and (AA1.name like '%%%s%%' or AA2.name like '%%%s%%') )as temp2, Monitor_area_seq as SQ2 where SQ2.id = temp2.SQid"%(keyword,keyword)
	search_seq = fetch(sql)
	res_list,temp_seq = [],[]
	for seq in search_seq:
		temp_seq.append(AREA_SEQ.objects.raw('select * FROM Monitor_area_seq where id = %s'%seq[0])[0])
		res_set=set()
		temp_count=0
		for nei in seq:
			temp_count+=1
			if temp_count==1 or nei==None: continue
			sql = 'select * from Monitor_neighbor where id=%s'%nei
			search_nei = fetch(sql)
			for nei in search_nei:
				res_set.add(nei[2])
				res_set.add(nei[3])
		res_list.append(res_set)

	search_video, braket = [],[]
	for area in res_list:
		braket=[]
		for aid in area:
			sql = "select V.id, V.startTime, V.endTime, A.name, A.loc1,A.loc2,A.loc3, C.setup_date,A.address,C.model from Monitor_cctv as C, Monitor_area as A, Monitor_cctv_area as CA , Monitor_video as v where CA.id_AREA_id=%s and v.id_CCTV_AREA_id = CA.id and A.id = CA.id_AREA_id and C.id = CA.id_CCTV_id"%aid
			if date_search:
				sql+=' and V.startTime >= "%s" and V.endTime <= "%s"'%(searchTimeParser(startdate),searchTimeParser(enddate))

			temp_video = fetch(sql)
			braket.append(temp_video)
		search_video.append(braket)
	zipped_search_video = zip(temp_seq, search_video)
	return render(request,'search.html',{'user':user, 'date_search':date_search, 'startdate':searchTimeParser(startdate), 'enddate':searchTimeParser(enddate), 'keyword':keyword, 'searchword':searchword, 'search_videos':search_videos, 'search_seq':search_seq, 'search_cctv':search_cctv, 'zipped_search_video':zipped_search_video})

def Statistic_download(request, pk):
	user = current_user(request)
	outputtext = ''
	sql = "SELECT * FROM Monitor_statistic WHERE id =%s"%pk
	targetST = STATISTIC.objects.raw(sql)[0]
	outputtext += '#record : %d\n'%targetST.num_record
	outputtext += 'duration : %d\n'%targetST.duration
	outputtext += '#object : %d\n'%targetST.num_obj
	outputtext += 'average speed : %f\n'%targetST.avg_speed
	outputtext += 'average size : %s\n'%targetST.avg_size
	with open('temp','w') as temp:
		temp.write(outputtext)
	fsock = open('temp','rb')
	response = HttpResponse(fsock)
	response['Content-Disposition'] = 'attachment; filename=video_statistic.txt'
	return response


# @구현완료
def current_user(request):
	try:
		sess_id = request.COOKIES['sess_id']
		sql = 'SELECT "Monitor_session"."id", "Monitor_session"."id_USER_id", "Monitor_session"."sess" FROM "Monitor_session" WHERE "sess" = "%s"'%sess_id
		user_instance = SESSION.objects.raw(sql)
		return user_instance[0].id_USER
	except:
		return False

# @구현완료
def find_user(email,pw):
	try:
		SQL = 'SELECT * FROM Monitor_user WHERE pw = "%s" AND email = "%s")'%(pw,email)
		return user[0]
	except:
		return False

# @구현완료
def Main(request):
	user = current_user(request)
	return render(request,'main.html',{'user':user})

# @구현완료
def LogIn(request):
	if request.method == "POST":
		PostEmail = request.POST.getlist('email')[0]
		PostPw = request.POST.getlist('pw')[0]
		sql = "SELECT * FROM Monitor_user AS U WHERE U.email='%s' AND U.pw='%s'"%(PostEmail,PostPw)
		user = fetch(sql)
		try:
			user = user[0]
			if user:
				sql = "UPDATE Monitor_user set is_on =1 where id = %s"%user[0] #user_id
				execute(sql)
				response = redirect('/main')
				randword = randomword(30)
				response.set_cookie('sess_id', randword, max_age=None)
				sql = "INSERT INTO Monitor_session (sess, id_user_id) values ('%s',%s)"%(randword,user[0])
				execute(sql)
				return response
		except:
			return render(request, 'error.html', {'error_msg':'ID or PW not matched'})
	return render(request, 'login.html')

# @구현완료
def Logout(request):
	user = current_user(request)
	sql = "UPDATE Monitor_user set is_on = 0 where id = %s"%user.id #user_id
	execute(sql)
	sql = "delete from Monitor_session where id_user_id = %s"%user.id
	execute(sql)
	response = redirect('/main',{'user':False})
	return response

# @구현완료
def Manage_admin(request):
	user = current_user(request)
	if request.method == "POST":
		email,pw,name,position,phone_number,is_super,is_on = request.POST.getlist('email')[0],request.POST.getlist('pw')[0],request.POST.getlist('name')[0],request.POST.getlist('position')[0],request.POST.getlist('phone_number')[0],0,0
		sql = "INSERT INTO Monitor_user (email, pw, name, position, phone_number, is_super, is_on) values ('%s','%s','%s','%s','%s',%s,%s)"%(email,pw,name,position,phone_number,is_super,is_on)
		execute(sql)
	all_user = USER.objects.raw("select * from Monitor_user")
	return render(request,'manage_admin.html',{'user':user,'all_user':all_user, 'positions':positions})

# @구현완료
def Manage_admin_delete(request, pk):
	user = current_user(request)
	all_user = USER.objects.raw("select * from Monitor_user")
	sql = "delete from Monitor_user where id = %s"%pk
	execute(sql)
	response = redirect('/manage_admin')
	return response

# @구현완료
def Manage_admin_cctv(request, pk):
	user = current_user(request)
	sql = "select * from Monitor_user where id=%s"%pk
	targetUser = USER.objects.raw(sql)
	sql = "select * from Monitor_cctv where id_USER_id = %s"%targetUser[0].id
	cctvs = CCTV.objects.raw(sql)
	return render(request, 'manage_admin_cctv.html', {'user':user, 'cctvs':cctvs})

# @구현완료
def Manage_cctv(request):
	user = current_user(request)
	cctvs = CCTV.objects.raw('select * from Monitor_cctv as A,Monitor_user as B where A.id_USER_id=B.id')
	return render(request, 'manage_cctv.html', {'user':user, 'cctvs':cctvs})

# @구현완료
def Manage_cctv_alloc(request,pk):
	user = current_user(request)
	if request.method == "POST":
		selected_cctvid,selected_userid = request.POST.getlist('cctv')[0],request.POST.getlist('user')[0]
		SQL = 'SELECT * FROM "Monitor_user" WHERE "Monitor_user"."id" = "%s"'%selected_userid
		selected_user_ins = USER.objects.raw(SQL)[0]
		SQL = 'SELECT * FROM "Monitor_cctv" WHERE "Monitor_cctv"."id" = "%s"'%selected_cctvid
		selected_cctv_ins = CCTV.objects.raw(SQL)[0]
		SQL = 'UPDATE "Monitor_cctv" SET "id_USER_id" = "%s" WHERE "Monitor_cctv"."id" = "%s"'%(selected_user_ins.id,selected_cctv_ins.id)
		with connection.cursor() as cursor:
			cursor.execute(SQL)
		connection.commit()
		cctvs = CCTV.objects.raw('select * from Monitor_cctv as A,Monitor_user as B where A.id_USER_id=B.id')
		return render(request, 'manage_cctv.html', {'user':user, 'cctvs':cctvs})

	cctv = CCTV.objects.raw("select * from Monitor_cctv where id = %s"%pk)[0]
	all_user = USER.objects.raw("select * from Monitor_user")
	return render(request, 'manage_cctv_alloc.html',{'user':user, 'thiscctv':cctv, 'all_user':all_user})

# @구현완료
def Manage_cctv_add(request):
	user = current_user(request)
	UPLOAD_DIR = '/home/ysm/Desktop/DB_TeamProject/VMS/Monitor/data/csv'
	if request.method == "POST":
		if 'csv' in request.FILES:
			try:
				file = request.FILES['csv']
				filename = file._name
				with open('%s/%s' % (UPLOAD_DIR, filename) , 'wb') as videofilePointer:
					for chunk in file.chunks():
						videofilePointer.write(chunk)
				with open('%s/%s' % (UPLOAD_DIR, filename), newline='') as csvfilePointer:
					csvReader = csv.reader(csvfilePointer, delimiter=',')
					for row in csvReader:
						model, setup_date, lat, lon = row[0],row[1],row[2],row[3]
						sql = "INSERT INTO Monitor_cctv (model,setup_date,lat,lon,id_USER_id) VALUES ('%s','%s',%f,%f,%d)"%(model,setup_date,float(lat),float(lon),user.id)
						execute(sql)
			except:
				return render(request, 'error.html', {'error_msg':'csv파일형식에 문제가 있습니다. 형식을 맞춰주세요.'})
		else:
			try:
				model,setup_date,lat,lon = request.POST.getlist('model')[0],request.POST.getlist('setup_date')[0],request.POST.getlist('lat')[0],request.POST.getlist('lon')[0]
				sql = "INSERT INTO Monitor_cctv (model,setup_date,lat,lon,id_USER_id) VALUES ('%s','%s',%f,%f,%d)"%(model,setup_date,float(lat),float(lon),user.id)
				execute(sql)
			except:
				return render(request, 'error.html', {'error_msg':'input값에 문제가 있습니다.'})
		cctvs = CCTV.objects.raw('select * from Monitor_cctv as A,Monitor_user as B where A.id_USER_id=B.id')
		return render(request, 'manage_cctv.html', {'user':user, 'cctvs':cctvs})
	#if not POST
	return render(request, 'manage_cctv_add.html', {'user':user})

# @구현완료
def Manage_cctv_delete(request, pk):
	user = current_user(request)

	try:
		targetCctv = CCTV.objects.get(id=pk)
		targetCctv.delete()
	except:
		print('error detection')

	cctvs = CCTV.objects.raw('select * from Monitor_cctv as A,Monitor_user as B where A.id_USER_id=B.id')
	return render(request, 'manage_cctv.html', {'user':user, 'cctvs':cctvs})

# @구현완료
def Manage_area_modify(request,pk):
	user = current_user(request)
	if request.method == "POST":
		name, addr 		 = request.POST.getlist('name')[0], request.POST.getlist('addr')[0]
		loc1, loc2, loc3 = request.POST.getlist('loc1')[0], request.POST.getlist('loc2')[0], request.POST.getlist('loc3')[0]
		lat, lon  		 = request.POST.getlist('lat')[0] , request.POST.getlist('lon')[0]
		sql = "UPDATE Monitor_area SET name='%s', address='%s',loc1='%s',loc2='%s',loc3='%s',lat=%f,lon=%f WHERE id = %s"%(name,addr,loc1,loc2,loc3,float(lat),float(lon),pk)
		execute(sql)
	targetArea = AREA.objects.raw("SELECT * FROM Monitor_area WHERE id=%d"%int(pk))[0]
	print(targetArea.name)
	return render(request, 'manage_area_modify.html', {'user':user, 'targetArea':targetArea})

# @구현완료
def Manage_area(request):
	user = current_user(request)
	sql = "SELECT * FROM Monitor_area"
	all_area = AREA.objects.raw(sql)
	if request.method == "POST":
		name = request.POST.getlist('name')[0]
		addr = request.POST.getlist('addr')[0]
		loc1 = request.POST.getlist('loc1')[0]
		loc2 = request.POST.getlist('loc2')[0]
		loc3 = request.POST.getlist('loc3')[0]
		lat  = request.POST.getlist('lat')[0]
		lon  = request.POST.getlist('lon')[0]
		sql = "INSERT INTO Monitor_area (name, address,loc1,loc2,loc3,lat,lon) VALUES ('%s','%s','%s','%s','%s',%f,%f)"%(name,addr,loc1,loc2,loc3,float(lat),float(lon))
		execute(sql)
		directory = "/home/ysm/Desktop/DB_TeamProject/VMS/Monitor/static/data/areas/"+name
		if not os.path.exists(directory):
		    os.makedirs(directory)
		if not os.path.exists(directory+'/video'):
		    os.makedirs(directory+'/video')
		if not os.path.exists(directory+'/metacsv'):
		    os.makedirs(directory+'/metacsv')
	return render(request, 'manage_area.html',{'user':user,'all_area':all_area})

# @구현완료
def Manage_area_delete(request,pk):
	user = current_user(request)
	sql = "DELETE FROM Monitor_area WHERE id=%s"%pk
	execute(sql)
	sql = "SELECT * FROM Monitor_area"
	allArea = AREA.objects.raw(sql)
	return render(request,'manage_area.html',{'user':user,'all_area':allArea})

# @구현완료
def Manage_neighbor(request):
	user = current_user(request)
	try:
		if request.method=="POST":
			area_id1 = request.POST.getlist('area1')[0]
			area_id2 = request.POST.getlist('area2')[0]
			if area_id1 == area_id2:
				return render(request, 'error.html', {'error_msg':'서로 같은 촬영공간을 이웃공간으로 할 수 없습니다.'})
			path = request.POST.getlist('path')[0]
			sql = "INSERT INTO Monitor_neighbor (path, id_AREA1_id, id_AREA2_id) VALUES ('%s',%d,%d)"%(path,int(area_id1),int(area_id2))
			execute(sql)
	except:
		return render(request, 'error.html', {'error_msg':'값을 정확히 주세요'})

	sql = "SELECT * FROM Monitor_neighbor"
	all_nei = NEIGHBOR.objects.raw(sql)
	sql = "SELECT * FROM Monitor_area"
	all_area = AREA.objects.raw(sql)

	return render(request,'manage_neighbor.html',{'user':user, 'all_nei':all_nei, 'all_area':all_area})

# @구현완료
def Manage_neighbor_map(request,pk):
	user = current_user(request)
	sql = "SELECT * FROM Monitor_neighbor WHERE id=%d"%int(pk)
	targetNEI = NEIGHBOR.objects.raw(sql)[0]
	try:
		if request.method == "POST":
			path = request.POST.getlist('path')[0]
			sql = "UPDATE Monitor_neighbor SET path='%s' WHERE id = %d"%(path,int(pk))
			execute(sql)
	except:
		return render(request, 'error.html', {'error_msg':'올바른 인풋값을 주세요'})

	sql = "SELECT * FROM Monitor_neighbor WHERE id=%d"%int(pk)
	targetNEI = NEIGHBOR.objects.raw(sql)[0]
	return render(request,'manage_neighbor_map.html',{'user':user, 'targetNEI':targetNEI})

# @ 구현완료
def Manage_neighbor_delete(request, pk):
	user = current_user(request)
	try:
		sql = "DELETE FROM Monitor_neighbor WHERE id=%s"%pk
		execute(sql)
	except:
		return render(request, 'error.html', {'error_msg':'알 수 없는 에러'})

	sql = "DELETE FROM Monitor_area_seq WHERE id_NEI1_id = %d or id_NEI2_id = %d or id_NEI3_id = %d or id_NEI4_id = %d"%(int(pk),int(pk),int(pk),int(pk))
	try:
		execute(sql)
	except:
		return render(request, 'error.html', {'error_msg':'알 수 없는 에러22'})
	sql="SELECT * FROM Monitor_neighbor"
	all_nei = NEIGHBOR.objects.raw(sql)
	sql="SELECT * FROM Monitor_area"
	all_area = AREA.objects.raw(sql)
	return render(request,'manage_neighbor.html',{'user':user, 'all_nei':all_nei, 'all_area':all_area})

# @구현완료
def Manage_sequence(request):
	user = current_user(request)
	sql="SELECT * FROM Monitor_neighbor"
	all_nei = NEIGHBOR.objects.raw(sql)
	if request.method=="POST":
		nei1 = request.POST.getlist('nei1')[0]
		nei2 = request.POST.getlist('nei2')[0]
		if nei1 == nei2:
			return render(request, 'error.html', {'error_msg':'같은 이웃공간으로 공간시퀀스를 정의할 수 없음'})
		sql = "SELECT * FROM Monitor_neighbor WHERE id=%s"%nei1
		n1 = NEIGHBOR.objects.raw(sql)[0]
		sql = "SELECT * FROM Monitor_neighbor WHERE id=%s"%nei2
		n2 = NEIGHBOR.objects.raw(sql)[0]
		sql = "INSERT INTO Monitor_area_seq (id_NEI1_id,id_NEI2_id) VALUES (%s,%s)"%(n1.id,n2.id)
		execute(sql)
	sql = "SELECT * FROM Monitor_area_seq"
	all_seq = AREA_SEQ.objects.raw(sql)
	return render(request,'manage_sequence.html',{'user':user,'all_seq':all_seq,'all_nei':all_nei})

# @구현완료
def Manage_sequence_append(request,pk):
	user = current_user(request)
	sql = "SELECT * FROM Monitor_area_seq WHERE id=%s"%pk
	targetSEQ = AREA_SEQ.objects.raw(sql)[0]
	countSEQ = count(targetSEQ)
	if request.method == 'POST':
		selNei    = request.POST.getlist('nei')[0]
		sql = "SELECT * FROM Monitor_neighbor WHERE id = %s"%selNei
		selNeiIns = NEIGHBOR.objects.raw(sql)[0]
		if countSEQ is 1:
			sql = "UPDATE Monitor_area_seq SET id_NEI2_id=%d WHERE id=%s"%(selNeiIns.id,pk)
			execute(sql)
		elif countSEQ is 2:
			sql = "UPDATE Monitor_area_seq SET id_NEI3_id=%d WHERE id=%s"%(selNeiIns.id,pk)
			execute(sql)
		elif countSEQ is 3:
			sql = "UPDATE Monitor_area_seq SET id_NEI4_id=%d WHERE id=%s"%(selNeiIns.id,pk)
			execute(sql)

	sql = "SELECT * FROM Monitor_area_seq WHERE id=%s"%pk
	targetSEQ = AREA_SEQ.objects.raw(sql)[0]
	countSEQ = count(targetSEQ)

	parti_area = set()
	try:
		parti_area.add(targetSEQ.id_NEI1.id_AREA1_id)
		parti_area.add(targetSEQ.id_NEI1.id_AREA2_id)
		parti_area.add(targetSEQ.id_NEI2.id_AREA1_id)
		parti_area.add(targetSEQ.id_NEI2.id_AREA2_id)
		parti_area.add(targetSEQ.id_NEI3.id_AREA1_id)
		parti_area.add(targetSEQ.id_NEI3.id_AREA2_id)
		parti_area.add(targetSEQ.id_NEI4.id_AREA1_id)
		parti_area.add(targetSEQ.id_NEI4.id_AREA2_id)
	except:
		pass
	areas = list(parti_area)
	templistAREA = []
	for area in areas:
		sql = "SELECT * FROM Monitor_area WHERE id=%d"%area
		tempAREA = AREA.objects.raw(sql)[0]
		templistAREA.append(tempAREA)
	areas = templistAREA

	parti_Neis=set()
	for i in areas:
		sql = "SELECT * FROM Monitor_neighbor WHERE id_AREA1_id = %s or id_AREA2_id = %s"%(i.id,i.id)
		Or = NEIGHBOR.objects.raw(sql)
		for j in Or:
			parti_Neis.add(j)
	try:
		parti_Neis.remove(targetSEQ.id_NEI1)
		parti_Neis.remove(targetSEQ.id_NEI2)
		parti_Neis.remove(targetSEQ.id_NEI3)
		parti_Neis.remove(targetSEQ.id_NEI4)
	except:
		pass
	parti_Neis_list=list(parti_Neis)
	return render(request,'manage_sequence_append.html',{'user':user,'targetSEQ':targetSEQ, 'len': countSEQ, 'count':range(countSEQ),'parti_Neis_list':parti_Neis_list})

def Manage_sequence_del(request,pk):
	user = current_user(request)
	sql = "SELECT * FROM Monitor_area_seq WHERE id=%s"%pk
	targetSEQ = AREA_SEQ.objects.raw(sql)[0]
	countSEQ = count(targetSEQ)

	if request.method == 'POST':
		selNei = request.POST.getlist('nei')[0]
		sql = "SELECT * FROM Monitor_neighbor WHERE id=%s"%selNei
		selNeiIns = NEIGHBOR.objects.raw(sql)[0]
		if countSEQ is 3:
			if selNeiIns == targetSEQ.id_NEI1:
				targetSEQ.id_NEI1_id = targetSEQ.id_NEI2_id
				targetSEQ.id_NEI2_id = targetSEQ.id_NEI3_id
				targetSEQ.id_NEI3_id = None
			elif selNeiIns == targetSEQ.id_NEI2:
				targetSEQ.id_NEI2_id = targetSEQ.id_NEI3_id
				targetSEQ.id_NEI3_id = None
			elif selNeiIns == targetSEQ.id_NEI3:
				targetSEQ.id_NEI3_id = None

		elif countSEQ is 4:
			if selNeiIns == targetSEQ.id_NEI1:
				targetSEQ.id_NEI1_id = targetSEQ.id_NEI2_id
				targetSEQ.id_NEI2_id = targetSEQ.id_NEI3_id
				targetSEQ.id_NEI3_id = targetSEQ.id_NEI4_id
				targetSEQ.id_NEI4_id = None
			elif selNeiIns == targetSEQ.id_NEI2:
				targetSEQ.id_NEI2_id = targetSEQ.id_NEI3_id
				targetSEQ.id_NEI3_id = targetSEQ.id_NEI4_id
				targetSEQ.id_NEI4_id = None
			elif selNeiIns == targetSEQ.id_NEI3:
				targetSEQ.id_NEI3_id = targetSEQ.id_NEI4_id
				targetSEQ.id_NEI4_id = None
			elif selNeiIns == targetSEQ.id_NEI4:
				targetSEQ.id_NEI4_id = None
		targetSEQ.save()

	sql = "SELECT * FROM Monitor_area_seq WHERE id=%s"%pk
	targetSEQ = AREA_SEQ.objects.raw(sql)[0]
	countSEQ = count(targetSEQ)

	arr=[]
	parti_nei1, parti_nei2, parti_nei3, parti_nei4 = set(),set(),set(),set()
	try:
		parti_nei1.add(targetSEQ.id_NEI1.id_AREA1)
		parti_nei1.add(targetSEQ.id_NEI1.id_AREA2)
		arr.append(parti_nei1)

		parti_nei2.add(targetSEQ.id_NEI2.id_AREA1)
		parti_nei2.add(targetSEQ.id_NEI2.id_AREA2)
		arr.append(parti_nei2)

		parti_nei3.add(targetSEQ.id_NEI3.id_AREA1)
		parti_nei3.add(targetSEQ.id_NEI3.id_AREA2)
		arr.append(parti_nei3)

		parti_nei4.add(targetSEQ.id_NEI4.id_AREA1)
		parti_nei4.add(targetSEQ.id_NEI4.id_AREA2)
		arr.append(parti_nei4)
	except:
		pass

	possible = []
	if countSEQ is 4:
		for i in arr:
			temp = arr.copy()
			temp.remove(i)
			sum = 0
			case1 = temp[0].intersection(temp[1])
			if len(case1) == 0:
				sum+=1
			case2 = temp[1].intersection(temp[2])
			if len(case2) == 0:
				sum+=1
			case3 = temp[2].intersection(temp[0])
			if len(case3) == 0:
				sum+=1
			if sum >= 2:
				possible.append(False)
			else:
				possible.append(True)
	elif countSEQ is 3:
		for i in arr:
			temp = arr.copy()
			temp.remove(i)
			sum = 0
			case1 = temp[0].intersection(temp[1])
			if len(case1) == 0:
				sum+=1
			if sum >= 1:
				possible.append(False)
			else:
				possible.append(True)

	if countSEQ is 4:
		all_area_in = [targetSEQ.id_NEI1,targetSEQ.id_NEI2,targetSEQ.id_NEI3,targetSEQ.id_NEI4]
	elif countSEQ is 3:
		all_area_in = [targetSEQ.id_NEI1,targetSEQ.id_NEI2,targetSEQ.id_NEI3]
	elif countSEQ is 2:
		all_area_in = [targetSEQ.id_NEI1,targetSEQ.id_NEI2]

	zipped = zip(possible,all_area_in)

	return render(request,'manage_sequence_del.html',{'user':user,'targetSEQ':targetSEQ, 'len': countSEQ, 'count':range(countSEQ),'zipped':zipped})

# @구현완료
def Manage_sequence_remove(request,pk):
	user = current_user(request)
	sql = "DELETE FROM Monitor_area_seq WHERE id=%s"%pk
	execute(sql)
	sql = "SELECT * FROM Monitor_area_seq"
	all_seq = AREA_SEQ.objects.raw(sql)
	return render(request,'manage_sequence.html',{'user':user,'all_seq':all_seq})

# @구현완료
def Manage_sequence_map(request,pk):
	user = current_user(request)
	sql = "SELECT * FROM Monitor_area_seq WHERE id=%s"%pk
	targetSEQ = AREA_SEQ.objects.raw(sql)[0]
	ret,temp_set= [],[]
	try:
		ret.append(targetSEQ.id_NEI1)
		ret.append(targetSEQ.id_NEI2)
		ret.append(targetSEQ.id_NEI3)
		ret.append(targetSEQ.id_NEI4)
	except:
		pass

	try:
		if targetSEQ.id_NEI1.id_AREA1 not in temp_set : temp_set.append(targetSEQ.id_NEI1.id_AREA1)
		if targetSEQ.id_NEI1.id_AREA2 not in temp_set : temp_set.append(targetSEQ.id_NEI1.id_AREA2)
		if targetSEQ.id_NEI2.id_AREA1 not in temp_set : temp_set.append(targetSEQ.id_NEI2.id_AREA1)
		if targetSEQ.id_NEI2.id_AREA2 not in temp_set : temp_set.append(targetSEQ.id_NEI2.id_AREA2)
		if targetSEQ.id_NEI3.id_AREA1 not in temp_set : temp_set.append(targetSEQ.id_NEI3.id_AREA1)
		if targetSEQ.id_NEI3.id_AREA2 not in temp_set : temp_set.append(targetSEQ.id_NEI3.id_AREA2)
		if targetSEQ.id_NEI4.id_AREA1 not in temp_set : temp_set.append(targetSEQ.id_NEI4.id_AREA1)
		if targetSEQ.id_NEI4.id_AREA2 not in temp_set : temp_set.append(targetSEQ.id_NEI4.id_AREA2)
	except:
		pass

	retAREA = temp_set
	cntAREA = range(len(temp_set))
	zipAREA = zip(cntAREA,temp_set)

	lat, lon = 0, 0
	for i in retAREA:
		lat += float(i.lat)
		lon += float(i.lon)

	clat = lat/(count(targetSEQ)+1)
	clon = lon/(count(targetSEQ)+1)

	return render(request,'manage_sequence_map.html',{'user':user,'cntAREA':cntAREA,'retAREA':retAREA,'zipAREA':zipAREA,'clat':clat,'clon':clon})

# @구현완료
def Manage_sequence_mapview(request,pk):
	user = current_user(request)
	sql = "SELECT * FROM Monitor_area_seq WHERE id=%d"%int(pk)
	targetSEQ = AREA_SEQ.objects.raw(sql)[0]
	return render(request,'manage_sequence_mapview.html',{'user':user,'targetSEQ':targetSEQ})

# @구현완료
def Admin_cctv(request):
	user = current_user(request)
	sql = "SELECT * FROM Monitor_cctv WHERE id_USER_id=%d"%user.id
	myCctvs = CCTV.objects.raw(sql)
	c_a={}
	for cctv in myCctvs:
		sql = "SELECT * FROM Monitor_cctv_area WHERE id_CCTV_id=%d"%cctv.id
		tt = CCTV_AREA.objects.raw(sql)
		temps=[]
		for rel in tt:
			sql = "SELECT * FROM Monitor_area WHERE id=%d"%rel.id_AREA_id
			area = AREA.objects.raw(sql)[0]
			temps.append(area)
		c_a.update({cctv:temps})
	return render(request, 'admin_cctv.html',{'user':user,'cctvs':myCctvs, 'cctv_area':c_a})

# @구현완료
def Admin_cctv_area_alloc(request,pk):
	user = current_user(request)
	cctv = CCTV.objects.raw("SELECT * FROM Monitor_cctv where id =%d"%int(pk))[0]
	allArea = AREA.objects.raw("SELECT * FROM Monitor_area")
	return render(request,'admin_cctv_area_alloc.html',{'user':user,'all_area':allArea, 'cctv':cctv})

# @구현완료
def Admin_cctv_area_alloc_append(request):
	user = current_user(request)
	sql = "SELECT * FROM Monitor_cctv where id_USER_id=%d"%user.id
	myCctvs = CCTV.objects.raw(sql)
	if request.method=="GET":
		try:
			cctvid,areaid = request.GET.getlist('cctvid')[0],request.GET.getlist('areaid')[0]
			sql_cctv = "SELECT * FROM Monitor_cctv WHERE id = %d"%int(cctvid)
			sql_area = "SELECT * FROM Monitor_area WHERE id = %d"%int(areaid)
			sql = "INSERT INTO Monitor_cctv_area (id_AREA_id, id_CCTV_id) VALUES (%d, %d)"%(int(areaid), int(cctvid))
			execute(sql)
			sql = "SELECT * FROM Monitor_cctv WHERE id_USER_id=%d"%int(user.id)
			myCctvs = CCTV.objects.raw(sql)
			c_a={}
			for cctv in myCctvs:
				sql = "SELECT * FROM Monitor_cctv_area WHERE id_CCTV_id=%d"%cctv.id
				tt = CCTV_AREA.objects.raw(sql)
				temps=[]
				for rel in tt:
					sql = "SELECT * FROM Monitor_area WHERE id=%d"%rel.id_AREA_id
					area = AREA.objects.raw(sql)[0]
					temps.append(area)
				c_a.update({cctv:temps})
		except:
			return render(request, 'error.html', {'error_msg':'에러가 발생했습니다.. 혹시 같은 촬영공간을 추가하지 않았나요?'})
		return render(request, 'admin_cctv.html',{'user':user,'cctvs':myCctvs, 'cctv_area':c_a})

# @구현완료
def Admin_video(request):
#일반관리자는 본인에게 할당된 촬영 영상 파일과 메타 로그 파일을 함께 업로드 할 수 있으며 이때 촬영공간과 파일 생성 시간을 지정하여 업로드한다.
	user = current_user(request)
	if request.method == "POST":
		cctvid = request.GET.getlist('cctvid')[0]
		areaid = request.GET.getlist('areaid')[0]
		sql = "SELECT * FROM Monitor_area WHERE id = %d"%int(areaid)
		areaName = AREA.objects.raw(sql)[0].name
		UPLOAD_DIR_V = '/home/ysm/Desktop/DB_TeamProject/VMS/Monitor/static/data/areas/%s/video'%areaName
		UPLOAD_DIR_M = '/home/ysm/Desktop/DB_TeamProject/VMS/Monitor/static/data/areas/%s/metacsv'%areaName

		if 'video' in request.FILES and 'metacsv' in request.FILES:
			file = request.FILES['video']
			filename = file._name
			fp = open('%s/%s' % (UPLOAD_DIR_V, filename) , 'wb')
			for chunk in file.chunks():
				fp.write(chunk)
			fp.close()

			file2 = request.FILES['metacsv']
			filename2 = file2._name
			fp2 = open('%s/%s' % (UPLOAD_DIR_M, filename2) , 'wb')
			for chunk in file2.chunks():
				fp2.write(chunk)
			fp2.close()

			sql = "SELECT * FROM Monitor_cctv_area WHERE id_CCTV_id = %d and id_AREA_id = %d"%(int(cctvid),int(areaid))
			targetCCTV_AREA = CCTV_AREA.objects.raw(sql)[0]

			VideoFilepath = 'data/areas/%s/video/%s' % (areaName, filename)
			MetaFilepath = 'data/areas/%s/metacsv/%s' % (areaName, filename2)
			duration = timeparser(VideoFilepath)

			startTime = '%s-%s-%s %s:00:00'%(duration[0][:4],duration[0][4:6],duration[0][6:8],duration[1])
			endTime = '%s-%s-%s %s:00:00'%(duration[0][:4],duration[0][4:6],duration[0][6:8],str(int(duration[1])+1))
			sql = "INSERT INTO Monitor_video (filePath, metaPath, startTime, endTime, id_CCTV_AREA_id) VALUES ('%s','%s','%s','%s',%d)"%(VideoFilepath,MetaFilepath,startTime,endTime,targetCCTV_AREA.id)
			newVideo_id = execute(sql)
			sql = "SELECT * FROM Monitor_video WHERE id=%d"%newVideo_id
			newVideo = VIDEO.objects.raw(sql)[0]

			numRec, duras, Objs, sumVel, sumSize, listColors= 0, [], set(), 0, 0, []
			avrVel, avrSize = 0, 0
			graph_x, graph_y, graph_size, graph_speed = [],[],[],[]
			sumX, sumY = 0,0
			with open('%s/%s' % (UPLOAD_DIR_M, filename2), newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',')
				for row in spamreader:
					sql = "INSERT INTO Monitor_metalog (id_obj,time,loc_obj_x,loc_obj_y,size_obj,speed_obj,color_obj,id_VIDEO_id) VALUES ('%s','%s',%f,%f,%f,%f,'%s',%d)"%(row[1],metaTimeParser(row[0]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),row[6],newVideo_id)
					newMETALOG_id = execute(sql)
					sql = "SELECT * FROM Monitor_metalog WHERE id =%d"%newMETALOG_id
					newMETALOG = METALOG.objects.raw(sql)[0]

					graph_x.append(row[2])
					graph_y.append(row[3])
					graph_size.append(row[4])
					graph_speed.append(row[5])
					duras.append(DateTime(row[0]))
					Objs.add(row[1])

					sumX += float(row[2])
					sumY += float(row[3])
					sumSize += float(row[4])
					sumVel  += float(row[5])
					listColors.append(row[6])

					numRec += 1
				avrX    = sumX/numRec
				avrY    = sumY/numRec
				avrVel  = sumVel/numRec
				avrSize = sumSize/numRec
				dura = (duras[-1]-duras[0]).seconds

				saveDIR = '/home/ysm/Desktop/DB_TeamProject/VMS/Monitor/static/data/statistic/%d'%newVideo_id
				csvFILE = '%s/%s' % (UPLOAD_DIR_M, filename2)
				makeGraph(csvFILE, saveDIR)

				sql = "INSERT INTO Monitor_statistic (num_record, duration, num_obj, avg_speed, avg_size, graph_img_path, id_METALOG_id) "
				sql += "VALUES (%d, %d, %d, %f, %f, '%s', %d)"%(int(numRec),int(dura),len(Objs),float(avrVel),float(avrSize),saveDIR+'_tran_loc.png',newVideo_id)
				execute(sql)

	return render(request, 'admin_video.html',{'user':user})

# @구현완료
def Video_view(request,pk):
	user = current_user(request)
	sql = "select * from Monitor_video as V, Monitor_cctv_area as CA, Monitor_area as A where V.id = %s and V.id_CCTV_AREA_id = CA.id and CA.id_AREA_id = A.id"%pk

	with connection.cursor() as cursor:
		cursor.execute(sql)
		target_video = cursor.fetchall()

	sql = 'select * from Monitor_metalog where id_VIDEO_id = %s'%pk
	with connection.cursor() as cursor:
		cursor.execute(sql)
		target_meta = cursor.fetchall()

	sql = "SELECT * FROM Monitor_statistic where id_METALOG_id=%s"%pk
	with connection.cursor() as cursor:
		cursor.execute(sql)
		target_stati = cursor.fetchall()[0]

	graph = target_stati[-2]
	graph = graph.replace('/home/ysm/Desktop/DB_TeamProject/VMS/Monitor/static/','')
	# graph2 = graph.replace('_tran_loc.png','')+'_tran_size.png'

	sql = "SELECT * FROM Monitor_statistic WHERE id_METALOG_id = %s"%pk
	targetSTATISCTIC = STATISTIC.objects.raw(sql)[0]
	print(targetSTATISCTIC)
	return render(request, 'video_view.html',{'user':user, 'target_video':target_video,'target_meta':target_meta,'graph':graph,'target_stat':targetSTATISCTIC})

# @구현완료
def Map(request):
	lat = request.GET.getlist('lat')[0]
	lon = request.GET.getlist('lon')[0]
	return render(request,'map.html',{'lat':lat,'lon':lon})

# @구현완료
def Manage_neighbor_innermap(request,pk):
	sql = "SELECT * FROM Monitor_neighbor WHERE id=%s"%pk
	targetNEI = NEIGHBOR.objects.raw(sql)[0]
	center_lat = (float(targetNEI.id_AREA1.lat) + float(targetNEI.id_AREA2.lat))/2
	center_lon = (float(targetNEI.id_AREA1.lon) + float(targetNEI.id_AREA2.lon))/2

	return render(request,'manage_neighbor_innermap.html',{'targetNEI':targetNEI,'center_lat':center_lat,'center_lon':center_lon})

# @구현완료
def My(request):
	user = current_user(request)
	if request.method == "POST":
		try:
			targetUSER_id = user.id
			pw,name,position,phone_number = request.POST.getlist('pw')[0],request.POST.getlist('name')[0],request.POST.getlist('position')[0],request.POST.getlist('phone_number')[0]
			sql = "UPDATE Monitor_user set pw='%s', name='%s', position='%s', phone_number='%s' where id='%s'"%(pw,name,position,phone_number,targetUSER_id)
			execute(sql)
		except:
			return render(request, 'error.html', {'error_msg':'올바르지 않은 전달입니다.'})
	return render(request,'my.html',{'user':user, 'positions':positions})

# @구현완료
def Video_search(request):
	user = current_user(request)
	return render(request,'video_search.html',{'user':user})


def Manage_videos(request):
	user = current_user(request)
	if request.method=="POST":
		print(request.POST)
		startTime = request.POST.getlist('start-time')[0]
		endTime = request.POST.getlist('end-time')[0]
		sql = "SELECT id FROM Monitor_video AS V WHERE V.startTime >= '%s' and V.endTime <= '%s'"%(searchTimeParser(startTime),searchTimeParser(endTime))
		targetVIDEOid = fetch(sql)
		targetVIDEOid = [x[0] for x in targetVIDEOid]
		print(targetVIDEOid)
		for vid in targetVIDEOid:
			sql = "DELETE FROM Monitor_video WHERE id = %d"%vid
			execute(sql)
			sql = "DELETE FROM Monitor_metalog WHERE id_VIDEO_id = %d"%vid
			execute(sql)
			sql = "DELETE FROM Monitor_statistic WHERE id_METALOG_id = %d"%vid
			execute(sql)
	sql = "SELECT V.id, V.startTime, V.endTime, A.name, C.model, C.setup_date FROM Monitor_video as V, Monitor_cctv_area as CA, Monitor_area as A, Monitor_cctv as C WHERE V.id_CCTV_AREA_id = CA.id AND A.id = CA.id_AREA_id AND C.id = id_CCTV_id ORDER BY V.startTime"
	all_video = fetch(sql)

	return render(request,'manage_videos.html',{'user':user, 'all_video':all_video})
