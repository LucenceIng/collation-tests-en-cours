<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:tei="http://www.tei-c.org/ns/1.0"
        xmlns:csv="csv:csv">
        <xsl:output method="text" encoding="utf-8" />
        <xsl:strip-space elements="*"/>
        
        <!-- fichier xsl pour transformation vers csv pour le par 2 pour tests sur collatex -->
        
        <!-- on enlève les données du header-->
        <xsl:template match="tei:teiHeader"/>
    
        <!-- on en lève les mots des heads de ez -->
        <xsl:template match="tei:head"/>
        
        <!-- on place le mot dans chaque colonne -->
        <xsl:template match="tei:w">
            <!-- pour le premier mot du par, on a besoin de créer l'en-tête du csv -->
            <xsl:variable name="place">
                <xsl:number count="tei:w" from="tei:p" level="any"/>
            </xsl:variable>
            <xsl:if test="$place=1">
                <xsl:text>id</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>token</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>LEMME</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>PPOS</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>MODE</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>TEMPS</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>PERS.</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>NOMB.</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>GENRE</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>CAS</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>DEGRE</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>PPOSM</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>flectM</xsl:text>
                <xsl:text>;</xsl:text>
                <xsl:text>REMARQUES</xsl:text>
                <xsl:text>&#xa;</xsl:text>
            </xsl:if>
            <!-- première colonne avec identifiant du mot -->
            <xsl:value-of select="@xml:id"/>
            <xsl:text>;</xsl:text>
            <!-- seconde colonne avec valeur du mot -->
            <xsl:value-of select="."/>
            <!-- retour à la ligne -->
            <xsl:text>&#xa;</xsl:text>  
        </xsl:template>
    
    <!-- on applique cela que sur le p 2 qui nous intéresse -->
    <xsl:template match="tei:p">
        <xsl:choose>
            <xsl:when test="@n='002'">
            <xsl:apply-templates/>   
        </xsl:when> 
        <xsl:otherwise/>
        </xsl:choose>
    </xsl:template>
    
        
    </xsl:stylesheet>
