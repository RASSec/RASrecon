#定向全自动化渗透测试
###F_A_S_T扫描器


##### 介绍
为了省去繁琐的手工测试和常用漏洞的搜索工作，提升工作的效率，才有了此工具，工具对于前期的收集采用了市面上大量的工具集合，不漏扫的原则，最大化的提升工具可用性，可扩展性等要求，开发次扫描器。

##### 插件介绍
* 邮箱、姓名域反查询记录 
* Requests、wydomain、subdomainburter、gxfr
* Wydomain 	-利用搜索引擎收集域名 加强了改进版
* Subdomain 	-爆破域名以及三级域名 加强了修改改进版
* Gxfr 		-利用了bing和谷歌搜索 收集域名 加强了改进版
* BBScan 		-批量扫描整个段或者定向地址，加强了修改改进版
* webprinter -web指纹识别

##### Win下所需程序
* Nmap 		-服务、端口、exp精确扫描
* 批处理 		-进行监听和执行命令
* awvs扫描器  -批量扫描web应用
---后续待开发---




#####生成报告
说明
######
#####使用方式
* 可以直接执行 ```python main.py -d cert.org.cn```
* 如何检测后需要直接执行扫描应用，可以执行 ```启动程序.bat``` 文件，监听扫描结果

#####功能说明
* 前期需要挂VPN收集刺探信息
* 域名自动收集
* 端口自动判断
* 指纹自动识别
* 路径自动破解
* 计划大型扫描
* 批量进行WVS扫描并识别高中危漏洞

* 批量进行NESSUS扫描自动识别高中危漏洞

__author__ : yds



## Stargazers over time

[![Stargazers over time](https://starchart.cc/RASSec/pentestER-Fully-automatic-scanner.svg)](https://starchart.cc/RASSec/pentestER-Fully-automatic-scanner)



