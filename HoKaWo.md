### istruzioni per convertire e mettere in cloud i file HIS di HoKaWo.

* aprire minio https://minio.cloud.infn.it/minio/ e mettere nel folder  sotto cygno-analysis/hroot (o dove si preferisce)
* collegarsi alla cloud https://notebook.cygno.cloud.infn.it:8888/ e far partire un container (anche con poca memoria) 
* una volta partito aprire un terminale (in alto a destra) e eseguire il comando:

        cygno_his2root -d /workarea/cloud-storage/cygno-analysis/hroot (-d cancella i file HIS dopo la conversione)
  
* se il comando non e' dispobile instllare le librerie 

        pip install git+https://github.com/gmazzitelli/cygno_repo.git

