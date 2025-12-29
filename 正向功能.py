import requests

HOST = 'http://172.31.132.234:8000/api2' #定义全局变量HOST
TOKEN = None                #定义全局变量TOKEN
REPO_ID = None              #定义全局变量资料库ID
REPO_ID_encrypted = None    #定义全局变量加密后的资料库ID
UPLOAD_URL = ""
DOWNLOAD_URL = ""

class TestSeaFile:

    def test_get_token(self):
        # 验证正确信息登录获取授权令牌
        global TOKEN
        url = f'{HOST}/auth-token/'
        body = {'username':'tqh@123.com', 'password':123456}
        response = requests.post(url, data=body)
        assert response.status_code == 200
        TOKEN = response.json().get('token')
        print(response.json())
        return TOKEN

    def test_check_account_info(self):
        # 验证获取账户信息
        url = f'{HOST}/account/info/'
        response = requests.get(url, headers= {'Authorization': f'Token {TOKEN}'})
        assert response.status_code == 200

    def test_create_database(self):
        # 验证新建资料库
        global REPO_ID
        url = f'{HOST}/repos/'
        body = {'name': '新建资料库'}
        response = requests.post(url, headers= {'Authorization': f'Token {TOKEN}'}, data=body)
        assert response.status_code == 200
        REPO_ID = response.json().get('repo_id')
        print(response.json().get('repo_id'))
        return REPO_ID

    def test_create_encrypted_database(self):
        # 验证新建加密资料库
        global REPO_ID_encrypted
        url = f'{HOST}/repos/'
        body = {'name': '新建加密资料库', 'passwd': 123456789}
        response = requests.post(url, headers= {'Authorization': f'Token {TOKEN}'}, data=body)
        assert response.status_code == 200
        REPO_ID_encrypted = response.json().get('repo_id')
        return REPO_ID_encrypted

    def test_check_database_passwd(self):
        # 验证加密资料库的密码
        url = f'{HOST}/repos/{REPO_ID_encrypted}'
        body = {'passwd': 123456789}
        response = requests.post(url, headers= {'Authorization': f'Token {TOKEN}'}, data=body)
        assert response.status_code == 200

    def test_get_database_list(self):
        # 验证获取资料库列表
        url = f'{HOST}/repos/'
        response = requests.get(url, headers= {'Authorization': f'Token {TOKEN}'})
        assert response.status_code == 200

    def test_get_database_info(self):
        # 验证获取新建资料库信息
        url = f'{HOST}/repos/{REPO_ID}/'
        response = requests.get(url, headers= {'Authorization': f'Token {TOKEN}'})
        assert response.status_code == 200

    def test_rename_database(self):
        # 验证重命名资料库
        url = f'{HOST}/repos/{REPO_ID}/?op=rename'
        body = {'repo_name': '重命名的资料库'}
        response = requests.post(url, headers={'Authorization': f'Token {TOKEN}'}, data=body)
        assert response.status_code == 200
        assert response.json() == 'success'

    def test_get_rename_database_info(self):
        # 验证获取重命名资料库信息
        url = f'{HOST}/repos/{REPO_ID}/'
        response = requests.get(url, headers= {'Authorization': f'Token {TOKEN}'})
        print(response.json().get('name'))


    def test_get_upload_link(self):
        # 验证获取上传链接
        global UPLOAD_URL
        url = f'{HOST}/repos/{REPO_ID}/upload-link/'
        response = requests.get(url, headers={'Authorization': f'Token {TOKEN}'})
        assert response.status_code == 200
        UPLOAD_URL = response.json()
        print(response.json())
        return UPLOAD_URL

    def test_upload_file(self):
        # 验证上传文件
        url = UPLOAD_URL
        print(url)
        body = {'parent_dir':'/'}
        f = open('Seafile.postman_collection.json','rb')
        files = {'file': f}
        response = requests.post(url, files=files, data= body, headers={'Authorization': f'Token {TOKEN}'})
        assert response.status_code == 200

    def test_get_download_link(self):
        # 验证获取下载链接
        global DOWNLOAD_URL
        url = f'{HOST}/repos/{REPO_ID}/file/?p=/Seafile.postman_collection.json'
        response = requests.get(url, headers={'Authorization': f'Token {TOKEN}'})
        print(response.json())
        assert response.status_code == 200
        DOWNLOAD_URL = response.json()
        return DOWNLOAD_URL

    def test_get_file_info(self):
        # 验证获取文件信息
        url = f'{HOST}/repos/{REPO_ID}/file/detail/?p=/Seafile.postman_collection.json'
        response = requests.get(url, headers={'Authorization': f'Token {TOKEN}'})
        assert response.status_code == 200

    def test_download_file(self):
        # 验证下载文件
        url = DOWNLOAD_URL
        print(url)
        response = requests.get(url, headers={'Authorization': f'Token {TOKEN}'})
        assert response.status_code == 200

    def test_rename_file(self):
        # 验证重命名文件
        url = f'{HOST}/repos/{REPO_ID}/file/?p=/Seafile.postman_collection.json'
        body = {'operation':'rename', 'newname':'重命名的文件.json'}
        response = requests.post(url, headers={'Authorization': f'Token {TOKEN}'}, data=body)
        assert response.status_code == 404

    def test_delete_file(self):
        # 验证删除文件
        url = f'{HOST}/repos/{REPO_ID}/file/?p=/重命名的文件.json'
        response = requests.delete(url, headers={'Authorization': f'Token {TOKEN}'})
        assert response.status_code == 200

    def test_delete_database(self):
        # 验证删除资料库
        url = f'{HOST}/repos/{REPO_ID}/'
        response = requests.delete(url, headers= {'Authorization': f'Token {TOKEN}'})
        assert response.status_code == 200
