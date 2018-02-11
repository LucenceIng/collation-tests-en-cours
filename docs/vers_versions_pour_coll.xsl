<?xml version="1.0" encoding="UTF-8"?>
<!-- fichier pour passer de la version de travail à version pour collation-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="tei" version="2.0">
    
    <!-- génération de la sortie -->
    <xsl:output method="xml" version="1.0" indent="yes" omit-xml-declaration="yes" encoding="UTF-8"/>
    
    <xsl:strip-space elements="*"/>
    <xsl:template match="/">
        <xsl:element name="text">
            <xsl:variable name="val">
                <xsl:choose>
                    <xsl:when test="//tei:bibl[@xml:id][parent::tei:p]">
                        <xsl:value-of select="//tei:bibl/@xml:id"/>
                    </xsl:when>
                    <xsl:when test="//tei:idno[@xml:id][parent::tei:bibl]">
                        <xsl:value-of select="//tei:idno/@xml:id"/>
                    </xsl:when>
                </xsl:choose>
            </xsl:variable>
            <xsl:attribute name="id">
                <xsl:value-of select="$val"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
   
   <!-- on enlève le header -->
    <xsl:template match="*[ancestor::tei:teiHeader]"/>
    
    <!-- on enlève les div out : on ne veut garder que les mots et la structuration en paragraphes -->
    
    <xsl:template match="tei:head"/>
    
    <xsl:template match="tei:div[@rend='out']"/>
    
    
    <!-- on crée des p avec les n  -->
  
    <xsl:template match="tei:p[not(ancestor::tei:teiHeader)]">
            <xsl:element name="p">
                    <xsl:attribute name="n">
                        <xsl:value-of select="@n"/>
                    </xsl:attribute> 
                <xsl:apply-templates/>
            </xsl:element>
    </xsl:template>

   
    <!-- on reprend les mots -->
    <xsl:template match="tei:w">
        <xsl:element name="w">
            <xsl:attribute name="xml:id">
                <xsl:value-of select="@xml:id"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

      

</xsl:stylesheet>