<?xml version="1.0" encoding="UTF-8"?>
<!--<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="no" encoding="UTF-8" omit-xml-declaration="yes"/>
    <xsl:template match="*|@*">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*"/>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="/*">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <!-\- insert a <w/> milestone before the first word -\->
            <w/>
            <xsl:apply-templates/>
        </xsl:copy>
    </xsl:template>
    <!-\- convert <add>, <sic>, and <crease> to milestones (and leave them that way)
             CUSTOMIZE HERE: add other elements that may span multiple word tokens
        -\->
    <xsl:template match="add | sic | crease ">
        <xsl:element name="{name()}">
            <xsl:attribute name="n">start</xsl:attribute>
        </xsl:element>
        <xsl:apply-templates/>
        <xsl:element name="{name()}">
            <xsl:attribute name="n">end</xsl:attribute>
        </xsl:element>
    </xsl:template>
    <xsl:template match="note"/>
    <xsl:template match="text()">
        <xsl:call-template name="whiteSpace">
            <xsl:with-param name="input" select="translate(.,'&#x0a;',' ')"/>
        </xsl:call-template>
    </xsl:template>
    <xsl:template name="whiteSpace">
        <xsl:param name="input"/>
        <xsl:choose>
            <xsl:when test="not(contains($input, ' '))">
                <xsl:value-of select="$input"/>
            </xsl:when>
            <xsl:when test="starts-with($input,' ')">
                <xsl:call-template name="whiteSpace">
                    <xsl:with-param name="input" select="substring($input,2)"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="substring-before($input, ' ')"/>
                <w/>
                <xsl:call-template name="whiteSpace">
                    <xsl:with-param name="input" select="substring-after($input,' ')"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>-->
<!--<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="xml" indent="no" omit-xml-declaration="yes"/>
    <xsl:template match="/*">
        <xsl:copy>
            <xsl:apply-templates select="w"/>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="w">
        <!-\- faking <xsl:for-each-group> as well as the "<<" and except" operators -\->
        <xsl:variable name="tooFar" select="following-sibling::w[1] | following-sibling::w[1]/following::node()"/>
        <w>
            <xsl:copy-of select="following-sibling::node()[count(. | $tooFar) != count($tooFar)]"/>
        </w>
    </xsl:template>-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="xml" indent="yes" omit-xml-declaration="yes"/>
    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="w">
        <!--<!-\- faking <xsl:for-each-group> as well as the "<<" and except" operators -\->
        <xsl:variable name="tooFar" select="following-sibling::w[1] | following-sibling::w[1]/following::node()"/>
        <w>
            <xsl:copy-of select="following-sibling::node()[count(. | $tooFar) != count($tooFar)]"/>
        </w>-->
        <xsl:element name="w">
            <xsl:attribute name="xml:id">
                <xsl:value-of select="@xml:id"/>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>
