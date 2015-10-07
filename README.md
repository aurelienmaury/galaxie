# Galaxie

Prerequisites

* pip aiml pyaudio

brew cmu-pocketsphinx
+ dl les acoustic models french


* espeak (brew, ..)
* sox (brew, ..)
* mbrola voices (http://tcts.fpms.ac.be/synthesis/mbrola.html)


copy de backup:

sphinx_fe -argfile
    fr-fr/feat.params
    -samprate 16000
    -c bonjour.fileids -di . -do . -ei wav -eo mfc -mswav yes

pocketsphinx_mdef_convert -text fr-fr/mdef fr-fr/mdef.txt

bw -hmmdir fr-fr -moddeffn fr-fr/mdef.txt -ts2cbfn .cont. -feat 1s_c_d_dd -cmn current -agc none -dictfn fr-fr.dic  -ctlfn bonjour.fileids  -lsnfn transcription_aa -accumdir .


map_adapt \
    -moddeffn fr-fr/mdef.txt \
    -ts2cbfn .ptm. \
    -meanfn fr-fr/means \
    -varfn fr-fr/variances \
    -mixwfn fr-fr/mixture_weights \
    -tmatfn fr-fr/transition_matrices \
    -accumdir . \
    -mapmeanfn fr-fr-adapt/means \
    -mapvarfn fr-fr-adapt/variances \
    -mapmixwfn fr-fr-adapt/mixture_weights \
    -maptmatfn fr-fr-adapt/transition_matrices


   /usr/local/lib/python2.7/site-packages

   sox msg0000.wav --bits 16 --encoding signed-integer --endian little msg0001.raw


