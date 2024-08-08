# kawa-python-scripts


## 1. Connect your workspace to GitHub

### 1.a Generate your personal access token

In order to connect your KAWA workspace to GitHub, you need to generate a Personal access token.
This can be done from the settings menu of your profile.
Go to: `developer settings > Tokens (classic)`

To access public repositories, make sure to set this scope: `public_repoAccess`


### 1.b Set up the connection between KAWA and GitHub

From KAWA, click on the settings icon (cog) at the bottom right of your screen.
Then click on `Source Control`.
There, you can fill the following values:

- Source control type: GitHub
- API Endpoint: If you are using the public Github servers, leave it to: https://api.github.com/. Otherwise use the URL to your company's repository.
- Access Token: Input the token you generated on the previous step
- Repo Name: You can put the entire URL of your repo: for example: https://github.com/kawa-analytics/kawa-toolkits. You can also specify the repository name by itself: `kawa-analytics/kawa-toolkits`.
- Branch Name: This is the name of the branch that KAWA will retrieve the scripts from. for example: `main`


## 2. Create Toolkits and Tools

In order for KAWA to execute your scripts, you have to declare them as KAWA tools, 
inside KAWA toolkits.





