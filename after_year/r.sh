if [ "$1" == "" ]; then
  pdflatex article.tex  
elif [ "$1" == "clear" ]; then
  rm *.log
  rm *.aux
  rm *.pdf
  rm *.backup
else
  echo "usage: ./r.sh [clear]"
fi
