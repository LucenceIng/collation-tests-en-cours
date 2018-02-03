<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    xmlns:cx="http://interedition.eu/collatex/ns/1.0"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0"
    version="2.0">
    
  <!-- <xsl:param name="valMot">
        <xsl:for-each select="cx:apparatus/tei:app/tei:rdg[@wit='w1']">
            <xsl:for-each select="tokenize(., '\s+')"><xsl:value-of select="."/></xsl:for-each>
        </xsl:for-each>
    </xsl:param>-->
    <!--<xsl:param name="valMotListe" as="xs:string+">
        <xsl:for-each select="document('occ_presence.xml')/root/row">
            <xsl:value-of select="child::word[parent::row/child::Ez='0']"/>
            <xsl:text> </xsl:text>
        </xsl:for-each>
    </xsl:param>-->
  <!-- <xsl:param name="egal">
        <xsl:for-each select="$valMot">
 
            <xsl:if test=".=tokenize($valMotListe, '\s+')">
                   <xsl:value-of select="."/>
               </xsl:if>
           
        </xsl:for-each>
    </xsl:param>-->
    
    <xsl:template match="/">
        <!--<xsl:for-each select="$valMotListe">
            <xsl:value-of select="."/>
            <xsl:text>&#xA;</xsl:text>
        </xsl:for-each>-->
        <!--<xsl:apply-templates select="descendant::tei:rdg[@wit='w1']"/>-->
        <xsl:apply-templates select="descendant::tei:app"/>
    </xsl:template>
    
    <xsl:template match="tei:app">
        <!--<xsl:for-each select="tei:rdg[1]/tei:w">
            
            <xsl:if test=". = tei:rdg[2]/tei:w">
                <xsl:text></xsl:text>
            </xsl:if>
        </xsl:for-each>-->
        <xsl:variable name="rdg2" select="tei:rdg[2]"/>
        <xsl:for-each select="tokenize(tei:rdg[1], '\s+')">
            <xsl:choose>
                <xsl:when test=". = tokenize($rdg2, '\s+')">
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="."/>
                    <xsl:text> seulement dans 1</xsl:text>
                    <xsl:text>&#xA;</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
    </xsl:template>
    
    <!--<xsl:template match="tei:rdg[@wit='w1']">
        <!-\-<xsl:value-of select="$valMot"/>-\->
       <xsl:variable name="aoMot" as="xs:string+">
            <xsl:for-each select="tokenize(., '\s+')">
                <xsl:value-of select="."/>
            </xsl:for-each>
        </xsl:variable>
       <!-\-     <xsl:variable name="mot">
            <xsl:for-each select="document('occ_presence.xml')/root/row">
                <xsl:value-of select="child::word[parent::row/child::Ez='0'][.=$aoMot]"/>
            </xsl:for-each>
              
        </xsl:variable>-\->
       <xsl:variable name="egal" as="xs:string+">
    <xsl:for-each select="$aoMot">
        <xsl:choose><xsl:when test=". =$valMotListe">
            <xsl:value-of select="."/></xsl:when></xsl:choose>
    </xsl:for-each>
   
        </xsl:variable>
       <!-\- <xsl:element name="mot"><xsl:for-each select="$valMot">
            <xsl:value-of select="."/>
        </xsl:for-each></xsl:element>-\->
    <!-\-    <xsl:value-of select="$mot"/>-\->
        <!-\-<xsl:for-each select="."><xsl:value-of select="$egal"/></xsl:for-each>-\->
       <xsl:for-each select=".">
           <xsl:choose><xsl:when test="contains(., $egal)">
            <xsl:element name="w">
                <xsl:value-of select="$egal"/>
            </xsl:element>
            <xsl:element name="rdg">
                <xsl:value-of select="."/>
            </xsl:element>
        </xsl:when></xsl:choose></xsl:for-each>  </xsl:template>-->
</xsl:stylesheet>