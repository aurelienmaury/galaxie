#!/bin/sh

set -x
OLD_MODEL_DIR="$1-$(date +%Y%m%d%H%M)"
NEW_MODEL_DIR=$1
MODEL_NAME=$2
TRAINING_DIR=$3

SCRIPTPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PATH="$PATH:/usr/local/Cellar/cmu-sphinxtrain/HEAD/libexec/sphinxtrain/"

cp -R $NEW_MODEL_DIR $OLD_MODEL_DIR

cat $TRAINING_DIR/transcription | cut -d "(" -f2 | cut -d")" -f1 > $TRAINING_DIR/file_ids

cd $NEW_MODEL_DIR && sphinx_fe -argfile $MODEL_NAME/feat.params -samprate 16000 -c $TRAINING_DIR/file_ids -di $TRAINING_DIR -do . -ei wav -eo mfc -mswav yes

cd $NEW_MODEL_DIR && pocketsphinx_mdef_convert -text $MODEL_NAME/mdef $MODEL_NAME/mdef.txt

cd $NEW_MODEL_DIR && bw -hmmdir fr-fr -moddeffn $MODEL_NAME/mdef.txt -ts2cbfn .cont. -feat 1s_c_d_dd -cmn current -agc none -dictfn $MODEL_NAME.dic  -ctlfn $TRAINING_DIR/file_ids  -lsnfn $TRAINING_DIR/transcription -accumdir .

cd $NEW_MODEL_DIR && map_adapt \
    -moddeffn $MODEL_NAME/mdef.txt \
    -ts2cbfn .cont. \
    -meanfn $OLD_MODEL_DIR/$MODEL_NAME/means \
    -varfn $OLD_MODEL_DIR/$MODEL_NAME/variances \
    -mixwfn $OLD_MODEL_DIR/$MODEL_NAME/mixture_weights \
    -tmatfn $OLD_MODEL_DIR/$MODEL_NAME/transition_matrices \
    -accumdir . \
    -mapmeanfn $MODEL_NAME/means \
    -mapvarfn $MODEL_NAME/variances \
    -mapmixwfn $MODEL_NAME/mixture_weights \
    -maptmatfn $MODEL_NAME/transition_matrices

rm $NEW_MODEL_DIR/$MODEL_NAME/mdef.txt
rm $NEW_MODEL_DIR/*.mfc
rm $NEW_MODEL_DIR/*_counts
rm $TRAINING_DIR/file_ids