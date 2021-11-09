### istruzioni per convertire e mettere in cloud i file HIS di HoKaWo.

* dal pc windows aprire winscp e mettere i file HIS nel folder /media/cygno/hroot/WIN/
* i file saranno automaticamente trasformati in CYGNO root histograms e inviati in cloud
* WARNING: i file si devono ncessariamente chimare **RunXXXXX.HIS**



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

### appunti di viaggio (CERN ROOT reistallazione su iMac intel e istallazione su Air M1 attarverso homebrew):

intel:

        brew uninstall root
        brew uninstall --ignore-dependencies python3
        ls -l /usr/local/bin/python* (per controllare che abbai rimosso i link)
        brew list python
        pip3 install jupyter
        brew link --overwrite gcc (per il proiblema del ImportError: dlopen(/Users/rock/laugh/laugh-finder/python-training/laughenv/lib/python3.6/site-packages/scipy/linalg/_fblas.cpython-36m-darwin.so, 2): Symbol not found: ___addtf3)

M1:

        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
        brew install python
        brew install root
        pip3 install jupyter
        rehash (zsh e' duro d'orecchie)

il problema e' che dalla 3.7 non esiste piu' root_numpy (vedi https://github.com/scikit-hep/root_numpy/tree/master/root_numpy)

per far partire juputer notebook usare 

        python3 -m notebook (o jupyer notebook come al solito)
