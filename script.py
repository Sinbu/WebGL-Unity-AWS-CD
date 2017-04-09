import requests
import json
import tinys3
import zipfile
import StringIO
import os

def lambda_handler(event, context):
	conn = tinys3.Connection(S3_ACCESS_KEY,S3_SECRET_KEY)
	tokenId = "Basic" + UNITY_API_KEY
	s3bucket = S3_BUCKET_NAME
	print event
	buildLink = event["links"]["api_self"]["href"]

	authPayload = {"Authorization": tokenId}
	buildData = requests.get("https://build-api.cloud.unity3d.com" + buildLink, headers=authPayload)
	primaryLink = json.loads(buildData.text)["links"]["download_primary"]["href"]
	print primaryLink
	results = requests.get(primaryLink)
	zip = zipfile.ZipFile(StringIO.StringIO(results.content))
	zip.extractall("/tmp/")

	f = open("/tmp/WebGL build/index.html",'rb')
	conn.upload('index.html',f,s3bucket)

	files = os.listdir("/tmp/WebGL build/Build")
	for filename in files:
		f = open("/tmp/WebGL build/Build/" + filename,'rb')
		conn.upload("Build/" + filename,f,s3bucket)
	files = os.listdir("tmp/WebGL build/TemplateData")
	for filename in files:
		f = open("/tmp/WebGL build/TemplateData/" + filename,'rb')
		conn.upload("TemplateData/" + filename,f,s3bucket)

	return "Done"