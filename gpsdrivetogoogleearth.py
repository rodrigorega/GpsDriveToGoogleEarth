#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
GpsDriveToGoogleEarth 2.10pre4

This script exports APs from GpsDrive to Google Earth .kml

Based on: http://www.larsen-b.com/Article/212.html

Changelog:
    Now supports GpsDrive 2.10pre4 database.
    Accepts .kml output file as argument.
    Added unique icons to open, wpa and web WiFis.
    Deleted "&" char, unsupported by Google Earth .kml.
    Information balloon no shows ESSID, BSSID, security and GPS coords.
    Rewrote part of the code that gets WiFi type.
    Added GpsDrive Logo.
"""

import MySQLdb
import sys


def main():
    """ Main function """

    if len(sys.argv) >= 2:  # if we have input file
        funcion_escribe_kml()
    else:
        print "- Error: You must give a input .kml file"
        print "- example: python gpsdrivetogoogleearth.py ap-list.kml"


def funcion_escribe_kml():
    """ Read date from database and write output .kml file """

    DB = "geoinfo"  # default database name
    LOGIN = "gast"  # default login
    PASSWORD = "gast"  # default password

    cnx = MySQLdb.connect(db=DB, user=LOGIN, passwd=PASSWORD)
    cursor = cnx.cursor()

    cursor.execute("SELECT * from wlan order by essid")
    results = cursor.fetchall()

    print "Total APs: %s" % len(results)  # print total AP count

    f = open(sys.argv[1], 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://earth.google.com/kml/2.2">\n')
    f.write('  <Folder>\n')
    f.write('    <name>GpsDrive+Kismet wifis</name>\n')
    # By default folder is showed
    f.write('    <visibility>1</visibility>\n')
    # GpsDrive icon
    f.write('      <ScreenOverlay>\n')
    f.write('        <name>Info</name>\n')
    f.write('        <description>Wifi data</description>\n')
    f.write('        <visibility>1</visibility>\n')
    f.write('        <Icon>\n')
    f.write('          <href>https://raw.github.com/rodrigorega/GpsDriveToGoogleEarth/master/img/gpsdrivelogo.png</href>\n')
    f.write('        </Icon>\n')
    f.write('        <overlayXY x="0" y="-1" xunits="fraction" yunits="fraction"/>\n')
    f.write('        <screenXY x="0" y="0" xunits="fraction" yunits="fraction"/>\n')
    f.write('        <rotationXY x="0" y="0" xunits="fraction" yunits="fraction"/>\n')
    f.write('        <size x="0" y="0" xunits="fraction" yunits="fraction"/>\n')
    f.write('      </ScreenOverlay>')

    # write all APs to .kml file
    for line in results:
        name = line[6].replace('&', 'and')  # To  avoid Google Earth errors
        wep = line[8]
        lat = line[1]
        lon = line[2]
        mac = line[5]

        f.write('\n')
        f.write('   <Placemark>\n')
        f.write('     <name>%s</name>\n' % name)
        f.write('     <description>')
        f.write('       <![CDATA[ <table width="300"><tr><td>')
        f.write('         - EESID: %s\n <br />' % name)
        f.write('         - BBSID: %s\n <br />' % mac)
        tipo_ap = funcion_tipo_ap(wep)
        f.write('         - Security: %s\n <br />' % tipo_ap)
        f.write('         - GPS coords.: %s, %s\n <br />' % (lon, lat))
        f.write('         </td></tr></table> ]]>')
        f.write('     </description>\n')
        f.write('     <visibility>1</visibility>\n')

        tipo_ap = funcion_tipo_ap(wep)  # get AP type

        # Draw AP icon
        f.write('<Style>')
        f.write('<IconStyle>')
        f.write(' <Icon><href>https://raw.github.com/rodrigorega/GpsDriveToGoogleEarth/master/img/%s.png</href></Icon>\n' % tipo_ap)
        f.write('</IconStyle>')
        f.write('</Style>')
        f.write('     <Point><coordinates>%s,%s,45</coordinates></Point>\n' % (lon, lat))
        f.write('   </Placemark>\n')

    f.write('  </Folder>\n')
    f.write('</kml>')


def funcion_tipo_ap(codigo):
    """ Returns AP type (WPA, WEP or Open) """

    dic_tipo_ap = {  # Dictionary of known AP types
        0: 'open',
        2: 'wep',
        34: 'unk',
        98: 'wpa',
        226: 'wpa',
        234: 'wpa',
        706: 'wpa',
        738: 'wpa'
        }

    if codigo in dic_tipo_ap:
        tipo_ap = dic_tipo_ap[codigo]
    else:
        tipo_ap = 'unk'
    return tipo_ap


main()
