<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    xmlns:cx="http://interedition.eu/collatex/ns/1.0"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0"
    version="2.0">
    
    <xsl:output method="xml" indent="yes" omit-xml-declaration="no" encoding="UTF-8"/>
    
   <!-- <xsl:template match="tei:rdg">
        <xsl:variable name="valAo">
            <xsl:value-of select=".[@wit='w1']"/>
        </xsl:variable>
        <xsl:variable name="valEz">
            <xsl:value-of select=".[@wit='w2']"/>
        </xsl:variable>
        <xsl:variable name="mot">
            <xsl:for-each select="document('occ_presence.xml')/root/row[child::Ez=0]"> 
                    <xsl:value-of select="child::word"/>
                
            </xsl:for-each> 
        </xsl:variable> -->
     
       <!-- <xsl:choose>
            <xsl:when test="$valAo[contains($test, $mot)]">
                <xsl:element name="rdg">
                <xsl:value-of select="$valAo"/>
            </xsl:element></xsl:when>
        </xsl:choose>-->
 <!--       <xsl:for-each select="$valAo">
            <xsl:choose>
                <xsl:when test="contains(., $mot )">
                    <xsl:value-of select="$valAo"/>
                </xsl:when>
            </xsl:choose>
        </xsl:for-each> -->
        
      <!-- <xsl:choose>
            <xsl:when test="$valAo[contains(., $mot)]">
                <xsl:value-of select="$mot"/>     
            </xsl:when>
        </xsl:choose> -->
        
        
       
        
    
    
 <!--  <xsl:template name="pmot">
        <xsl:variable name="mot">
            <xsl:for-each select="document('occ_presence.xml')/root/row">
            <xsl:choose>
                <xsl:when test="child::Ez= 0">
                <xsl:value-of select="child::word"/>
            </xsl:when>
            </xsl:choose>
        </xsl:for-each>            
        </xsl:variable>
   </xsl:template> -->
   
     <!--       <xsl:variable name="aoVal">
                <xsl:for-each select="document('sortie_1.xml')/cx:apparatus/tei:app/tei:rdg[@wit='w1']"> -->
                <!--    <xsl:choose><xsl:when test="document('sortie_1.xml')/cx:apparatus/tei:app/tei:rdg[@wit='w1'][contains(., $mott)]" >-->
    <!--     <xsl:value-of select="."/>
                    </xsl:when>
                    </xsl:choose>-->
                
    <!--  </xsl:for-each>   <xsl:for-each select="document('sortie_1.xml')/cx:apparatus/tei:app/tei:rdg[@wit='w1'][contains(., $mott)]">
                <xsl:value-of select="."/>
                </xsl:for-each>
            </xsl:variable> </xsl:variable>-->
      <!--  <xsl:variable name="ezVal">
            <xsl:for-each select="document('sortie_1.xml')/cx:apparatus/tei:app/tei:rdg[@wit='w2'][parent::tei:app/child::tei:rdg[contains(., $mott)]]">
                <xsl:value-of select="."/>
            </xsl:for-each>
        </xsl:variable> -->
        
        <xsl:template match="tei:rdg">
            <xsl:variable name="mot">
                <xsl:for-each select="document('occ_presence.xml')/root/row/word[parent::word/child::Ez=0]">
                  <xsl:value-of select="."/>
                </xsl:for-each>            
            </xsl:variable>  
       <xsl:variable name="aoVal">
                <xsl:for-each select=".[@wit='w1']"> 
             <xsl:value-of select="."/>
                </xsl:for-each>
       </xsl:variable>
      <xsl:variable name="aoCont">
              <xsl:for-each select="tokenize($aoVal, '\s+')">
                  <xsl:value-of select="."/>
             </xsl:for-each>        
      </xsl:variable>
            <xsl:value-of select="$aoCont"/>
            
            <!--<xsl:variable name="aoCont">
                <xsl:for-each select="contains($aoVal, $mot)">
                    <xsl:value-of select="$aoVal[contains($aoVal, $mot)]"/>
                </xsl:for-each>
            </xsl:variable>-->
            <!--<xsl:variable name="test">
                <xsl:choose>
                    <xsl:when test="$aoCont=$mot">
                        <xsl:value-of select="$aoCont"/>
                    </xsl:when>
                </xsl:choose>
            </xsl:variable>-->
            <!--<xsl:for-each select="$aoVal">
                <xsl:value-of select="$aoCont"/>
            </xsl:for-each>-->
            <xsl:for-each select="contains($aoVal, $mot)">
                <xsl:if test="$aoCont=$mot">
                   <!-- <xsl:choose>
                        <xsl:when test="contains(., $test)">-->
                <xsl:variable name="egal">
                    <xsl:value-of select="$aoCont"/>
                </xsl:variable>
                    <xsl:element name="w"> 
                    <xsl:attribute name="type">
                        <xsl:text>aexam</xsl:text>
                    </xsl:attribute>
                    <xsl:value-of select="$egal"/>
                    </xsl:element> 
                      <xsl:element name="app">
                    <xsl:element name="rdg">
                        <xsl:attribute name="wit"><xsl:text>#Ao</xsl:text></xsl:attribute>
                        <xsl:value-of select="$aoVal"/> 
                    </xsl:element>
                        </xsl:element><!--</xsl:when></xsl:choose>--></xsl:if></xsl:for-each>
            
                
        </xsl:template>
                <!--    <xsl:element name="rdg">
                        <xsl:attribute name="wit"><xsl:text>#Ez</xsl:text></xsl:attribute> 
                        <xsl:value-of select="following::tei:rdg[@wit='w2']"/>
                    </xsl:element> -->
         <!--       </xsl:element> 
               </xsl:for-each>  
            </xsl:when>

        </xsl:choose>
        </xsl:for-each>
                
    </xsl:template>-->
            
          <!--  <xsl:variable name="ezVal">
                <xsl:value-of select="../tei:rdg[@wit='w2']"/>
            </xsl:variable> -->
        
            <!--  <xsl:element name="app">            
                <xsl:element name="rdg">
                    <xsl:attribute name="wit">
                        <xsl:text>#Ao</xsl:text>                            </xsl:attribute> 
           <xsl:text>Cou</xsl:text>
                </xsl:element>   -->
               <!--   <xsl:element name="rdg">
                    <xsl:attribute name="wit">
                        <xsl:text>#Ez</xsl:text>
                    </xsl:attribute>
                </xsl:element>
        </xsl:element>--> 
  
   
        
        
       <!-- <xsl:choose>
          <xsl:when test="document('sortie_1.xml')/cx:apparatus/tei:app/tei:rdg[@wit='w1'][contains(., $mott)]" >
             
              <! 
         <xsl:for-each select=".">
             <xsl:element name="app">            
                <xsl:element name="rdg">
                    <xsl:attribute name="wit">
                        <xsl:text>#Ao</xsl:text>                            </xsl:attribute> 
                    <xsl:value-of select="$aoVal"/>
                </xsl:element>   -->
               <!-- <xsl:element name="rdg">
                    <xsl:attribute name="wit">
                        <xsl:text>#Ez</xsl:text>
                    </xsl:attribute>
                    <xsl:value-of select="document('sortie_1.xml')/cx:apparatus/tei:app/tei:rdg[@wit='w2']"/>
                </xsl:element>
        </xsl:element>  </xsl:for-each> 
            </xsl:when>
        </xsl:choose>-->
        
<!--     <xsl:template match="tei:rdg"> 
            <xsl:variable name="mot">
                <xsl:choose> 
                    <xsl:when test="document('occ_presence.xml')/root/row/word[parent::row/child::Ez=0]">
                    <xsl:for-each select="document('occ_presence.xml')/root/row/word[parent::row/child::Ez=0]">
                        <xsl:value-of select="."/>                    
                </xsl:for-each> </xsl:when>
                </xsl:choose>
                
            </xsl:variable>
               
                    <xsl:value-of select="$mot"/>   
                    <xsl:if test="contains(., $mot)">
                        <xsl:element name="rdg">
                            <xsl:attribute name="wit">
                                <xsl:value-of select="@wit"/>
                                
                            </xsl:attribute>
                            <xsl:value-of select="."/>    
                        </xsl:element>
                    </xsl:if>
                    
            
                

        
        
     
       
    </xsl:template> -->

</xsl:stylesheet>