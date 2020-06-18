<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:mf="http://example.com/mf"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs mf"
    version="2.0">

    <xsl:key name="phrase" match="phrase" use="@input"/>

    <xsl:function name="mf:replace-phrases" as="xs:string">
        <xsl:param name="phrases" as="element(phrase)*"/>
        <xsl:param name="text" as="xs:string"/>
        <xsl:choose>
            <xsl:when test="not($phrases)">
                <xsl:sequence select="$text"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:sequence select="mf:replace-phrases($phrases[position() gt 1], replace($text, $phrases[1]/@input, $phrases[1]/@output))"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:function>

    <xsl:param name="phrases">
        <phrases>
            <phrase input="  " output=" "/>
            <!-- harminisation caractères chiants et espacements -->
            <phrase input="(’|'|ʼ)" output="'"/>
            <phrase input="\s+?-\s+?" output="-"/>
            <phrase input="\( " output="("/>
            <phrase input=" \)" output=")"/>
            <!-- chiffres collés à la virgule -->
            <phrase input=",(\d) " output=", $1 "/>
            <!-- Harmonisation du type de document (L.a.s., D.s.) -->
            <phrase input="(L\.?\s?a\.?\s?s\.?)" output="L. a. s."/>
            <phrase input="(L\.?\s?s\.?)" output="L. s."/>
            <phrase input="(D\.?\s?a\.?\s?s\.?)" output="D. a. s"/>
            <phrase input="(D\.?\s?s\.?)" output="D. s."/>
            <phrase input="(P\.?\s?s\.?)" output="P. s."/>
            <phrase input="(P\.\s?a\.?\s?s\.?)" output="P. a. s."/>
            <phrase input=" Let " output=" Let. "/>
            <phrase input="^Let " output="Let. "/>
            <phrase input=" lig " output=" lig. "/>
            <phrase input=" lig," output=" lig.,"/>
            <phrase input=" lig;" output=" lig.;"/>
            <phrase input=" sig " output=" sig. "/>
            <phrase input=" sig," output=" sig.,"/>
            <phrase input=" sig;" output=" sig.;"/>
            <phrase input=" aut " output=" aut. "/>
            <phrase input=" aut," output=" aut.,"/>
            <phrase input=" aut;" output=" aut.;"/>
            <!-- correction des formats (in4, in8, infol en in-4) -->
            <phrase input=" in([0-9]+) " output=" in-$1 "/>
            <phrase input=" in([0-9]+)$" output=" in-$1"/>
            <phrase input=" in([0-9]+)\." output=" in-$1."/>
            <phrase input=" in([0-9]+)," output=" in-$1,"/>
            <phrase input=" in([0-9]+);" output=" in-$1;"/>
            <phrase input=" inf " output=" in-f. "/>
            <phrase input=" inf$" output=" in-f."/>
            <phrase input=" inf," output=" in-f.,"/>
            <phrase input=" inf\." output=" in-f."/>
            <phrase input=" infol " output=" in-fol. "/>
            <phrase input=" infol$" output=" in-fol."/>
            <phrase input=" infol," output=" in-fol.,"/>
            <phrase input=" infol\." output=" in-fol."/>
            <!-- ajout de point d'abréviation oublié -->
            <phrase input=" obl " output=" obl. "/>
            <phrase input=" obl," output=" obl.,"/>
            <phrase input=" obl;" output=" obl.;"/>
            <phrase input=" (\d+) p " output=" $1 p. "/>
            <phrase input=" Acad " output=" Acad. "/>
            <phrase input="l'Acad " output="l'Acad. "/>
            <phrase input=" fr " output=" fr. "/>
            <phrase input=" fr," output=" fr.,"/>
            <phrase input=" fr;" output=" fr.;"/>
            <phrase input=" pl " output=" pl. "/>
            <phrase input=" pl," output=" pl.,"/>
            <phrase input=" pl;" output=" pl.;"/>
            <!-- passage des prix avec centimes sous forme décimale -->
            <phrase input=" (\d)\s(\d\d?)$" output=" $1.$2"/>
            <phrase input=" (\d\d)\s(\d\d?)$" output=" $1.$2"/>
            <phrase input=" (\d\d\d)\s(\d\d?)$" output=" $1.$2"/>
            <!-- correction des fractions mal formées 1/ 2 en 1/2 -->
            <phrase input=" (\d)\s?/\s?(\d)" output=" $1/$2"/>

        </phrases>
    </xsl:param>

    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* , node()"/>
        </xsl:copy>
    </xsl:template>


    <xsl:template match="desc">
        <xsl:copy>
            <xsl:value-of select="mf:replace-phrases($phrases/phrases/phrase, .)"/>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>
