<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <!-- vers xml 002 -->
    <!-- juste avec les lemmes pour le moment -->
    <!-- depuis A et B. xml avec insertion des XML depuis CSV -->
    <!-- donc règles qui appellent que le p 2 -->
    <xsl:output method="xml" encoding="utf-8" indent="yes" omit-xml-declaration="yes" />
    <xsl:strip-space elements="*"/>
    
    <xsl:template match="text">
        <xsl:element name="text">
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="p[not(@n='002')]"/>
    
    <xsl:template match="p[@n='002']">
        <xsl:element name="p">
            <xsl:attribute name="n">
                <xsl:value-of select="@n"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="w">
        <xsl:variable name="idM">
            <xsl:value-of select="@xml:id"/>
        </xsl:variable>
        <xsl:variable name="idT">
                <xsl:value-of select="substring($idM, 1, 2)"/>              
        </xsl:variable>
        <xsl:variable name="lemme">
            <xsl:choose>
                <xsl:when test="$idT='Ao'">
                <xsl:value-of select="document('AF_deCSV_002.xml')/root/row/LEMME[parent::row/child::id=$idM]"/>
            </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="document('MF_deCSV_002.xml')/root/row/LEMME[parent::row/child::id=$idM]"/>  
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <xsl:element name="w">
            <xsl:attribute name="xml:id">
                <xsl:value-of select="@xml:id"/>
            </xsl:attribute>
            <xsl:attribute name="lemma">
                <xsl:value-of select="$lemme"/>
            </xsl:attribute>
            <xsl:value-of select="."/>            
        </xsl:element>
    </xsl:template>
             
</xsl:stylesheet>