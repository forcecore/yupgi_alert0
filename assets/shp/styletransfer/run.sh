for f in in/nairon*.png ; do
    echo $f
    g=`basename "$f" .png`

    #for style in snow grass desert ; do
    for style in ultra ; do
        python3 -u neural_style_transfer.py \
            --iter=10 \
            --content_weight=0.0001 \
            --style_weight=5.0 \
            --tv_weight=1.0 \
            "$f" \
            "in/$style.png" \
            "$style.$g"
    done
done
