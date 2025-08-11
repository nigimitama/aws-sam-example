# sam pipline のテスト

次のコマンドで pipeline の設定を開始します。

```sh
# pipelineのセットアップ
# --bootstrap: 対話型のインターフェースで設定を行う
$ sam pipeline init --bootstrap
```

たくさん質問が出てくるので答えていきます。

```sh
Select a pipeline template to get started:
        1 - AWS Quick Start Pipeline Templates
        2 - Custom Pipeline Template Location
Choice: 1
```

まずテンプレートですが、Quick Start Pipeline Templates を使います。

```sh
Select CI/CD system
        1 - Jenkins
        2 - GitLab CI/CD
        3 - GitHub Actions
        4 - Bitbucket Pipelines
        5 - AWS CodePipeline
Choice: 3
```

今回は GitHub Actions を選びます

```sh
You are using the 2-stage pipeline template.
 _________    _________
|         |  |         |
| Stage 1 |->| Stage 2 |
|_________|  |_________|

Checking for existing stages...

[!] None detected in this account.

Do you want to go through stage setup process now? If you choose no, you can still reference other bootstrapped resources. [Y/n]: Y # Enter
```

Enter (=Y) を押します

### Stage 1 の設定

```sh
Stage 1 Setup

[1] Stage definition
Enter a configuration name for this stage. This will be referenced later when you use the sam pipeline init command:
Stage configuration name: dev # dev → prod の二段階構成にしてみます
```

ひとまず `dev` という名前にします

```sh
[2] Account details
The following AWS credential sources are available to use.
To know more about configuration AWS credentials, visit the link below:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
        1 - Environment variables (not available)
        2 - default (named profile)
        q - Quit and configure AWS credentials
Select a credential source to associate with this stage: 2 # 使いたい認証方法を選ぶ
```

使いたい認証方法を選びます。今回は aws cli の defaul profile を選んでいます。

```sh
Enter the region in which you want these resources to be created [ap-northeast-1]: # 変える必要がないのでEnter
```

```sh
Select a user permissions provider:
        1 - IAM (default)
        2 - OpenID Connect (OIDC)
Choice (1, 2): # そのままEnter
```

```sh
Enter the pipeline IAM user ARN if you have previously created one, or we will create one for you []:  # そのままEnter
```

```sh
[3] Reference application build resources
Enter the pipeline execution role ARN if youe for you []:  # そのままEnter
Enter the CloudFormation execution role ARN if you have previously created one, or we will create one for you []:  # そのままEnter
Please enter the artifact bucket ARN for your Lambda function. If you do not have a bucket, we will create one for you []: # そのままEnter
```

ARN の入力系はぜんぶ空のまま Enter してこの場で作成させます。

```sh
Does your application contain any IMAGE type Lambda functions? [y/N]: y # 今回はImageを使うLambdaを使ってみる
Please enter the ECR image repository ARN(s) for your Image type function(s).If you do not yet have a repository, we will create one for you []: # そのままEnter
```

対象の Lambda が zip でデプロイするタイプなのか Image を使うタイプなのか質問が来ます。この例では Iamge を使っていますので y を押します。

```sh
[4] Summary
Below is the summary of the answers:
        1 - Account: XXXXXXXXXXXXXX
        2 - Stage configuration name: dev
        3 - Region: ap-northeast-1
        4 - Pipeline user: [to be created]
        5 - Pipeline execution role: [to be created]
        6 - CloudFormation execution role: [to be created]
        7 - Artifacts bucket: [to be created]
        8 - ECR image repository: [to be created]
Press enter to confirm the values above, or select an item to edit the value:  # Enterを押して続行

This will create the following required resources for the 'dev' configuration:
        - Pipeline IAM user
        - Pipeline execution role
        - CloudFormation execution role
        - Artifact bucket
        - ECR image repository
Should we proceed with the creation? [y/N]: y # この場で作る
```

#### Github Actions の設定

作られたリソースのログの中に AWS の認証情報があります。

```sh
The following resources were created in your account:
        - Pipeline execution role
        - CloudFormation execution role
        - Artifact bucket
        - Pipeline IAM user
        - ECR image repository
Pipeline IAM user credential:
        AWS_ACCESS_KEY_ID: XXXXXXXXXXXXXXXXXXXXXXX
        AWS_SECRET_ACCESS_KEY: XXXXXXXXXXXXXXXXXXXXXXX
```

これらをコピーして Github Actions の Repository Secrets に貼り付けます。

参考：

https://docs.github.com/ja/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets#creating-secrets-for-a-repository

### Stage 2 の設定

Stage1 作成後、続けて Stage2 を作るかどうかの質問が出るので Enter で進めます。

```sh
Only 1 stage(s) were detected, fewer than what the template requires: 2. If these are incorrect, delete .aws-sam/pipeline/pipelineconfig.toml and rerun

Do you want to go through stage setup process now? If you choose no, you can still reference other bootstrapped resources. [Y/n]: # Enter
```

```sh
Stage 2 Setup

[1] Stage definition
Enter a configuration name for this stage. This will be referenced later when you use the sam pipeline init command:
Stage configuration name: prod # 名前を設定
```

```sh
[2] Account details
The following AWS credential sources are available to use.
To know more about configuration AWS credentials, visit the link below:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
        1 - Environment variables (not available)
        2 - default (named profile)
        q - Quit and configure AWS credentials
Select a credential source to associate with this stage: 2
```

```sh
[3] Reference application build resources
Enter the pipeline execution role ARN if you have previously created one, or we will create one for you []:  # Enterを押す
Enter the CloudFormation execution role ARN if you have previously created one, or we will create one for you []: # Enterを押す
Please enter the artifact bucket ARN for your Lambda function. If you do not have a bucket, we will create one for you []: # Enterを押す
Does your application contain any IMAGE type Lambda functions? [y/N]: y # yを押す（LambdaがImageを使う場合）
Please enter the ECR image repository ARN(s) for your Image type function(s).If you do not yet have a repository, we will create one for you []: # Enterを押す
```

### Github Actions の設定

```sh
Checking for existing stages...

2 stage(s) were detected, matching the template requirements. If these are incorrect, delete .aws-sam/pipeline/pipelineconfig.toml and rerun

This template configures a pipeline that deploys a serverless application to a testing and a production stage.

What is the GitHub secret name for pipeline user account access key ID? [AWS_ACCESS_KEY_ID]: # Github Actionsに設定したSecretsの名前に合わせる
What is the GitHub Secret name for pipeline user account access key secret? [AWS_SECRET_ACCESS_KEY]: # Github Actionsに設定したSecretsの名前に合わせる
```

Github Actions の secret name については設定した Secrets の名前に合わせます。

```sh
What is the git branch used for production deployments? [main]: # mainブランチを使うならそのままEnter
What is the template file path? [template.yaml]: # template.yamlを使うならそのままEnter
```

他にもブランチ名なども確認されます。変える必要がなければ Enter で進めていきます。

```sh
Here are the stage configuration names detected in .aws-sam/pipeline/pipelineconfig.toml:
        1 - dev
        2 - prod
Select an index or enter the stage 1's configuration name (as provided during the bootstrapping): 1
What is the sam application stack name for stage 1?: sam-app-dev
```

最後に stage の順番と CloudFormation の Stack Name について尋ねられます。

この例では`sam-app-dev`としました。

prod についても同様にそれぞれ `2`、`sam-app-prod` と回答します。

```
Successfully created the pipeline configuration file(s):
        - .github/workflows/pipeline.yaml
```

これで完了し、Github Actions の設定ファイル `.github/workflows/pipeline.yaml` が生成されます。

`.aws-sam/pipeline/pipelineconfig.toml` も作られ、ソースコードはだいたいこのようになっています。

```
.
├── .aws-sam
│   ├── build.toml
│   └── pipeline
│       └── pipelineconfig.toml
├── .github
│   └── workflows
│       └── pipeline.yaml
├── .gitignore
├── README.md
├── samconfig.toml
├── src
│   ├── Dockerfile
│   └── app.py
└── template.yaml
```

## 参考

https://aws.amazon.com/jp/blogs/compute/introducing-aws-sam-pipelines-automatically-generate-deployment-pipelines-for-serverless-applications/
