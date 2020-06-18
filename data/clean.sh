#!/bin/bash
usage()
{
    echo "usage: <command> options:<d|f|h>"
    echo "   -h, --help               display help"
    echo "   -f, --filename           name of the file"
    echo "   -d, --directory          name of the directory (for multiple files)"
}
while getopts ":f:d:" opt; do
    case "${opt}" in
        #f | --filename)
        f )
            echo "processing a single file";
            f=${OPTARG}
            ;;
        d )
             echo "processing all files in directory";
             d=${OPTARG}
            ;;
        h | --help)
            usage
            exit
            ;;
        *)
            usage
            exit
            ;;
    esac
done

#testing if there is a filename correctly mentioned, otherwise exit
if [ -f "$f" ]
  then
    b=$(basename ${f} .xml)
    #Getting rid of TEI namespace
    sed -i "" 's/xmlns=\"http\:\/\/www\.tei-c\.org\/ns\/1\.0"//g' ${f};
    #Applying XSLT
    java -jar _transformation/saxon9he.jar -o:${b}_new.xml ${f} _transformation/cleanDesc.xsl;
    #Re-introducing TEI namespace
    sed -i "" 's/<TEI /<TEI xmlns=\"http\:\/\/www\.tei-c\.org\/ns\/1\.0\" /g' ${f};
    sed -i "" 's/<TEI /<TEI xmlns=\"http\:\/\/www\.tei-c\.org\/ns\/1\.0\" /g' ${b}_new.xml ;
    #Create/add to folder
    mkdir -p Data_clean;
    mv ${b}_new.xml Data_clean;
    exit;
else [ -d "$d" ]
    mkdir -p ${d}_clean;
    for f in ${d}/*.xml;
      do
      #if [[ "$f" != *\.xml ]]
      #then
        b=$(basename "$f" .xml)
        #Getting rid of TEI namespace
        sed -i "" 's/xmlns=\"http\:\/\/www\.tei-c\.org\/ns\/1\.0"//g' ${f};
        #Applying XSLT
        java -jar _transformation/saxon9he.jar -o:${b}_clean.xml ${f} _transformation/cleanDesc.xsl;
        #Re-introducing TEI namespace
        sed -i "" 's/<TEI /<TEI xmlns=\"http\:\/\/www\.tei-c\.org\/ns\/1\.0\" /g' ${f};
        sed -i "" 's/<TEI /<TEI xmlns=\"http\:\/\/www\.tei-c\.org\/ns\/1\.0\" /g' ${b}_clean.xml ;
        #Move to folder
        mv ${b}_clean.xml ${d}_clean;
      #fi
    done
fi

