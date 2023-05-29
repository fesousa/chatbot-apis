
.\setupenv.ps1
sam build
sam package --region us-east-1 --resolve-s3
sam deploy --stack-name api-chatbot --region us-east-1 --capabilities CAPABILITY_IAM --resolve-s3 --parameter-overrides "UserMail=$Env:USERMAIL PwdMail=$Env:PWDMAIL ServerMail=$Env:SERVERMAIL PortMail=$Env:PORTMAIL"
