### istruzioni per convertire e mettere in cloud i file HIS di HoKaWo.

* dal pc windows aprire WINSCP (cygno@192.168.1.143) e mettere i file HIS nel folder /media/cygno/hroot/WIN/
* i file saranno automaticamente trasformati in CYGNO root histograms e inviati in cloud
* WARNING: i file si devono ncessariamente chimare **RunXXXXX.HIS** con la **R** maiuscola **5 cifre** e **HIS** maiuscolo!



#### OLD (ma sepre valido)

* aprire minio https://minio.cloud.infn.it/minio/ e mettere nel folder  sotto cygno-analysis/hroot (o dove si preferisce)
* collegarsi alla cloud https://notebook.cygno.cloud.infn.it:8888/ e far partire un container (anche con poca memoria) 
* una volta partito aprire un terminale (in alto a destra) e eseguire il comando:

        cygno_his2root -d /workarea/cloud-storage/cygno-analysis/hroot (-d cancella i file HIS dopo la conversione)
        o
        cygno_his2root -d -f /workarea/cloud-storage/cygno-analysis/hroot/RunXXXXX.HIS (per il singolo file)
  
* se il comando non e' dispobile instllare le librerie 

        pip install git+https://github.com/gmazzitelli/cygno_repo.git

* per spostarli nel foledr data lo devono fare Eamanule, Giulia o Giovanni

### processi ###

        nohup ~/DAQ/offline/hroot2cloud_loop.sh  > /media/cygno/hroot/hroot2cloud_loop.log 2>&1 &

