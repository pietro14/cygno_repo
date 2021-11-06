### istruzioni per convertire e mettere in cloud i file HIS di HoKaWo.

* aprire minio https://minio.cloud.infn.it/minio/ e mettere nel folder  sotto cygno-analysis/tmp 
* collegarsi alla cloud https://notebook.cygno.cloud.infn.it:8888/ e far partire un container (anche con poca memoria) 
* una volta partito aprire un terminale e eseguire il comando:

        cygno_his2root /workarea/cloud-storage/cygno-analysis/tmp
  
* se il comando non e' dispobile istllare le librerie 

        pip install git+https://github.com/gmazzitelli/cygno_repo.git
