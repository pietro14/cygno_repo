### istruzioni per convertire e mettere in cloud i file HIS di HoKaWo.

* dal pc windows aprire WINSCP (cygno@192.168.1.143) e mettere i file HIS nel folder /media/cygno/hroot/WIN/
* i file saranno automaticamente trasformati in CYGNO root histograms e inviati in cloud
* WARNING: i file si devono ncessariamente chimare **RunXXXXX.HIS** con la **R** maiuscola **5 cifre** e **HIS** maiuscolo!


### processi (expert only) ###

contemporanememte sul PC del DAQ Linux deve girare il processo:

        nohup ~/DAQ/offline/hroot2cloud_loop.sh  > /media/cygno/hroot/hroot2cloud_loop.log 2>&1 &
        
il relativi log files sono conenuti nel folder:

        /media/cygno/hroot/

* daq_converted_HIS_err.log
* daq_converted_HIS.log - files HIS converted in ROOT
* daq_converted.log - files ROOT converted in HROOT
* daq_stored_HIS_err.log
* daq_stored_HIS.log - files HIS converted in ROOT stored on cloud
* daq_stored.log - files ROOT converted in HROOT stored on cloud
* his2hroot2cloud.log
* mid2hroot2cloud.log

tools, lo script **copyupload.sh** copia file da un disco locale per numero di run e li mette in cloud resattando le storie relative 

controllare un file  convertito o storato nei log:

        run=05790; grep $run daq_converted_HIS.log; grep $run daq_stored_HIS.log
        
resettare il log per un file convertito o storato:

        run=05790; cp *.log bck/ ; grep -v $run bck/daq_converted_HIS.log > daq_converted_HIS.log; grep -v $run bck/daq_stored_HIS.log > daq_stored_HIS.log


#### OLD (ma sepre valido)

* aprire minio https://minio.cloud.infn.it/minio/ e mettere nel folder  sotto cygno-analysis/hroot (o dove si preferisce)
* collegarsi alla cloud https://notebook.cygno.cloud.infn.it:8888/ e far partire un container (anche con poca memoria) 
* una volta partito aprire un terminale (in alto a destra) e eseguire il comando:

        cygno_his2root -d /workarea/cloud-storage/cygno-analysis/hroot (-d cancella i file HIS dopo la conversione)
        o
        cygno_his2root -d -f /workarea/cloud-storage/cygno-analysis/hroot/RunXXXXX.HIS (per il singolo file)
  
* se il comando non e' dispobile instllare le librerie 

        pip install git+https://github.com/gmazzitelli/cygno_repo.git

* per spostarli nel folder data lo devono fare Eamanule, Giulia o Giovanni
