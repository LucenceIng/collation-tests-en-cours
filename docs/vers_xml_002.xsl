<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <!-- vers xml 002 -->
    <!-- juste avec les lemmes pour le moment -->
    <xsl:output method="xml" encoding="utf-8" indent="yes" />
    <xsl:strip-space elements="*"/>
    
    <xsl:template match="root">
        <xsl:variable name="id">
            <xsl:value-of select="descendant::id/substring(text(), 1, 2)"/>
        </xsl:variable>               
                <xsl:text>{
        "witnesses" : [
        {
        "id" : "A",
        "tokens" : [</xsl:text>
                <xsl:apply-templates/>
               
                 
               <xsl:text>]
                    }, 
                    {
                    "id" : "B",
                    "tokens" : [</xsl:text>
                <xsl:for-each select="document('MF_deCSV_002.xml')/root/row">
                    <xsl:variable name="positionez">
                        <xsl:number count="row" from="root" level="any"/>
                    </xsl:variable>
                    <xsl:variable name="dernierez">
                        <xsl:for-each select="parent::root">
                            <xsl:value-of select="sum(count(child::row))"/>
                        </xsl:for-each>
                    </xsl:variable>
                    <xsl:choose>
                        <xsl:when test=".[$positionez=$dernierez]">
                            <xsl:text>{
        "-xml:id": "</xsl:text><xsl:value-of select="child::id"/><xsl:text>",
        "lemme" : "</xsl:text><xsl:value-of select="child::LEMME"/><xsl:text>",
        "t": "</xsl:text><xsl:value-of select="child::token"/><xsl:text> "
        }</xsl:text>     
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>{
        "-xml:id": "</xsl:text><xsl:value-of select="child::id"/><xsl:text>",
        "lemme" : "</xsl:text><xsl:value-of select="child::LEMME"/><xsl:text>",
        "t": "</xsl:text><xsl:value-of select="child::token"/><xsl:text> "
        },</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:for-each>   
                <xsl:text>]
            }
        ]
    }</xsl:text>
        <!-- création du docs qui contient la version pour collationner au niveau des lemmes -->
        <xsl:result-document href="002_lemmes.json" output-version="text" encoding="utf-8">
            <xsl:text>{
        "witnesses" : [
        {
        "id" : "A",
        "tokens" : [</xsl:text>
            <xsl:apply-templates mode="docs"/> 
            <xsl:text>]
                    }, 
                    {
                    "id" : "B",
                    "tokens" : [</xsl:text>
            <xsl:for-each select="document('MF_deCSV_002.xml')/root/row">
                <xsl:variable name="positionez">
                    <xsl:number count="row" from="root" level="any"/>
                </xsl:variable>
                <xsl:variable name="dernierez">
                    <xsl:for-each select="parent::root">
                        <xsl:value-of select="sum(count(child::row))"/>
                    </xsl:for-each>
                </xsl:variable>
                <xsl:choose>
                    <xsl:when test=".[$positionez=$dernierez]">
                        <xsl:text>{
        "-xml:id": "</xsl:text><xsl:value-of select="child::id"/><xsl:text>",
        "forme" : "</xsl:text><xsl:value-of select="child::token"/><xsl:text>",
        "t": "</xsl:text><xsl:value-of select="child::LEMME"/><xsl:text> "
        }</xsl:text>     
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>{
        "-xml:id": "</xsl:text><xsl:value-of select="child::id"/><xsl:text>",
        "forme" : "</xsl:text><xsl:value-of select="child::token"/><xsl:text>",
        "t": "</xsl:text><xsl:value-of select="child::LEMME"/><xsl:text> "
        },</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>            
            <xsl:text>]
            }
        ]
    }</xsl:text>            
        </xsl:result-document>  
        <!-- création du doc juste avec les lemmes -->
        <xsl:result-document href="002_QUE_lemmes.json" output-version="text" encoding="utf-8">
            <xsl:text>{
        "witnesses" : [
        {
        "id" : "A",
        "tokens" : [</xsl:text>
            <xsl:apply-templates mode="lemmes"/> 
            <xsl:text>]
                    }, 
                    {
                    "id" : "B",
                    "tokens" : [</xsl:text>
            <xsl:for-each select="document('MF_deCSV_002.xml')/root/row">
                <xsl:variable name="positionez">
                    <xsl:number count="row" from="root" level="any"/>
                </xsl:variable>
                <xsl:variable name="dernierez">
                    <xsl:for-each select="parent::root">
                        <xsl:value-of select="sum(count(child::row))"/>
                    </xsl:for-each>
                </xsl:variable>
                <xsl:choose>
                    <xsl:when test=".[$positionez=$dernierez]">
                        <xsl:text>{
        "t": "</xsl:text><xsl:value-of select="child::LEMME"/><xsl:text> "
        }</xsl:text>     
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>{
        "t": "</xsl:text><xsl:value-of select="child::LEMME"/><xsl:text> "
        },</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>            
            <xsl:text>]
            }
        ]
    }</xsl:text>            
        </xsl:result-document>
    </xsl:template>
    
    <!-- sur les row, pour la version qui ne contient que les lemmes -->
    <xsl:template match="row" mode="lemmes">
        <xsl:variable name="position">
            <xsl:number count="row" from="root" level="any"/>
        </xsl:variable>
        <xsl:variable name="dernier">
            <xsl:for-each select="parent::root">
                <xsl:value-of select="sum(count(child::row))"/>
            </xsl:for-each>
        </xsl:variable>
        <xsl:choose>
            <xsl:when test=".[$position=$dernier]">
                <xsl:text>{     
              "t": "</xsl:text><xsl:value-of select="child::LEMME"/><xsl:text>"
            }
              </xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>{
        "t": "</xsl:text><xsl:value-of select="child::LEMME"/><xsl:text> "
        },
        </xsl:text> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!-- sur les row, pour la version qui va collationner au niveau des lemmes -->
    <xsl:template match="row" mode="docs">
        <xsl:variable name="position">
            <xsl:number count="row" from="root" level="any"/>
        </xsl:variable>
        <xsl:variable name="dernier">
            <xsl:for-each select="parent::root">
                <xsl:value-of select="sum(count(child::row))"/>
            </xsl:for-each>
        </xsl:variable>
        <xsl:choose>
            <xsl:when test=".[$position=$dernier]">
                <xsl:text>{"-xml:id": "</xsl:text><xsl:value-of select="child::id"/><xsl:text>",
              "forme" : "</xsl:text><xsl:value-of select="child::token"/><xsl:text>",      
              "t": "</xsl:text><xsl:value-of select="child::LEMME"/><xsl:text> "
            }
              </xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>{
        "-xml:id": "</xsl:text><xsl:value-of select="child::id"/><xsl:text>",
        "forme" : "</xsl:text><xsl:value-of select="child::token"/><xsl:text>",
        "t": "</xsl:text><xsl:value-of select="child::LEMME"/><xsl:text> "
        },
        </xsl:text> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- sur les row, pour la version qui collationne au niveau des formes-->
    <xsl:template match="row">        
        <xsl:variable name="position">
            <xsl:number count="row" from="root" level="any"/>
        </xsl:variable>
        <xsl:variable name="dernier">
            <xsl:for-each select="parent::root">
                <xsl:value-of select="sum(count(child::row))"/>
            </xsl:for-each>
        </xsl:variable>
        <xsl:choose>
            <xsl:when test=".[$position=$dernier]">
                <xsl:text>{"-xml:id": "</xsl:text><xsl:value-of select="child::id"/><xsl:text>",
              "lemme" : "</xsl:text><xsl:value-of select="child::LEMME"/><xsl:text>",      
              "t": "</xsl:text><xsl:value-of select="child::token"/><xsl:text> "
            }
              </xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>{
        "-xml:id": "</xsl:text><xsl:value-of select="child::id"/><xsl:text>",
        "lemme" : "</xsl:text><xsl:value-of select="child::LEMME"/><xsl:text>",
        "t": "</xsl:text><xsl:value-of select="child::token"/><xsl:text> "
        },
        </xsl:text> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
   
      
</xsl:stylesheet>