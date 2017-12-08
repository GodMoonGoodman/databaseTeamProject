from django.db import models
class USER(models.Model):
	email = models.CharField('email',max_length=20, unique=True)
	pw = models.CharField('pw',max_length=10)
	name = models.CharField('name',max_length=30)
	position = models.CharField('position',max_length=20)
	phone_number = models.CharField(max_length=15, unique=True)
	is_super = models.BooleanField('is_super', default=False)
	is_on = models.BooleanField('is_on', default=False)

class AREA(models.Model):
	name = models.CharField('name',max_length=10, unique=True)
	address = models.CharField('addr',max_length=30)
	loc1 = models.CharField('loc1',max_length=10)
	loc2 = models.CharField('loc2',max_length=10)
	loc3 = models.CharField('loc3',max_length=10)
	lat = models.FloatField('lat')
	lon = models.FloatField('lon')

class SESSION(models.Model):
	id_USER = models.ForeignKey(USER)
	sess = models.CharField('sess', max_length=30, unique=True)
	class Meta:
		unique_together = (('id_USER', 'sess',))

class NEIGHBOR(models.Model):
	id_AREA1 = models.ForeignKey(AREA, related_name='id_area1', on_delete=models.CASCADE)
	id_AREA2 = models.ForeignKey(AREA, related_name='id_area2', on_delete=models.CASCADE)
	path = models.CharField('path',max_length=30)
	class Meta:
		unique_together = (('id_AREA1', 'id_AREA2','path',))

class CCTV(models.Model):
	model = models.CharField('model', max_length=20)
	setup_date = models.DateField('setup_date')
	id_USER = models.ForeignKey(USER, default=None)
	lat = models.FloatField('lat', null=True)
	lon = models.FloatField('lon', null=True)

class AREA_SEQ(models.Model):
	id_NEI1 = models.ForeignKey(NEIGHBOR, related_name='id_nei1',null=True, on_delete=models.CASCADE)
	id_NEI2 = models.ForeignKey(NEIGHBOR, related_name='id_nei2',null=True, on_delete=models.CASCADE)
	id_NEI3 = models.ForeignKey(NEIGHBOR, related_name='id_nei3',null=True, on_delete=models.CASCADE)
	id_NEI4 = models.ForeignKey(NEIGHBOR, related_name='id_nei4',null=True, on_delete=models.CASCADE)

	def __str__(self):
		if self.id_NEI3 == None and self.id_NEI4 == None:
			return '<%s>-%s-<%s>,<%s>-%s-<%s>'%(
				self.id_NEI1.id_AREA1.name, self.id_NEI1.path, self.id_NEI1.id_AREA2.name,
				self.id_NEI2.id_AREA1.name, self.id_NEI2.path, self.id_NEI2.id_AREA2.name)
		if self.id_NEI3 != None and self.id_NEI4 == None:
			return '<%s>-%s-<%s>,<%s>-%s-<%s>,<%s>-%s-<%s>'%(
				self.id_NEI1.id_AREA1.name, self.id_NEI1.path, self.id_NEI1.id_AREA2.name,
				self.id_NEI2.id_AREA1.name, self.id_NEI2.path, self.id_NEI2.id_AREA2.name,
				self.id_NEI3.id_AREA1.name, self.id_NEI3.path, self.id_NEI3.id_AREA2.name)
		if self.id_NEI3 != None and self.id_NEI4 != None:
			return '<%s>-%s-<%s>,<%s>-%s-<%s>,<%s>-%s-<%s>,<%s>-%s-<%s>'%(
				self.id_NEI1.id_AREA1.name, self.id_NEI1.path, self.id_NEI1.id_AREA2.name,
				self.id_NEI2.id_AREA1.name, self.id_NEI2.path, self.id_NEI2.id_AREA2.name,
				self.id_NEI3.id_AREA1.name, self.id_NEI3.path, self.id_NEI3.id_AREA2.name,
				self.id_NEI4.id_AREA1.name, self.id_NEI4.path, self.id_NEI4.id_AREA2.name)
	class Meta:
		unique_together = (('id_NEI1', 'id_NEI2','id_NEI3','id_NEI4',))

class CCTV_AREA(models.Model):
	id_CCTV = models.ForeignKey(CCTV, on_delete=models.CASCADE)
	id_AREA = models.ForeignKey(AREA, on_delete=models.CASCADE)
	class Meta:
		unique_together = (('id_CCTV', 'id_AREA',))

class VIDEO(models.Model):
	filePath = models.FilePathField('file_path',max_length=300, default='')
	metaPath = models.FilePathField('meta_path',max_length=300, default='')
	id_CCTV_AREA = models.ForeignKey(CCTV_AREA)
	startTime = models.DateTimeField('start_time')
	endTime = models.DateTimeField('end_time',)
	
	class Meta:
		unique_together = (('id_CCTV_AREA', 'startTime','endTime',))

class METALOG(models.Model):
	id_obj = models.CharField('id_obj',max_length=11)#object3
	time = models.DateTimeField('time')#1509000829
	loc_obj_x = models.FloatField('loc_x')#36.225, 186.223
	loc_obj_y = models.FloatField('loc_y')#36.225, 186.223
	size_obj = models.FloatField('size')#165.0
	speed_obj = models.FloatField('speed')#32
	color_obj = models.CharField('color',max_length=11)#YELLOW
	id_VIDEO = models.ForeignKey(VIDEO)#videofile

	# class Meta:
	# 	unique_together = (('id_obj', 'time','id_VIDEO_id'))

class STATISTIC(models.Model):
	id_METALOG = models.OneToOneField(METALOG,unique=True)
	num_record = models.IntegerField('num_rec')
	duration = models.IntegerField('duration')
	num_obj = models.IntegerField('num_obj')
	avg_speed = models.FloatField('avg_spd')
	avg_size = models.FloatField('avg_size')
	graph_img_path = models.FilePathField('img_path',max_length=100)