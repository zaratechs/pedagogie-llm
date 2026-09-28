 - git-b 
 - git remote add origin https://github.com/zaratechs/cv.git
 - git init
 - git remote add origin https://github.com/zaratechs/cv.git
 - git config --global --add safe.directory F:/cvm/8-Dev/Workspace/blog
 - git add .
 - git commit -m "Blog pédagogique Réda Hamza"
 - git push -u origin master
 -  git push origin
 -  git push --set-upstream origin master
 -  git remote add origin https://github.com/zaratechs/cv.git
 -   git push --set-upstream origin master


## git branch -M main
## git init
## git checkout -b projetScormFactory
###  Au besoin:  git config --global --add safe.directory F:/cvm/8-Dev/Workspace/competenceNum

- git add .
- git commit -m "Scorm Factory"
- git remote add origin https://github.com/zaratechs/Projets_P-dagogiques_IA.git
-  git push -u origin projetScormFactory

=========================================================================

Pour cloner une branche
git clone -b blog https://github.com/zaratechs/Projets_P-dagogiques_IA.git

Pour certifier que le dossier est safe!
 git config --global --add safe.directory F:/cvm/8-Dev/Workspace/revisionProgramme/backend

1. Renommer localement avec un nom intermédiaire
git branch -m revisionprogrammeBackend temp-branch-name

2. Renommer vers le bon nom (CamelCase)
git branch -m temp-branch-name RevisionProgrammeBackend

🔁 Ensuite côté GitHub (remote)

3. Pousser la nouvelle branche
git push origin RevisionProgrammeBackend

4. Supprimer l’ancienne branche distante
git push origin --delete revisionprogrammeBackend

5. Reconnecter le tracking
git push --set-upstream origin RevisionProgrammeBackend


Le “tracking”, c’est quoi ?

Quand tu fais :

git push --set-upstream origin RevisionProgrammeBackend

Tu dis à Git :

“Ma branche locale RevisionProgrammeBackend est liée à la branche distante origin/RevisionProgrammeBackend”

🔹 Pourquoi c’est important ?

Sans tracking :

À chaque push/pull, tu devras préciser :

git push origin RevisionProgrammeBackend
git pull origin RevisionProgrammeBackend

Avec tracking :

Tu peux juste faire :

git push
git pull

👉 Git sait automatiquement où envoyer et récupérer.

=============

Dès que vous poussez sur GitHub, voici ce qui se passe :

Votre git push origin main met à jour le dépôt GitHub.

GitHub envoie instantanément une notification à Vercel (via un webhook).

Vercel récupère le code, lance le build de production et met à jour votre site en ligne en quelques secondes (généralement 15 à 45 secondes).

Votre flux de travail au quotidien
À chaque fois que vous modifiez votre code en local :

Bash
git add .
git commit -m "Description de vos modifications"
git push origin main
C'est tout. Le site sur redahamza.ca ou trousse.redahamza.ca se met à jour tout seul.


==========================================================

…or create a new repository on the command line
echo "# tutoIAlocal" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/zaratechs/tutoIAlocal.git
git push -u origin main


…or push an existing repository from the command line
git remote add origin https://github.com/zaratechs/tutoIAlocal.git
git branch -M main
git push -u origin main


-----------------------------------------------------------------------

# 1. Supprimer complètement l'ancien remote "origin"
git remote remove origin

# 2. Lier le nouveau dépôt GitHub
git remote add origin https://github.com/zaratechs/programmeSciencesLettresArts.git

# 3. Vérifier que la nouvelle URL est bien active
git remote -v


git remote set-url origin https://github.com/zaratechs/conventionRH.git

gitmcp.io  gitingest  githubbox   gitreverse

moh4696/build-ai-agents-free

netsh wlan show profile "Bell378" key=clear



