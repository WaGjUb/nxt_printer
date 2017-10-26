#!/bin/bash

pictureFile="00000002.png"
bmpFile="face.bmp"
facePosFile="face.txt"
svgFile="face.svg"
outfile="lines.txt"
tempFile="/tmp/asdfg"

declare -a facePos

function takePic () {
    mplayer  -vo png -frames 2 tv:// > /dev/null 2> /dev/null
}

function detectFace(){
    ./facedetect/facedetect --biggest $pictureFile > $facePosFile
    facePos=($(cat $facePosFile)) #x y width heigth
}

function crop(){
    convert $pictureFile \
	    -crop \
	    "${facePos[3]}x${facePos[2]}+${facePos[0]}+${facePos[1]}" \
	    $bmpFile
    convert -colorspace GRAY $bmpFile $tempFile
    convert -gaussian-blur 5x5 $tempFile $tempFile
    convert -threshold 26500 $tempFile $bmpFile
}

function trace(){
    potrace --svg -z white -u 2 -a 0 -O 100 -t 100 --flat $bmpFile -o $svgFile
}

function svg2text(entrada, out){
    cat $entrada | \
	tr -d '\n' | \
	awk 'BEGIN{RS=">"} /^.*<path d=".*/{print $0} ' | \
	tr -d '<pathd="/' | \
	awk 'BEGIN{FS="z"}{for (i=0; i<NF; i++) print $i}' \
	    > $out
}

main(){
    echo "Olha o passarinho !"
    takePic
    # xdg-open $pictureFile &	

    echo "Tem algém ai?"
    detectFace

    echo ${facePos[@]}
    if [ ${facePos[@]} == 0 ]
    then
    	echo "Não encontrei ninguem :("
    	exit 1
    else
    	echo "Encontrei Alguem !"
    fi

    echo "Foco na pessoa !"
    crop
    xdg-open $bmpFile &

    echo "hora de desenhar"
    trace
    xdg-open $svgFile &

    echo "svg"
    svg2text
    cat $outfile
}

#main
export svg2text
