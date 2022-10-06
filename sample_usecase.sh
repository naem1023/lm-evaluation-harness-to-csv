steps=('300K' '312K' '314K' '315K' '316K' '317K' '318K' '319K' '320K' )

for step in "${steps[@]}" ; do
    python make_csv.py --base ../logs --model polyglot-ko-5.8b --step $step
done