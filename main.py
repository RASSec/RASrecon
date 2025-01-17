﻿#coding=utf-8
# __author__ = 'shuige'
# Full automatic scanning tool for Pentesters
# 1904521507[at]qq.com (http://github.com/rassec)
import os
import re
import sys
import time
import json
import requests
import argparse
import logging
from string import Template
from report_all import TEMPLATE_html
import subprocess
import webbrowser
import optparse
import platform

reload(sys)
sys.setdefaultencoding("utf-8")

subdomain_jiejie=[]
whatweb=[]
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
)

sysstr = platform.system()

'''
del txt files
waring wvs result report
'''
def system_vertify():
    if(sysstr =="Windows"):
        os.system("cls&&del *.txt&&del *.xml")
        os.system("cd report &&del *.html *.txt")
        os.system("mkdir d:\wwwscanresult")
        print "wvs saved d:\wwwscanresult"
        time.sleep(1)
    else:
        print "only for windows!"
        sys.exit(1)


class FlushFile(object):
    """Write-only flushing wrapper for file-type objects."""
    def __init__(self, f):
        self.f = f
    def write(self, x):
        self.f.write(x)
        self.f.flush()

sys.stdout = FlushFile(sys.__stdout__)

def save_result(filename, args):
    try:
        fd = open(filename, 'w')
        json.dump(args, fd, indent=4)
    finally:
        fd.close()

'''
    subdomainbuter interface 1
'''
def sub_doman_jiejie(url_domain):
    popen = subprocess.Popen(['python', 'subDomainsBrute.py', '{name}'.format(name=url_domain),'-t 150'], stdout = subprocess.PIPE)
    while True:
        next_line = popen.stdout.readline()
        if next_line == '' and popen.poll() != None:
            break
        '''sys.stdout.write(next_line)'''
        sys.stdout.write(next_line)
        subdomain_jiejie.append(next_line)
    return list(set(subdomain_jiejie))


'''
whatweb

'''
def sub_doman_what():

    popen = subprocess.Popen(['python', 'whatweb.py'], stdout = subprocess.PIPE)
    while True:
        next_line = popen.stdout.readline()
        if next_line == '' and popen.poll() != None:
            break
        '''sys.stdout.write(next_line)'''
        sys.stdout.write(next_line)
        whatweb.append(next_line)
    whatwebff=open('report/whatweb.html','w')
    for x in whatweb:
        whatwebff.write(str(x)+ "<br>")
    whatwebff.close()





'''
 wydomain interface 2
'''
def sub_domain_wydomain(url_domain):
    popen = subprocess.Popen(['python', 'wydomain.py', '-d','{name}'.format(name=url_domain)], stdout = subprocess.PIPE)
    while True:
        next_line = popen.stdout.readline()
        if next_line == '' and popen.poll() != None:
            break
        sys.stdout.write(next_line)

'''
sublistdir interface 3
'''
def sub_domain_sublist(url_domain):
    popen = subprocess.Popen(['python', 'sublist3r.py', '-d','{name}'.format(name=url_domain),'-o {name}_sublistdir.txt'.format(name=url_domain)], stdout = subprocess.PIPE)
    while True:
        next_line = popen.stdout.readline()
        if next_line == '' and popen.poll() != None:
            break
        sys.stdout.write(next_line)

'''
fourth interface
google and bing
'''
def sub_domain_gxfr(url_domain):
    popen = subprocess.Popen(['python', 'gxfr.py','--bxfr','--dns-lookup','-o','--domain','{name}'.format(name=url_domain)], stdout = subprocess.PIPE)
    while True:
        next_line = popen.stdout.readline()
        if next_line == '' and popen.poll() != None:
            break
        sys.stdout.write(next_line)
"""
make result outfile reqult.txt all_domain
"""
def make_domain():
    os.system("copy *.txt all_reqult.log && del *.txt")
    print("[+]del *txt\ncopy txt\n")
    list_domain = []
    f = open("all_reqult.log", "r")
    while True:
        line = f.readline()
        if '.' in line:
            line = line.strip('').strip('\r').strip('"').strip(',').strip('            \r\r\n",').strip('\r\r\n')
        print line
        if line:
            pass    # do something here
            line=line.strip()
            if '.' in line and '[S]' in line:
                list_domain.append(line.split('\t')[2])
            else:
                if '.' in line and '[R]' in line:
                    list_domain.append(line.split('\t')[3])
                else:
                    if '.' in line:
                        list_domain.append(line.replace(' ', '').strip("\\r").replace("\\r\\r\\n",''))
                        #print line
        else:
            break
    f.close()
    os.system("del all_reqult.log")
    list_domain = list(set(( list_domain )))
    print list_domain,len(list_domain)
    with open('result.txt','w') as outfile:
        outfile.write('\n'.join(list_domain))
    fopen1 = open('report/result.txt','w')
    fopen1.write('\n'.join(list_domain))
    fopen1.close()

'''
first whois scan
[\s\S]*
'''
def sub_domain_whois(url_domain):
    um=[]
    a1=requests.get("http://whois.alexa.cn/%s" %(url_domain))
    if 'Registration' not in a1.text:
        print 'whois error'
    else:
        out_result=re.findall(r'<pre class="whois-detail">([\s\S]*)</pre>', a1.text.encode("GBK",'ignore'))
        out_result_register=re.findall(r'http://(.*?)"', a1.text.encode("GBK",'ignore'))
        for x in out_result_register:
            if 'reverse_registrant/?query=' in x:
                um.append(x)
                break
        for x in out_result_register:
            if 'reverse_mail/?query=' in x:
                um.append(x)
                break
        print um[0], um[1]
        print out_result[0]
        with open('report/whois_email_user.html','w') as fwrite:
            fwrite.write('register_user:')
            fwrite.write('<a href="http://' + um[0] + '">注册者反查询</a>')
            fwrite.write('<br>')
            fwrite.write('email:')
            fwrite.write('<a href="http://' + um[1] + '">邮箱反查询</a>')
            fwrite.write('<br>')
            fwrite.write('<pre>')
            fwrite.write(out_result[0])
            fwrite.write('</pre>')

"""
scan web module
"""
def scanweb():
    popen = subprocess.Popen(['python', 'BBScan.py', '-f', 'result.txt'], stdout = subprocess.PIPE)
    while True:
        next_line = popen.stdout.readline()
        if next_line == '' and popen.poll() != None:
            break
        sys.stdout.write(next_line)



"""
nmap port service vul scan
popen = subprocess.Popen(['nmap', '-p','1-65535','-vv','-Pn', '-T4','-iL','result.txt','-oX','report/nmap_port_services.xml'], stdout = subprocess.PIPE)

"""
def scan_nmap(url_domain):
    popen = subprocess.Popen(['nmap', '-v','--script=banner,http-headers,http-title','-T4', '-iL', 'result.txt', '-oX', 'nmap_port_services.xml'], stdout = subprocess.PIPE)
    while True:
        next_line = popen.stdout.readline()
        if next_line == '' and popen.poll() != None:
            break
        sys.stdout.write(next_line)
'''
report_browser.html open


'''

def report_all():
    left_html=Template(TEMPLATE_html)
    html_doc = left_html.substitute({'domain_whois_email':'whois_email_user.html','domain_result': 'result.txt', 'domain_port': 'result_sentives.html', 'domain_webscan': 'result_sentivesweb.html','domain_whatweb':'whatweb.html'})
    with open('report/left.htm', 'w') as outFile:
        outFile.write(html_doc)

'''
php-nmap

'''

def scan_nmap_php():
    popen = subprocess.Popen(['php', 'import1.php', 'nmap_port_services.xml'], stdout=  subprocess.PIPE)
    while True:
        next_line = popen.stdout.readline()
        if next_line == '' and popen.poll() != None:
            break
        sys.stdout.write(next_line)
'''
main start
'''

def run(args):
    domain=args.domain
    if not domain:
        print '# Full automatic scanning tool for Pentesters\n# 1904521507[at]qq.com (http://github.com/rassec)'
        print('usage: f_a_s_t_scann.py -d cert.org.cn')
        sys.exit(1)
    try:
        print '''_________________________________________________________________________________________________
        _____           __              __          ______          __        __      __      _     _
        /    '          / |           /    )          /           /    )    /    )    / |     /|   /
    ---/__-------------/__|-----------\--------------/------------\--------/---------/__|----/-| -/--
      /               /   |            \            /              \      /         /   |   /  | /
    _/_______________/____|________(____/__________/___________(____/____(____/____/____|__/___|/____
              ------        ------          ------

                '''
        print '# Full automatic scan and Exp crack tool for Pentesters\n# only run windows\n# 1904521507[at]qq.com (http://github.com/rassec)'

        print "whois search..."
        
        #vpn_yes = raw_input("please open vpn!!!!!![y/n]")
        sub_domain_whois(domain)
        print "\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] first INTERFACE\nwaiting 5s ......\n\n"
        time.sleep(1)
        sub_domain_gxfr(domain)
        print "\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] second interface\nwaiting 5s ......\n\n"
        time.sleep(1)
        result=sub_doman_jiejie(domain)
        save_result('demo_geili.txt',result)
        print "\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] three interface\nwaiting 5s ......\n\n"
        time.sleep(1)
        sub_domain_wydomain(domain)
        print "\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] fourth interface\nwaiting 5s ......\n\n"
        time.sleep(1)
        sub_domain_sublist(domain)
        print("\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] make domain result\nwaiting 5s ......\n\n")
        time.sleep(1)
        make_domain()
        #vpn_no = raw_input("please shutdown vpn!!!!!!")
        time.sleep(1)
        print("\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] scan whatweb ...\nwaiting 5s ......\n\n")
        sub_doman_what()
        print("\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] scan web ...\nwaiting 5s ......\n\n")
        scanweb()
        print("\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] scan port ...\nwaiting 5s ......\n\n")
        time.sleep(1)
        #vpn_no = raw_input("please shutdown vpn!!!!!!")
        scan_nmap(domain)
        print("\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] report result ...\nwaiting 5s ......\n\n")
        time.sleep(1)
        scan_nmap_php()
        report_all()
        webbrowser.open_new_tab(os.path.abspath('report/index.htm'))
    except KeyboardInterrupt:
        sys.exit(1)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="f_a_s_t_scann.py v 2.0 to Full automatic scanning tool for Pentesters.")
    parser.add_argument("-d" , "--domain", metavar="",
        help="domain")
    args = parser.parse_args()
    system_vertify()
    try:
        run(args)
    except KeyboardInterrupt:
        sys.exit(1)