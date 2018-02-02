import dropbox

app_key = 'r35rb9wf4h4rp4b'
app_secret = '5pdlce9sah7bxg8'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()

access_token, user_id = flow.finish(code)

client = dropbox.client.DropboxClient(access_token)
print 'linked account: ', client.account_info()

f = open('dbTest.txt', 'rb')
response = client.put_file('/magnum-opus.txt', f)
print 'uploaded: ', response